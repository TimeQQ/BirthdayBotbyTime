import sqlite3

DB_NAME = "birthdays.db"

def init_db():
    """Создаёт таблицу friends, если её нет"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS friends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                birth_date TEXT NOT NULL
            )
        """)
        conn.commit()

def add_friend(user_id, name, birth_date):
    """Добавляет запись о друге"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO friends (user_id, name, birth_date) VALUES (?, ?, ?)",
            (user_id, name, birth_date)
        )
        conn.commit()
        return cursor.lastrowid

def get_friends(user_id):
    """Возвращает список друзей пользователя (id, name, birth_date)"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, birth_date FROM friends WHERE user_id = ? ORDER BY name",
            (user_id,)
        )
        return cursor.fetchall()

def delete_friend(record_id, user_id):
    """Удаляет запись, если она принадлежит пользователю"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM friends WHERE id = ? AND user_id = ?",
            (record_id, user_id)
        )
        conn.commit()
        return cursor.rowcount > 0

def get_all_friends():
    """Возвращает ВСЕ записи из БД (используется планировщиком)"""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, name, birth_date FROM friends")
        return cursor.fetchall()