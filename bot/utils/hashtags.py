import re
from typing import List

SUBJECT_HASHTAGS = {
    "IELTS": "#IELTS",
    "CEFR": "#CEFR",
    "SAT": "#SAT",
    "Prezident maktablariga tayyorlov": "#PrezidentMaktabi",
    "IT (Python backend)": "#PythonBackend",
    "English": "#English",
    "Rus tili": "#RusTili",
    "Matematika": "#Matematika",
    "Ixtisoslashtirilgan maktablarga tayyorlov": "#IxtisosMaktab",
    "Maktabgacha ta'lim": "#MaktabgachaTalim",
    "Ingliz tili": "#InglizTili",
    "Fizika": "#Fizika",
    "IT / Dasturlash": "#IT",
}


from typing import List, Optional


def create_hashtag_from_text(text: str) -> str:
    """Ixtiyoriy matndan chiroyli hashtag yasash."""
    if text in SUBJECT_HASHTAGS:
        return SUBJECT_HASHTAGS[text]
    
    # Harflar va raqamlardan boshqa belgilarni olib tashlash
    cleaned = re.sub(r"[^\w]", "", text)
    if cleaned:
        return f"#{cleaned}"
    return "#IPE"


def generate_hashtags(
    subjects: Optional[List[str]] = None,
    role: str = "teacher",
    region: Optional[str] = None
) -> str:
    """
    Vakansiya (rol), fanlar va hudud bo'yicha hashtaglar qatorini hosil qilish.
    """
    tags = []
    if role == "admin":
        tags.extend(["#Administrator", "#Admin"])
    elif role == "sales":
        tags.extend(["#Sotuvchi", "#Sales", "#SotuvBolimi"])
    else:
        tags.extend(["#Oqituvchi", "#Ustoz"])
        if subjects:
            for s in subjects:
                tag = create_hashtag_from_text(s.strip())
                if tag not in tags:
                    tags.append(tag)

    if region and region != "-":
        reg_tag = create_hashtag_from_text(region)
        if reg_tag not in tags:
            tags.append(reg_tag)

    return " ".join(tags)
