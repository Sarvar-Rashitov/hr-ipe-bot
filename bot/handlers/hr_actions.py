import logging
from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from bot import config, texts
from bot.states import HRActionState, CandidateReplyState
from bot.keyboards.inline import (
    get_candidate_reply_keyboard,
    get_hr_interview_templates_keyboard,
    get_hr_interview_time_keyboard
)
from bot.utils.formatter import sanitize_md
from bot.utils.hr_storage import get_submission_by_candidate_id
from bot.handlers.fallback import cancel_command

logger = logging.getLogger(__name__)


# -------------------------------------------------------------
# HR ACTION HANDLERS (Callback query)
# -------------------------------------------------------------
async def hr_action_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    HR menejer rezyumedagi tugmalarni bosganda (Suhbatga chaqirish / Xabar yozish / Rad etish).
    Callback data: hr_act:interview:123456 yoki hr_act:msg:123456 yoki hr_act:reject:123456
    """
    query = update.callback_query
    user = update.effective_user
    if not query or not user:
        return ConversationHandler.END

    # Ruxsat tekshiruvi: HR yoki Admin bo'lishi shart
    if not config.is_hr(user.id):
        await query.answer("⛔️ Sizda HR amallarini bajarish huquqi yo'q.", show_alert=True)
        return ConversationHandler.END

    data_parts = query.data.split(":")
    if len(data_parts) < 3:
        await query.answer("Noto'g'ri buyruq.")
        return ConversationHandler.END

    action = data_parts[1]
    try:
        candidate_id = int(data_parts[2])
    except ValueError:
        await query.answer("Nomzod ID noto'g'ri.")
        return ConversationHandler.END

    await query.answer()

    # 1. SUHBATGA CHAQIRISH (Shablonlar menyusi)
    if action == "interview":
        keyboard = get_hr_interview_templates_keyboard(candidate_id)
        await query.message.reply_text(
            f"📅 **Nomzod (ID: `{candidate_id}`) ni suhbatga chaqirish:**\n\n"
            f"Quyidagi shablonlardan birini tanlang yoki o'zingiz xabar yozing:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        return ConversationHandler.END

    # 2. XABAR YOZISH (Erkin xabar)
    elif action == "msg":
        context.user_data["hr_target_candidate_id"] = candidate_id
        await query.message.reply_text(
            f"✉️ **Nomzod (ID: `{candidate_id}`) ga xabar yuborish:**\n\n"
            + texts.HR_PROMPT_CUSTOM_MESSAGE,
            parse_mode="Markdown"
        )
        return HRActionState.ENTER_MESSAGE

    # 3. RAD ETISH
    elif action == "reject":
        sub = get_submission_by_candidate_id(candidate_id)
        name = sub.get("full_name") if sub else "Nomzod"
        msg_text = texts.HR_REJECT_TEMPLATE.format(name=name)
        try:
            await context.bot.send_message(
                chat_id=candidate_id,
                text=msg_text,
                parse_mode="Markdown"
            )
            await query.message.reply_text(
                f"✅ Nomzod (ID: `{candidate_id}`, {name}) ga muloyim rad javobi yetkazildi.",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Nomzodga rad javobi yuborishda xatolik: {e}")
            await query.message.reply_text(
                f"⚠️ Nomzodga xabar yuborib bo'lmadi (ehtimol botni bloklagan): {e}"
            )
        return ConversationHandler.END

    return ConversationHandler.END


# -------------------------------------------------------------
# INTERVIEW TEMPLATES CALLBACKS
# -------------------------------------------------------------
# -------------------------------------------------------------
# INTERVIEW TIMING & INVITATION DISPATCH
# -------------------------------------------------------------
INTERVIEW_TIME_MAP = {
    "t1": "Ertaga soat 11:00 da",
    "t2": "Ertaga soat 15:00 da",
    "t3": "Indinga soat 11:00 da",
    "t4": "Indinga soat 15:00 da",
    "t_flex": "Kelishilgan vaqtda",
}


async def _send_interview_invitation(
    context: ContextTypes.DEFAULT_TYPE,
    candidate_id: int,
    interview_type: str,
    datetime_text: str
) -> tuple[bool, str, str]:
    """Nomzodga rasmiy suhbat taklifnomasini yuborish yordamchi funksiyasi."""
    sub = get_submission_by_candidate_id(candidate_id)
    raw_name = sub.get("full_name") if sub else "Hurmatli nomzod"
    name = sanitize_md(raw_name)
    role_key = sub.get("role", "teacher") if sub else "teacher"
    role_names = {
        "teacher": "O'qituvchi",
        "admin": "Administrator",
        "sales": "Sotuv mutaxassisi"
    }
    role_name = role_names.get(role_key, "mutaxassislik")
    safe_datetime = sanitize_md(datetime_text)

    if interview_type == "office":
        loc_url = config.OFFICE_LOCATION_URL
        msg_text = texts.HR_INVITE_OFFICE_TEMPLATE.format(
            name=name,
            role=role_name,
            datetime=safe_datetime,
            location_url=loc_url
        )
        reply_kb = get_candidate_reply_keyboard(location_url=loc_url)
    else:
        msg_text = texts.HR_INVITE_ONLINE_TEMPLATE.format(
            name=name,
            role=role_name,
            datetime=safe_datetime
        )
        reply_kb = get_candidate_reply_keyboard()

    try:
        await context.bot.send_message(
            chat_id=candidate_id,
            text=msg_text,
            reply_markup=reply_kb,
            parse_mode="Markdown"
        )
        return True, raw_name, role_name
    except Exception as e:
        logger.error(f"Nomzodga suhbat taklifini yuborishda xatolik: {e}")
        return False, raw_name, str(e)


# -------------------------------------------------------------
# INTERVIEW TEMPLATES CALLBACKS
# -------------------------------------------------------------
async def hr_template_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Suhbat shabloni tanlanganda (Ofis / Online / Custom).
    Callback data: hr_tpl:office:123456 yoki hr_tpl:online:123456 yoki hr_tpl:custom:123456
    """
    query = update.callback_query
    user = update.effective_user
    if not query or not user or not config.is_hr(user.id):
        if query:
            await query.answer("Ruxsat berilmagan!", show_alert=True)
        return ConversationHandler.END

    data_parts = query.data.split(":")
    tpl_type = data_parts[1]
    candidate_id = int(data_parts[2]) if len(data_parts) > 2 and data_parts[2].isdigit() else 0

    if tpl_type == "cancel":
        await query.answer("Bekor qilindi.")
        try:
            await query.edit_message_text("❌ Suhbatga chaqirish bekor qilindi.")
        except Exception:
            pass
        context.user_data.pop("hr_target_candidate_id", None)
        context.user_data.pop("hr_interview_type", None)
        return ConversationHandler.END

    sub = get_submission_by_candidate_id(candidate_id)
    name = sub.get("full_name") if sub else "Hurmatli nomzod"

    if tpl_type == "office":
        context.user_data["hr_target_candidate_id"] = candidate_id
        context.user_data["hr_interview_type"] = "office"
        await query.answer()
        prompt_text = texts.HR_PROMPT_INTERVIEW_DATETIME.format(
            name=name,
            candidate_id=candidate_id,
            format_name="🏫 Ofisda jonli suhbat"
        )
        time_kb = get_hr_interview_time_keyboard(candidate_id, "office")
        await query.message.reply_text(
            prompt_text,
            reply_markup=time_kb,
            parse_mode="Markdown"
        )
        return HRActionState.ENTER_INTERVIEW

    elif tpl_type == "online":
        context.user_data["hr_target_candidate_id"] = candidate_id
        context.user_data["hr_interview_type"] = "online"
        await query.answer()
        prompt_text = texts.HR_PROMPT_INTERVIEW_DATETIME.format(
            name=name,
            candidate_id=candidate_id,
            format_name="💻 Online suhbat (Google Meet)"
        )
        time_kb = get_hr_interview_time_keyboard(candidate_id, "online")
        await query.message.reply_text(
            prompt_text,
            reply_markup=time_kb,
            parse_mode="Markdown"
        )
        return HRActionState.ENTER_INTERVIEW

    elif tpl_type == "custom":
        context.user_data["hr_target_candidate_id"] = candidate_id
        await query.answer()
        await query.message.reply_text(
            f"✍️ **{name}** (ID: `{candidate_id}`) ga yuboriladigan shaxsiy suhbat taklifnomasini yozing:\n\n"
            + texts.HR_PROMPT_CUSTOM_MESSAGE,
            parse_mode="Markdown"
        )
        return HRActionState.ENTER_MESSAGE

    return ConversationHandler.END


async def hr_interview_time_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Tezkor sana/vaqt tugmasi bosilganda nomzodga taklifnoma yuborish.
    Callback data: hr_t:{candidate_id}:{prefix}:{time_code}
    """
    query = update.callback_query
    user = update.effective_user
    if not query or not user or not config.is_hr(user.id):
        if query:
            await query.answer("Ruxsat berilmagan!", show_alert=True)
        return ConversationHandler.END

    data_parts = query.data.split(":")
    if len(data_parts) < 4:
        await query.answer("Noto'g'ri buyruq.")
        return ConversationHandler.END

    candidate_id = int(data_parts[1]) if data_parts[1].isdigit() else 0
    prefix = data_parts[2]
    time_code = data_parts[3]

    interview_type = "office" if prefix == "off" else "online"
    datetime_text = INTERVIEW_TIME_MAP.get(time_code, "Kelishilgan vaqtda")

    await query.answer()

    success, name, detail = await _send_interview_invitation(
        context, candidate_id, interview_type, datetime_text
    )

    if success:
        loc_str = f"\n🗺 Manzil: {config.OFFICE_LOCATION_URL}" if interview_type == "office" else ""
        await query.edit_message_text(
            f"✅ **{name}** (ID: `{candidate_id}`) ga suhbat taklifnomasi yuborildi!\n\n"
            f"📅 **Suhbat vaqti:** {datetime_text}{loc_str}",
            parse_mode="Markdown"
        )
    else:
        await query.edit_message_text(f"⚠️ Nomzodga taklifnoma yuborib bo'lmadi: {detail}")

    context.user_data.pop("hr_target_candidate_id", None)
    context.user_data.pop("hr_interview_type", None)
    return ConversationHandler.END


async def hr_receive_interview_datetime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """HR o'zi qo'lda sana va vaqt kiritganda qabul qilib nomzodga yuborish."""
    msg = update.message
    user = update.effective_user
    if not msg or not user or not config.is_hr(user.id):
        return ConversationHandler.END

    candidate_id = context.user_data.get("hr_target_candidate_id")
    interview_type = context.user_data.get("hr_interview_type", "office")

    if not candidate_id:
        await msg.reply_text("⚠️ Nomzod aniqlanmadi. Amal bekor qilindi.")
        return ConversationHandler.END

    raw_datetime = msg.text or msg.caption or ""
    if not raw_datetime.strip():
        await msg.reply_text("⚠️ Iltimos, suhbat kuni va soatini matn ko'rinishida yozing:")
        return HRActionState.ENTER_INTERVIEW

    datetime_text = raw_datetime.strip()

    success, name, detail = await _send_interview_invitation(
        context, candidate_id, interview_type, datetime_text
    )

    if success:
        loc_str = f"\n🗺 Manzil: {config.OFFICE_LOCATION_URL}" if interview_type == "office" else ""
        await msg.reply_text(
            f"✅ **{name}** (ID: `{candidate_id}`) ga suhbat taklifnomasi muvaffaqiyatli yuborildi!\n\n"
            f"📅 **Suhbat vaqti:** {datetime_text}{loc_str}",
            parse_mode="Markdown"
        )
    else:
        await msg.reply_text(f"⚠️ Nomzodga taklifnoma yuborib bo'lmadi: {detail}")

    context.user_data.pop("hr_target_candidate_id", None)
    context.user_data.pop("hr_interview_type", None)
    return ConversationHandler.END


# -------------------------------------------------------------
# HR CUSTOM MESSAGE RECEIVE
# -------------------------------------------------------------
async def hr_receive_custom_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """HR menejer yozgan erkin xabarni nomzodga yetkazish."""
    msg = update.message
    user = update.effective_user
    if not msg or not user or not config.is_hr(user.id):
        return ConversationHandler.END

    candidate_id = context.user_data.get("hr_target_candidate_id")
    if not candidate_id:
        await msg.reply_text("⚠️ Nomzod aniqlanmadi. Amal bekor qilindi.")
        return ConversationHandler.END

    custom_text = msg.text or msg.caption or ""
    if not custom_text:
        await msg.reply_text("⚠️ Iltimos, matnli xabar yozing:")
        return HRActionState.ENTER_MESSAGE

    sent_text = texts.CANDIDATE_RECEIVED_HR_MSG.format(text=custom_text)
    reply_kb = get_candidate_reply_keyboard()

    try:
        await context.bot.send_message(
            chat_id=candidate_id,
            text=sent_text,
            reply_markup=reply_kb,
            parse_mode="Markdown"
        )
        await msg.reply_text(
            f"✅ Xabaringiz nomzodga (ID: `{candidate_id}`) muvaffaqiyatli yetkazildi!",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Nomzodga xabar yetkazishda xatolik: {e}")
        await msg.reply_text(f"⚠️ Nomzodga xabar yetkazib bo'lmadi: {e}")

    context.user_data.pop("hr_target_candidate_id", None)
    return ConversationHandler.END


def get_hr_message_conversation_handler() -> ConversationHandler:
    """HR xabar yozish va suhbatga chaqirish conversation handleri."""
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(hr_action_callback, pattern=r"^hr_act:"),
            CallbackQueryHandler(hr_template_callback, pattern=r"^hr_tpl:"),
            CallbackQueryHandler(hr_interview_time_callback, pattern=r"^hr_t:"),
        ],
        states={
            HRActionState.ENTER_MESSAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, hr_receive_custom_message),
            ],
            HRActionState.ENTER_INTERVIEW: [
                CallbackQueryHandler(hr_interview_time_callback, pattern=r"^hr_t:"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, hr_receive_interview_datetime),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_command),
        ],
        allow_reentry=True,
        per_message=False
    )


# -------------------------------------------------------------
# CANDIDATE REPLY TO HR
# -------------------------------------------------------------
async def candidate_start_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Nomzod 'HR ga javob yozish' tugmasini bosganda."""
    query = update.callback_query
    if query:
        await query.answer()
        await query.message.reply_text(
            texts.CANDIDATE_REPLY_PROMPT,
            parse_mode="Markdown"
        )
    return CandidateReplyState.ENTER_REPLY


async def candidate_receive_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Nomzod yozgan javobni HR guruhiga va zaxiraga yetkazish."""
    msg = update.message
    user = update.effective_user
    if not msg or not user:
        return ConversationHandler.END

    reply_text = msg.text or msg.caption or ""
    if not reply_text:
        await msg.reply_text("⚠️ Iltimos, matnli xabar yozing:")
        return CandidateReplyState.ENTER_REPLY

    name = user.full_name or "Nomzod"
    username_str = f"@{user.username}" if user.username else "Username yo'q"

    # HR guruhiga yuboriladigan xabar
    forward_text = (
        f"💬 **NOMZODDAN YANGI JAVOB XABARI!**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 **Nomzod:** {name}\n"
        f"🆔 **ID:** `{user.id}`\n"
        f"📱 **Telegram:** {username_str}\n\n"
        f"📝 **Xabar matni:**\n{reply_text}\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )

    hr_kb = get_hr_interview_templates_keyboard(user.id)

    # HR_CHAT_ID ga yuborish
    if config.HR_CHAT_ID:
        try:
            await context.bot.send_message(
                chat_id=config.HR_CHAT_ID,
                text=forward_text,
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"HR chatiga nomzod javobini yuborishda xatolik: {e}")

    await msg.reply_text(
        texts.CANDIDATE_REPLY_SENT,
        parse_mode="Markdown"
    )
    return ConversationHandler.END


def get_candidate_reply_conversation_handler() -> ConversationHandler:
    """Nomzod javob qaytarish conversation handleri."""
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(candidate_start_reply, pattern=r"^cand_reply$"),
        ],
        states={
            CandidateReplyState.ENTER_REPLY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, candidate_receive_reply),
            ]
        },
        fallbacks=[
            CommandHandler("cancel", cancel_command),
        ],
        allow_reentry=True,
        per_message=False
    )


# -------------------------------------------------------------
# HR GROUP TELEGRAM REPLY FORWARDING
# -------------------------------------------------------------
async def hr_group_reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Agar HR menejer HR guruhida turib, bot yuborgan anketaga Telegramning
    oddiy 'Reply' tugmasi orqali javob yozsa, ushbu xabarni avtomatik nomzodga yetkazish.
    """
    msg = update.message
    user = update.effective_user
    if not msg or not user or not msg.reply_to_message:
        return

    # Faqat HR_CHAT_ID guruhida yoki HR menejerdan kelsa
    if msg.chat_id != config.HR_CHAT_ID and not config.is_hr(user.id):
        return

    replied = msg.reply_to_message
    # Repled message bot tomonidan yuborilgan bo'lishi kerak
    if not replied.from_user or not replied.from_user.is_bot:
        return

    # Repled xabar matni yoki captionidan candidate_id ni qidirish
    content = replied.text or replied.caption or ""
    candidate_id = None

    # Qidirish usuli 1: Agar ID saqlangan bo'lsa
    import re
    id_match = re.search(r"ID:\s*`?(\d+)`?", content)
    if id_match:
        candidate_id = int(id_match.group(1))

    # Qidirish usuli 2: reply_markup dagi callback_data dan
    if not candidate_id and replied.reply_markup:
        for row in replied.reply_markup.inline_keyboard:
            for btn in row:
                if btn.callback_data and btn.callback_data.startswith("hr_act:"):
                    parts = btn.callback_data.split(":")
                    if len(parts) >= 3 and parts[2].isdigit():
                        candidate_id = int(parts[2])
                        break

    if not candidate_id:
        return

    hr_text = msg.text or msg.caption or ""
    if not hr_text:
        return

    sent_text = texts.CANDIDATE_RECEIVED_HR_MSG.format(text=hr_text)
    reply_kb = get_candidate_reply_keyboard()

    try:
        await context.bot.send_message(
            chat_id=candidate_id,
            text=sent_text,
            reply_markup=reply_kb,
            parse_mode="Markdown"
        )
        await msg.reply_text(
            f"✅ Xabaringiz nomzodga (ID: `{candidate_id}`) yetkazildi!",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.warning(f"Telegram Reply orqali nomzodga xabar yuborishda xatolik: {e}")
