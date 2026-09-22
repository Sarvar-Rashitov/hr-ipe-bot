import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Loyihaning asosiy yo'li
BASE_DIR = Path(__file__).resolve().parent.parent

# .env faylini yuklash
load_dotenv(BASE_DIR / ".env")

# Logging sozlamalari
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, LOG_LEVEL, logging.INFO)
)
logger = logging.getLogger("ipe_hr_bot")

# Asosiy o'zgaruvchilar
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# Resumelar tushadigan kanal ID
_channel_id_raw = os.getenv("CHANNEL_ID", "").strip()
try:
    CHANNEL_ID = int(_channel_id_raw) if _channel_id_raw else ""
except ValueError:
    CHANNEL_ID = _channel_id_raw

# Obuna tekshiriladigan kanal username yoki ID
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "").strip()

# HR jamoasi chat ID
_hr_chat_id_raw = os.getenv("HR_CHAT_ID", "").strip()
try:
    HR_CHAT_ID = int(_hr_chat_id_raw) if _hr_chat_id_raw else ""
except ValueError:
    HR_CHAT_ID = _hr_chat_id_raw

# Adminlar ID ro'yxati
_admin_ids_raw = os.getenv("ADMIN_IDS", "").strip()
ADMIN_IDS: list[int] = []
if _admin_ids_raw:
    for part in _admin_ids_raw.split(","):
        part = part.strip()
        if part.isdigit() or (part.startswith("-") and part[1:].isdigit()):
            ADMIN_IDS.append(int(part))

# Users JSON fayli yo'li
USERS_FILE = BASE_DIR / "users.json"


def get_channel_link() -> str:
    """Kanalga o'tish tugmasi uchun havola yaratish."""
    if not CHANNEL_USERNAME:
        return "https://t.me/ipeschool_uz"
    if CHANNEL_USERNAME.startswith("https://t.me/"):
        return CHANNEL_USERNAME
    clean_username = CHANNEL_USERNAME.lstrip("@")
    return f"https://t.me/{clean_username}"


def is_admin(user_id: int) -> bool:
    """Foydalanuvchi adminlar ro'yxatida borligini tekshirish."""
    return user_id in ADMIN_IDS


def validate_config() -> bool:
    """Sozlamalarni tekshirish va xatolik bo'lsa ogohlantirish."""
    errors = []
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        errors.append("BOT_TOKEN .env faylida ko'rsatilmagan!")
    if not CHANNEL_ID:
        errors.append("CHANNEL_ID ko'rsatilmagan!")
    if not CHANNEL_USERNAME:
        errors.append("CHANNEL_USERNAME ko'rsatilmagan!")
    if not HR_CHAT_ID:
        errors.append("HR_CHAT_ID ko'rsatilmagan!")

    if errors:
        for err in errors:
            logger.warning(f"Konfiguratsiya xatosi: {err}")
        return False
    return True
