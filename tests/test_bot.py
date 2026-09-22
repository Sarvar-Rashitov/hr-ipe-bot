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
from bot.utils.storage import add_user, load_users, get_users_count
from bot.keyboards.inline import (
    get_subscription_keyboard,
    get_regions_keyboard,
    get_degree_keyboard,
    get_russian_level_keyboard,
    get_experience_keyboard,
    get_subjects_keyboard,
    get_average_result_keyboard,
    get_rating_5_keyboard,
    get_work_type_keyboard,
    get_phone_request_keyboard
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


class TestStorage(unittest.TestCase):
    def test_storage(self):
        initial_count = get_users_count()
        # Test adding a unique user
        test_uid = 999999999
        add_user(test_uid)
        users = load_users()
        self.assertIn(test_uid, users)


if __name__ == "__main__":
    unittest.main()
