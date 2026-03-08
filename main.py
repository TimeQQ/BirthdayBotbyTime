import logging
from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN
from db import init_db
from handlers import start, help_command, add_friend_handler, list_friends, remove_friend
from scheduler import setup_scheduler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def post_init(app):
    """Вызывается после запуска event loop, но до начала polling."""
    setup_scheduler(app)
    logger.info("Планировщик запущен внутри post_init")

def main():
    init_db()
    logger.info("База данных готова")

    # Правильное создание приложения с post_init
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # Регистрация обработчиков команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("add", add_friend_handler))
    app.add_handler(CommandHandler("list", list_friends))
    app.add_handler(CommandHandler("remove", remove_friend))

    logger.info("Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()