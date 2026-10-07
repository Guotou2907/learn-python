from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import HTTPException
import sqlite3

class UTF8JSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"

app = FastAPI(default_response_class=UTF8JSONResponse)

class MovieCreate(BaseModel):
    name:str
    rating:float
    link:str = ""

@app.post("/movies")
def create_movies(movie:MovieCreate):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    # 插入数据
    cursor.execute(
        "INSERT INTO movies (name, rating, link) VALUES (?, ?, ?)",
        (movie.name, movie.rating, movie.link)
    )
    conn.commit()
    
    # 获取刚才插入的这一行的自增 id
    new_id = cursor.lastrowid
    
    conn.close()
    
    return {
        "message": "添加成功",
        "movie": {
            "id": new_id,
            "name": movie.name,
            "rating": movie.rating,
            "link": movie.link
        }
    }



@app.get("/")
def read_root():
    return {"message":"hello this is movie API"}

@app.get("/movies")
def get_movies(min_rating: float = 0.0):

    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id,name,rating,link FROM movies WHERE rating >= ?",(min_rating,))
    rows = cursor.fetchall()
    
    conn.close()

    movies_list = []
    for row in rows:
        movies_list.append({
            "id":row[0],
            "name":row[1],
            "rating":row[2],
            "link":row[3]
        })

    return {"count":len(movies_list),"movies":movies_list}

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id,name,rating,link FROM movies WHERE id = ?",(movie_id,))
    row = cursor.fetchone()

    conn.close()


    if not row :
        raise HTTPException(status_code=404, detail="查无此片")
    else:
        movie = {
            "id":row[0],
            "name":row[1],
            "rating":row[2],
            "link":row[3]
            }
        return {"movie":movie}
    
