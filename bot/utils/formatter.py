from typing import Dict, Any, Tuple, Optional
from bot.utils.hashtags import generate_hashtags


def format_resume(data: Dict[str, Any]) -> Tuple[str, Optional[str]]:
    """
    Nomzod anketasini vakansiya (rol) bo'yicha formatlash.
    Qaytaradi: (caption_yoki_xabar, qoshimcha_to'liq_matn_agar_kerak_bo'lsa)
    """
    role = data.get("role", "teacher")

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
    work_type = data.get("work_type", "-")
    salary = data.get("expected_salary", "-")

    if role == "admin":
        hashtags = generate_hashtags(role="admin", region=region)
        admin_software = data.get("admin_office_software", "-")
        admin_multitasking = data.get("admin_multitasking", "-")
        admin_reception = data.get("admin_guest_reception", "-")
        admin_conflict = data.get("admin_conflict_resolution", "-")
        admin_attendance = data.get("admin_attendance_payments", "-")
        admin_last_job = data.get("admin_last_job", "-")
        admin_why_ipe = data.get("admin_why_ipe", "-")
        admin_goals_2y = data.get("admin_goals_2y", "-")

        full_text = (
            f"{hashtags}\n\n"
            f"📋 **YANGI ADMINISTRATOR NOMZODI (ANKETA)**\n"
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
            f"• **Umumiy tajriba:** {experience} yil\n\n"
            f"💼 **MA'MURIY KO'NIKMALAR:**\n"
            f"• **Dasturlar va CRM:** {admin_software}\n"
            f"• **Multitasking va stress:** {admin_multitasking}\n"
            f"• **Mehmonlarni kutib olish:** {admin_reception}\n"
            f"• **Nizolarni hal qilish misoli:** {admin_conflict}\n"
            f"• **Davomat va to'lovlar nazorati:** {admin_attendance}\n"
            f"• **Oxirgi ish joyi va sababi:** {admin_last_job}\n\n"
            f"🎯 **HAMKORLIK VA SHARTLAR:**\n"
            f"• **Nega aynan IPE School:** {admin_why_ipe}\n"
            f"• **2 yildan keyingi maqsad:** {admin_goals_2y}\n"
            f"• **Ish turi:** {work_type}\n"
            f"• **Kutilayotgan oylik maosh:** {salary}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 _IPE School HR Bot orqali qabul qilindi_"
        )

        if len(full_text) <= 1024:
            return full_text, None

        caption = (
            f"{hashtags}\n\n"
            f"👤 **YANGI ADMINISTRATOR NOMZODI**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"• **F.I.SH:** {full_name}\n"
            f"• **Telefon:** `{phone}`\n"
            f"• **Telegram:** {username}\n"
            f"• **Hudud:** {region} ({age} yosh)\n"
            f"• **Daraja:** {degree} | {university}\n"
            f"• **Tajriba:** {experience} yil\n"
            f"• **Ingliz tili:** {english_level} | **Rus tili:** {russian_level}\n"
            f"• **Ish turi:** {work_type}\n"
            f"• **Kutilayotgan maosh:** {salary}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👇 _To'liq anketa tafsilotlari quyida keltirilgan:_"
        )
        return caption, full_text

    elif role == "sales":
        hashtags = generate_hashtags(role="sales", region=region)
        sales_exp = data.get("sales_experience", "-")
        sales_crm = data.get("sales_crm_tools", "-")
        sales_record = data.get("sales_record", "-")
        sales_objections = data.get("sales_objections", "-")
        sales_diff_client = data.get("sales_difficult_client", "-")
        sales_kpi = data.get("sales_kpi_rating", "-")
        sales_last_job = data.get("sales_last_job", "-")
        sales_why_ipe = data.get("sales_why_ipe", "-")
        sales_goals_2y = data.get("sales_goals_2y", "-")

        full_text = (
            f"{hashtags}\n\n"
            f"📋 **YANGI SOTUV MUTAXASSISI NOMZODI (ANKETA)**\n"
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
            f"• **Umumiy tajriba:** {experience} yil\n\n"
            f"📈 **SOTUV KO'NIKMALARI VA NATIJALAR:**\n"
            f"• **Sotuv yo'nalishi va tajribasi:** {sales_exp}\n"
            f"• **CRM va IP-telefoniya:** {sales_crm}\n"
            f"• **Shaxsiy sotuv rekordi:** {sales_record}\n"
            f"• **E'tirozlar bilan ishlash:** {sales_objections}\n"
            f"• **Qiyin mijoz bilan ishlash misoli:** {sales_diff_client}\n"
            f"• **KPI va stressga chidamlilik:** {sales_kpi}\n"
            f"• **Oxirgi ish joyi va sababi:** {sales_last_job}\n\n"
            f"🎯 **HAMKORLIK VA SHARTLAR:**\n"
            f"• **Nega aynan IPE School:** {sales_why_ipe}\n"
            f"• **2 yildan keyingi maqsad:** {sales_goals_2y}\n"
            f"• **Ish turi:** {work_type}\n"
            f"• **Kutilayotgan oylik maosh:** {salary}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🤖 _IPE School HR Bot orqali qabul qilindi_"
        )

        if len(full_text) <= 1024:
            return full_text, None

        caption = (
            f"{hashtags}\n\n"
            f"👤 **YANGI SOTUV MUTAXASSISI NOMZODI**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"• **F.I.SH:** {full_name}\n"
            f"• **Telefon:** `{phone}`\n"
            f"• **Telegram:** {username}\n"
            f"• **Hudud:** {region} ({age} yosh)\n"
            f"• **Daraja:** {degree} | {university}\n"
            f"• **Tajriba:** {experience} yil\n"
            f"• **Ingliz tili:** {english_level} | **Rus tili:** {russian_level}\n"
            f"• **Ish turi:** {work_type}\n"
            f"• **Kutilayotgan maosh:** {salary}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👇 _To'liq anketa tafsilotlari quyida keltirilgan:_"
        )
        return caption, full_text

    else:
        # Default: O'qituvchi (Ustoz)
        subjects = data.get("subjects", [])
        hashtags = generate_hashtags(subjects, role="teacher", region=region)
        subjects_str = ", ".join(subjects) if isinstance(subjects, list) else str(subjects)

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

        if len(full_text) <= 1024:
            return full_text, None

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
