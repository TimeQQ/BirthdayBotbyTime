from datetime import datetime

def parse_date(date_str):
    """
    Парсит дату из строки формата ДД.ММ.ГГГГ.
    Возвращает объект date или None при ошибке.
    """
    try:
        return datetime.strptime(date_str, "%d.%m.%Y").date()
    except ValueError:
        return None

def format_date(date_obj_or_str):
    """Принимает строку ISO (YYYY-MM-DD) или объект date, возвращает ДД.ММ.ГГГГ"""
    if isinstance(date_obj_or_str, str):
        date_obj = datetime.strptime(date_obj_or_str, "%Y-%m-%d").date()
    else:
        date_obj = date_obj_or_str
    return date_obj.strftime("%d.%m.%Y")

def today_day_month():
    """Возвращает кортеж (сегодняшний_день, сегодняшний_месяц)"""
    today = datetime.now().date()
    return today.day, today.month