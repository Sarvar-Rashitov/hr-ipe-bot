import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot import texts
from bot.keyboards.inline import get_about_keyboard
from bot.handlers.start import start_handler

logger = logging.getLogger(__name__)


async def about_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Biz haqimizda va bot yaratuvchilari sahifasi (/about yoki 'about_us' tugmasi)."""
    keyboard = get_about_keyboard()

    if update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.edit_message_text(
                texts.ABOUT_US_TEXT,
                reply_markup=keyboard,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        except Exception:
            await update.callback_query.message.reply_text(
                texts.ABOUT_US_TEXT,
                reply_markup=keyboard,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
    elif update.message:
        await update.message.reply_text(
            texts.ABOUT_US_TEXT,
            reply_markup=keyboard,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Botdan foydalanish bo'yicha yordam (/help yoki 'bot_help' tugmasi)."""
    keyboard = get_about_keyboard()

    if update.callback_query:
        await update.callback_query.answer()
        try:
            await update.callback_query.edit_message_text(
                texts.HELP_TEXT,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception:
            await update.callback_query.message.reply_text(
                texts.HELP_TEXT,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
    elif update.message:
        await update.message.reply_text(
            texts.HELP_TEXT,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )


async def back_to_start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bosh sahifaga qaytish ('back_to_start' tugmasi)."""
    query = update.callback_query
    if query:
        await query.answer()
        try:
            await query.message.delete()
        except Exception:
            pass
        # Yangi bosh sahifa xabarini chiqarish
        await start_handler(update, context)
