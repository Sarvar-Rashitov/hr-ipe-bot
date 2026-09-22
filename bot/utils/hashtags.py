import re
from typing import List

SUBJECT_HASHTAGS = {
    "Matematika": "#Matematika",
    "Ingliz tili": "#InglizTili",
    "Fizika": "#Fizika",
    "Kimyo": "#Kimyo",
    "Biologiya": "#Biologiya",
    "Tarix": "#Tarix",
    "Ona tili va adabiyot": "#OnaTili",
    "IT / Dasturlash": "#IT",
    "Mental arifmetika": "#MentalArifmetika",
    "Boshlang'ich ta'lim": "#BoshlangichTalim",
    "Geografiya": "#Geografiya",
    "Rus tili": "#RusTili",
    "Koreys tili": "#KoreysTili",
    "Nemis tili": "#NemisTili",
    "Arab tili": "#ArabTili",
    "Huquq": "#Huquq",
    "Iqtisodiyot": "#Iqtisodiyot",
    "Robototexnika": "#Robototexnika",
}


def create_hashtag_from_text(subject: str) -> str:
    """Ixtiyoriy fan nomidan chiroyli hashtag yasash."""
    if subject in SUBJECT_HASHTAGS:
        return SUBJECT_HASHTAGS[subject]
    
    # Harflar va raqamlardan boshqa belgilarni olib tashlash
    cleaned = re.sub(r"[^\w]", "", subject)
    if cleaned:
        return f"#{cleaned}"
    return "#Oqituvchi"


def generate_hashtags(subjects: List[str]) -> str:
    """
    Fanlar ro'yxatidan hashtaglar qatorini hosil qilish.
    Masalan: ['Matematika', 'Fizika'] -> '#Matematika #Fizika'
    """
    if not subjects:
        return "#Nomzod #Oqituvchi"
    
    tags = []
    for s in subjects:
        tag = create_hashtag_from_text(s.strip())
        if tag not in tags:
            tags.append(tag)
    
    return " ".join(tags)
