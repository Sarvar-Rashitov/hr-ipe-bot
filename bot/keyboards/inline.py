from typing import List, Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# Barcha fanlar ro'yxati (IPE School kurslari)
AVAILABLE_SUBJECTS = [
    "IELTS",
    "CEFR",
    "SAT",
    "Prezident maktablariga tayyorlov",
    "IT (Python backend)",
    "English",
    "Rus tili",
    "Matematika",
    "Ixtisoslashtirilgan maktablarga tayyorlov",
    "Maktabgacha ta'lim"
]

# Hududlar ro'yxati
REGIONS = [
    "Toshkent shahri",
    "Toshkent viloyati",
    "Andijon viloyati",
    "Buxoro viloyati",
    "Farg'ona viloyati",
    "Jizzax viloyati",
    "Xorazm viloyati",
    "Namangan viloyati",
    "Navoiy viloyati",
    "Qashqadaryo viloyati",
    "Qoraqalpog'iston Resp.",
    "Samarqand viloyati",
    "Sirdaryo viloyati",
    "Surxondaryo viloyati"
]


def get_start_keyboard(channel_url: str, website_url: str = "https://ipeschool.uz") -> InlineKeyboardMarkup:
    """
    /start xabari uchun menyu tugmalari:
    1-qator: Kanal va Sayt (yonma-yon)
    2-qator: Asosiy katta 'Rezyume to'ldirish' tugmasi
    3-qator: 'Biz haqimizda' va 'Yordam'
    """
    keyboard = [
        [
            InlineKeyboardButton("📢 Telegram kanal", url=channel_url),
            InlineKeyboardButton("🌐 Rasmiy sayt", url=website_url)
        ],
        [
            InlineKeyboardButton("📝 Rezyume to'ldirish", callback_data="start_resume")
        ],
        [
            InlineKeyboardButton("ℹ️ Biz haqimizda", callback_data="about_us"),
            InlineKeyboardButton("❓ Yordam", callback_data="bot_help")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_about_keyboard() -> InlineKeyboardMarkup:
    """Biz haqimizda va yordam sahifasi tugmalari."""
    keyboard = [
        [
            InlineKeyboardButton("📝 Rezyume to'ldirish", callback_data="start_resume"),
        ],
        [
            InlineKeyboardButton("🔙 Bosh sahifa", callback_data="back_to_start")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_vacancies_keyboard() -> InlineKeyboardMarkup:
    """Vakansiyalar (lavozimlar) ro'yxati inline tugmalari."""
    keyboard = [
        [InlineKeyboardButton("👨‍🏫 O'qituvchi (Ustoz)", callback_data="vacancy:teacher")],
        [InlineKeyboardButton("💼 Administrator", callback_data="vacancy:admin")],
        [InlineKeyboardButton("📈 Sotuv mutaxassisi (Sotuvchi)", callback_data="vacancy:sales")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_subscription_keyboard(channel_url: str) -> InlineKeyboardMarkup:
    """Majburiy obuna tugmalari."""
    keyboard = [
        [InlineKeyboardButton("🔗 Kanalga a'zo bo'lish", url=channel_url)],
        [InlineKeyboardButton("✅ Obuna bo'ldim", callback_data="check_subscription")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_phone_request_keyboard() -> ReplyKeyboardMarkup:
    """Telefon raqam ulashish tugmasi."""
    keyboard = [
        [KeyboardButton("📱 Telefon raqamni yuborish", request_contact=True)],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_username_keyboard(user_username: Optional[str] = None) -> InlineKeyboardMarkup:
    """Telegram username tanlash tugmalari."""
    buttons = []
    if user_username:
        clean = user_username.lstrip("@")
        buttons.append([InlineKeyboardButton(f"✅ @{clean} ni saqlash", callback_data=f"username_auto:{clean}")])
    buttons.append([InlineKeyboardButton("❌ Username yo'q", callback_data="username_none")])
    return InlineKeyboardMarkup(buttons)


def get_regions_keyboard() -> InlineKeyboardMarkup:
    """14 ta viloyat/shahar inline tugmalari (2 tadan qator)."""
    buttons = []
    row = []
    for reg in REGIONS:
        row.append(InlineKeyboardButton(reg, callback_data=f"region:{reg}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)


def get_degree_keyboard() -> InlineKeyboardMarkup:
    """Ilmiy daraja / ma'lumot tugmalari."""
    keyboard = [
        [InlineKeyboardButton("🎓 Bakalavr", callback_data="degree:Bakalavr")],
        [InlineKeyboardButton("🎓 Magistr", callback_data="degree:Magistr")],
        [InlineKeyboardButton("🔬 Doktorant / PhD", callback_data="degree:Doktorant")],
        [InlineKeyboardButton("📚 Tugallanmagan oliy", callback_data="degree:Tugallanmagan oliy")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_russian_level_keyboard() -> InlineKeyboardMarkup:
    """Rus tili darajasi tugmalari."""
    keyboard = [
        [
            InlineKeyboardButton("🌟 Yuqori", callback_data="ru_level:Yuqori"),
            InlineKeyboardButton("👍 O'rta", callback_data="ru_level:O'rta")
        ],
        [
            InlineKeyboardButton("🌱 Boshlang'ich", callback_data="ru_level:Boshlang'ich"),
            InlineKeyboardButton("❌ Bilmayman", callback_data="ru_level:Bilmayman")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_experience_keyboard() -> InlineKeyboardMarkup:
    """Tajriba yillari tugmalari."""
    keyboard = [
        [
            InlineKeyboardButton("0 yil (yangi)", callback_data="exp:0"),
            InlineKeyboardButton("1-2 yil", callback_data="exp:1-2")
        ],
        [
            InlineKeyboardButton("3-5 yil", callback_data="exp:3-5"),
            InlineKeyboardButton("5+ yil", callback_data="exp:5+")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_subjects_keyboard(selected_subjects: List[str]) -> InlineKeyboardMarkup:
    """
    Fanlar ro'yxati (checkbox ko'rinishida, ko'p tanlovli).
    """
    buttons = []
    row = []
    for i, subj in enumerate(AVAILABLE_SUBJECTS):
        icon = "✅" if subj in selected_subjects else "⬜"
        text = f"{icon} {subj}"
        row.append(InlineKeyboardButton(text, callback_data=f"subj_toggle:{i}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    # Pastki qatorda yakunlash tugmasi
    count_text = f" ({len(selected_subjects)} ta tanlandi)" if selected_subjects else ""
    buttons.append([
        InlineKeyboardButton(f"✅ Tayyor / Davom etish{count_text}", callback_data="subj_done")
    ])
    return InlineKeyboardMarkup(buttons)


def get_average_result_keyboard() -> InlineKeyboardMarkup:
    """O'quvchilar o'rtacha natijasi (1 dan 10 gacha sonlar)."""
    row1 = [InlineKeyboardButton(str(i), callback_data=f"avg_res:{i}") for i in range(1, 6)]
    row2 = [InlineKeyboardButton(str(i), callback_data=f"avg_res:{i}") for i in range(6, 11)]
    return InlineKeyboardMarkup([row1, row2])


def get_rating_5_keyboard() -> InlineKeyboardMarkup:
    """Qiyin o'quvchi bilan ishlash bahosi (⭐️1 - ⭐️5)."""
    row = [InlineKeyboardButton(f"⭐️ {i}", callback_data=f"diff_rate:{i}") for i in range(1, 6)]
    return InlineKeyboardMarkup([row])


def get_work_type_keyboard() -> InlineKeyboardMarkup:
    """Ish turi tugmalari."""
    keyboard = [
        [InlineKeyboardButton("💼 Full-time (to'liq stavka)", callback_data="work:Full-time")],
        [InlineKeyboardButton("🕒 Part-time (yarim stavka)", callback_data="work:Part-time")],
        [InlineKeyboardButton("🔄 Moslashuvchan grafik", callback_data="work:Moslashuvchan grafik")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_admin_main_keyboard() -> InlineKeyboardMarkup:
    """Admin boshqaruv paneli tugmalari."""
    keyboard = [
        [InlineKeyboardButton("📢 Reklama yuborish (Broadcast)", callback_data="admin_broadcast")],
        [
            InlineKeyboardButton("📊 Statistika", callback_data="admin_stats"),
            InlineKeyboardButton("🔄 Qayta yangilash", callback_data="admin_refresh")
        ],
        [InlineKeyboardButton("👤 Nomzod sifatida ko'rish (Preview)", callback_data="admin_candidate_preview")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_broadcast_confirm_keyboard() -> InlineKeyboardMarkup:
    """Reklamani yuborishni tasdiqlash yoki bekor qilish (PDF standarti)."""
    keyboard = [
        [
            InlineKeyboardButton("✅ Yuborish", callback_data="bc_send"),
            InlineKeyboardButton("❌ Bekor qilish", callback_data="bc_cancel")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
