import html
import json
import logging
import traceback
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from bot import texts

logger = logging.getLogger(__name__)


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Anketani yoki har qanday oqimni bekor qilish (/cancel)."""
    context.user_data.clear()
    
    msg = update.effective_message
    if msg:
        await msg.reply_text(
            texts.CANCEL_SUCCESS,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="Markdown"
        )
    
    return ConversationHandler.END


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Barcha kutilmagan xatoliklarni ushlab logga yozish."""
    logger.error("Botda xatolik yuz berdi:", exc_info=context.error)
    
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    
    logger.error(f"Traceback:\n{tb_string}")
    
    # Agar xabar yuborish imkoni bo'lsa foydalanuvchiga bildirish
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "⚠️ Texnik xatolik yuz berdi. Iltimos, /start buyrug'i orqali qayta urinib ko'ring."
            )
        except Exception:
            pass
