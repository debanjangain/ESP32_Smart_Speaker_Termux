import sqlite3

DB_PATH = "backend/deb_server/database/memory.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            key TEXT PRIMARY KEY,
            value TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def remember_fact(key, value):
    conn = get_connection()
    c = conn.cursor()
    c.execute("REPLACE INTO memory (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def recall_fact(key):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT value FROM memory WHERE key=?", (key,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def forget_fact(key):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM memory WHERE key=?", (key,))
    conn.commit()
    conn.close()
