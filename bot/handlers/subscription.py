import logging
from telegram import Update
from telegram.constants import ChatMemberStatus
from telegram.ext import ContextTypes
from bot import config, texts
from bot.keyboards.inline import get_subscription_keyboard

logger = logging.getLogger(__name__)


async def check_user_subscription(bot, user_id: int) -> bool:
    """
    Foydalanuvchi kanalga a'zo ekanligini get_chat_member orqali tekshirish.
    Agar sozlamalarda kanal ko'rsatilmagan bo'lsa, tekshiruvdan o'tkaziladi.
    """
    if not config.CHANNEL_USERNAME:
        return True
    
    # Agar bot token yoki kanal noto'g'ri bo'lsa yoki test muhitida bo'lsa
    if config.CHANNEL_USERNAME.startswith("@test") or config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        return True

    try:
        member = await bot.get_chat_member(
            chat_id=config.CHANNEL_USERNAME,
            user_id=user_id
        )
        # Qabul qilinadigan statuslar
        valid_statuses = {
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.RESTRICTED
        }
        return member.status in valid_statuses
    except Exception as e:
        logger.warning(f"Obunani tekshirishda xatolik ({config.CHANNEL_USERNAME}, {user_id}): {e}")
        # Agar bot kanalda admin bo'lmasa yoki kanal topilmasa:
        return False
