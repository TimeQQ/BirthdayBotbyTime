from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from db import get_all_friends
from utils import today_day_month

async def check_birthdays(app):
    """
    Функция, которая запускается каждый день в 9:00.
    Проверяет, у кого сегодня день рождения, и отправляет уведомления.
    """
    day, month = today_day_month()
    birthdays_today = {}

    for user_id, name, birth_date_str in get_all_friends():
        bd = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        if bd.day == day and bd.month == month:
            birthdays_today.setdefault(user_id, []).append(name)

    for uid, names in birthdays_today.items():
        text = "🎉 Сегодня день рождения празднует:\n" + "\n".join(f"• {n}" for n in names)
        try:
            await app.bot.send_message(chat_id=uid, text=text)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {uid}: {e}")

def setup_scheduler(app):
    """Настраивает и запускает планировщик"""
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        check_birthdays,
        trigger=CronTrigger(hour=9, minute=0),
        args=[app],
        id="birthday_check"
    )
    scheduler.start()
    print("Планировщик запущен. Проверка каждый день в 9:00.")
    return scheduler