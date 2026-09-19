import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent / "memory.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():

    with get_connection() as conn:

        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                key TEXT PRIMARY KEY,
                value TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()


def remember_fact(key, value):

    with get_connection() as conn:

        c = conn.cursor()

        c.execute(
            "REPLACE INTO memory (key, value) VALUES (?, ?)",
            (key, value)
        )

        conn.commit()


def recall_fact(key):

    with get_connection() as conn:

        c = conn.cursor()

        c.execute(
            "SELECT value FROM memory WHERE key=?",
            (key,)
        )

        row = c.fetchone()

        return row[0] if row else None


def forget_fact(key):

    with get_connection() as conn:

        c = conn.cursor()

        c.execute(
            "DELETE FROM memory WHERE key=?",
            (key,)
        )

        conn.commit()
        
