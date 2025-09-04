# database.py
import sqlite3
from pathlib import Path

DB_PATH = Path("data.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    # Tabel link
    c.execute("""
    CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        creator_id INTEGER,
        title TEXT,
        content TEXT,
        price INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    # Tabel orders
    c.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        link_id INTEGER,
        buyer_id INTEGER,
        amount INTEGER,
        status TEXT DEFAULT 'pending', -- pending / paid
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        paid_at TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()