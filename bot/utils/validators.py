import re
from typing import Optional, Tuple


def validate_full_name(text: str) -> Tuple[bool, str]:
    """
    Ism va familiyani tekshirish.
    Kamida 2 ta so'zdan iborat bo'lishi kerak.
    """
    if not text:
        return False, ""
    cleaned = text.strip()
    words = [w for w in cleaned.split() if len(w) > 1]
    if len(words) >= 2:
        return True, " ".join(words)
    return False, ""


def validate_phone(text: str) -> Tuple[bool, str]:
    """
    Telefon raqamini tekshirish va tozalash.
    Qabul qilinadigan formatlar:
    +998901234567, 998901234567, 901234567, +998 90 123-45-67 va h.k.
    """
    if not text:
        return False, ""
    
    # Faqat raqamlar va '+' belgisini qoldirish
    digits_only = re.sub(r"[^\d]", "", text)
    
    # Agar 9 ta raqam bo'lsa (masalan 901234567) -> +998 qo'shamiz
    if len(digits_only) == 9:
        digits_only = "998" + digits_only
    
    # O'zbekiston raqami 12 ta raqamdan iborat (998XXXXXXXXX)
    if len(digits_only) == 12 and digits_only.startswith("998"):
        formatted = f"+{digits_only}"
        return True, formatted
    
    return False, ""


def validate_age(text: str) -> Tuple[bool, int]:
    """
    Yoshni tekshirish: 18 dan 70 gacha bo'lgan butun son.
    """
    if not text:
        return False, 0
    cleaned = text.strip()
    if cleaned.isdigit():
        age = int(cleaned)
        if 18 <= age <= 70:
            return True, age
    return False, 0


def validate_positive_int(text: str, min_val: int = 1, max_val: Optional[int] = None) -> Tuple[bool, int]:
    """
    Musbat butun sonni tekshirish (masalan: guruh hajmi, tajriba).
    """
    if not text:
        return False, 0
    cleaned = text.strip()
    if cleaned.isdigit():
        val = int(cleaned)
        if val >= min_val and (max_val is None or val <= max_val):
            return True, val
    return False, 0


def validate_salary(text: str) -> Tuple[bool, int, str]:
    """
    Kutilayotgan maoshni tekshirish va formatlash.
    Masalan: 6000000 -> (True, 6000000, "6 000 000 so'm")
    """
    if not text:
        return False, 0, ""
    # "so'm", "som", "uzs", dollar belgilari, bo'shliqlar va nuqtalarni tozalash
    cleaned = re.sub(r"[^\d]", "", text)
    if cleaned and cleaned.isdigit():
        val = int(cleaned)
        if val > 0:
            formatted_str = f"{val:,}".replace(",", " ") + " so'm"
            return True, val, formatted_str
    return False, 0, ""
