import sqlite3
conn = sqlite3.connect("test.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS student(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER
)
""")

cursor.execute("INSERT INTO student (name, age) VALUES (?, ?)", ("小明", 20))
cursor.execute("INSERT INTO student (name, age) VALUES (?, ?)", ("小红", 22))

cursor.execute("SELECT name, age FROM student")
results = cursor.fetchall()
for row in results:
    print(f"姓名：{row[0]}，年龄：{row[1]}")

conn.close()
