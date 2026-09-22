from enum import IntEnum, auto


class ResumeState(IntEnum):
    """Anketa (resume) savollarining ketma-ketlik state'lari."""
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
    WORK_TYPE = auto()                 # 28. Ish turi
    EXPECTED_SALARY = auto()           # 29. Kutilayotgan oylik maosh
    PHOTO = auto()                     # 30. Nomzodning rasmi


class AdminState(IntEnum):
    """Admin reklama yuborish (broadcast) jarayoni state'lari."""
    BROADCAST_MESSAGE = auto()  # Reklama xabarini qabul qilish (matn/rasm/video)
    BROADCAST_CONFIRM = auto()  # Tasdiqlashni kutish
