import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from bot import config, texts
from bot.keyboards.inline import get_start_keyboard
from bot.utils.storage import save_user

logger = logging.getLogger(__name__)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /start buyrug'i handleri:
    1. Foydalanuvchini users.json ga saqlash (save_user).
    2. Agar ADMIN bo'lsa — maxsus Admin boshqaruv paneli interfeysini ochish.
    3. Agar oddiy foydalanuvchi bo'lsa — image.png, IPE School ma'lumoti va anketani chiqarish.
    """
    user = update.effective_user
    if not user or not update.message:
        return

    # 1. users.json ga saqlash
    save_user(user.id)

    # 2. Agar foydalanuvchi ADMIN bo'lsa — Admin interfeysini chiqarish
    if config.is_admin(user.id):
        from bot.handlers.admin import admin_panel
        await admin_panel(update, context)
        return
    
    # 2. Tugmalarni shakllantirish
    channel_url = config.get_channel_link()
    keyboard = get_start_keyboard(channel_url, config.WEBSITE_URL, config.INSTAGRAM_URL)


    # 3. Rasm bilan xabar yuborish
    if config.IMAGE_PATH.exists():
        try:
            with open(config.IMAGE_PATH, "rb") as photo_file:
                await update.message.reply_photo(
                    photo=photo_file,
                    caption=texts.START_WELCOME,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
            return
        except Exception as e:
            logger.error(f"Rasmni yuborishda xatolik: {e}")

    # Fallback: Agar rasm topilmasa yoki yuborishda xatolik bo'lsa, oddiy matn sifatida yuborish
    await update.message.reply_text(
        texts.START_WELCOME,
        reply_markup=keyboard,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
