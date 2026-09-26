# IPE School HR / Resume Bot 🤖

**IPE School** ([ipeschool.uz](https://ipeschool.uz)) o'quv markaziga turli mutaxassisliklar (O'qituvchi, Administrator, Sotuvchi) bo'yicha nomzodlardan to'liq anketa (rezyume) yig'ish, ularni maxsus formatda yopiq Telegram kanaliga (`CHANNEL_ID`) va HR jamoasi guruhiga (`HR_CHAT_ID`) yuborish, nomzodlar bilan bot orqali to'g'ridan-to'g'ri muloqot qilish, ularni suhbatga chaqirish hamda adminlarga foydalanuvchilar bazasiga reklama (broadcast) yuborish imkonini beruvchi ko'p funksiyali Telegram bot.

---

## 🚀 Texnologiyalar va Imkoniyatlar

- **Asosiy kutubxona:** `python-telegram-bot==21.*` (to'liq async/await).
- **Xotira va uzluksizlik (Persistence):** `PicklePersistence` orqali bot qayta yuklanganda yoki server vaqtincha to'xtaganda (masalan, Render da spin-down) nomzodning to'xtagan joyi yo'qolmaydi.
- **Zaxira tizimi:** Har bir to'ldirilgan anketa darhol `data/submissions.json` fayliga zaxiralanadi.
- **Rasm va Fayllar:** Nomzod rasmni oddiy Telegram fotosurati yoki siqilmagan fayl (Document: `.jpg`, `.png`, `.webp`, `.heic` va h.k.) sifatida yuborsa ham to'liq qabul qilinadi.
- **Bir nechta majburiy kanallar:** Nomzod belgilangan bir yoki bir nechta Telegram kanallariga (`REQUIRED_CHANNELS`) a'zo bo'lmaguncha anketa to'ldira olmaydi.
- **Instagram va Sayt integratsiyasi:** `/start` menyusida rasmiy Instagram sahifasi (`INSTAGRAM_URL`) va veb-sayt (`WEBSITE_URL`) tugmalari.
- **3 xil mutaxassislik bo'yicha saralangan savollar:**
  1. 👨‍🏫 **O'qituvchi (Teacher):** 30 ta pedagogik, metodik va fan savollari.
  2. 🏢 **Administrator (Admin):** 22 ta tashkiliy, mijozlar bilan ishlash va operatsion savollar.
  3. 💼 **Sotuv mutaxassisi (Sales):** 23 ta sotuv tajribasi, CRM, e'tirozlar bilan ishlash va KPI savollari.
- **HR Jamoasi Boshqaruvi va Muloqot:**
  - Anketa ostida interaktiv tugmalar: **`[📅 Suhbatga chaqirish]`**, **`[✉️ Xabar yuborish]`**, **`[❌ Rad etish]`**.
  - **Suhbatga chaqirish:** 
    - Jonli suhbat (Ofisda) yoki Online suhbat (Google Meet).
    - **Google Maps lokatsiyasi:** Avtomatik ravishda manzil havolasi (`https://maps.app.goo.gl/7g5mPL7AD5kscFqi9`) va xarita tugmasi biriktiriladi.
    - **Suhbat kuni va vaqti:** Tezkor tugmalar (`Ertaga 11:00`, `Ertaga 15:00` va h.k.) yoki erkin matn orqali istalgan sana va soatni belgilash imkoniyati.
  - **Nomzod javobi:** Nomzod botdan HR xabarini olganda `[✍️ HR ga javob yozish]` tugmasi orqali qayta javob yoza oladi. Nomzod javobi to'g'ridan-to'g'ri HR guruhiga boradi.
  - **Telegram Reply integratsiyasi:** HR guruhida turib rezyumega oddiy Telegram "Reply" (Javob) qilinsa ham, bot xabarni avtomatik o'sha nomzodga yetkazadi.
  - **Ko'p HR qo'llab-quvvatlash:** Bir nechta HR menejerlar ID lari va Admin paneldan HR larni qo'shish/o'chirish imkoniyati.
- **Admin Panel (`/admin`):**
  - Foydalanuvchilar soni statistikasi.
  - HR menejerlar ro'yxatini ko'rish, yangi HR ID qo'shish yoki o'chirish.
  - Reklama tarqatish (matn, rasm, video + preview ko'rish va hisobot).

---

## 📁 Loyiha Strukturasi

```
hr-ipe-bot-live/
├── bot/
│   ├── __init__.py
│   ├── main.py                  # Botni ishga tushirish (PicklePersistence bilan)
│   ├── config.py                # .env parametrlari va ko'p kanalli parser
│   ├── states.py                # ConversationHandler statelari
│   ├── texts.py                 # Matnlar, savollar va HR taklifnoma shablonlari
│   │
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py             # /start, Instagram va sayt havolalari
│   │   ├── subscription.py      # Bir nechta kanallarga a'zolikni tekshirish
│   │   ├── resume_flow.py       # Rolga mos anketa to'ldirish (Teacher/Admin/Sales)
│   │   ├── hr_actions.py        # Suhbatga chaqirish, manzil, kun/vaqt, HR javoblari
│   │   ├── admin.py             # Admin panel, reklama va HR boshqaruvi
│   │   └── fallback.py          # /cancel va xatoliklar handleri
│   │
│   ├── keyboards/
│   │   ├── __init__.py
│   │   └── inline.py            # Barcha inline menyular va tugmalar
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py        # Telefon, yosh, maosh, ism validatsiyalari
│       ├── formatter.py         # Anketani chiroyli Markdown formatiga aylantirish
│       ├── hashtags.py          # Fanlar va lavozimlar bo'yicha #hashtaglar
│       ├── storage.py           # users.json bilan ishlash
│       └── hr_storage.py        # Dinamik HR ID lar va zaxira arizalar fayli
│
├── data/                        # Runtime ma'lumotlar papkasi (Gitga kiritilmaydi)
│   ├── .gitkeep
│   ├── bot_persistence.pickle   # Conversation state saqlash fayli
│   ├── hr_managers.json         # Qo'shimcha HR menejerlar ID lari
│   └── submissions.json         # Barcha arizalar zaxirasi
│
├── tests/
│   └── test_bot.py              # 23 ta avtomatlashtirilgan unit testlar
├── .env.example                 # Sozlamalar namunasi
├── requirements.txt             # Kerakli Python kutubxonalari
├── users.json                   # Reklama uchun foydalanuvchilar ID bazasi
└── README.md                    # Loyiha hujjati
```

---

## ⚙️ O'rnatish va Sozlash

### 1. Loyihani yuklab olish va virtual muhit yaratish

```bash
# Virtual muhit yaratish
python -m venv venv

# Virtual muhitni faollashtirish:
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# Linux / macOS:
source venv/bin/activate
```

### 2. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 3. `.env` faylini sozlash

Loyiha ildizidagi `.env` faylini quyidagi parametrlar bilan to'ldiring:

```env
# Telegram Bot Token (@BotFather dan olinadi)
BOT_TOKEN=1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ

# Resumelar yuboriladigan yopiq kanal ID'si (masalan: -1001234567890)
CHANNEL_ID=-1001234567890

# Bir nechta majburiy obuna kanallari (vergul bilan ajratilgan)
REQUIRED_CHANNELS=@ipeschool_jobs, @ipeschool
CHANNEL_USERNAME=@ipeschool_jobs

# HR jamoasi chati ID'si (masalan: -1009876543210)
HR_CHAT_ID=-1009876543210

# Adminlar Telegram ID ro'yxati (vergul bilan ajratilgan)
ADMIN_IDS=111111111,222222222

# HR menejerlar Telegram ID ro'yxati (vergul bilan ajratilgan)
HR_MANAGER_IDS=333333333,444444444

# Rasmiy Instagram sahifasi
INSTAGRAM_URL=https://www.instagram.com/ipe_school

# Rasmiy sayt
WEBSITE_URL=https://ipeschool.uz

# Suhbat manzili havolasi (Google Maps)
OFFICE_LOCATION_URL=https://maps.app.goo.gl/7g5mPL7AD5kscFqi9
```

> **Muhim:** Bot kanalga va HR guruhiga xabar yuborishi, shuningdek a'zolikni tekshirishi uchun barcha kanallarda va guruhlarda **Administrator** huquqiga ega bo'lishi shart!

---

## ▶️ Botni Ishga Tushirish va Testlash

### Botni ishga tushirish:
```bash
python -m bot.main
```

### Unit testlarni tekshirish:
```bash
python -m unittest discover tests
```

---

## 📋 Mutaxassisliklar bo'yicha Savollar

### 1. 👨‍🏫 O'qituvchi (30 ta savol):
1. Ism, familiya
2. Telefon raqami
3. Telegram username
4. Yashash hududi
5. Yosh (18–70 oralig'ida)
6. Universitet
7. Fakultet / Yo'nalish
8. Ilmiy daraja (Bakalavr, Magistr...)
9. Ingliz tili darajasi
10. Rus tili darajasi
11. O'qituvchilik tajribasi
12. Dars beradigan fan(lar) (Ko'p tanlovli)
13. Eng katta guruh hajmi
14. Oxirgi ish joyi va ketish sababi
15. O'quvchilar erishgan natijalar
16. Eng yaxshi o'quvchi natijasi
17. O'quvchilarning umumiy o'rtacha natijasi (1–10)
18. Kursda saqlab qolish (retention) choralari
19. Kelmay qo'ygan o'quvchi bilan ishlash qadamlari
20. Qiyin o'quvchi bilan ishlash bahosi (⭐️1–5)
20b. Qiyin vaziyat bo'yicha aniq misol
21. Odatdagi dars jarayoni tuzilishi
22. Darsda zamonaviy pedagogik metodlar
23. Darsda zamonaviy texnologiyalardan foydalanish
24. Har xil darajadagi o'quvchilar bilan ishlash yondashuvi
25. Norozi ota-ona bilan muzokara tajribasi
26. Nega aynan IPE School?
27. 2 yildan keyingi kasbiy maqsad
28. Ish tartibi (Full-time / Part-time)
29. Kutilayotgan oylik maosh
30. 3x4 rasm (Fotosurat yoki sifatli fayl)

### 2. 🏢 Administrator (22 ta savol):
1–10: Umumiy ma'lumotlar (Ism, telefon, yosh, ta'lim, tillar)  
11: Umumiy ish tajribasi  
12: Administratorlik tajribasi  
13: Kompyuter va dasturlar bilimi (Word, Excel, CRM...)  
14: Mijozlar bilan ishlash tajribasi  
15: Stressli/ziddiyatli vaziyatlarda qanday yo'l tutasiz?  
16: Qiyin mijoz bilan amaliy misol  
17: Kunlik vazifalarni rejalashtirish (Time-management)  
18: Nega aynan IPE School?  
19: 2 yildan keyingi maqsad  
20: Ish tartibi (Full-time / Part-time)  
21: Kutilayotgan oylik maosh  
22: 3x4 rasm (Fotosurat yoki sifatli fayl)

### 3. 💼 Sotuv mutaxassisi / Sales (23 ta savol):
1–10: Umumiy ma'lumotlar (Ism, telefon, yosh, ta'lim, tillar)  
11: Umumiy ish tajribasi  
12: Sotuv sohasidagi tajriba (issiq/sovuq qo'ng'iroqlar, lidlar)  
13: Ishlatgan CRM va telefoniya vositalari  
14: Eng yuqori sotuv rekordi  
15: Mijoz e'tirozlari ("Qimmat", "O'ylab ko'raman") bilan ishlash  
16: Murakkab mijozga sotuv qilish bo'yicha aniq misol  
17: KPI va sotuv rejalarini bajarish mahorati (⭐️1–5)  
18: Oxirgi ish joyi va ketish sababi  
19: Nega aynan IPE School?  
20: 2 yildan keyingi maqsad  
21: Ish tartibi (Full-time / Part-time)  
22: Kutilayotgan oylik maosh  
23: 3x4 rasm (Fotosurat yoki sifatli fayl)

---

## 👥 HR Boshqaruvi va Aloqa Funksiyalari

1. **HR Xabarlari va Suhbatga Chaqirish:**
   - Har bir kelgan anketa ostida tezkor amallar mavjud.
   - Suhbat kuni va soatini belgilashda HR tezkor tugmalardan foydalanishi yoki chatga erkin sana/soat yozishi mumkin.
   - Nomzodga borgan taklifnomada **Google Maps lokatsiyasi** va **`[✍️ HR ga javob yozish]`** tugmasi taqdim etiladi.
2. **Telegram Reply orqali avtomatik javob berish:**
   - HR menejerlari guruhda anketa xabariga oddiy Telegram "Reply" qilishsa, bot xabarni darhol nomzodga yetkazadi.
3. **Ko'p HR qo'llab-quvvatlash:**
   - Adminlar `/admin` buyrug'i orqali **`[👥 HR Menejerlar]`** bo'limiga kirib yangi HR ID qo'shishi yoki o'chirishi mumkin.