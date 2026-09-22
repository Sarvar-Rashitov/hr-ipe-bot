# IPE School HR / Resume Bot 🤖

**IPE School** ([ipeschool.uz](https://ipeschool.uz)) o'quv markaziga o'qituvchilikka nomzodlardan 30 ta savoldan iborat to'liq anketa (resume) yig'ish, ularni tuzilgan holda yopiq Telegram kanaliga (`CHANNEL_ID`) va HR jamoasi guruhiga (`HR_CHAT_ID`) yuborish hamda adminlarga barcha foydalanuvchilarga reklama xabarlari (broadcast) yuborish imkonini beruvchi Telegram bot.

---

## 🚀 Texnologiyalar va Xususiyatlar

- **Kutubxona:** `python-telegram-bot==21.*` (to'liq async/await)
- **Konfiguratsiya:** `python-dotenv`
- **Ma'lumotlar bazasi:** Talab etilmaydi — barcha javoblar `context.user_data` ichida vaqtincha saqlanadi, yakunida `users.json` faqat reklama tarqatish foydalanuvchilar ro'yxati uchun ishlatiladi.
- **Obuna tekshiruvi:** Nomzod kanalda a'zo bo'lmasdan anketani boshlay olmaydi (`get_chat_member`).
- **Anketa oqimi (ConversationHandler):** 30 ta savoldan iborat to'liq suhbat oqimi, qat'iy ma'lumot validatsiyasi (telefon, yosh, maosh, ko'p tanlovli fanlar).
- **Fanlar bo'yicha #Hashtag generatori:** Tanlangan fanlar avtomatik tarzda Telegram qidiruvi uchun qulay hashtaglar (`#Matematika #Fizika ...`) bilan formatlanadi.
- **Admin Panel (/admin):**
  - Foydalanuvchilar soni statistikasi
  - Reklama yuborish (rasm / video / matn + caption)
  - Yuborishdan oldin admin uchun Preview ko'rish
  - Tasdiqlash va xatoliklarni inobatga oluvchi hisobot

---

## 📁 Loyiha Strukturasi

```
hr-ipe-bot/
├── bot/
│   ├── __init__.py
│   ├── main.py                  # Botni ishga tushirish nuqtasi
│   ├── config.py                # .env sozlamalari va sozlama tekshiruvi
│   ├── states.py                # ConversationHandler statelari (IntEnum)
│   ├── texts.py                 # Barcha statik matnlar va savollar
│   │
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py             # /start, obuna tekshiruvi
│   │   ├── subscription.py      # "Obuna bo'ldim" handleri va tekshiruv
│   │   ├── resume_flow.py       # 30 ta savolli anketa oqimi
│   │   ├── admin.py             # Admin panel va reklama tarqatish
│   │   └── fallback.py          # /cancel va xatoliklarni ushlovchi handler
│   │
│   ├── keyboards/
│   │   ├── __init__.py
│   │   └── inline.py            # Barcha inline va reply klaviaturalar
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py        # Telefon, yosh, maosh kabi validatsiyalar
│       ├── formatter.py         # Resumeni chiroyli kartaga aylantirish
│       ├── hashtags.py          # Fanlar hashtag generatori
│       └── storage.py           # users.json bilan ishlash
│
├── .env                         # Maxfiy token va parametrlar
├── .env.example                 # Namuna sozlamalar
├── requirements.txt             # Kerakli kutubxonalar
├── users.json                   # Reklama uchun foydalanuvchilar ID bazasi
└── README.md                    # Hujjat va yo'riqnoma
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

Loyiha ildizidagi `.env` faylini oching va qiymatlarni to'ldiring:

```env
# Telegram Bot Token (@BotFather dan olinadi)
BOT_TOKEN=1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ

# Resumelar yuboriladigan yopiq kanal ID'si (masalan: -1001234567890)
CHANNEL_ID=-1001234567890

# Obuna tekshirish uchun kanal username (masalan: @ipeschool_jobs) yoki -100... id
CHANNEL_USERNAME=@ipeschool_jobs

# HR jamoasi chati ID'si (masalan: -1009876543210)
HR_CHAT_ID=-1009876543210

# Adminlar Telegram ID ro'yxati (vergul bilan ajratilgan)
ADMIN_IDS=111111111,222222222
```

> **Eslatma:** Bot kanalga va HR guruhiga xabar yuborishi va a'zolikni tekshirishi uchun kanalda va guruhda **Administrator** huquqiga ega bo'lishi shart!

---

## ▶️ Botni Ishga Tushirish

```bash
python -m bot.main
```

---

## 📋 30 ta Anketa Savollari Ro'yxati

1. **Ism, familiya** (matn, kamida 2 ta so'z)
2. **Telefon raqami** (kontakt ulashish yoki `+998XXXXXXXXX` regex tekshiruvi)
3. **Telegram username** (avtomatik taklif yoki qo'lda kiritish)
4. **Yashash hududi** (14 ta viloyat/shahar inline tugmalari)
5. **Yosh** (18–70 oralig'ida butun son)
6. **Tugatgan universitet nomi**
7. **Yo'nalish / Fakultet**
8. **Daraja** (Bakalavr, Magistr, Doktorant, Tugallanmagan)
9. **Ingliz tili darajasi** (IELTS, CEFR yoki sertifikatsiz)
10. **Rus tili darajasi** (Yuqori, O'rta, Boshlang'ich, Bilmayman)
11. **O'qituvchilik tajribasi** (0, 1-2, 3-5, 5+ yil)
12. **Fan(lar)** (ko'p tanlovli checkbox uslubi, «✅ Tayyor» tugmasi bilan)
13. **Eng katta guruh hajmi** (musbat butun son)
14. **Oxirgi ish joyi va ketish sababi**
15. **O'quvchilar natijalari** (misollar)
16. **Eng yaxshi o'quvchi natijasi**
17. **O'rtacha natija** (1–10 shkala)
18. **Retention choralari** (o'quvchilarni saqlab qolish choralari)
19. **Darsga kelmay qo'ygan o'quvchi bilan ishlash qadamlari**
20. **Qiyin o'quvchi bilan ishlash bahosi** (⭐️1–5)
20b. **Qiyin o'quvchi bo'yicha aniq misol**
21. **Odatdagi dars jarayoni tuzilishi**
22. **Qo'llaniladigan metodlar**
23. **Texnologiyadan foydalanish**
24. **Turli darajadagi o'quvchilar bilan ishlash yondashuvi**
25. **Norozi ota-ona bilan muzokara tajribasi**
26. **Nega aynan IPE School**
27. **2 yildan keyingi maqsad**
28. **Ish turi** (Full-time, Part-time, Moslashuvchan grafik)
29. **Kutilayotgan oylik maosh** (so'mda, formatlangan holda)
30. **Nomzodning rasmi** (faqat sifatli rasm qabul qilinadi)

---

## 📢 Admin Funksiyalari

Adminlar ro'yxatida bo'lgan foydalanuvchilar botda `/admin` buyrug'ini yuborishlari mumkin:
1. **Statistika:** Hozirgacha botga kirgan foydalanuvchilar umumiy sonini ko'rish.
2. **Reklama yuborish:**
   - Botga rasm, video (caption bilan) yoki oddiy matn yuboring.
   - Bot sizga xabarning qanday ko'rinishini (Preview) yuboradi va tasdiqlash so'raydi.
   - «✅ Tasdiqlash va yuborish» bosilgach, barcha foydalanuvchilarga xabar tarqatiladi.
   - Yakunida yuborilgan va xatolik bergan xabarlar hisoboti taqdim etiladi.