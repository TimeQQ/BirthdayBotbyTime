from telegram import Update
from telegram.ext import ContextTypes
from db import add_friend, get_friends, delete_friend
from utils import parse_date, format_date

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я помогу не забыть дни рождения друзей.\n\n"
        "Команды:\n"
        "/add <имя> <ДД.ММ.ГГГГ> — добавить друга\n"
        "/list — список друзей\n"
        "/remove <id> — удалить запись\n"
        "/help — подсказка"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 Справка:\n"
        "/add Василий 12.04.1985 — добавить друга\n"
        "/list — показать список\n"
        "/remove 3 — удалить запись с номером 3\n\n"
        "Дата всегда в формате ДД.ММ.ГГГГ"
    )

async def add_friend_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❌ Используйте: /add <имя> <ДД.ММ.ГГГГ>")
        return

    *name_parts, date_str = args
    name = " ".join(name_parts)
    date_obj = parse_date(date_str)
    if not date_obj:
        await update.message.reply_text("❌ Неверный формат даты. Нужно: ДД.ММ.ГГГГ")
        return

    add_friend(update.effective_user.id, name, date_obj.isoformat())
    await update.message.reply_text(f"✅ Запись добавлена: {name} ({format_date(date_obj)})")

async def list_friends(update: Update, context: ContextTypes.DEFAULT_TYPE):
    friends = get_friends(update.effective_user.id)
    if not friends:
        await update.message.reply_text("📭 У вас пока нет сохранённых друзей.")
        return

    lines = []
    for fid, name, bd_str in friends:
        lines.append(f"{fid}. {name} — {format_date(bd_str)}")
    await update.message.reply_text("📋 Ваши друзья:\n" + "\n".join(lines))

async def remove_friend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args or not args[0].isdigit():
        await update.message.reply_text("❌ Укажите ID записи для удаления: /remove <id>")
        return

    record_id = int(args[0])
    success = delete_friend(record_id, update.effective_user.id)
    if success:
        await update.message.reply_text("✅ Запись удалена.")
    else:
        await update.message.reply_text("❌ Запись не найдена или не принадлежит вам.")