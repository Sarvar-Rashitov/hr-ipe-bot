import unittest
from bot.utils.validators import (
    validate_full_name,
    validate_phone,
    validate_age,
    validate_positive_int,
    validate_salary
)
from bot.utils.hashtags import generate_hashtags, create_hashtag_from_text
from bot.utils.formatter import format_resume
from bot.utils.storage import (
    add_user,
    load_users,
    get_users_count,
    save_user,
    get_all_user_ids,
    remove_user
)
from bot.keyboards.inline import (
    get_start_keyboard,
    get_vacancies_keyboard,
    get_subscription_keyboard,
    get_regions_keyboard,
    get_degree_keyboard,
    get_russian_level_keyboard,
    get_experience_keyboard,
    get_subjects_keyboard,
    get_average_result_keyboard,
    get_rating_5_keyboard,
    get_work_type_keyboard,
    get_phone_request_keyboard,
    get_admin_main_keyboard,
    get_broadcast_confirm_keyboard,
    get_about_keyboard,
    AVAILABLE_SUBJECTS
)


class TestValidators(unittest.TestCase):
    def test_full_name(self):
        valid, name = validate_full_name("Alisher Navoiy")
        self.assertTrue(valid)
        self.assertEqual(name, "Alisher Navoiy")

        valid, _ = validate_full_name("Alisher")
        self.assertFalse(valid)

        valid, _ = validate_full_name("")
        self.assertFalse(valid)

    def test_phone(self):
        cases = [
            ("+998901234567", True, "+998901234567"),
            ("998901234567", True, "+998901234567"),
            ("901234567", True, "+998901234567"),
            ("+998 (90) 123-45-67", True, "+998901234567"),
            ("123456", False, ""),
            ("salom", False, ""),
        ]
        for inp, expected_valid, expected_out in cases:
            valid, out = validate_phone(inp)
            self.assertEqual(valid, expected_valid, f"Failed for {inp}")
            if expected_valid:
                self.assertEqual(out, expected_out)

    def test_age(self):
        self.assertTrue(validate_age("18")[0])
        self.assertTrue(validate_age("70")[0])
        self.assertTrue(validate_age("25")[0])
        self.assertFalse(validate_age("17")[0])
        self.assertFalse(validate_age("71")[0])
        self.assertFalse(validate_age("abc")[0])

    def test_positive_int(self):
        self.assertTrue(validate_positive_int("15", 1, 100)[0])
        self.assertFalse(validate_positive_int("0", 1, 100)[0])
        self.assertFalse(validate_positive_int("-5", 1, 100)[0])
        self.assertFalse(validate_positive_int("abc", 1, 100)[0])

    def test_salary(self):
        valid, val, s = validate_salary("5000000")
        self.assertTrue(valid)
        self.assertEqual(val, 5000000)
        self.assertEqual(s, "5 000 000 so'm")

        valid, val, s = validate_salary("7 500 000 so'm")
        self.assertTrue(valid)
        self.assertEqual(val, 7500000)

        self.assertFalse(validate_salary("0")[0])
        self.assertFalse(validate_salary("maosh")[0])


class TestHashtags(unittest.TestCase):
    def test_hashtags(self):
        tags = generate_hashtags(["Matematika", "Ingliz tili"])
        self.assertIn("#Matematika", tags)
        self.assertIn("#InglizTili", tags)

        single = create_hashtag_from_text("Fizika")
        self.assertEqual(single, "#Fizika")


class TestFormatter(unittest.TestCase):
    def test_format_resume(self):
        data = {
            "full_name": "Test Nomzod",
            "phone": "+998901234567",
            "username": "@testnomzod",
            "region": "Toshkent shahri",
            "age": 28,
            "university": "O'zMU",
            "faculty": "Matematika",
            "degree": "Magistr",
            "english_level": "IELTS 7.5",
            "russian_level": "Yuqori",
            "experience_years": "5+",
            "subjects": ["Matematika", "Fizika"],
            "max_group_size": 20,
            "last_job": "Xususiy maktab",
            "student_results": "Olimpiada 1-o'rin",
            "best_student_result": "IELTS 8.5",
            "average_result": "9",
            "retention_methods": "Interaktiv metodlar",
            "dropout_steps": "Telefon orqali suhbat",
            "difficult_student_rating": "5",
            "difficult_student_example": "Alohida yondashuv ko'rsatilgan",
            "lesson_structure": "45 min amaliyot",
            "methods": "Gamification",
            "technology_usage": "Quizlet",
            "mixed_level_approach": "Differensial ta'lim",
            "parent_negotiation": "Muloyim tushuntirish",
            "why_ipe": "Katta jamoa",
            "goals_2y": "Katta ustoz bo'lish",
            "work_type": "Full-time",
            "expected_salary": "8 000 000 so'm"
        }
        caption, full_text = format_resume(data)
        self.assertIn("#Matematika", caption)
        self.assertIn("Test Nomzod", caption)

    def test_format_resume_admin(self):
        data = {
            "role": "admin",
            "full_name": "Madina Rahimova",
            "phone": "+998911234567",
            "username": "@madina_admin",
            "region": "Toshkent shahri",
            "age": 25,
            "university": "O'zJOKU",
            "faculty": "Menejment",
            "degree": "Bakalavr",
            "english_level": "B2",
            "russian_level": "Yuqori",
            "experience_years": "2 yil",
            "admin_office_software": "Excel, Word, Modme CRM",
            "admin_multitasking": "Yuqori, vazifalarni Trello orqali rejalashtiraman",
            "admin_guest_reception": "Samimiy tabassum va qulaylik",
            "admin_conflict_resolution": "Xotirjam tinglab, yechim taklif qilganman",
            "admin_attendance_payments": "Ha, Modme orqali kunlik nazorat qilganman",
            "admin_last_job": "Edu Center, karyera o'sishi uchun",
            "admin_why_ipe": "Katta jamoa va zamonaviy tizim",
            "admin_goals_2y": "Bosh administrator bo'lish",
            "work_type": "Full-time",
            "expected_salary": "6 000 000 so'm"
        }
        caption, full_text = format_resume(data)
        self.assertIn("#Administrator", caption)
        self.assertIn("Madina Rahimova", caption)

    def test_format_resume_sales(self):
        data = {
            "role": "sales",
            "full_name": "Javohir Toshmatov",
            "phone": "+998931234567",
            "username": "@javohir_sales",
            "region": "Samarqand viloyati",
            "age": 26,
            "university": "SamDU",
            "faculty": "Marketing",
            "degree": "Bakalavr",
            "english_level": "O'rta",
            "russian_level": "Yuqori",
            "experience_years": "3 yil",
            "sales_experience": "Ta'lim va IT kurslari sotuvi, issiq/sovuq qo'ng'iroqlar",
            "sales_crm_tools": "AmoCRM, Bitrix24, Zadarma telefoniya",
            "sales_record": "Bir oyda 45 ta o'quvchi (120 mln so'm)",
            "sales_objections": "Qiymatni ko'rsatish va xavfni kamaytirish orqali",
            "sales_difficult_client": "Ikkilangan ota-onaga ochiq dars taklif qilib sotuv qilganman",
            "sales_kpi_rating": "5 - har doim planni 100%+ bajarganman",
            "sales_last_job": "Online School, yangi maqsadlar uchun",
            "sales_why_ipe": "Sifatli ta'lim mahsulotini sotishni xohlayman",
            "sales_goals_2y": "Sotuv bo'limi boshlig'i (ROP) bo'lish",
            "work_type": "Full-time",
            "expected_salary": "10 000 000 so'm"
        }
        caption, full_text = format_resume(data)
        self.assertIn("#Sotuvchi", caption)
        self.assertIn("Javohir Toshmatov", caption)


class TestKeyboards(unittest.TestCase):
    def test_keyboards_generate_without_error(self):
        kb_sub = get_subscription_keyboard("https://t.me/ipeschool_jobs")
        self.assertIsNotNone(kb_sub)

        kb_reg = get_regions_keyboard()
        self.assertIsNotNone(kb_reg)

        kb_deg = get_degree_keyboard()
        self.assertIsNotNone(kb_deg)

        kb_ru = get_russian_level_keyboard()
        self.assertIsNotNone(kb_ru)

        kb_exp = get_experience_keyboard()
        self.assertIsNotNone(kb_exp)

        kb_subj = get_subjects_keyboard(["Matematika"])
        self.assertIsNotNone(kb_subj)

        kb_avg = get_average_result_keyboard()
        self.assertIsNotNone(kb_avg)

        kb_rat = get_rating_5_keyboard()
        self.assertIsNotNone(kb_rat)

        kb_work = get_work_type_keyboard()
        self.assertIsNotNone(kb_work)

        kb_phone = get_phone_request_keyboard()
        self.assertIsNotNone(kb_phone)

    def test_vacancies_keyboard(self):
        kb_vac = get_vacancies_keyboard()
        self.assertIsNotNone(kb_vac)
        # 3 ta tugma (qatorlar bo'yicha)
        self.assertEqual(len(kb_vac.inline_keyboard), 3)
        self.assertEqual(kb_vac.inline_keyboard[0][0].callback_data, "vacancy:teacher")
        self.assertEqual(kb_vac.inline_keyboard[1][0].callback_data, "vacancy:admin")
        self.assertEqual(kb_vac.inline_keyboard[2][0].callback_data, "vacancy:sales")

    def test_start_keyboard(self):
        kb_start = get_start_keyboard("https://t.me/ipeschool", "https://ipeschool.uz", "https://www.instagram.com/ipe_school")
        self.assertIsNotNone(kb_start)
        # 4 qator
        self.assertEqual(len(kb_start.inline_keyboard), 4)
        # 1-qator: 2 ta tugma (Telegram kanal va Instagram)
        self.assertEqual(len(kb_start.inline_keyboard[0]), 2)
        self.assertEqual(kb_start.inline_keyboard[0][0].url, "https://t.me/ipeschool")
        self.assertEqual(kb_start.inline_keyboard[0][1].url, "https://www.instagram.com/ipe_school")
        # 2-qator: 1 ta tugma (sayt)
        self.assertEqual(len(kb_start.inline_keyboard[1]), 1)
        self.assertEqual(kb_start.inline_keyboard[1][0].url, "https://ipeschool.uz")
        # 3-qator: 1 ta tugma (start_resume callback)
        self.assertEqual(len(kb_start.inline_keyboard[2]), 1)
        self.assertEqual(kb_start.inline_keyboard[2][0].callback_data, "start_resume")
        # 4-qator: 2 ta tugma (about_us va bot_help)
        self.assertEqual(len(kb_start.inline_keyboard[3]), 2)
        self.assertEqual(kb_start.inline_keyboard[3][0].callback_data, "about_us")
        self.assertEqual(kb_start.inline_keyboard[3][1].callback_data, "bot_help")


    def test_about_keyboard(self):
        kb_about = get_about_keyboard()
        self.assertIsNotNone(kb_about)
        self.assertEqual(len(kb_about.inline_keyboard), 2)
        self.assertEqual(kb_about.inline_keyboard[0][0].callback_data, "start_resume")
        self.assertEqual(kb_about.inline_keyboard[1][0].callback_data, "back_to_start")

    def test_subjects_list(self):
        self.assertIn("IELTS", AVAILABLE_SUBJECTS)
        self.assertIn("IT (Python backend)", AVAILABLE_SUBJECTS)
        self.assertIn("Prezident maktablariga tayyorlov", AVAILABLE_SUBJECTS)
        self.assertEqual(len(AVAILABLE_SUBJECTS), 10)

    def test_admin_keyboards(self):
        kb_admin = get_admin_main_keyboard()
        self.assertIsNotNone(kb_admin)
        self.assertEqual(len(kb_admin.inline_keyboard), 3)

        kb_confirm = get_broadcast_confirm_keyboard()
        self.assertIsNotNone(kb_confirm)
        self.assertEqual(kb_confirm.inline_keyboard[0][0].callback_data, "bc_send")
        self.assertEqual(kb_confirm.inline_keyboard[0][1].callback_data, "bc_cancel")


class TestStorage(unittest.TestCase):
    def test_storage(self):
        test_uid = 999999999
        add_user(test_uid)
        users = load_users()
        self.assertIn(test_uid, users)

    def test_save_and_get_and_remove_user(self):
        test_uid = 888888888
        save_user(test_uid)
        all_users = get_all_user_ids()
        self.assertIn(test_uid, all_users)

        # Test remove user
        removed = remove_user(test_uid)
        self.assertTrue(removed)
        self.assertNotIn(test_uid, get_all_user_ids())


class TestNewFeatures(unittest.TestCase):
    def test_role_question_numbering(self):
        """Admin (22), Sotuvchi (23) va Ustoz (30) savol raqamlari tekshiruvi."""
        from bot import texts

        # 11-savol matni
        self.assertIn("O'qituvchilik", texts.get_experience_question("teacher"))
        self.assertIn("Kasbiy ish tajribangiz", texts.get_experience_question("admin"))
        self.assertIn("Kasbiy ish tajribangiz", texts.get_experience_question("sales"))

        # Admin: 20 (Ish turi), 21 (Maosh), 22 (Rasm)
        self.assertTrue(texts.get_work_type_question("admin").startswith("2️⃣0️⃣"))
        self.assertTrue(texts.get_salary_question("admin").startswith("2️⃣1️⃣"))
        self.assertTrue(texts.get_photo_question("admin").startswith("2️⃣2️⃣"))

        # Sotuvchi: 21 (Ish turi), 22 (Maosh), 23 (Rasm)
        self.assertTrue(texts.get_work_type_question("sales").startswith("2️⃣1️⃣"))
        self.assertTrue(texts.get_salary_question("sales").startswith("2️⃣2️⃣"))
        self.assertTrue(texts.get_photo_question("sales").startswith("2️⃣3️⃣"))

        # Ustoz: 28 (Ish turi), 29 (Maosh), 30 (Rasm)
        self.assertTrue(texts.get_work_type_question("teacher").startswith("2️⃣8️⃣"))
        self.assertTrue(texts.get_salary_question("teacher").startswith("2️⃣9️⃣"))
        self.assertTrue(texts.get_photo_question("teacher").startswith("3️⃣0️⃣"))

    def test_sanitize_md(self):
        """Markdown buzuvchi belgilar to'g'ri escape qilinishi tekshiruvi."""
        from bot.utils.formatter import sanitize_md
        self.assertEqual(sanitize_md("Ali_Vali"), "Ali\\_Vali")
        self.assertEqual(sanitize_md("*Top*"), "\\*Top\\*")
        self.assertEqual(sanitize_md("[Test]"), "\\[Test\\]")
        self.assertEqual(sanitize_md(""), "-")
        self.assertEqual(sanitize_md(None), "-")

    def test_multi_channel_subscription_keyboard(self):
        """Bir nechta kanalli obuna tugmalari tekshiruvi."""
        test_channels = [
            {"title": "📢 1-kanal", "url": "https://t.me/chan1"},
            {"title": "📢 2-kanal", "url": "https://t.me/chan2"}
        ]
        kb = get_subscription_keyboard(test_channels)
        self.assertEqual(len(kb.inline_keyboard), 3)
        self.assertEqual(kb.inline_keyboard[0][0].url, "https://t.me/chan1")
        self.assertEqual(kb.inline_keyboard[1][0].url, "https://t.me/chan2")
        self.assertEqual(kb.inline_keyboard[2][0].callback_data, "check_subscription")

    def test_hr_keyboards(self):
        """HR harakatlar klaviaturalari tekshiruvi."""
        from bot.keyboards.inline import get_hr_resume_keyboard, get_admin_hr_keyboard
        kb_hr = get_hr_resume_keyboard(12345678)
        self.assertEqual(kb_hr.inline_keyboard[0][0].callback_data, "hr_act:interview:12345678")
        self.assertEqual(kb_hr.inline_keyboard[0][1].callback_data, "hr_act:msg:12345678")
        self.assertEqual(kb_hr.inline_keyboard[1][0].callback_data, "hr_act:reject:12345678")

        kb_manage = get_admin_hr_keyboard([999999])
        self.assertTrue(any("hr_del:999999" in btn.callback_data for row in kb_manage.inline_keyboard for btn in row if btn.callback_data))

    def test_hr_storage(self):
        """HR menejerlarni saqlash va zaxira arizalar fayli tekshiruvi."""
        from bot.utils.hr_storage import add_hr_manager, remove_hr_manager, load_hr_manager_ids, save_submission

        test_hr = 7777777
        add_hr_manager(test_hr)
        self.assertIn(test_hr, load_hr_manager_ids())
        remove_hr_manager(test_hr)
        self.assertNotIn(test_hr, load_hr_manager_ids())

        sub_id = save_submission({
            "candidate_user_id": 12345,
            "full_name": "Test Nomzod",
            "role": "admin"
        })
        self.assertTrue(sub_id.startswith("SUB-"))

    def test_interview_location_and_datetime(self):
        """Suhbat manzili havolasi va sana/vaqt belgilash tizimi tekshiruvi."""
        from bot.keyboards.inline import get_candidate_reply_keyboard, get_hr_interview_time_keyboard
        from bot import config, texts

        # 1. Configdagi Google Maps manzili
        self.assertEqual(config.OFFICE_LOCATION_URL, "https://maps.app.goo.gl/7g5mPL7AD5kscFqi9")

        # 2. Nomzod javob klaviaturasi (manzil linki bilan)
        kb_loc = get_candidate_reply_keyboard(location_url=config.OFFICE_LOCATION_URL)
        self.assertEqual(len(kb_loc.inline_keyboard), 2)
        self.assertEqual(kb_loc.inline_keyboard[0][0].url, "https://maps.app.goo.gl/7g5mPL7AD5kscFqi9")
        self.assertEqual(kb_loc.inline_keyboard[1][0].callback_data, "cand_reply")

        # 3. HR sana/vaqt tanlash klaviaturasi
        kb_time = get_hr_interview_time_keyboard(123456, "office")
        self.assertGreaterEqual(len(kb_time.inline_keyboard), 4)
        self.assertEqual(kb_time.inline_keyboard[0][0].callback_data, "hr_t:123456:off:t1")
        self.assertEqual(kb_time.inline_keyboard[0][1].callback_data, "hr_t:123456:off:t2")

        # 4. Shablon matni to'g'ri formatlanishi
        formatted_invite = texts.HR_INVITE_OFFICE_TEMPLATE.format(
            name="Jasur",
            role="Administrator",
            datetime="28-sentabr soat 14:00 da",
            location_url=config.OFFICE_LOCATION_URL
        )
        self.assertIn("Jasur", formatted_invite)
        self.assertIn("Administrator", formatted_invite)
        self.assertIn("28-sentabr soat 14:00 da", formatted_invite)
        self.assertIn("https://maps.app.goo.gl/7g5mPL7AD5kscFqi9", formatted_invite)


if __name__ == "__main__":
    unittest.main()

