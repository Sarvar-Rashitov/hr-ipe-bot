import sys
import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler
)
from bot import config
from bot.handlers.start import start_handler
from bot.handlers.resume_flow import get_resume_conversation_handler
from bot.handlers.admin import admin_panel, get_admin_broadcast_conversation_handler
from bot.handlers.fallback import cancel_command, error_handler

logger = logging.getLogger("ipe_hr_bot")


def build_application():
    """Bot dasturini sozlash va barcha handlerlarni ro'yxatdan o'tkazish."""
    if not config.BOT_TOKEN or config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error(
            "DIQQAT: .env faylida BOT_TOKEN ko'rsatilmagan! "
            "Iltimos, .env faylini ochib, @BotFather bergan tokenni kiriting."
        )

    config.validate_config()

    application = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # 1. Global /cancel komandasi
    application.add_handler(CommandHandler("cancel", cancel_command), group=0)

    # 2. Admin buyruqlari va paneli
    application.add_handler(CommandHandler("admin", admin_panel), group=1)
    application.add_handler(CallbackQueryHandler(admin_panel, pattern="^admin_refresh$"), group=1)
    application.add_handler(get_admin_broadcast_conversation_handler(), group=1)

    # 3. Anketa (Resume) oqimi ConversationHandler
    application.add_handler(get_resume_conversation_handler(), group=2)

    # 4. /start handleri
    application.add_handler(CommandHandler("start", start_handler), group=3)

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
