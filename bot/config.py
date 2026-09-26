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

# Obuna tekshiriladigan kanal username yoki ID (yagona kanal uchun backward-compatibility)
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "").strip()

# Bir nechta majburiy obuna kanallari (vergul bilan: @kanal1, @kanal2)
REQUIRED_CHANNELS_RAW = os.getenv("REQUIRED_CHANNELS", "").strip()

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

# HR menejerlar ID ro'yxati (.env dan)
_hr_ids_raw = os.getenv("HR_MANAGER_IDS", "").strip()
HR_MANAGER_IDS: list[int] = []
if _hr_ids_raw:
    for part in _hr_ids_raw.split(","):
        part = part.strip()
        if part.isdigit() or (part.startswith("-") and part[1:].isdigit()):
            HR_MANAGER_IDS.append(int(part))

# Users JSON fayli yo'li
USERS_FILE = BASE_DIR / "users.json"

# Data papkasi va persistence
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
PERSISTENCE_FILE = DATA_DIR / "bot_persistence.pickle"

# Start xabari uchun rasm yo'li
IMAGE_PATH = BASE_DIR / "image.png"

# Rasmiy sayt havolasi
WEBSITE_URL = os.getenv("WEBSITE_URL", "https://ipeschool.uz").strip()

# Instagram sahifasi havolasi
INSTAGRAM_URL = os.getenv("INSTAGRAM_URL", "https://www.instagram.com/ipe_school").strip()

# Suhbat ofisi manzili havolasi (Google Maps)
OFFICE_LOCATION_URL = os.getenv(
    "OFFICE_LOCATION_URL",
    "https://maps.app.goo.gl/7g5mPL7AD5kscFqi9"
).strip()


def get_required_channels() -> list[dict]:
    """
    Majburiy obuna bo'lishi kerak bo'lgan Telegram kanallar ro'yxati.
    Har bir element: {'index': 1, 'chat_id': '@...', 'username': '@...', 'url': 'https://...', 'title': '...'}
    """
    items = []
    if REQUIRED_CHANNELS_RAW:
        items = [x.strip() for x in REQUIRED_CHANNELS_RAW.split(",") if x.strip()]
    elif CHANNEL_USERNAME:
        items = [CHANNEL_USERNAME]

    channels = []
    for idx, item in enumerate(items, 1):
        if not item:
            continue
        if item.startswith("https://t.me/"):
            clean = item.replace("https://t.me/", "").strip("/").lstrip("+")
            username = f"@{clean}" if not clean.startswith("joinchat") else item
            url = item
            title = f"{idx}-kanal" if clean.startswith("joinchat") else f"📢 {username}"
            chat_id = username if not clean.startswith("joinchat") else item
        elif item.startswith("-100") or (item.startswith("-") and item[1:].isdigit()):
            try:
                chat_id = int(item)
            except ValueError:
                chat_id = item
            username = str(item)
            url = f"https://t.me/c/{str(item).replace('-100', '')}/1"
            title = f"📢 {idx}-kanal"
        else:
            clean = item.lstrip("@")
            username = f"@{clean}"
            chat_id = username
            url = f"https://t.me/{clean}"
            title = f"📢 {username}"

        channels.append({
            "index": idx,
            "chat_id": chat_id,
            "username": username,
            "url": url,
            "title": title
        })

    return channels


def get_channel_link() -> str:
    """Kanalga o'tish tugmasi uchun havola yaratish (birinchi kanal havolasi)."""
    channels = get_required_channels()
    if channels:
        return channels[0]["url"]
    if not CHANNEL_USERNAME:
        return "https://t.me/ipeschool_uz"
    if CHANNEL_USERNAME.startswith("https://t.me/"):
        return CHANNEL_USERNAME
    clean_username = CHANNEL_USERNAME.lstrip("@")
    return f"https://t.me/{clean_username}"


def is_admin(user_id: int) -> bool:
    """Foydalanuvchi adminlar ro'yxatida borligini tekshirish."""
    return user_id in ADMIN_IDS


def is_hr(user_id: int) -> bool:
    """Foydalanuvchi HR menejer yoki Admin ekanligini tekshirish."""
    if is_admin(user_id) or user_id in HR_MANAGER_IDS:
        return True
    try:
        from bot.utils.hr_storage import load_hr_manager_ids
        return user_id in load_hr_manager_ids()
    except Exception:
        return False


def validate_config() -> bool:
    """Sozlamalarni tekshirish va xatolik bo'lsa ogohlantirish."""
    errors = []
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        errors.append("BOT_TOKEN .env faylida ko'rsatilmagan!")
    if not CHANNEL_ID:
        errors.append("CHANNEL_ID ko'rsatilmagan!")
    if not CHANNEL_USERNAME and not REQUIRED_CHANNELS_RAW:
        errors.append("CHANNEL_USERNAME yoki REQUIRED_CHANNELS ko'rsatilmagan!")
    if not HR_CHAT_ID:
        errors.append("HR_CHAT_ID ko'rsatilmagan!")

    if errors:
        for err in errors:
            logger.warning(f"Konfiguratsiya xatosi: {err}")
        return False
    return True

