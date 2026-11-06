import sqlite3
from datetime import datetime

def connect(db_path):
    con = sqlite3.connect(str(db_path))
    con.row_factory = sqlite3.Row
    return con

def init_db(db_path):
    with connect(db_path) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            result_count INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )""")

def save_search(db_path, query, result_count):
    with connect(db_path) as con:
        con.execute("INSERT INTO searches(query,result_count,created_at) VALUES(?,?,?)",
                    (query, result_count, datetime.now().strftime("%d %b %Y, %I:%M %p")))

def get_history(db_path):
    with connect(db_path) as con:
        return con.execute("SELECT * FROM searches ORDER BY id DESC LIMIT 100").fetchall()

def clear_history(db_path):
    with connect(db_path) as con:
        con.execute("DELETE FROM searches")
