import sqlite3
import json

# 1. 读取 JSON
with open("douban_top250_oop.json", "r", encoding="utf-8") as f:
    movies = json.load(f)

# 2. 连接数据库
conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

# 3. 建表
cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rating REAL,
    link TEXT
)
""")

# 4. 插入数据
for movie in movies:
    # 在这里写 INSERT 语句
    cursor.execute("INSERT INTO movies (name, rating, link) VALUES (?, ?, ?)",(movie["name"],movie["rating"],movie["link"]))

# 5. 提交
conn.commit()

# 6. 查询：找出评分大于 9.0 的电影，按评分降序，取前 5 部
# 在这里写 SELECT 语句
cursor.execute("SELECT name,rating FROM movies WHERE rating > 9.0 ORDER BY rating DESC LIMIT 5")
results = cursor.fetchall()
print(f"找到了{len(results)}部电影")
for row in results:
    print(f"电影名字：{row[0]},电影评分：{row[1]}")
# 提示：cursor.execute(...) 然后 cursor.fetchall()

# 7. 关闭
conn.close()
