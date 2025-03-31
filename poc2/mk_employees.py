import sqlite3

conn = sqlite3.connect("employees.db")
cur = conn.cursor()

# テーブル作成
cur.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT)")

# データ挿入
cur.executemany(
    "INSERT INTO employees (name, department) VALUES (?, ?)",
    [
        ("Alice", "Engineering"),
        ("Bob", "HR"),
        ("Charlie", "Marketing"),
    ]
)

conn.commit()
conn.close()