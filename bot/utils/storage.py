import json
import logging
import threading
from bot.config import USERS_FILE

logger = logging.getLogger(__name__)
_lock = threading.Lock()


def load_users() -> list[int]:
    """users.json faylidan barcha user ID larini o'qib olish."""
    with _lock:
        if not USERS_FILE.exists():
            return []
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return [int(u) for u in data if str(u).isdigit() or (str(u).startswith("-") and str(u)[1:].isdigit())]
                return []
        except Exception as e:
            logger.error(f"users.json faylini o'qishda xatolik: {e}")
            return []


def save_users(users: list[int]) -> None:
    """users.json fayliga saqlash."""
    with _lock:
        try:
            unique_sorted = sorted(list(set(users)))
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump(unique_sorted, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"users.json fayliga yozishda xatolik: {e}")


def add_user(user_id: int) -> bool:
    """
    Foydalanuvchini ro'yxatga qo'shish.
    Agar yangi bo'lsa True, allaqachon mavjud bo'lsa False qaytaradi.
    """
    users = load_users()
    if user_id not in users:
        users.append(user_id)
        save_users(users)
        logger.info(f"Yangi foydalanuvchi qo'shildi: {user_id}")
        return True
    return False


# PDF talabi bo'yicha nomlanishlar
def save_user(chat_id: int) -> bool:
    """Foydalanuvchi chat_id sini users.json ga saqlash."""
    return add_user(chat_id)


def get_all_user_ids() -> list[int]:
    """Barcha foydalanuvchilar ID larini olish."""
    return load_users()


def remove_user(user_id: int) -> bool:
    """
    Botni bloklagan yoki chatni o'chirgan foydalanuvchini users.json dan o'chirish.
    (PDF 7-sahifa tavsiyasi)
    """
    users = load_users()
    if user_id in users:
        users.remove(user_id)
        save_users(users)
        logger.info(f"Foydalanuvchi ro'yxatdan o'chirildi (blok/o'chirilgan): {user_id}")
        return True
    return False


def get_users_count() -> int:
    """Foydalanuvchilar umumiy sonini qaytarish."""
    return len(load_users())
