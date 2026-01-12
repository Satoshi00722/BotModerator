import sqlite3
from datetime import datetime, timedelta

# ================== DB CONNECT ==================
conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

# ================== USERS ==================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    day TEXT,
    posts_count INTEGER
)
""")

# ================== CHANNELS ==================
cursor.execute("""
CREATE TABLE IF NOT EXISTS channels (
    channel_id INTEGER PRIMARY KEY,
    title TEXT,
    username TEXT
)
""")

conn.commit()

# ================== CHANNELS LOGIC ==================
def add_channel(channel_id: int, title: str, username: str):
    cursor.execute(
        "INSERT OR REPLACE INTO channels (channel_id, title, username) VALUES (?, ?, ?)",
        (channel_id, title, username)
    )
    conn.commit()


def get_channels():
    cursor.execute("SELECT channel_id, title, username FROM channels")
    return cursor.fetchall()


def get_channel(channel_id: int):
    cursor.execute(
        "SELECT channel_id, title, username FROM channels WHERE channel_id = ?",
        (channel_id,)
    )
    return cursor.fetchone()


def delete_channel(channel_id: int):
    cursor.execute(
        "DELETE FROM channels WHERE channel_id = ?",
        (channel_id,)
    )
    conn.commit()

# ================== POSTS LIMIT (3 / DAY) ==================
def can_post(user_id: int) -> bool:
    today = datetime.now().date().isoformat()

    cursor.execute(
        "SELECT day, posts_count FROM users WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()

    # если юзера нет — можно постить
    if not row:
        return True

    day, count = row

    # если новый день — сбрасываем лимит
    if day != today:
        return True

    # лимит 3 поста
    return count < 3


def update_post_time(user_id: int):
    today = datetime.now().date().isoformat()

    cursor.execute(
        "SELECT day, posts_count FROM users WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()

    if not row:
        cursor.execute(
            "INSERT INTO users (user_id, day, posts_count) VALUES (?, ?, ?)",
            (user_id, today, 1)
        )
    else:
        day, count = row

        if day != today:
            cursor.execute(
                "UPDATE users SET day = ?, posts_count = ? WHERE user_id = ?",
                (today, 1, user_id)
            )
        else:
            cursor.execute(
                "UPDATE users SET posts_count = posts_count + 1 WHERE user_id = ?",
                (user_id,)
            )

    conn.commit()
