from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import database, models
from fastapi.middleware.cors import CORSMiddleware

# 创建所有表（如果表不存在）
models.Base.metadata.create_all(bind=database.engine)

class UTF8JSONResponse(JSONResponse):
    media_type = "application/json;charset=utf-8"

app = FastAPI(default_response_class=UTF8JSONResponse)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 允许任何网页来调（开发阶段用，上线要收紧）
    allow_methods=["*"],
    allow_headers=["*"],
)

# 依赖注入：每次请求来，自动开一个 session，请求结束自动关闭
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MovieCreate(BaseModel):
    name: str = Field(min_length=1)
    rating: float = Field(ge=0, le=10)
    link: str = ""

@app.get("/movies")
def get_movies(
    min_rating: float = 0.0,
    keyword: str = "",        # 新增：搜索关键字
    limit: int = 10,          # 新增：每页条数
    offset: int = 0,          # 新增：起始位置
    db: Session = Depends(get_db)
):
    # 1. 先建一个基础查询（不执行）
    query = db.query(models.MovieDB)

    # 2. 如果传了评分条件，加上过滤
    if min_rating > 0:
        query = query.filter(models.MovieDB.rating >= min_rating)

    # 3. 如果传了搜索关键字，加上模糊匹配
    # SQLAlchemy 的 contains 相当于 SQL 里的 LIKE '%keyword%'
    if keyword:
        query = query.filter(models.MovieDB.name.contains(keyword))

    # 4. 先算总数（注意：算总数必须要在分页之前）
    total = query.count()

    # 5. 再执行分页查询
    movies = query.offset(offset).limit(limit).all()

    # 6. 转换为字典列表返回
    movies_list = [{"id": m.id, "name": m.name, "rating": m.rating, "link": m.link} for m in movies]

    return {
        "total": total,        # 重要！前端靠这个算总页数
        "count": len(movies_list), 
        "movies": movies_list
    }

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.MovieDB).filter(models.MovieDB.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="查无此片")
    return {"movie": {"id": movie.id, "name": movie.name, "rating": movie.rating, "link": movie.link}}

@app.post("/movies", status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    # 创建一个新的数据库对象
    new_movie = models.MovieDB(name=movie.name, rating=movie.rating, link=movie.link)
    db.add(new_movie)      # 加入会话
    db.commit()            # 提交
    db.refresh(new_movie)  # 刷新，拿到自增 ID
    
    return {"message": "添加成功", "movie": {"id": new_movie.id, "name": new_movie.name, "rating": new_movie.rating, "link": new_movie.link}}
