import asyncio
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from telegram.error import TelegramError
from bot import config, texts
from bot.states import AdminState, AdminHRState
from bot.keyboards.inline import (
    get_admin_main_keyboard,
    get_broadcast_confirm_keyboard,
    get_start_keyboard,
    get_admin_hr_keyboard
)
from bot.utils.storage import (
    load_users,
    get_users_count,
    get_all_user_ids,
    remove_user
)
from bot.utils.hr_storage import (
    get_all_hr_managers,
    add_hr_manager,
    remove_hr_manager
)
from bot.handlers.fallback import cancel_command


logger = logging.getLogger(__name__)


# -------------------------------------------------------------
# ADMIN PANEL DASHBOARD
# -------------------------------------------------------------
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Admin panelni ochish (/admin yoki /start admin bo'lganda)."""
    user = update.effective_user
    if not user or not config.is_admin(user.id):
        if update.message:
            await update.message.reply_text(texts.ADMIN_ACCESS_DENIED)
        return

    total = get_users_count()
    text = texts.ADMIN_PANEL_TITLE.format(total_users=total)

    if update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.edit_message_text(
                text,
                reply_markup=get_admin_main_keyboard(),
                parse_mode="Markdown"
            )
        except Exception:
            await update.callback_query.message.reply_text(
                text,
                reply_markup=get_admin_main_keyboard(),
                parse_mode="Markdown"
            )
    elif update.message:
        await update.message.reply_text(
            text,
            reply_markup=get_admin_main_keyboard(),
            parse_mode="Markdown"
        )


async def admin_stats_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Batafsil statistikani ko'rsatish."""
    query = update.callback_query
    user = update.effective_user
    if not user or not config.is_admin(user.id):
        if query:
            await query.answer("Ruxsat berilmagan!", show_alert=True)
        return

    await query.answer()
    total = get_users_count()
    channel = config.CHANNEL_USERNAME or "Ko'rsatilmagan"
    hr_chat = str(config.HR_CHAT_ID) or "Ko'rsatilmagan"

    text = texts.ADMIN_STATS_TEXT.format(
        total_users=total,
        channel=channel,
        hr_chat_id=hr_chat
    )

    back_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Admin panelga qaytish", callback_data="admin_refresh")]
    ])

    try:
        await query.edit_message_text(
            text,
            reply_markup=back_keyboard,
            parse_mode="Markdown"
        )
    except Exception:
        await query.message.reply_text(
            text,
            reply_markup=back_keyboard,
            parse_mode="Markdown"
        )


async def admin_candidate_preview_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Nomzod ko'rinishini (preview) adminga ko'rsatish."""
    query = update.callback_query
    user = update.effective_user
    if not user or not config.is_admin(user.id):
        if query:
            await query.answer("Ruxsat berilmagan!", show_alert=True)
        return

    await query.answer()
    channel_url = config.get_channel_link()
    candidate_kb = get_start_keyboard(channel_url, config.WEBSITE_URL, config.INSTAGRAM_URL)

    # Qo'shimcha admin panelga qaytish tugmasini qo'shish
    buttons = [row.copy() for row in candidate_kb.inline_keyboard]
    buttons.append([InlineKeyboardButton("🔙 Admin panelga qaytish", callback_data="admin_refresh")])
    preview_kb = InlineKeyboardMarkup(buttons)


    caption = (
        "👁 **[ADMIN PREVIEW] Nomzodlar uchun ko'rinish:**\n\n"
        + texts.START_WELCOME
    )

    if config.IMAGE_PATH.exists():
        try:
            with open(config.IMAGE_PATH, "rb") as photo_file:
                await query.message.reply_photo(
                    photo=photo_file,
                    caption=caption,
                    reply_markup=preview_kb,
                    parse_mode="Markdown"
                )
            return
        except Exception as e:
            logger.error(f"Preview rasmini yuborishda xatolik: {e}")

    await query.message.reply_text(
        caption,
        reply_markup=preview_kb,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )


# -------------------------------------------------------------
# BROADCAST (REKLAMA YUBORISH) OQIMI
# -------------------------------------------------------------
async def start_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Reklama yuborish jarayonini boshlash (/broadcast yoki inline tugma)."""
    user = update.effective_user
    if not user or not config.is_admin(user.id):
        if update.callback_query:
            await update.callback_query.answer("Ruxsat berilmagan!", show_alert=True)
        return ConversationHandler.END

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            texts.ADMIN_BROADCAST_PROMPT,
            parse_mode="Markdown"
        )
    elif update.message:
        await update.message.reply_text(
            texts.ADMIN_BROADCAST_PROMPT,
            parse_mode="Markdown"
        )
    return AdminState.BROADCAST_MESSAGE


async def receive_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Admin yuborgan reklama xabarini qabul qilish va preview ko'rsatish."""
    user = update.effective_user
    if not user or not config.is_admin(user.id):
        return ConversationHandler.END

    msg = update.message
    if not msg:
        return AdminState.BROADCAST_MESSAGE

    broadcast_data = {
        "text": msg.text or msg.caption or "",
        "photo": msg.photo[-1].file_id if msg.photo else None,
        "video": msg.video.file_id if msg.video else None,
    }

    if not broadcast_data["text"] and not broadcast_data["photo"] and not broadcast_data["video"]:
        await msg.reply_text("⚠️ Iltimos, faqat rasm, video yoki matnli xabar yuboring.")
        return AdminState.BROADCAST_MESSAGE

    context.user_data["broadcast"] = broadcast_data

    # 1. Preview ko'rsatish — xuddi shu xabarni adminning o'ziga qayta yuboradi (PDF 4-sahifa)
    await msg.reply_text("👁 **Siz yuborgan xabar preview ko'rinishi:**", parse_mode="Markdown")
    try:
        await msg.copy(chat_id=msg.chat_id)
    except Exception:
        if broadcast_data["photo"]:
            await context.bot.send_photo(
                chat_id=user.id,
                photo=broadcast_data["photo"],
                caption=broadcast_data["text"]
            )
        elif broadcast_data["video"]:
            await context.bot.send_video(
                chat_id=user.id,
                video=broadcast_data["video"],
                caption=broadcast_data["text"]
            )
        else:
            await context.bot.send_message(
                chat_id=user.id,
                text=broadcast_data["text"]
            )

    # 2. Tasdiqlash so'rovi (PDF 5-sahifa)
    await msg.reply_text(
        texts.ADMIN_BROADCAST_PREVIEW,
        reply_markup=get_broadcast_confirm_keyboard()
    )
    return AdminState.BROADCAST_CONFIRM


async def confirm_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Reklamani barcha foydalanuvchilarga yuborish yoki bekor qilish."""
    query = update.callback_query
    user = update.effective_user
    if not user or not config.is_admin(user.id):
        return ConversationHandler.END

    await query.answer()

    # Bekor qilish bosilgan bo'lsa
    if query.data in ("bc_cancel", "broadcast_cancel"):
        await query.edit_message_text(texts.ADMIN_BROADCAST_CANCELLED)
        context.user_data.clear()
        return ConversationHandler.END

    data = context.user_data.get("broadcast")
    if not data:
        await query.message.reply_text("⚠️ Xabar ma'lumotlari topilmadi. Qaytadan /admin bosing.")
        return ConversationHandler.END

    user_ids = get_all_user_ids()
    if not user_ids:
        await query.message.reply_text("⚠️ Hozircha bazada foydalanuvchilar mavjud emas.")
        context.user_data.clear()
        return ConversationHandler.END

    status_msg = await query.message.reply_text(texts.ADMIN_BROADCAST_START)

    sent = 0
    failed = 0

    for uid in user_ids:
        try:
            if data["photo"]:
                await context.bot.send_photo(
                    uid,
                    data["photo"],
                    caption=data["text"]
                )
            elif data["video"]:
                await context.bot.send_video(
                    uid,
                    data["video"],
                    caption=data["text"]
                )
            else:
                await context.bot.send_message(
                    uid,
                    data["text"]
                )
            sent += 1
        except Exception as e:
            failed += 1
            logger.warning(f"Foydalanuvchiga yuborilmadi ({uid}): {e}")
            # Bot bloklangan yoki chat topilmasa, ro'yxatdan o'chirish (PDF 7-sahifa)
            remove_user(uid)

        # Telegram flood-limitidan saqlanish uchun (PDF 6-sahifa)
        await asyncio.sleep(0.05)

    result_text = texts.ADMIN_BROADCAST_FINISH.format(
        sent_count=sent,
        failed_count=failed
    )
    await status_msg.edit_text(result_text, parse_mode="Markdown")
    context.user_data.clear()
    return ConversationHandler.END


async def cancel_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Reklama yuborishni bekor qilish."""
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text(texts.ADMIN_BROADCAST_CANCELLED)
    context.user_data.clear()
    return ConversationHandler.END


def get_admin_broadcast_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            CommandHandler("broadcast", start_broadcast),
            CallbackQueryHandler(start_broadcast, pattern="^admin_broadcast$"),
        ],
        states={
            AdminState.BROADCAST_MESSAGE: [
                MessageHandler(
                    (filters.PHOTO | filters.VIDEO | filters.TEXT) & ~filters.COMMAND,
                    receive_broadcast_message
                )
            ],
            AdminState.BROADCAST_CONFIRM: [
                CallbackQueryHandler(confirm_broadcast, pattern="^(bc_|broadcast_)"),
            ]
        },
        fallbacks=[
            CommandHandler("cancel", cancel_command),
            CallbackQueryHandler(cancel_broadcast, pattern="^(bc_cancel|broadcast_cancel)$"),
        ],
        allow_reentry=True,
        per_message=False
    )


# -------------------------------------------------------------
# HR MENEJERLARNI BOSHQARISH
# -------------------------------------------------------------
async def admin_hr_manage_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Admin panelda HR menejerlar ro'yxatini ko'rsatish."""
    query = update.callback_query
    user = update.effective_user
    if not user or not config.is_admin(user.id):
        if query:
            await query.answer("Ruxsat berilmagan!", show_alert=True)
        return

    await query.answer()
    managers = get_all_hr_managers(config.HR_MANAGER_IDS)
    text = texts.HR_MANAGEMENT_TITLE.format(count=len(managers))
    keyboard = get_admin_hr_keyboard(managers)

    try:
        await query.edit_message_text(
            text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    except Exception:
        await query.message.reply_text(
            text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )


async def admin_hr_delete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """HR menejerni o'chirish."""
    query = update.callback_query
    user = update.effective_user
    if not user or not config.is_admin(user.id):
        if query:
            await query.answer("Ruxsat berilmagan!", show_alert=True)
        return

    del_id = int(query.data.split(":")[1])
    remove_hr_manager(del_id)
    await query.answer(f"HR ID {del_id} o'chirildi!", show_alert=True)

    managers = get_all_hr_managers(config.HR_MANAGER_IDS)
    text = texts.HR_MANAGEMENT_TITLE.format(count=len(managers))
    keyboard = get_admin_hr_keyboard(managers)

    try:
        await query.edit_message_text(
            text,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    except Exception:
        pass


async def start_add_hr_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Yangi HR qo'shish so'rovini boshlash."""
    query = update.callback_query
    user = update.effective_user
    if not user or not config.is_admin(user.id):
        if query:
            await query.answer("Ruxsat berilmagan!", show_alert=True)
        return ConversationHandler.END

    await query.answer()
    await query.message.reply_text(
        texts.HR_ADD_PROMPT,
        parse_mode="Markdown"
    )
    return AdminHRState.ENTER_HR_ID


async def receive_hr_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Yangi HR ID sini qabul qilish va saqlash."""
    msg = update.message
    user = update.effective_user
    if not msg or not user or not config.is_admin(user.id):
        return ConversationHandler.END

    text = (msg.text or "").strip()
    if not text.isdigit():
        await msg.reply_text("⚠️ Noto'g'ri format. Iltimos, faqat musbat raqamlardan iborat Telegram ID kiriting:")
        return AdminHRState.ENTER_HR_ID

    new_id = int(text)
    add_hr_manager(new_id)

    managers = get_all_hr_managers(config.HR_MANAGER_IDS)
    await msg.reply_text(
        texts.HR_ADD_SUCCESS.format(user_id=new_id),
        parse_mode="Markdown"
    )
    await msg.reply_text(
        texts.HR_MANAGEMENT_TITLE.format(count=len(managers)),
        reply_markup=get_admin_hr_keyboard(managers),
        parse_mode="Markdown"
    )
    return ConversationHandler.END


def get_admin_hr_conversation_handler() -> ConversationHandler:
    """Yangi HR qo'shish conversation handleri."""
    return ConversationHandler(
        entry_points=[
            CallbackQueryHandler(start_add_hr_callback, pattern=r"^hr_add$"),
        ],
        states={
            AdminHRState.ENTER_HR_ID: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_hr_id),
            ]
        },
        fallbacks=[
            CommandHandler("cancel", cancel_command),
        ],
        allow_reentry=True,
        per_message=False
    )

