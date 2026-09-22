import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from bot import config, texts
from bot.keyboards.inline import get_subscription_keyboard
from bot.utils.storage import add_user
from bot.handlers.subscription import check_user_subscription

logger = logging.getLogger(__name__)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /start buyrug'i handleri:
    1. Foydalanuvchini users.json ga saqlash.
    2. Bot va IPE School haqida ma'lumot berish.
    3. Majburiy obuna holatini tekshirish va tugmalarni chiqarish.
    """
    user = update.effective_user
    if not user:
        return

    # 1. users.json ga saqlash
    add_user(user.id)
    
    # 2. Obunani tekshirish
    is_subscribed = await check_user_subscription(context.bot, user.id)
    
    if not is_subscribed:
        # Obuna bo'lmagan bo'lsa - kanal linki va "Obuna bo'ldim" tugmasini ko'rsatish
        channel_url = config.get_channel_link()
        await update.message.reply_text(
            texts.START_WELCOME,
            reply_markup=get_subscription_keyboard(channel_url),
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
    else:
        # Agar allaqachon obuna bo'lgan bo'lsa
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 Anketani to'ldirish", callback_data="start_resume")]
        ])
        await update.message.reply_text(
            f"👋 **Xush kelibsiz, {user.first_name}!**\n\n"
            "Siz **IPE School** o'quv markazining rasmiy botidasiz.\n"
            "Kanalimizga a'zoligingiz tasdiqlangan. O'qituvchilik anketasini to'ldirish uchun quyidagi tugmani bosing:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
