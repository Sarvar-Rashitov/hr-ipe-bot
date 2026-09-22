"""Barcha statik matnlar va xabarlar to'plami."""

# -------------------------------------------------------------
# START VA OBUNA MATNLARI
# -------------------------------------------------------------
START_WELCOME = (
    "👋 **Assalomu alaykum!**\n\n"
    "Siz **IPE School** o'quv markazining o'qituvchilar uchun anketa topshirish rasmiy botidasiz.\n\n"
    "🌐 Saytimiz: [ipeschool.uz](https://ipeschool.uz)\n"
    "🎯 Ushbu bot orqali siz o'qituvchilik lavozimiga ariza topshirishingiz mumkin.\n"
    "⏱ Anketa to'ldirish taxminan **5-7 daqiqa** vaqtingizni oladi.\n\n"
    "📌 Botdan to'liq foydalanish va anketani boshlash uchun quyidagi rasmiy kanalimizga a'zo bo'ling:"
)

SUBSCRIPTION_REQUIRED = (
    "Botdan foydalanish uchun quyidagi kanalga obuna bo'ling:"
)

SUBSCRIPTION_NOT_FOUND = (
    "❌ **Siz hali kanalimizga obuna bo'lmadingiz!**\n\n"
    "Iltimos, avval kanalga a'zo bo'ling va so'ngra **«✅ Obuna bo'ldim»** tugmasini bosing."
)

SUBSCRIPTION_SUCCESS = (
    "✅ **Obunangiz muvaffaqiyatli tasdiqlandi!**\n\n"
    "Endi IPE School jamoasiga qo'shilish uchun anketani to'ldirishni boshlashingiz mumkin.\n"
    "Anketani to'xtatish uchun istalgan vaqt /cancel buyrug'ini yuborishingiz mumkin.\n\n"
    "Keling, boshlaymiz! 👇"
)

# -------------------------------------------------------------
# ANKETA SAVOLLARI (1 - 30)
# -------------------------------------------------------------
Q_FULL_NAME = (
    "1️⃣ **Ism va familiyangizni kiriting:**\n"
    "_(Masalan: Alisher Navoiy)_"
)

Q_PHONE = (
    "2️⃣ **Telefon raqamingizni yuboring:**\n"
    "Quyidagi tugma orqali kontaktingizni ulashishingiz yoki raqamni `+998XXXXXXXXX` formatida yozishingiz mumkin."
)

Q_USERNAME = (
    "3️⃣ **Telegram username'ingiz:**\n"
    "Agar mavjud bo'lsa username'ingizni yuboring yoki quyidagi tugmalardan birini tanlang."
)

Q_REGION = (
    "4️⃣ **Yashash hududingizni tanlang:**\n"
    "Quyidagi ro'yxatdan o'zingiz istiqomat qiladigan hududni belgilang:"
)

Q_AGE = (
    "5️⃣ **Yoshingizni kiriting:**\n"
    "_(Masalan: 25)_"
)

Q_UNIVERSITY = (
    "6️⃣ **Tugatgan universitetingiz nomi:**\n"
    "_(Masalan: O'zbekiston Milliy Universiteti)_"
)

Q_FACULTY = (
    "7️⃣ **Tugatgan yo'nalishingiz / fakultetingiz:**\n"
    "_(Masalan: Amaliy matematika va intellektual texnologiyalar)_"
)

Q_DEGREE = (
    "8️⃣ **Ilmiy darajangiz / ma'lumotingizni tanlang:**"
)

Q_ENGLISH_LEVEL = (
    "9️⃣ **Ingliz tili darajangiz:**\n"
    "_(Masalan: IELTS 7.5, CEFR B2, Intermediate yoki sertifikat yo'q)_"
)

Q_RUSSIAN_LEVEL = (
    "🔟 **Rus tili darajangizni tanlang:**"
)

Q_EXPERIENCE_YEARS = (
    "1️⃣1️⃣ **O'qituvchilik tajribangiz (necha yil):**\n"
    "Quyidagi variantlardan birini tanlang yoki o'zingiz raqam sifatida yozing:"
)

Q_SUBJECTS = (
    "1️⃣2️⃣ **Qaysi fan(lar)dan dars berasiz?**\n\n"
    "Bir yoki bir nechta fanni tanlashingiz mumkin. Tanlash yakunlangach **«✅ Tayyor / Davom etish»** tugmasini bosing:"
)

Q_MAX_GROUP_SIZE = (
    "1️⃣3️⃣ **Siz dars bergan eng katta guruh hajmi (o'quvchilar soni):**\n"
    "_(Faqat butun son kiriting, masalan: 15)_"
)

Q_LAST_JOB = (
    "1️⃣4️⃣ **Oxirgi ish joyingiz va u yerdan ketish sababingiz:**\n"
    "_(Erkin matn shaklida yozing)_"
)

Q_STUDENT_RESULTS = (
    "1️⃣5️⃣ **O'quvchilaringiz erishgan natijalar (misollar keltiring):**\n"
    "_(Masalan: IELTS 8.0, Milliy sertifikat A+, DTM 180 ball va h.k.)_"
)

Q_BEST_STUDENT_RESULT = (
    "1️⃣6️⃣ **Siz erishgan eng faxrli / eng yaxshi o'quvchi natijasi:**\n"
    "_(Erkin matn shaklida yozing)_"
)

Q_AVERAGE_RESULT = (
    "1️⃣7️⃣ **O'quvchilaringizning umumiy o'rtacha natijasini 1 dan 10 gacha baholang:**"
)

Q_RETENTION_METHODS = (
    "1️⃣8️⃣ **O'quvchilarni kursda saqlab qolish (retention) uchun qanday choralar ko'rasiz?**\n"
    "_(Erkin matn shaklida yozing)_"
)

Q_DROPOUT_STEPS = (
    "1️⃣9️⃣ **Darsga kelmay qo'ygan yoki qiziqishi so'ngan o'quvchi bilan ishlash qadamlaringiz:**\n"
    "_(Erkin matn shaklida yozing)_"
)

Q_DIFFICULT_STUDENT_RATING = (
    "2️⃣0️⃣ **Qiyin / injiq o'quvchilar bilan ishlash mahoratingizni baholang (1-5 ⭐️):**"
)

Q_DIFFICULT_STUDENT_EXAMPLE = (
    "2️⃣0️⃣ (b) **Shu bo'yicha amaliyotingizdagi aniq bir misolni yozib bering:**\n"
    "_(Qiyin vaziyat qanday bo'lgan va uni qanday hal qilgansiz?)_"
)

Q_LESSON_STRUCTURE = (
    "2️⃣1️⃣ **Sizning odatdagi dars jarayoningiz qanday tuzilgan?**\n"
    "_(Vaqt taqsimoti, yangi mavzu, amaliyot, takrorlash va h.k.)_"
)

Q_METHODS = (
    "2️⃣2️⃣ **Darsda qanday zamonaviy pedagogik metodlardan foydalanasiz?**\n"
    "_(Masalan: Interactive learning, Flipped classroom, Gamification va h.k.)_"
)

Q_TECHNOLOGY_USAGE = (
    "2️⃣3️⃣ **Darslarda zamonaviy texnologiyalardan qanday foydalanasiz?**\n"
    "_(Masalan: Interaktiv doska, Kahoot, Quizlet, AI vositalari va h.k.)_"
)

Q_MIXED_LEVEL_APPROACH = (
    "2️⃣4️⃣ **Bitta guruhda turli darajadagi (kuchli va sekin o'zlashtiruvchi) o'quvchilar bo'lsa, darsni qanday tashkillashtirasiz?**"
)

Q_PARENT_NEGOTIATION = (
    "2️⃣5️⃣ **Norozi yoki xavotirdagi ota-ona bilan muzokara olib borish tajribangiz haqida yozing:**"
)

Q_WHY_IPE = (
    "2️⃣6️⃣ **Nega aynan IPE School o'quv markazida ishlashni xohlaysiz?**"
)

Q_GOALS_2Y = (
    "2️⃣7️⃣ **Kelgusi 2 yildan keyingi kasbiy maqsadingiz qanday?**"
)

Q_WORK_TYPE = (
    "2️⃣8️⃣ **Sizga qaysi ish turi qulay?**"
)

Q_EXPECTED_SALARY = (
    "2️⃣9️⃣ **Kutilayotgan oylik maoshingiz miqdori (so'mda):**\n"
    "_(Faqat raqam kiriting, masalan: 6000000)_"
)

Q_PHOTO = (
    "3️⃣0️⃣ **O'zingizning sifatli va xushmuomala rasmingizni yuboring:**\n"
    "_(Iltimos, rasmni hujjat (file) sifatida emas, oddiy rasm (photo) holatida yuboring)_"
)

# -------------------------------------------------------------
# VALIDATSIYA VA XATOLIK MATNLARI
# -------------------------------------------------------------
ERR_INVALID_FULL_NAME = (
    "⚠️ Iltimos, ism va familiyangizni to'liq kiriting (kamida 2 ta so'z).\n"
    "Masalan: _Alisher Navoiy_"
)

ERR_INVALID_PHONE = (
    "⚠️ Telefon raqam noto'g'ri kiritildi.\n"
    "Iltimos, quyidagi tugma orqali kontaktingizni ulashing yoki raqamni `+998901234567` formatida yozing."
)

ERR_INVALID_AGE = (
    "⚠️ Yosh faqat 18 dan 70 gacha bo'lgan butun son bo'lishi kerak.\n"
    "Iltimos, qaytadan kiriting (Masalan: 24):"
)

ERR_INVALID_NUMBER = (
    "⚠️ Iltimos, faqat musbat butun son kiriting."
)

ERR_INVALID_SALARY = (
    "⚠️ Maosh miqdori noto'g'ri kiritildi. Iltimos, musbat raqam kiriting.\n"
    "Masalan: `6000000` yoki `7 500 000`"
)

ERR_NO_SUBJECT_SELECTED = (
    "⚠️ Iltimos, kamida bitta fanni tanlang, so'ngra «✅ Tayyor / Davom etish» tugmasini bosing."
)

ERR_PHOTO_REQUIRED = (
    "⚠️ Iltimos, faqat **rasm** (photo) yuboring! Hujjat (fayl), video yoki matn qabul qilinmaydi."
)

CANCEL_SUCCESS = (
    "❌ **Anketa to'ldirish bekor qilindi.**\n\n"
    "Qayta boshlash uchun /start buyrug'ini bering."
)

SUBMISSION_SUCCESS = (
    "🎉 **Tabriklaymiz! Anketangiz muvaffaqiyatli qabul qilindi!**\n\n"
    "HR jamoamiz arizangizni ko'rib chiqib, tez orada siz bilan bog'lanishadi.\n\n"
    "Biz bilan bo'lganingiz uchun rahmat! Hurmat bilan, **IPE School** jamoasi."
)

# -------------------------------------------------------------
# ADMIN MATNLARI
# -------------------------------------------------------------
ADMIN_PANEL_TITLE = (
    "👑 **IPE School HR Bot — Admin Panel**\n\n"
    "👥 **Jami foydalanuvchilar:** `{total_users}` nafar\n\n"
    "Kerakli bo'limni tanlang:"
)

ADMIN_ACCESS_DENIED = (
    "⛔️ Kechirasiz, sizda ushbu bo'limga kirish huquqi yo'q."
)

ADMIN_BROADCAST_PROMPT = (
    "📢 **Reklama xabarini yuborish:**\n\n"
    "Foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yuboring.\n"
    "U oddiy matn, rasm yoki video (izoh / caption bilan birga) bo'lishi mumkin.\n\n"
    "Bekor qilish uchun: /cancel"
)

ADMIN_BROADCAST_PREVIEW = (
    "👁 **Xabarni ko'rib chiqish (Preview):**\n\n"
    "Quyida xabaringiz foydalanuvchilarga qanday ko'rinishi namoyish etildi.\n"
    "Barcha `{total_users}` ta foydalanuvchiga yuborishni tasdiqlaysizmi?"
)

ADMIN_BROADCAST_START = (
    "⏳ Reklama xabari yuborilmoqda, iltimos kuting..."
)

ADMIN_BROADCAST_FINISH = (
    "✅ **Reklama yuborish yakunlandi!**\n\n"
    "📊 **Natijalar:**\n"
    "• Muvaffaqiyatli yuborildi: **{sent_count}** ta\n"
    "• Xatoliklar (bloklagan/o'chirilgan): **{failed_count}** ta"
)

ADMIN_BROADCAST_CANCELLED = (
    "❌ Reklama yuborish bekor qilindi."
)
