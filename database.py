import sqlite3
from datetime import datetime, timedelta

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

# ===== USERS =====
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    last_post TEXT
)
""")

# ===== CHANNELS =====
cursor.execute("""
CREATE TABLE IF NOT EXISTS channels (
    channel_id INTEGER PRIMARY KEY,
    title TEXT,
    username TEXT
)
""")

conn.commit()

# ===== CHANNELS LOGIC =====
def add_channel(channel_id, title, username):
    cursor.execute(
        "INSERT OR REPLACE INTO channels (channel_id, title, username) VALUES (?, ?, ?)",
        (channel_id, title, username)
    )
    conn.commit()

def get_channels():
    cursor.execute("SELECT channel_id, title, username FROM channels")
    return cursor.fetchall()

def get_channel(channel_id):
    cursor.execute(
        "SELECT channel_id, title, username FROM channels WHERE channel_id=?",
        (channel_id,)
    )
    return cursor.fetchone()

# ===== POSTS LIMIT =====
def can_post(user_id):
    cursor.execute("SELECT last_post FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    if not row:
        return True
    return datetime.now() - datetime.fromisoformat(row[0]) >= timedelta(days=1)

def update_post_time(user_id):
    cursor.execute(
        "INSERT OR REPLACE INTO users (user_id, last_post) VALUES (?, ?)",
        (user_id, datetime.now().isoformat())
    )
    conn.commit()
