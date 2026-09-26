import os
import sys
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from telegram import BotCommand
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    PicklePersistence,
    filters
)
from bot import config
from bot.handlers.start import start_handler
from bot.handlers.resume_flow import get_resume_conversation_handler
from bot.handlers.admin import (
    admin_panel,
    admin_stats_callback,
    admin_candidate_preview_callback,
    admin_hr_manage_callback,
    admin_hr_delete_callback,
    get_admin_hr_conversation_handler,
    get_admin_broadcast_conversation_handler
)
from bot.handlers.hr_actions import (
    get_hr_message_conversation_handler,
    get_candidate_reply_conversation_handler,
    hr_group_reply_handler
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

    # Persistence sozlash (Render qayta yuklanganda holat va anketalar yo'qolmasligi uchun)
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    persistence = PicklePersistence(filepath=str(config.PERSISTENCE_FILE))

    application = (
        ApplicationBuilder()
        .token(config.BOT_TOKEN)
        .persistence(persistence)
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
    application.add_handler(CallbackQueryHandler(admin_hr_manage_callback, pattern="^admin_hr_manage$"), group=1)
    application.add_handler(CallbackQueryHandler(admin_hr_delete_callback, pattern=r"^hr_del:"), group=1)
    application.add_handler(get_admin_hr_conversation_handler(), group=1)
    application.add_handler(get_admin_broadcast_conversation_handler(), group=1)
    application.add_handler(get_hr_message_conversation_handler(), group=1)

    # 3. Anketa (Resume) oqimi ConversationHandler va Nomzod javobi
    application.add_handler(get_resume_conversation_handler(), group=2)
    application.add_handler(get_candidate_reply_conversation_handler(), group=2)

    # 4. /start, /about, /help va umumiy menyu handlerlari
    application.add_handler(CommandHandler("start", start_handler), group=3)
    application.add_handler(CommandHandler("about", about_handler), group=3)
    application.add_handler(CommandHandler("help", help_handler), group=3)
    application.add_handler(CallbackQueryHandler(about_handler, pattern="^about_us$"), group=3)
    application.add_handler(CallbackQueryHandler(help_handler, pattern="^bot_help$"), group=3)
    application.add_handler(CallbackQueryHandler(back_to_start_callback, pattern="^back_to_start$"), group=3)

    # 5. HR guruhi Telegram Reply orqali nomzodga xabar yuborish
    application.add_handler(MessageHandler(filters.REPLY & filters.TEXT & ~filters.COMMAND, hr_group_reply_handler), group=4)

    # 6. Global xatoliklarni ushlovchi handler
    application.add_error_handler(error_handler)


    return application


# Global telegram application instansiyasi (lifespan uchun)
telegram_app = None


@asynccontextmanager
async def lifespan(web_app: FastAPI):
    """Render Web Service va FastAPI uchun lifespan: botni ishga tushirish va to'xtatish."""
    global telegram_app
    logger.info("Render Web Service ishga tushmoqda...")

    if not config.BOT_TOKEN or config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.warning(
            "DIQQAT: BOT_TOKEN aniqlanmadi! "
            "Render Dashboard -> Environment Variables bo'limida BOT_TOKEN ni kiriting."
        )
    else:
        try:
            telegram_app = build_application()
            await telegram_app.initialize()
            await telegram_app.start()
            await telegram_app.updater.start_polling(drop_pending_updates=True)
            logger.info("Telegram bot muvaffaqiyatli ishga tushdi va polling boshlandi.")
        except Exception as e:
            logger.error(f"Telegram botni ishga tushirishda xatolik yuz berdi: {e}")

    yield

    if telegram_app:
        logger.info("Telegram bot to'xtatilmoqda...")
        try:
            if telegram_app.updater and telegram_app.updater.running:
                await telegram_app.updater.stop()
            if telegram_app.running:
                await telegram_app.stop()
            await telegram_app.shutdown()
            logger.info("Telegram bot to'xtatildi.")
        except Exception as e:
            logger.error(f"Telegram botni to'xtatishda xatolik yuz berdi: {e}")


# Render Web Service uchun FastAPI ilovasi
app = FastAPI(
    title="IPE School HR Bot",
    description="Render Web Service hosting va Telegram Bot health check API",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Render port tekshiruvi va xizmat holati."""
    bot_running = telegram_app is not None and telegram_app.running
    return {
        "status": "online",
        "service": "IPE School HR Bot",
        "bot_running": bot_running,
        "message": "Bot Render serverida muvaffaqiyatli ishlamoqda."
    }


@app.get("/health")
async def health():
    """Uptime monitoring (UptimeRobot, cron-job) uchun health check endpoint."""
    return {"status": "healthy"}


def main():
    """Botni ishga tushirish asosiy nuqtasi."""
    port_str = os.getenv("PORT")
    
    # Agar Render yoki boshqa bulutli hosting muhitida PORT o'zgaruvchisi berilgan bo'lsa:
    if port_str:
        import uvicorn
        port = int(port_str)
        logger.info(f"Render hosting muhiti aniqlandi (PORT={port}). Uvicorn serveri ishga tushmoqda...")
        uvicorn.run("bot.main:app", host="0.0.0.0", port=port, log_level="info")
        return

    # Mahalliy (lokal) ishlab chiqish rejimida to'g'ridan-to'g'ri polling:
    logger.info("IPE School HR Bot lokal rejimda ishga tushirilmoqda...")
    if not config.BOT_TOKEN or config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("\n" + "=" * 60)
        print("XATOLIK: BOT_TOKEN aniqlanmadi!")
        print("Iltimos, .env faylini oching va haqiqiy BOT_TOKEN ni kiriting.")
        print("=" * 60 + "\n")
        sys.exit(1)

    bot_app = build_application()
    logger.info("Bot muvaffaqiyatli ishga tushdi va xabarlarni kutmoqda...")
    bot_app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()

