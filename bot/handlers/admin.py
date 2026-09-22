import asyncio
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
from telegram.error import TelegramError
from bot import config, texts
from bot.states import AdminState
from bot.keyboards.inline import (
    get_admin_main_keyboard,
    get_broadcast_confirm_keyboard
)
from bot.utils.storage import load_users, get_users_count
from bot.handlers.fallback import cancel_command

logger = logging.getLogger(__name__)


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Admin panelni ochish (/admin)."""
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


async def start_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Reklama yuborish jarayonini boshlash."""
    query = update.callback_query
    user = update.effective_user
    if not user or not config.is_admin(user.id):
        if query:
            await query.answer("Ruxsat berilmagan!", show_alert=True)
        return ConversationHandler.END

    if query:
        await query.answer()
        await query.message.reply_text(
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
    broadcast_data = {}

    if msg.photo:
        broadcast_data["type"] = "photo"
        broadcast_data["file_id"] = msg.photo[-1].file_id
        broadcast_data["caption"] = msg.caption or ""
    elif msg.video:
        broadcast_data["type"] = "video"
        broadcast_data["file_id"] = msg.video.file_id
        broadcast_data["caption"] = msg.caption or ""
    elif msg.text:
        broadcast_data["type"] = "text"
        broadcast_data["text"] = msg.text
    else:
        await msg.reply_text("⚠️ Iltimos, faqat rasm, video yoki matnli xabar yuboring.")
        return AdminState.BROADCAST_MESSAGE

    context.user_data["broadcast_data"] = broadcast_data

    # 1. Admin uchun xabarning ko'rinishini (preview) chiqarish
    await msg.reply_text("👁 **Siz yuborgan xabar preview ko'rinishi:**", parse_mode="Markdown")
    if broadcast_data["type"] == "photo":
        await context.bot.send_photo(
            chat_id=user.id,
            photo=broadcast_data["file_id"],
            caption=broadcast_data["caption"]
        )
    elif broadcast_data["type"] == "video":
        await context.bot.send_video(
            chat_id=user.id,
            video=broadcast_data["file_id"],
            caption=broadcast_data["caption"]
        )
    elif broadcast_data["type"] == "text":
        await context.bot.send_message(
            chat_id=user.id,
            text=broadcast_data["text"]
        )

    # 2. Tasdiqlash so'rovi
    total = get_users_count()
    await msg.reply_text(
        texts.ADMIN_BROADCAST_PREVIEW.format(total_users=total),
        reply_markup=get_broadcast_confirm_keyboard(),
        parse_mode="Markdown"
    )
    return AdminState.BROADCAST_CONFIRM


async def confirm_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Reklamani barcha foydalanuvchilarga yuborish."""
    query = update.callback_query
    user = update.effective_user
    if not user or not config.is_admin(user.id):
        return ConversationHandler.END

    await query.answer()
    broadcast_data = context.user_data.get("broadcast_data")
    if not broadcast_data:
        await query.message.reply_text("⚠️ Xabar ma'lumotlari topilmadi. Qaytadan /admin bosing.")
        return ConversationHandler.END

    users = load_users()
    if not users:
        await query.message.reply_text("⚠️ Hozircha hech qanday foydalanuvchi mavjud emas.")
        context.user_data.clear()
        return ConversationHandler.END

    status_msg = await query.message.reply_text(texts.ADMIN_BROADCAST_START)

    sent_count = 0
    failed_count = 0
    msg_type = broadcast_data["type"]

    for uid in users:
        try:
            if msg_type == "photo":
                await context.bot.send_photo(
                    chat_id=uid,
                    photo=broadcast_data["file_id"],
                    caption=broadcast_data["caption"]
                )
            elif msg_type == "video":
                await context.bot.send_video(
                    chat_id=uid,
                    video=broadcast_data["file_id"],
                    caption=broadcast_data["caption"]
                )
            elif msg_type == "text":
                await context.bot.send_message(
                    chat_id=uid,
                    text=broadcast_data["text"]
                )
            sent_count += 1
            await asyncio.sleep(0.05)  # Telegram limitlariga tushmaslik uchun
        except TelegramError as e:
            logger.warning(f"Foydalanuvchiga yuborilmadi ({uid}): {e}")
            failed_count += 1
        except Exception as e:
            logger.error(f"Kutilmagan xatolik ({uid}): {e}")
            failed_count += 1

    result_text = texts.ADMIN_BROADCAST_FINISH.format(
        sent_count=sent_count,
        failed_count=failed_count
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
                CallbackQueryHandler(confirm_broadcast, pattern="^broadcast_confirm$"),
                CallbackQueryHandler(cancel_broadcast, pattern="^broadcast_cancel$"),
            ]
        },
        fallbacks=[
            CommandHandler("cancel", cancel_command),
            CallbackQueryHandler(cancel_broadcast, pattern="^broadcast_cancel$"),
        ],
        allow_reentry=True,
        per_message=False
    )
