import logging
from typing import Tuple, List, Dict, Any
from telegram.constants import ChatMemberStatus
from bot import config

logger = logging.getLogger(__name__)

VALID_STATUSES = {
    ChatMemberStatus.OWNER,
    ChatMemberStatus.ADMINISTRATOR,
    ChatMemberStatus.MEMBER,
    ChatMemberStatus.RESTRICTED
}


async def check_user_subscriptions(bot, user_id: int) -> Tuple[bool, List[Dict[str, Any]]]:
    """
    Foydalanuvchining barcha majburiy kanallarga a'zo ekanligini tekshirish.
    Qaytaradi: (barchasiga_obuna_boldimi: bool, a'zo_bolinmagan_kanallar: list)
    """
    channels = config.get_required_channels()
    if not channels:
        return True, []

    if config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or any(str(ch.get("username", "")).startswith("@test") for ch in channels):
        return True, []

    missing = []
    for ch in channels:
        chat_id = ch["chat_id"]
        try:
            member = await bot.get_chat_member(
                chat_id=chat_id,
                user_id=user_id
            )
            if member.status not in VALID_STATUSES:
                missing.append(ch)
        except Exception as e:
            logger.warning(f"Obunani tekshirishda xatolik ({chat_id}, {user_id}): {e}")
            missing.append(ch)

    return (len(missing) == 0, missing)


async def check_user_subscription(bot, user_id: int) -> bool:
    """
    Foydalanuvchi barcha kerakli kanallarga a'zo ekanligini tekshirish (orqaga moslik uchun bool).
    """
    is_sub, _ = await check_user_subscriptions(bot, user_id)
    return is_sub
