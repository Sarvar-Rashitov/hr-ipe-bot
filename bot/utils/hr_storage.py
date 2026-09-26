import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

# Data papkasi
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

HR_MANAGERS_FILE = DATA_DIR / "hr_managers.json"
SUBMISSIONS_FILE = DATA_DIR / "submissions.json"


def load_hr_manager_ids() -> List[int]:
    """Saqlangan HR menejerlar Telegram ID ro'yxatini yuklash."""
    if not HR_MANAGERS_FILE.exists():
        return []
    try:
        with open(HR_MANAGERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return [int(uid) for uid in data if str(uid).isdigit()]
    except Exception as e:
        logger.error(f"HR menejerlar faylini o'qishda xatolik: {e}")
    return []


def save_hr_manager_ids(manager_ids: List[int]) -> bool:
    """HR menejerlar ID ro'yxatini faylga saqlash."""
    try:
        # Dublikatlardan tozalash
        clean_ids = list(dict.fromkeys(manager_ids))
        with open(HR_MANAGERS_FILE, "w", encoding="utf-8") as f:
            json.dump(clean_ids, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"HR menejerlar fayliga yozishda xatolik: {e}")
        return False


def add_hr_manager(user_id: int) -> bool:
    """Yangi HR menejerni qo'shish."""
    managers = load_hr_manager_ids()
    if user_id not in managers:
        managers.append(user_id)
        return save_hr_manager_ids(managers)
    return True


def remove_hr_manager(user_id: int) -> bool:
    """HR menejerni ro'yxatdan o'chirish."""
    managers = load_hr_manager_ids()
    if user_id in managers:
        managers.remove(user_id)
        return save_hr_manager_ids(managers)
    return False


def get_all_hr_managers(env_managers: Optional[List[int]] = None) -> List[int]:
    """
    Barcha HR menejerlar ID ro'yxati (.env dagi va fayldagi birlashtirilgan).
    """
    file_managers = load_hr_manager_ids()
    combined = list(file_managers)
    if env_managers:
        for mid in env_managers:
            if mid not in combined:
                combined.append(mid)
    return combined


def save_submission(data: Dict[str, Any]) -> str:
    """
    Kelib tushgan yangi anketani data/submissions.json fayliga zaxira sifatida saqlash.
    Qaytaradi: submission_id (masalan: SUB-20260926-112000-1234)
    """
    submissions = []
    if SUBMISSIONS_FILE.exists():
        try:
            with open(SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, list):
                    submissions = loaded
        except Exception as e:
            logger.error(f"Submissions faylini o'qishda xatolik: {e}")

    now = datetime.now()
    candidate_id = data.get("candidate_user_id") or data.get("user_id") or "unknown"
    submission_id = f"SUB-{now.strftime('%Y%m%d-%H%M%S')}-{candidate_id}"

    record = {
        "submission_id": submission_id,
        "created_at": now.isoformat(),
        "candidate_user_id": candidate_id,
        "role": data.get("role", "teacher"),
        "full_name": data.get("full_name", ""),
        "phone": data.get("phone", ""),
        "username": data.get("username", ""),
        "data": {k: v for k, v in data.items() if not k.startswith("_")}
    }

    submissions.append(record)

    try:
        with open(SUBMISSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(submissions, f, ensure_ascii=False, indent=2)
        logger.info(f"Anketa muvaffaqiyatli zaxiraga olindi: {submission_id}")
    except Exception as e:
        logger.error(f"Submissions faylini saqlashda xatolik: {e}")

    return submission_id


def get_submission_by_candidate_id(candidate_id: int) -> Optional[Dict[str, Any]]:
    """Nomzod ID bo'yicha oxirgi anketani qidirish."""
    if not SUBMISSIONS_FILE.exists():
        return None
    try:
        with open(SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
            submissions = json.load(f)
            # Oxirgisidan boshlab qidirish
            for sub in reversed(submissions):
                if sub.get("candidate_user_id") == candidate_id:
                    return sub
    except Exception as e:
        logger.error(f"Submissions qidirishda xatolik: {e}")
    return None
