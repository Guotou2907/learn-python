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
def get_movies(min_rating: float = 0.0, db: Session = Depends(get_db)):
    # 完全不用写 SQL！直接按面向对象查表
    movies = db.query(models.MovieDB).filter(models.MovieDB.rating >= min_rating).all()
    
    movies_list = [{"id": m.id, "name": m.name, "rating": m.rating, "link": m.link} for m in movies]
    return {"count": len(movies_list), "movies": movies_list}

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
