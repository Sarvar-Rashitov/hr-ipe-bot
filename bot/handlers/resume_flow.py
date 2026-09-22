import logging
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from bot import config, texts
from bot.states import ResumeState
from bot.keyboards.inline import (
    get_vacancies_keyboard,
    get_phone_request_keyboard,
    get_username_keyboard,
    get_regions_keyboard,
    get_degree_keyboard,
    get_russian_level_keyboard,
    get_experience_keyboard,
    get_subjects_keyboard,
    get_average_result_keyboard,
    get_rating_5_keyboard,
    get_work_type_keyboard,
    get_subscription_keyboard,
    AVAILABLE_SUBJECTS
)
from bot.utils.validators import (
    validate_full_name,
    validate_phone,
    validate_age,
    validate_positive_int,
    validate_salary
)
from bot.utils.formatter import format_resume
from bot.handlers.subscription import check_user_subscription
from bot.handlers.fallback import cancel_command

logger = logging.getLogger(__name__)


# -------------------------------------------------------------
# ENTRY POINTS & VACANCY SELECTION
# -------------------------------------------------------------
async def start_resume_flow(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Anketa oqimini boshlash: Obunani tekshirish va vakansiya tanlashni ko'rsatish."""
    user = update.effective_user
    if not user:
        return ConversationHandler.END

    # Obunani tekshirish
    is_sub = await check_user_subscription(context.bot, user.id)
    if not is_sub:
        channel_url = config.get_channel_link()
        if update.callback_query:
            await update.callback_query.answer(
                "❌ Siz hali kanalga obuna bo'lmadingiz! Iltimos, avval kanalimizga a'zo bo'ling.",
                show_alert=True
            )
            await update.callback_query.message.reply_text(
                texts.SUBSCRIPTION_NOT_FOUND,
                reply_markup=get_subscription_keyboard(channel_url),
                parse_mode="Markdown"
            )
        elif update.effective_message:
            await update.effective_message.reply_text(
                texts.SUBSCRIPTION_NOT_FOUND,
                reply_markup=get_subscription_keyboard(channel_url),
                parse_mode="Markdown"
            )
        return ConversationHandler.END

    context.user_data.clear()
    context.user_data["subjects"] = []

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(
            texts.CHOOSE_VACANCY,
            reply_markup=get_vacancies_keyboard(),
            parse_mode="Markdown"
        )
    elif update.message:
        await update.message.reply_text(
            texts.CHOOSE_VACANCY,
            reply_markup=get_vacancies_keyboard(),
            parse_mode="Markdown"
        )

    return ResumeState.VACANCY_SELECT


async def check_sub_and_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """'Obuna bo'ldim' tugmasi bosilganda obunani tekshirib, vakansiya tanlashga o'tish."""
    query = update.callback_query
    user = update.effective_user
    if not query or not user:
        return ConversationHandler.END

    is_sub = await check_user_subscription(context.bot, user.id)
    if not is_sub:
        await query.answer("❌ Siz hali kanalga obuna bo'lmadingiz!", show_alert=True)
        channel_url = config.get_channel_link()
        try:
            await query.edit_message_text(
                texts.SUBSCRIPTION_NOT_FOUND,
                reply_markup=get_subscription_keyboard(channel_url),
                parse_mode="Markdown"
            )
        except Exception:
            pass
        return ConversationHandler.END

    await query.answer("✅ Obuna tasdiqlandi!")
    context.user_data.clear()
    context.user_data["subjects"] = []

    try:
        await query.edit_message_text(
            texts.SUBSCRIPTION_SUCCESS,
            parse_mode="Markdown"
        )
    except Exception:
        pass

    await query.message.reply_text(
        texts.CHOOSE_VACANCY,
        reply_markup=get_vacancies_keyboard(),
        parse_mode="Markdown"
    )
    return ResumeState.VACANCY_SELECT


async def step_vacancy_selected(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Nomzod qaysi vakansiyaga topshirishni tanlaganda."""
    query = update.callback_query
    if not query:
        return ResumeState.VACANCY_SELECT
    await query.answer()

    role = query.data.split(":", 1)[1]  # "teacher", "admin", "sales"
    context.user_data["role"] = role

    role_names = {
        "teacher": "👨‍🏫 O'qituvchi (Ustoz)",
        "admin": "💼 Administrator",
        "sales": "📈 Sotuv mutaxassisi (Sotuvchi)"
    }
    selected_name = role_names.get(role, "O'qituvchi")

    try:
        await query.edit_message_text(
            f"✅ **Tanlangan yo'nalish:** {selected_name}\n\n"
            f"Keling, anketani to'ldirishni boshlaymiz!",
            parse_mode="Markdown"
        )
    except Exception:
        pass

    await query.message.reply_text(
        texts.Q_FULL_NAME,
        parse_mode="Markdown"
    )
    return ResumeState.FULL_NAME


async def step_vacancy_invalid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Tugma o'rniga matn yozilganda ogohlantirish."""
    await update.message.reply_text(
        "Iltimos, yuqoridagi tugmalardan birini tanlang:",
        reply_markup=get_vacancies_keyboard()
    )
    return ResumeState.VACANCY_SELECT


# -------------------------------------------------------------
# STEP 1: FULL NAME
# -------------------------------------------------------------
async def step_full_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    is_valid, name = validate_full_name(text)
    if not is_valid:
        await update.message.reply_text(texts.ERR_INVALID_FULL_NAME, parse_mode="Markdown")
        return ResumeState.FULL_NAME

    context.user_data["full_name"] = name
    await update.message.reply_text(
        texts.Q_PHONE,
        reply_markup=get_phone_request_keyboard(),
        parse_mode="Markdown"
    )
    return ResumeState.PHONE


# -------------------------------------------------------------
# STEP 2: PHONE
# -------------------------------------------------------------
async def step_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    phone_text = ""
    if update.message.contact:
        phone_text = update.message.contact.phone_number
    elif update.message.text:
        phone_text = update.message.text

    is_valid, phone = validate_phone(phone_text)
    if not is_valid:
        await update.message.reply_text(
            texts.ERR_INVALID_PHONE,
            reply_markup=get_phone_request_keyboard(),
            parse_mode="Markdown"
        )
        return ResumeState.PHONE

    context.user_data["phone"] = phone
    user_username = update.effective_user.username if update.effective_user else None

    # Reply keyboardni olib tashlab, keyingi savolni yuboramiz
    await update.message.reply_text(
        "✅ Telefon raqam qabul qilindi.",
        reply_markup=ReplyKeyboardRemove()
    )
    await update.message.reply_text(
        texts.Q_USERNAME,
        reply_markup=get_username_keyboard(user_username),
        parse_mode="Markdown"
    )
    return ResumeState.USERNAME


# -------------------------------------------------------------
# STEP 3: USERNAME
# -------------------------------------------------------------
async def step_username_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("username_auto:"):
        clean_user = data.split(":", 1)[1]
        context.user_data["username"] = f"@{clean_user}"
    elif data == "username_none":
        context.user_data["username"] = "Username yo'q"

    await query.message.reply_text(
        texts.Q_REGION,
        reply_markup=get_regions_keyboard(),
        parse_mode="Markdown"
    )
    return ResumeState.REGION


async def step_username_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    if text.startswith("@"):
        context.user_data["username"] = text
    else:
        context.user_data["username"] = f"@{text}" if text.lower() != "yo'q" else "Username yo'q"

    await update.message.reply_text(
        texts.Q_REGION,
        reply_markup=get_regions_keyboard(),
        parse_mode="Markdown"
    )
    return ResumeState.REGION


# -------------------------------------------------------------
# STEP 4: REGION
# -------------------------------------------------------------
async def step_region_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    region = query.data.split(":", 1)[1]
    context.user_data["region"] = region

    await query.message.reply_text(texts.Q_AGE, parse_mode="Markdown")
    return ResumeState.AGE


async def step_region_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["region"] = text
    await update.message.reply_text(texts.Q_AGE, parse_mode="Markdown")
    return ResumeState.AGE


# -------------------------------------------------------------
# STEP 5: AGE
# -------------------------------------------------------------
async def step_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    is_valid, age = validate_age(text)
    if not is_valid:
        await update.message.reply_text(texts.ERR_INVALID_AGE, parse_mode="Markdown")
        return ResumeState.AGE

    context.user_data["age"] = age
    await update.message.reply_text(texts.Q_UNIVERSITY, parse_mode="Markdown")
    return ResumeState.UNIVERSITY


# -------------------------------------------------------------
# STEP 6: UNIVERSITY
# -------------------------------------------------------------
async def step_university(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    if len(text) < 2:
        await update.message.reply_text("⚠️ Iltimos, universitet nomini to'liq kiriting:")
        return ResumeState.UNIVERSITY

    context.user_data["university"] = text
    await update.message.reply_text(texts.Q_FACULTY, parse_mode="Markdown")
    return ResumeState.FACULTY


# -------------------------------------------------------------
# STEP 7: FACULTY
# -------------------------------------------------------------
async def step_faculty(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    if len(text) < 2:
        await update.message.reply_text("⚠️ Iltimos, yo'nalish yoki fakultet nomini kiriting:")
        return ResumeState.FACULTY

    context.user_data["faculty"] = text
    await update.message.reply_text(
        texts.Q_DEGREE,
        reply_markup=get_degree_keyboard(),
        parse_mode="Markdown"
    )
    return ResumeState.DEGREE


# -------------------------------------------------------------
# STEP 8: DEGREE
# -------------------------------------------------------------
async def step_degree_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    degree = query.data.split(":", 1)[1]
    context.user_data["degree"] = degree

    await query.message.reply_text(texts.Q_ENGLISH_LEVEL, parse_mode="Markdown")
    return ResumeState.ENGLISH_LEVEL


async def step_degree_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["degree"] = text
    await update.message.reply_text(texts.Q_ENGLISH_LEVEL, parse_mode="Markdown")
    return ResumeState.ENGLISH_LEVEL


# -------------------------------------------------------------
# STEP 9: ENGLISH LEVEL
# -------------------------------------------------------------
async def step_english_level(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["english_level"] = text
    await update.message.reply_text(
        texts.Q_RUSSIAN_LEVEL,
        reply_markup=get_russian_level_keyboard(),
        parse_mode="Markdown"
    )
    return ResumeState.RUSSIAN_LEVEL


# -------------------------------------------------------------
# STEP 10: RUSSIAN LEVEL
# -------------------------------------------------------------
async def step_russian_level_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    level = query.data.split(":", 1)[1]
    context.user_data["russian_level"] = level

    await query.message.reply_text(
        texts.Q_EXPERIENCE_YEARS,
        reply_markup=get_experience_keyboard(),
        parse_mode="Markdown"
    )
    return ResumeState.EXPERIENCE_YEARS


async def step_russian_level_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["russian_level"] = text
    await update.message.reply_text(
        texts.Q_EXPERIENCE_YEARS,
        reply_markup=get_experience_keyboard(),
        parse_mode="Markdown"
    )
    return ResumeState.EXPERIENCE_YEARS


# -------------------------------------------------------------
# STEP 11: EXPERIENCE YEARS
# -------------------------------------------------------------
async def step_experience_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    exp = query.data.split(":", 1)[1]
    context.user_data["experience_years"] = exp

    role = context.user_data.get("role", "teacher")
    if role == "admin":
        await query.message.reply_text(
            texts.Q_ADMIN_OFFICE_SOFTWARE,
            parse_mode="Markdown"
        )
        return ResumeState.ADMIN_OFFICE_SOFTWARE
    elif role == "sales":
        await query.message.reply_text(
            texts.Q_SALES_EXPERIENCE,
            parse_mode="Markdown"
        )
        return ResumeState.SALES_EXPERIENCE
    else:
        selected = context.user_data.setdefault("subjects", [])
        await query.message.reply_text(
            texts.Q_SUBJECTS,
            reply_markup=get_subjects_keyboard(selected),
            parse_mode="Markdown"
        )
        return ResumeState.SUBJECTS


async def step_experience_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["experience_years"] = text

    role = context.user_data.get("role", "teacher")
    if role == "admin":
        await update.message.reply_text(
            texts.Q_ADMIN_OFFICE_SOFTWARE,
            parse_mode="Markdown"
        )
        return ResumeState.ADMIN_OFFICE_SOFTWARE
    elif role == "sales":
        await update.message.reply_text(
            texts.Q_SALES_EXPERIENCE,
            parse_mode="Markdown"
        )
        return ResumeState.SALES_EXPERIENCE
    else:
        selected = context.user_data.setdefault("subjects", [])
        await update.message.reply_text(
            texts.Q_SUBJECTS,
            reply_markup=get_subjects_keyboard(selected),
            parse_mode="Markdown"
        )
        return ResumeState.SUBJECTS


# -------------------------------------------------------------
# STEP 12: SUBJECTS (Multi-Select Checkbox)
# -------------------------------------------------------------
async def step_subjects_toggle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    idx = int(query.data.split(":", 1)[1])
    subject_name = AVAILABLE_SUBJECTS[idx]

    selected: list = context.user_data.setdefault("subjects", [])
    if subject_name in selected:
        selected.remove(subject_name)
    else:
        selected.append(subject_name)

    await query.answer()
    try:
        await query.edit_message_reply_markup(
            reply_markup=get_subjects_keyboard(selected)
        )
    except Exception:
        pass

    return ResumeState.SUBJECTS


async def step_subjects_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    selected: list = context.user_data.get("subjects", [])
    if not selected:
        await query.answer(texts.ERR_NO_SUBJECT_SELECTED, show_alert=True)
        return ResumeState.SUBJECTS

    await query.answer("✅ Fanlar saqlandi!")
    await query.message.reply_text(texts.Q_MAX_GROUP_SIZE, parse_mode="Markdown")
    return ResumeState.MAX_GROUP_SIZE


# -------------------------------------------------------------
# STEP 13: MAX GROUP SIZE
# -------------------------------------------------------------
async def step_max_group_size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    is_valid, size = validate_positive_int(text, min_val=1, max_val=1000)
    if not is_valid:
        await update.message.reply_text(texts.ERR_INVALID_NUMBER, parse_mode="Markdown")
        return ResumeState.MAX_GROUP_SIZE

    context.user_data["max_group_size"] = size
    await update.message.reply_text(texts.Q_LAST_JOB, parse_mode="Markdown")
    return ResumeState.LAST_JOB


# -------------------------------------------------------------
# STEP 14: LAST JOB
# -------------------------------------------------------------
async def step_last_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["last_job"] = text
    await update.message.reply_text(texts.Q_STUDENT_RESULTS, parse_mode="Markdown")
    return ResumeState.STUDENT_RESULTS


# -------------------------------------------------------------
# STEP 15: STUDENT RESULTS
# -------------------------------------------------------------
async def step_student_results(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["student_results"] = text
    await update.message.reply_text(texts.Q_BEST_STUDENT_RESULT, parse_mode="Markdown")
    return ResumeState.BEST_STUDENT_RESULT


# -------------------------------------------------------------
# STEP 16: BEST STUDENT RESULT
# -------------------------------------------------------------
async def step_best_student_result(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["best_student_result"] = text
    await update.message.reply_text(
        texts.Q_AVERAGE_RESULT,
        reply_markup=get_average_result_keyboard(),
        parse_mode="Markdown"
    )
    return ResumeState.AVERAGE_RESULT


# -------------------------------------------------------------
# STEP 17: AVERAGE RESULT (1-10)
# -------------------------------------------------------------
async def step_average_result_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    score = query.data.split(":", 1)[1]
    context.user_data["average_result"] = score

    await query.message.reply_text(texts.Q_RETENTION_METHODS, parse_mode="Markdown")
    return ResumeState.RETENTION_METHODS


async def step_average_result_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["average_result"] = text
    await update.message.reply_text(texts.Q_RETENTION_METHODS, parse_mode="Markdown")
    return ResumeState.RETENTION_METHODS


# -------------------------------------------------------------
# STEP 18: RETENTION METHODS
# -------------------------------------------------------------
async def step_retention_methods(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["retention_methods"] = text
    await update.message.reply_text(texts.Q_DROPOUT_STEPS, parse_mode="Markdown")
    return ResumeState.DROPOUT_STEPS


# -------------------------------------------------------------
# STEP 19: DROPOUT STEPS
# -------------------------------------------------------------
async def step_dropout_steps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["dropout_steps"] = text
    await update.message.reply_text(
        texts.Q_DIFFICULT_STUDENT_RATING,
        reply_markup=get_rating_5_keyboard(),
        parse_mode="Markdown"
    )
    return ResumeState.DIFFICULT_STUDENT_RATING


# -------------------------------------------------------------
# STEP 20: DIFFICULT STUDENT RATING (1-5)
# -------------------------------------------------------------
async def step_difficult_student_rating_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    rating = query.data.split(":", 1)[1]
    context.user_data["difficult_student_rating"] = rating

    await query.message.reply_text(texts.Q_DIFFICULT_STUDENT_EXAMPLE, parse_mode="Markdown")
    return ResumeState.DIFFICULT_STUDENT_EXAMPLE


async def step_difficult_student_rating_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["difficult_student_rating"] = text
    await update.message.reply_text(texts.Q_DIFFICULT_STUDENT_EXAMPLE, parse_mode="Markdown")
    return ResumeState.DIFFICULT_STUDENT_EXAMPLE


# -------------------------------------------------------------
# STEP 20b: DIFFICULT STUDENT EXAMPLE
# -------------------------------------------------------------
async def step_difficult_student_example(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["difficult_student_example"] = text
    await update.message.reply_text(texts.Q_LESSON_STRUCTURE, parse_mode="Markdown")
    return ResumeState.LESSON_STRUCTURE


# -------------------------------------------------------------
# STEP 21: LESSON STRUCTURE
# -------------------------------------------------------------
async def step_lesson_structure(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["lesson_structure"] = text
    await update.message.reply_text(texts.Q_METHODS, parse_mode="Markdown")
    return ResumeState.METHODS


# -------------------------------------------------------------
# STEP 22: METHODS
# -------------------------------------------------------------
async def step_methods(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["methods"] = text
    await update.message.reply_text(texts.Q_TECHNOLOGY_USAGE, parse_mode="Markdown")
    return ResumeState.TECHNOLOGY_USAGE


# -------------------------------------------------------------
# STEP 23: TECHNOLOGY USAGE
# -------------------------------------------------------------
async def step_technology_usage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["technology_usage"] = text
    await update.message.reply_text(texts.Q_MIXED_LEVEL_APPROACH, parse_mode="Markdown")
    return ResumeState.MIXED_LEVEL_APPROACH


# -------------------------------------------------------------
# STEP 24: MIXED LEVEL APPROACH
# -------------------------------------------------------------
async def step_mixed_level_approach(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["mixed_level_approach"] = text
    await update.message.reply_text(texts.Q_PARENT_NEGOTIATION, parse_mode="Markdown")
    return ResumeState.PARENT_NEGOTIATION


# -------------------------------------------------------------
# STEP 25: PARENT NEGOTIATION
# -------------------------------------------------------------
async def step_parent_negotiation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["parent_negotiation"] = text
    await update.message.reply_text(texts.Q_WHY_IPE, parse_mode="Markdown")
    return ResumeState.WHY_IPE


# -------------------------------------------------------------
# STEP 26: WHY IPE
# -------------------------------------------------------------
async def step_why_ipe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["why_ipe"] = text
    await update.message.reply_text(texts.Q_GOALS_2Y, parse_mode="Markdown")
    return ResumeState.GOALS_2Y


# -------------------------------------------------------------
# STEP 27: GOALS 2 YEARS
# -------------------------------------------------------------
async def step_goals_2y(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["goals_2y"] = text
    await update.message.reply_text(
        texts.Q_WORK_TYPE,
        reply_markup=get_work_type_keyboard(),
        parse_mode="Markdown"
    )
    return ResumeState.WORK_TYPE


# -------------------------------------------------------------
# ADMINISTRATOR HANDLERS
# -------------------------------------------------------------
async def step_admin_office_software(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["admin_office_software"] = update.message.text.strip()
    await update.message.reply_text(texts.Q_ADMIN_MULTITASKING, parse_mode="Markdown")
    return ResumeState.ADMIN_MULTITASKING


async def step_admin_multitasking(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["admin_multitasking"] = update.message.text.strip()
    await update.message.reply_text(texts.Q_ADMIN_GUEST_RECEPTION, parse_mode="Markdown")
    return ResumeState.ADMIN_GUEST_RECEPTION


async def step_admin_guest_reception(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["admin_guest_reception"] = update.message.text.strip()
    await update.message.reply_text(texts.Q_ADMIN_CONFLICT_RESOLUTION, parse_mode="Markdown")
    return ResumeState.ADMIN_CONFLICT_RESOLUTION


async def step_admin_conflict_resolution(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["admin_conflict_resolution"] = update.message.text.strip()
    await update.message.reply_text(texts.Q_ADMIN_ATTENDANCE_PAYMENTS, parse_mode="Markdown")
    return ResumeState.ADMIN_ATTENDANCE_PAYMENTS


async def step_admin_attendance_payments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["admin_attendance_payments"] = update.message.text.strip()
    await update.message.reply_text(texts.Q_ADMIN_LAST_JOB, parse_mode="Markdown")
    return ResumeState.ADMIN_LAST_JOB


async def step_admin_last_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["admin_last_job"] = update.message.text.strip()
    await update.message.reply_text(texts.Q_ADMIN_WHY_IPE, parse_mode="Markdown")
    return ResumeState.ADMIN_WHY_IPE


async def step_admin_why_ipe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["admin_why_ipe"] = update.message.text.strip()
    await update.message.reply_text(texts.Q_ADMIN_GOALS_2Y, parse_mode="Markdown")
    return ResumeState.ADMIN_GOALS_2Y


async def step_admin_goals_2y(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["admin_goals_2y"] = update.message.text.strip()
    await update.message.reply_text(
        texts.Q_WORK_TYPE,
        reply_markup=get_work_type_keyboard(),
        parse_mode="Markdown"
    )
    return ResumeState.WORK_TYPE


# -------------------------------------------------------------
# SOTUV MUTAXASSISI HANDLERS
# -------------------------------------------------------------
async def step_sales_experience(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["sales_experience"] = update.message.text.strip()
    await update.message.reply_text(texts.Q_SALES_CRM_TOOLS, parse_mode="Markdown")
    return ResumeState.SALES_CRM_TOOLS


async def step_sales_crm_tools(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["sales_crm_tools"] = update.message.text.strip()
    await update.message.reply_text(texts.Q_SALES_RECORD, parse_mode="Markdown")
    return ResumeState.SALES_RECORD


async def step_sales_record(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["sales_record"] = update.message.text.strip()
    await update.message.reply_text(texts.Q_SALES_OBJECTIONS, parse_mode="Markdown")
    return ResumeState.SALES_OBJECTIONS


async def step_sales_objections(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["sales_objections"] = update.message.text.strip()
    await update.message.reply_text(texts.Q_SALES_DIFFICULT_CLIENT, parse_mode="Markdown")
    return ResumeState.SALES_DIFFICULT_CLIENT


async def step_sales_difficult_client(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["sales_difficult_client"] = update.message.text.strip()
    await update.message.reply_text(texts.Q_SALES_KPI_RATING, parse_mode="Markdown")
    return ResumeState.SALES_KPI_RATING


async def step_sales_kpi_rating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["sales_kpi_rating"] = update.message.text.strip()
    await update.message.reply_text(texts.Q_SALES_LAST_JOB, parse_mode="Markdown")
    return ResumeState.SALES_LAST_JOB


async def step_sales_last_job(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["sales_last_job"] = update.message.text.strip()
    await update.message.reply_text(texts.Q_SALES_WHY_IPE, parse_mode="Markdown")
    return ResumeState.SALES_WHY_IPE


async def step_sales_why_ipe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["sales_why_ipe"] = update.message.text.strip()
    await update.message.reply_text(texts.Q_SALES_GOALS_2Y, parse_mode="Markdown")
    return ResumeState.SALES_GOALS_2Y


async def step_sales_goals_2y(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["sales_goals_2y"] = update.message.text.strip()
    await update.message.reply_text(
        texts.Q_WORK_TYPE,
        reply_markup=get_work_type_keyboard(),
        parse_mode="Markdown"
    )
    return ResumeState.WORK_TYPE


# -------------------------------------------------------------
# STEP 28: WORK TYPE
# -------------------------------------------------------------
async def step_work_type_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    work_type = query.data.split(":", 1)[1]
    context.user_data["work_type"] = work_type

    await query.message.reply_text(texts.Q_EXPECTED_SALARY, parse_mode="Markdown")
    return ResumeState.EXPECTED_SALARY


async def step_work_type_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    context.user_data["work_type"] = text
    await update.message.reply_text(texts.Q_EXPECTED_SALARY, parse_mode="Markdown")
    return ResumeState.EXPECTED_SALARY


# -------------------------------------------------------------
# STEP 29: EXPECTED SALARY
# -------------------------------------------------------------
async def step_expected_salary(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    is_valid, _, formatted_salary = validate_salary(text)
    if not is_valid:
        await update.message.reply_text(texts.ERR_INVALID_SALARY, parse_mode="Markdown")
        return ResumeState.EXPECTED_SALARY

    context.user_data["expected_salary"] = formatted_salary
    await update.message.reply_text(texts.Q_PHOTO, parse_mode="Markdown")
    return ResumeState.PHOTO


# -------------------------------------------------------------
# STEP 30: PHOTO & FINAL SUBMISSION
# -------------------------------------------------------------
async def step_photo_invalid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Foydalanuvchi rasm o'rniga fayl yoki matn yuborganda."""
    await update.message.reply_text(texts.ERR_PHOTO_REQUIRED, parse_mode="Markdown")
    return ResumeState.PHOTO


async def step_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Nomzod rasmini qabul qilish va anketani yuborish."""
    photo = update.message.photo[-1]
    context.user_data["photo_file_id"] = photo.file_id

    # Formatlash
    caption, full_text = format_resume(context.user_data)

    # 1. CHANNEL_ID ga yuborish
    if config.CHANNEL_ID:
        try:
            await context.bot.send_photo(
                chat_id=config.CHANNEL_ID,
                photo=photo.file_id,
                caption=caption,
                parse_mode="Markdown"
            )
            if full_text:
                await context.bot.send_message(
                    chat_id=config.CHANNEL_ID,
                    text=full_text,
                    parse_mode="Markdown"
                )
        except Exception as e:
            logger.error(f"CHANNEL_ID ga yuborishda xatolik: {e}")

    # 2. HR_CHAT_ID ga yuborish
    if config.HR_CHAT_ID:
        try:
            await context.bot.send_photo(
                chat_id=config.HR_CHAT_ID,
                photo=photo.file_id,
                caption=caption,
                parse_mode="Markdown"
            )
            if full_text:
                await context.bot.send_message(
                    chat_id=config.HR_CHAT_ID,
                    text=full_text,
                    parse_mode="Markdown"
                )
        except Exception as e:
            logger.error(f"HR_CHAT_ID ga yuborishda xatolik: {e}")

    # Foydalanuvchiga muvaffaqiyat xabari
    await update.message.reply_text(
        texts.SUBMISSION_SUCCESS,
        parse_mode="Markdown"
    )

    # Sessiyani tozalash (DB yo'q)
    context.user_data.clear()
    return ConversationHandler.END


# -------------------------------------------------------------
# CONVERSATION HANDLER FABRIKASI
# -------------------------------------------------------------
def get_resume_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            CommandHandler("anketa", start_resume_flow),
            CallbackQueryHandler(start_resume_flow, pattern="^start_resume$"),
            CallbackQueryHandler(check_sub_and_start, pattern="^check_subscription$"),
        ],
        states={
            ResumeState.VACANCY_SELECT: [
                CallbackQueryHandler(step_vacancy_selected, pattern="^vacancy:"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_vacancy_invalid),
            ],
            ResumeState.FULL_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_full_name),
            ],
            ResumeState.PHONE: [
                MessageHandler(filters.CONTACT | (filters.TEXT & ~filters.COMMAND), step_phone),
            ],
            ResumeState.USERNAME: [
                CallbackQueryHandler(step_username_callback, pattern="^username_"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_username_text),
            ],
            ResumeState.REGION: [
                CallbackQueryHandler(step_region_callback, pattern="^region:"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_region_text),
            ],
            ResumeState.AGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_age),
            ],
            ResumeState.UNIVERSITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_university),
            ],
            ResumeState.FACULTY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_faculty),
            ],
            ResumeState.DEGREE: [
                CallbackQueryHandler(step_degree_callback, pattern="^degree:"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_degree_text),
            ],
            ResumeState.ENGLISH_LEVEL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_english_level),
            ],
            ResumeState.RUSSIAN_LEVEL: [
                CallbackQueryHandler(step_russian_level_callback, pattern="^ru_level:"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_russian_level_text),
            ],
            ResumeState.EXPERIENCE_YEARS: [
                CallbackQueryHandler(step_experience_callback, pattern="^exp:"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_experience_text),
            ],
            # O'qituvchi bosqichlari
            ResumeState.SUBJECTS: [
                CallbackQueryHandler(step_subjects_toggle, pattern="^subj_toggle:"),
                CallbackQueryHandler(step_subjects_done, pattern="^subj_done$"),
            ],
            ResumeState.MAX_GROUP_SIZE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_max_group_size),
            ],
            ResumeState.LAST_JOB: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_last_job),
            ],
            ResumeState.STUDENT_RESULTS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_student_results),
            ],
            ResumeState.BEST_STUDENT_RESULT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_best_student_result),
            ],
            ResumeState.AVERAGE_RESULT: [
                CallbackQueryHandler(step_average_result_callback, pattern="^avg_res:"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_average_result_text),
            ],
            ResumeState.RETENTION_METHODS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_retention_methods),
            ],
            ResumeState.DROPOUT_STEPS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_dropout_steps),
            ],
            ResumeState.DIFFICULT_STUDENT_RATING: [
                CallbackQueryHandler(step_difficult_student_rating_callback, pattern="^diff_rate:"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_difficult_student_rating_text),
            ],
            ResumeState.DIFFICULT_STUDENT_EXAMPLE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_difficult_student_example),
            ],
            ResumeState.LESSON_STRUCTURE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_lesson_structure),
            ],
            ResumeState.METHODS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_methods),
            ],
            ResumeState.TECHNOLOGY_USAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_technology_usage),
            ],
            ResumeState.MIXED_LEVEL_APPROACH: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_mixed_level_approach),
            ],
            ResumeState.PARENT_NEGOTIATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_parent_negotiation),
            ],
            ResumeState.WHY_IPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_why_ipe),
            ],
            ResumeState.GOALS_2Y: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_goals_2y),
            ],

            # Administrator bosqichlari
            ResumeState.ADMIN_OFFICE_SOFTWARE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_admin_office_software),
            ],
            ResumeState.ADMIN_MULTITASKING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_admin_multitasking),
            ],
            ResumeState.ADMIN_GUEST_RECEPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_admin_guest_reception),
            ],
            ResumeState.ADMIN_CONFLICT_RESOLUTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_admin_conflict_resolution),
            ],
            ResumeState.ADMIN_ATTENDANCE_PAYMENTS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_admin_attendance_payments),
            ],
            ResumeState.ADMIN_LAST_JOB: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_admin_last_job),
            ],
            ResumeState.ADMIN_WHY_IPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_admin_why_ipe),
            ],
            ResumeState.ADMIN_GOALS_2Y: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_admin_goals_2y),
            ],

            # Sotuv mutaxassisi bosqichlari
            ResumeState.SALES_EXPERIENCE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_sales_experience),
            ],
            ResumeState.SALES_CRM_TOOLS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_sales_crm_tools),
            ],
            ResumeState.SALES_RECORD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_sales_record),
            ],
            ResumeState.SALES_OBJECTIONS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_sales_objections),
            ],
            ResumeState.SALES_DIFFICULT_CLIENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_sales_difficult_client),
            ],
            ResumeState.SALES_KPI_RATING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_sales_kpi_rating),
            ],
            ResumeState.SALES_LAST_JOB: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_sales_last_job),
            ],
            ResumeState.SALES_WHY_IPE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_sales_why_ipe),
            ],
            ResumeState.SALES_GOALS_2Y: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_sales_goals_2y),
            ],

            # Yakuniy umumiy bosqichlar
            ResumeState.WORK_TYPE: [
                CallbackQueryHandler(step_work_type_callback, pattern="^work:"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_work_type_text),
            ],
            ResumeState.EXPECTED_SALARY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, step_expected_salary),
            ],
            ResumeState.PHOTO: [
                MessageHandler(filters.PHOTO, step_photo),
                MessageHandler(~filters.PHOTO & ~filters.COMMAND, step_photo_invalid),
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel_command),
        ],
        allow_reentry=True,
        per_message=False
    )
