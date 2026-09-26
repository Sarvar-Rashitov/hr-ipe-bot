from enum import IntEnum, auto


class ResumeState(IntEnum):
    """Anketa (resume) savollarining ketma-ketlik state'lari."""
    # 0. Vakansiya tanlash
    VACANCY_SELECT = auto()            # Vakansiyani tanlash (Ustoz, Admin, Sotuvchi)

    # Umumiy savollar (1 - 11)
    FULL_NAME = auto()                 # 1. Ism, familiya
    PHONE = auto()                     # 2. Telefon raqami
    USERNAME = auto()                  # 3. Telegram username
    REGION = auto()                    # 4. Yashash hududi
    AGE = auto()                       # 5. Yosh
    UNIVERSITY = auto()                # 6. Universitet
    FACULTY = auto()                   # 7. Yo'nalish/Fakultet
    DEGREE = auto()                    # 8. Daraja
    ENGLISH_LEVEL = auto()             # 9. Ingliz tili darajasi
    RUSSIAN_LEVEL = auto()             # 10. Rus tili darajasi
    EXPERIENCE_YEARS = auto()          # 11. Tajriba (yil)

    # O'qituvchi maxsus savollari
    SUBJECTS = auto()                  # 12. Fan(lar) (ko'p tanlovli)
    MAX_GROUP_SIZE = auto()            # 13. Eng katta guruh hajmi
    LAST_JOB = auto()                  # 14. Oxirgi ish joyi va ketish sababi
    STUDENT_RESULTS = auto()           # 15. O'quvchilar natijalari
    BEST_STUDENT_RESULT = auto()       # 16. Eng yaxshi o'quvchi natijasi
    AVERAGE_RESULT = auto()            # 17. O'rtacha natija (1-10)
    RETENTION_METHODS = auto()         # 18. Retention choralari
    DROPOUT_STEPS = auto()             # 19. Darsga kelmay qo'ygan o'quvchi bilan ishlash
    DIFFICULT_STUDENT_RATING = auto()  # 20. Qiyin o'quvchi bilan ishlash bahosi (1-5)
    DIFFICULT_STUDENT_EXAMPLE = auto() # 20b. Qiyin o'quvchi bo'yicha aniq misol
    LESSON_STRUCTURE = auto()          # 21. Odatdagi dars jarayoni
    METHODS = auto()                   # 22. Qo'llaniladigan metodlar
    TECHNOLOGY_USAGE = auto()          # 23. Texnologiyadan foydalanish
    MIXED_LEVEL_APPROACH = auto()      # 24. Turli darajadagi o'quvchilar bilan ishlash
    PARENT_NEGOTIATION = auto()        # 25. Norozi ota-ona bilan muzokara
    WHY_IPE = auto()                   # 26. Nega aynan IPE School
    GOALS_2Y = auto()                  # 27. 2 yildan keyingi maqsad

    # Administrator maxsus savollari
    ADMIN_OFFICE_SOFTWARE = auto()     # Kompyuter dasturlari va CRM/Excel
    ADMIN_MULTITASKING = auto()        # Multitasking va stress bahosi (1-5)
    ADMIN_GUEST_RECEPTION = auto()     # Mehmon/ota-onani kutib olish va muloqot
    ADMIN_CONFLICT_RESOLUTION = auto() # Nizolarni hal qilish amaliy misoli
    ADMIN_ATTENDANCE_PAYMENTS = auto() # Davomat va to'lov nazorati
    ADMIN_LAST_JOB = auto()            # Oxirgi ish joyi va ketish sababi
    ADMIN_WHY_IPE = auto()             # Nega aynan IPE School'da administratorlik
    ADMIN_GOALS_2Y = auto()            # 2 yildan keyingi kasbiy maqsad

    # Sotuv mutaxassisi maxsus savollari
    SALES_EXPERIENCE = auto()          # Sotuv tajribasi (qo'ng'iroqlar, lidlar)
    SALES_CRM_TOOLS = auto()           # CRM tizimlari va telefoniya (AmoCRM, Bitrix24)
    SALES_RECORD = auto()              # Bir oylik eng yuqori sotuv rekordi
    SALES_OBJECTIONS = auto()          # E'tirozlar bilan ishlash ("qimmat", "o'ylab ko'ramiz")
    SALES_DIFFICULT_CLIENT = auto()    # Qiyin mijoz bilan ishlash amaliy misoli
    SALES_KPI_RATING = auto()          # Oylik reja (KPI) va stress bahosi (1-5)
    SALES_LAST_JOB = auto()            # Oxirgi ish joyi va ketish sababi
    SALES_WHY_IPE = auto()             # Nega aynan IPE School'da sotuv mutaxassisi
    SALES_GOALS_2Y = auto()            # 2 yildan keyingi moliyaviy va kasbiy maqsad

    # Yakuniy umumiy savollar
    WORK_TYPE = auto()                 # 28. Ish turi
    EXPECTED_SALARY = auto()           # 29. Kutilayotgan oylik maosh
    PHOTO = auto()                     # 30. Nomzodning rasmi


class AdminState(IntEnum):
    """Admin reklama yuborish (broadcast) jarayoni state'lari."""
    BROADCAST_MESSAGE = auto()  # Reklama xabarini qabul qilish (matn/rasm/video)
    BROADCAST_CONFIRM = auto()  # Tasdiqlashni kutish


class HRActionState(IntEnum):
    """HR menejer nomzodga xabar yoki suhbat taklifnomasi yozish state'lari."""
    ENTER_MESSAGE = auto()     # Erkin xabar matnini qabul qilish
    ENTER_INTERVIEW = auto()   # Suhbat taklifnomasi matnini qabul qilish


class CandidateReplyState(IntEnum):
    """Nomzod HR xabariga javob yozish state'i."""
    ENTER_REPLY = auto()       # Nomzodning HR ga javob matni


class AdminHRState(IntEnum):
    """Admin yangi HR qo'shish state'i."""
    ENTER_HR_ID = auto()       # Yangi HR ID raqamini kiritish

