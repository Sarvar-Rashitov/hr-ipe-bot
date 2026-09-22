"""Barcha statik matnlar va xabarlar to'plami."""

# -------------------------------------------------------------
# START VA OBUNA MATNLARI
# -------------------------------------------------------------
START_WELCOME = (
    "👋 **Assalomu alaykum!**\n\n"
    "🏫 **IPE School o'quv markazi** — yoshlarga zamonaviy bilim va xalqaro standartlar asosida sifatli ta'lim beruvchi yetakchi markazlardan biridir. Biz o'quvchilarimizning yuksak natijalarga erishishi hamda ustozlarimizning professional rivojlanishi uchun barcha qulay shart-sharoitlarni taqdim etamiz.\n\n"
    "🎯 Ushbu bot orqali siz **IPE School** jamoasiga o'qituvchilik lavozimiga rezyume (anketa) topshirishingiz mumkin.\n\n"
    "📢 **Kanalimizga obuna bo'ling:**\n"
    "Barcha yangiliklar, bo'sh ish o'rinlari va muhim e'lonlardan doimiy xabardor bo'lish hamda anketani to'ldirish uchun rasmiy Telegram kanalimizga a'zo bo'lishingiz lozim.\n\n"
    "Quyidagi tugmalar orqali kanalimiz va saytimizga o'tishingiz yoki rezyume to'ldirishni boshlashingiz mumkin:"
)

SUBSCRIPTION_REQUIRED = (
    "Botdan to'liq foydalanish va rezyume to'ldirish uchun quyidagi kanalga obuna bo'ling:"
)

SUBSCRIPTION_NOT_FOUND = (
    "❌ **Siz hali rasmiy kanalimizga a'zo bo'lmadingiz!**\n\n"
    "Rezyume to'ldirishni boshlash uchun avval rasmiy kanalimizga obuna bo'ling, so'ngra quyidagi tugmani bosing."
)

SUBSCRIPTION_SUCCESS = (
    "✅ **Obunangiz muvaffaqiyatli tasdiqlandi!**\n\n"
    "Endi IPE School jamoasiga qo'shilish uchun anketani to'ldirishni boshlashingiz mumkin.\n"
    "Anketani to'xtatish uchun istalgan vaqt /cancel buyrug'ini yuborishingiz mumkin.\n\n"
    "Keling, boshlaymiz! 👇"
)

CHOOSE_VACANCY = (
    "💼 **Qaysi vakansiya (lavozim) bo'yicha rezyume topshirmoqchisiz?**\n\n"
    "Quyidagi yo'nalishlardan birini tanlang:"
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
# ADMINISTRATOR ANKETA SAVOLLARI
# -------------------------------------------------------------
Q_ADMIN_OFFICE_SOFTWARE = (
    "1️⃣2️⃣ **Kompyuter dasturlari va CRM bilish darajangiz:**\n"
    "Word, Excel, Google Sheets yoki CRM tizimlari (masalan, Modme, Bitrix24, va h.k.) bilan ishlash tajribangiz haqida yozing:"
)

Q_ADMIN_MULTITASKING = (
    "1️⃣3️⃣ **Bir vaqtda bir nechta vazifani bajarish (multitasking) va stressga chidamliligingiz:**\n"
    "Qizg'in vaziyatlarda ishingizni qanday rejalashtirasiz va stressli holatlarni qanday yengasiz?"
)

Q_ADMIN_GUEST_RECEPTION = (
    "1️⃣4️⃣ **O'quv markaziga kelgan mehmon va ota-onalarni kutib olish:**\n"
    "Sizningcha, markazimizga birinchi marta kelgan mehmon/ota-onada ajoyib taassurot qoldirish uchun qanday munosabat ko'rsatish lozim?"
)

Q_ADMIN_CONFLICT_RESOLUTION = (
    "1️⃣5️⃣ **Nizoli vaziyatlar yoki e'tirozlar bilan ishlash:**\n"
    "Norozi yoki asabiy ota-ona / o'quvchi murojaat qilganda qanday yo'l tutasiz? O'tmishdagi amaliy tajribangizdan misol keltiring:"
)

Q_ADMIN_ATTENDANCE_PAYMENTS = (
    "1️⃣6️⃣ **Davomat va to'lovlarni nazorat qilish:**\n"
    "O'quvchilar davomati, darsga kelmay qolganlarni aniqlash va o'z vaqtida to'lovlarni nazorat qilish bo'yicha tajribangiz bormi?"
)

Q_ADMIN_LAST_JOB = (
    "1️⃣7️⃣ **Oxirgi ish joyingiz va ketish sababi:**\n"
    "Oxirgi marta qayerda, qaysi lavozimda ishlagansiz va u yerdan ketishingizga nima sabab bo'lgan?"
)

Q_ADMIN_WHY_IPE = (
    "1️⃣8️⃣ **Nega aynan IPE School o'quv markazida administrator bo'lib ishlamoqchisiz?**\n"
    "Bizning jamoamizni tanlashingizga nima turtki bo'ldi?"
)

Q_ADMIN_GOALS_2Y = (
    "1️⃣9️⃣ **Kelgusi 2 yildan keyingi kasbiy maqsadingiz:**\n"
    "O'zingizni kelajakda qanday mutaxassis darajasida ko'rasiz?"
)

# -------------------------------------------------------------
# SOTUV MUTAXASSISI ANKETA SAVOLLARI
# -------------------------------------------------------------
Q_SALES_EXPERIENCE = (
    "1️⃣2️⃣ **Sotuv sohasidagi tajribangiz:**\n"
    "Qaysi sohalarda (ta'lim, xizmatlar, chakana, B2B/B2C) sotuv bilan shug'ullangansiz? Qo'ng'iroqlar (issiq/sovuq) bilan ishlash tajribangiz qanday?"
)

Q_SALES_CRM_TOOLS = (
    "1️⃣3️⃣ **CRM tizimlari va IP-telefoniya:**\n"
    "AmoCRM, Bitrix24 yoki boshqa CRM tizimlari, shuningdek IP-telefoniya bilan ishlash tajribangiz bormi?"
)

Q_SALES_RECORD = (
    "1️⃣4️⃣ **Eng katta shaxsiy sotuv rekordingiz:**\n"
    "Bir oy davomida erishgan eng yuqori sotuv natijangiz (summa yoki jalb qilingan o'quvchilar/mijozlar soni) haqida yozing:"
)

Q_SALES_OBJECTIONS = (
    "1️⃣5️⃣ **Mijoz e'tirozlari bilan ishlash:**\n"
    "Mijoz: *«Kurslaringiz qimmat ekan»* yoki *«O'ylab ko'rib xabar beramiz»* desa, unga qanday javob berasiz va sotuvni qanday yopasiz?"
)

Q_SALES_DIFFICULT_CLIENT = (
    "1️⃣6️⃣ **Qiyin yoki ikkilanuvchi mijoz bilan ishlash:**\n"
    "Ikkilanib turgan yoki norozi mijozni ko'ndirganingiz haqida aniq bitta hayotiy misol keltiring:"
)

Q_SALES_KPI_RATING = (
    "1️⃣7️⃣ **Oylik reja (KPI) va stressga chidamlilik:**\n"
    "Sotuv rejasini bajarishga munosabatingiz va bosim ostida ishlash qobiliyatingiz haqida qisqacha izoh bering:"
)

Q_SALES_LAST_JOB = (
    "1️⃣8️⃣ **Oxirgi ish joyingiz va ketish sababi:**\n"
    "Oxirgi marta qaysi kompaniyada sotuv bo'yicha ishlagansiz va nima sababdan ketgansiz?"
)

Q_SALES_WHY_IPE = (
    "1️⃣9️⃣ **Nega aynan IPE School'da sotuv mutaxassisi bo'lib ishlamoqchisiz?**\n"
    "Nima uchun aynan ta'lim sohasidagi sotuvni tanladingiz?"
)

Q_SALES_GOALS_2Y = (
    "2️⃣0️⃣ **Kelgusi 2 yildan keyingi moliyaviy va kasbiy maqsadingiz:**\n"
    "O'zingizni kelajakda qanday darajada (TOP menejer, boshliq) ko'rasiz va qancha daromadga chiqmoqchisiz?"
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
    "👑 **Assalomu alaykum, Hurmatli Administrator!**\n\n"
    "Siz **IPE School HR Bot** boshqaruv panelidasiz.\n\n"
    "📊 **Tizim holati:**\n"
    "• Jami foydalanuvchilar: `{total_users}` nafar\n"
    "• Bot holati: 🟢 Faol\n\n"
    "Quyidagi tugmalar orqali kerakli amalni tanlang:"
)

ADMIN_STATS_TEXT = (
    "📊 **IPE School HR Bot — Statistika**\n\n"
    "👥 **Jami foydalanuvchilar:** `{total_users}` nafar\n"
    "📢 **Obuna kanali:** `{channel}`\n"
    "💬 **HR guruhi ID:** `{hr_chat_id}`\n"
    "🤖 **Bot holati:** 🟢 Faol ishlamoqda\n\n"
    "_Foydalanuvchilar ro'yxati users.json faylida saqlanadi._"
)

ADMIN_ACCESS_DENIED = (
    "⛔️ Kechirasiz, sizda ushbu bo'limga kirish huquqi yo'q."
)

ADMIN_BROADCAST_PROMPT = (
    "📢 **Reklama uchun matn, rasm yoki video yuboring (caption bilan yozing):**\n\n"
    "Bekor qilish uchun: /cancel"
)

ADMIN_BROADCAST_PREVIEW = (
    "Yuqoridagidek barcha foydalanuvchilarga yuborilsinmi?"
)

ADMIN_BROADCAST_START = (
    "⏳ Reklama xabari barcha foydalanuvchilarga yuborilmoqda, iltimos kuting..."
)

ADMIN_BROADCAST_FINISH = (
    "✅ **{sent_count}** ta foydalanuvchiga yuborildi.\n"
    "⚠️ **{failed_count}** tasida xatolik (bot bloklangan)."
)

ADMIN_BROADCAST_CANCELLED = (
    "❌ Reklama yuborish bekor qilindi."
)

# -------------------------------------------------------------
# BIZ HAQIMIZDA VA YORDAM MATNLARI
# -------------------------------------------------------------
ABOUT_US_TEXT = (
    "🌟 **Biz Haqimizda — IPE School HR Bot**\n\n"
    "🏫 **IPE School** — zamonaviy texnologiyalar, chuqurlashtirilgan bilimlar va xalqaro ta'lim standartlarini o'zida jamlagan nufuzli ta'lim dargohi.\n\n"
    "━━━━━━━━━━━━━━━━━━━━\n"
    "💡 **Bot Yaratuvchilari (Mualliflar):**\n\n"
    "Ushbu avtomatlashtirilgan kadrlar tanlovi (HR) tizimi **IPE School** ning eng iqtidorli, intiluvchan va mehnatsevar yosh dasturchi o'quvchilari jamoasi tomonidan ishlab chiqilgan:\n\n"
    "👨‍💻 **Miraziz**\n"
    "👨‍💻 **Mirziyod**\n"
    "👨‍💻 **Qobiljon**\n"
    "👨‍💻 **Abduqodir**\n"
    "👨‍💻 **Feruzbek**\n"
    "👨‍💻 **Muxriddin**\n"
    "👨‍💻 **Doniyor**\n\n"
    "🔥 **O'quvchilarning Mehnati va Hissasi:**\n"
    "Ushbu iqtidorli yoshlar dasturlash sirlarini puxta egallab, nazariy bilimlarini real amaliyotda namoyon etishdi. Ular murakkab logik arxitektura, ko'p bosqichli vakansiyalar boshqaruvi, xavfsiz ma'lumotlar saqlash va Telegram API imkoniyatlarini birlashtirib, markaz faoliyatini avtomatlashtiruvchi professional HR tizimini yaratishdi.\n\n"
    "Ularning bu yo'ldagi fidokorona mehnati, izlanishi va yangilikka intilishi yuksak e'tirofga loyiq! 🚀\n\n"
    "🌐 **Rasmiy sayt:** [ipeschool.uz](https://ipeschool.uz)\n"
    "📢 **Kanalimiz:** @ipeschool"
)

HELP_TEXT = (
    "❓ **IPE School HR Bot — Foydalanish Bo'yicha Yordam**\n\n"
    "Ushbu bot orqali siz **IPE School** jamoasiga ishga kirish uchun masofadan turib to'liq rezyume topshirishingiz mumkin.\n\n"
    "📌 **Asosiy Buyruqlar:**\n"
    "• /start — Botni ishga tushirish va bosh sahifaga o'tish\n"
    "• /anketa — Vakansiyalar tanlovi va rezyume to'ldirish\n"
    "• /about — IPE School va bot yaratuvchilari haqida ma'lumot\n"
    "• /help — Foydalanish yo'riqnomasi\n"
    "• /cancel — Istalgan vaqt anketa to'ldirishni bekor qilish\n\n"
    "💼 **Mavjud Vakansiyalar:**\n"
    "1. 👨‍🏫 **O'qituvchi (Ustoz)**: IELTS, CEFR, SAT, Prezident maktabiga tayyorlov, Python Backend, Matematika va b.\n"
    "2. 💼 **Administrator**: O'quv markazi boshqaruvi va mijozlar bilan ishlash\n"
    "3. 📈 **Sotuv mutaxassisi (Sotuvchi)**: Kurslar va xizmatlar sotuvi\n\n"
    "Savollar yoki murojaatlar uchun bizning rasmiy kanalimizga murojaat qilishingiz mumkin."
)
