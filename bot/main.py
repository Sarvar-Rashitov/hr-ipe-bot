import sys
import logging
from telegram import BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler
)
from bot import config
from bot.handlers.start import start_handler
from bot.handlers.resume_flow import get_resume_conversation_handler
from bot.handlers.admin import (
    admin_panel,
    admin_stats_callback,
    admin_candidate_preview_callback,
    get_admin_broadcast_conversation_handler
)
from bot.handlers.about import (
    about_handler,
    help_handler,
    back_to_start_callback
)
from bot.handlers.fallback import cancel_command, error_handler

logger = logging.getLogger("ipe_hr_bot")


async def post_init(application) -> None:
    """Telegram 'Menu' tugmasi uchun buyruqlar ro'yxatini sozlash."""
    commands = [
        BotCommand("start", "Bosh sahifa / Botni ishga tushirish"),
        BotCommand("anketa", "Rezyume to'ldirish"),
        BotCommand("about", "Biz haqimizda va bot yaratuvchilari"),
        BotCommand("help", "Foydalanish bo'yicha yordam"),
        BotCommand("cancel", "Jarayonni bekor qilish"),
    ]
    try:
        await application.bot.set_my_commands(commands)
        logger.info("Telegram buyruqlar menyusi (set_my_commands) muvaffaqiyatli sozlandi.")
    except Exception as e:
        logger.warning(f"Buyruqlar menyusini sozlashda ogohlantirish: {e}")


def build_application():
    """Bot dasturini sozlash va barcha handlerlarni ro'yxatdan o'tkazish."""
    if not config.BOT_TOKEN or config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error(
            "DIQQAT: .env faylida BOT_TOKEN ko'rsatilmagan! "
            "Iltimos, .env faylini ochib, @BotFather bergan tokenni kiriting."
        )

    config.validate_config()

    application = (
        ApplicationBuilder()
        .token(config.BOT_TOKEN)
        .post_init(post_init)
        .build()
    )

    # 1. Global /cancel komandasi
    application.add_handler(CommandHandler("cancel", cancel_command), group=0)

    # 2. Admin buyruqlari va paneli
    application.add_handler(CommandHandler("admin", admin_panel), group=1)
    application.add_handler(CallbackQueryHandler(admin_panel, pattern="^admin_refresh$"), group=1)
    application.add_handler(CallbackQueryHandler(admin_stats_callback, pattern="^admin_stats$"), group=1)
    application.add_handler(CallbackQueryHandler(admin_candidate_preview_callback, pattern="^admin_candidate_preview$"), group=1)
    application.add_handler(get_admin_broadcast_conversation_handler(), group=1)

    # 3. Anketa (Resume) oqimi ConversationHandler
    application.add_handler(get_resume_conversation_handler(), group=2)

    # 4. /start, /about, /help va umumiy menyu handlerlari
    application.add_handler(CommandHandler("start", start_handler), group=3)
    application.add_handler(CommandHandler("about", about_handler), group=3)
    application.add_handler(CommandHandler("help", help_handler), group=3)
    application.add_handler(CallbackQueryHandler(about_handler, pattern="^about_us$"), group=3)
    application.add_handler(CallbackQueryHandler(help_handler, pattern="^bot_help$"), group=3)
    application.add_handler(CallbackQueryHandler(back_to_start_callback, pattern="^back_to_start$"), group=3)

    # 5. Global xatoliklarni ushlovchi handler
    application.add_error_handler(error_handler)

    return application


def main():
    """Botni ishga tushirish asosiy nuqtasi."""
    logger.info("IPE School HR Bot ishga tushirilmoqda...")
    
    if not config.BOT_TOKEN or config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("\n" + "=" * 60)
        print("XATOLIK: BOT_TOKEN aniqlanmadi!")
        print("Iltimos, .env faylini oching va haqiqiy BOT_TOKEN ni kiriting.")
        print("=" * 60 + "\n")
        sys.exit(1)

    app = build_application()
    logger.info("Bot muvaffaqiyatli ishga tushdi va xabarlarni kutmoqda...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
