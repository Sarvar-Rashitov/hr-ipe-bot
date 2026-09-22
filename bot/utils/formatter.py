from typing import Dict, Any, Tuple, Optional
from bot.utils.hashtags import generate_hashtags


def format_resume(data: Dict[str, Any]) -> Tuple[str, Optional[str]]:
    """
    Nomzod anketasini formatlash.
    Qaytaradi: (caption_yoki_xabar, qoshimcha_to'liq_matn_agar_kerak_bo'lsa)
    Telegram caption limiti 1024 ta belgi bo'lgani sababli,
    agar to'liq matn 1024 dan oshsa, rasm bilan qisqacha xulosa,
    ortidan esa to'liq anketa tafsilotlari yuboriladi.
    """
    subjects = data.get("subjects", [])
    hashtags = generate_hashtags(subjects)
    subjects_str = ", ".join(subjects) if isinstance(subjects, list) else str(subjects)

    full_name = data.get("full_name", "-")
    phone = data.get("phone", "-")
    username = data.get("username", "-")
    if username != "-" and not username.startswith("@") and username != "Username yo'q":
        username = f"@{username}"
        
    region = data.get("region", "-")
    age = data.get("age", "-")
    university = data.get("university", "-")
    faculty = data.get("faculty", "-")
    degree = data.get("degree", "-")
    english_level = data.get("english_level", "-")
    russian_level = data.get("russian_level", "-")
    experience = data.get("experience_years", "-")
    max_group = data.get("max_group_size", "-")
    last_job = data.get("last_job", "-")
    student_results = data.get("student_results", "-")
    best_student_result = data.get("best_student_result", "-")
    avg_result = data.get("average_result", "-")
    retention = data.get("retention_methods", "-")
    dropout = data.get("dropout_steps", "-")
    diff_rating = data.get("difficult_student_rating", "-")
    diff_example = data.get("difficult_student_example", "-")
    lesson_structure = data.get("lesson_structure", "-")
    methods = data.get("methods", "-")
    tech = data.get("technology_usage", "-")
    mixed_level = data.get("mixed_level_approach", "-")
    parent_neg = data.get("parent_negotiation", "-")
    why_ipe = data.get("why_ipe", "-")
    goals_2y = data.get("goals_2y", "-")
    work_type = data.get("work_type", "-")
    salary = data.get("expected_salary", "-")

    # To'liq batafsil anketa matni
    full_text = (
        f"{hashtags}\n\n"
        f"📋 **YANGI O'QITUVCHI NOMZODI (ANKETA)**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 **SHAXSIY MA'LUMOTLAR:**\n"
        f"• **F.I.SH:** {full_name}\n"
        f"• **Telefon:** `{phone}`\n"
        f"• **Telegram:** {username}\n"
        f"• **Hudud:** {region}\n"
        f"• **Yosh:** {age} yosh\n\n"
        f"🎓 **MA'LUMOT VA MALAKA:**\n"
        f"• **Universitet:** {university}\n"
        f"• **Fakultet / Yo'nalish:** {faculty}\n"
        f"• **Daraja:** {degree}\n"
        f"• **Ingliz tili:** {english_level}\n"
        f"• **Rus tili:** {russian_level}\n"
        f"• **Tajriba:** {experience} yil\n\n"
        f"📚 **FANLAR VA O'QITISH:**\n"
        f"• **Dars beradigan fanlari:** {subjects_str}\n"
        f"• **Eng katta guruh hajmi:** {max_group} nafar\n"
        f"• **Oxirgi ish joyi va sababi:** {last_job}\n"
        f"• **O'quvchilar natijalari:** {student_results}\n"
        f"• **Eng yaxshi natija:** {best_student_result}\n"
        f"• **O'rtacha natija (1-10):** {avg_result}/10\n\n"
        f"💡 **METODIKA VA PEDAGOGIKA:**\n"
        f"• **Retention (saqlab qolish):** {retention}\n"
        f"• **Qoldirgan o'quvchi bilan ishlash:** {dropout}\n"
        f"• **Qiyin o'quvchi bahosi (1-5):** {diff_rating} ⭐️\n"
        f"• **Qiyin o'quvchi amaliy misoli:** {diff_example}\n"
        f"• **Dars jarayoni tuzilishi:** {lesson_structure}\n"
        f"• **Qo'llaniladigan metodlar:** {methods}\n"
        f"• **Texnologiyadan foydalanish:** {tech}\n"
        f"• **Turli darajadagi o'quvchilar bilan ishlash:** {mixed_level}\n"
        f"• **Norozi ota-onalar bilan muzokara:** {parent_neg}\n\n"
        f"💼 **HAMKORLIK VA SHARTLAR:**\n"
        f"• **Nega aynan IPE School:** {why_ipe}\n"
        f"• **2 yildan keyingi maqsad:** {goals_2y}\n"
        f"• **Ish turi:** {work_type}\n"
        f"• **Kutilayotgan oylik maosh:** {salary}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 _IPE School HR Bot orqali qabul qilindi_"
    )

    # Agar matn 1024 belgidan oshmasa, uni bitta rasm captionida yuborish mumkin
    if len(full_text) <= 1024:
        return full_text, None

    # Agar 1024 dan oshsa:
    # 1. Rasm osti uchun chiroyli qisqartirilgan asosiy karta (caption)
    caption = (
        f"{hashtags}\n\n"
        f"👤 **YANGI O'QITUVCHI NOMZODI**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"• **F.I.SH:** {full_name}\n"
        f"• **Telefon:** `{phone}`\n"
        f"• **Telegram:** {username}\n"
        f"• **Hudud:** {region} ({age} yosh)\n"
        f"• **Daraja:** {degree} | {university}\n"
        f"• **Fanlar:** {subjects_str}\n"
        f"• **Tajriba:** {experience} yil\n"
        f"• **Ingliz tili:** {english_level} | **Rus tili:** {russian_level}\n"
        f"• **Ish turi:** {work_type}\n"
        f"• **Kutilayotgan maosh:** {salary}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👇 _To'liq 30 savolli anketa tafsiloti quyida keltirilgan:_"
    )

    return caption, full_text
