
import sqlite3
from datetime import datetime

DB_NAME = "learning_coach.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL DEFAULT '',
            subject TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            percentage REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)

    columns = conn.execute(
        "PRAGMA table_info(quiz_results)"
    ).fetchall()

    column_names = [column[1] for column in columns]

    if "username" not in column_names:
        conn.execute("""
            ALTER TABLE quiz_results
            ADD COLUMN username TEXT NOT NULL DEFAULT ''
        """)

    conn.commit()
    conn.close()


def save_quiz_result(username, subject, score, total_questions):
    percentage = (score / total_questions) * 100
    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT INTO quiz_results
        (username, subject, score, total_questions, percentage, date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (username, subject, score, total_questions, percentage, date))

    conn.commit()
    conn.close()


def get_quiz_results(username):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT subject, score, total_questions, percentage, date
        FROM quiz_results
        WHERE username = ?
        ORDER BY id DESC
    """, (username,)).fetchall()

    results = [dict(row) for row in rows]
    conn.close()

    return results

