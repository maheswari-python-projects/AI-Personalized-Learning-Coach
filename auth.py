
import sqlite3
import hashlib
import os

DB_NAME = "learning_coach.db"


def create_users_table():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def register_user(username, password):
    salt = os.urandom(16).hex()
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    ).hex()

    try:
        conn = sqlite3.connect(DB_NAME)
        conn.execute(
            "INSERT INTO users (username, password, salt) VALUES (?, ?, ?)",
            (username, hashed_password, salt)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False


def login_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    user = conn.execute(
        "SELECT password, salt FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    conn.close()

    if user is None:
        return False

    salt = user[1]
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    ).hex()

    return hashed_password == user[0]
