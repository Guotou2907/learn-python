import json
from database import SessionLocal, engine, Base
import models

# 创建所有表
Base.metadata.create_all(bind=engine)

# 读取 JSON
with open("douban_top250_oop.json", "r", encoding="utf-8") as f:
    movies = json.load(f)

# 创建 session
db = SessionLocal()

# 循环插入
for m in movies:
    new_movie = models.MovieDB(
        name=m["name"],
        rating=float(m["rating"]),  # 注意 rating 要转成浮点数
        link=m["link"]
    )
    db.add(new_movie)

db.commit()
db.close()
print(f"导入成功，共 {len(movies)} 部电影！")
