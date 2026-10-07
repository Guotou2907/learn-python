import sqlite3
from fastapi import FastAPI,HTTPException,status
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field

class UTF8JSONResponse(JSONResponse):
    media_type = "application/json;charset=utf-8"

app = FastAPI(default_response_class = UTF8JSONResponse)

class MovieCreate(BaseModel):
    name : str = Field(min_length = 0)
    rating : float = Field(ge = 0,le = 10)
    link : str = ""

@app.get("/movies")
def get_movies(min_rating:float = 0.0):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id,name,rating,link FROM movies WHERE rating >= ?",(min_rating,))
    rows = cursor.fetchall()
    conn.close()

    movies_list = []
    for row in rows:
        movies_list.append({"id":row[0],"name":row[1],"rating":row[2],"link":row[3]})

    return {"count":len(movies_list),"movies":movies_list}

@app.post("/movies", status_code=status.HTTP_201_CREATED)
def add_movie(movie:MovieCreate):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO movies (name,rating,link) VALUES (?,?,?)",(movie.name,movie.rating,movie.link))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return{"message":"添加成功","movie":{"id":new_id,"name":movie.name,"rating":movie.rating,"link":movie.rating}}

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    conn = sqlite3.connect("movies.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id,name,rating,link FROM movies WHERE id = ?",(movie_id,))
    row = cursor.fetchone()
    cursor.close()

    if not row:
        raise HTTPException(status_code=404,detail="查无此片")
    return {"movie":{"id":row[0],"name":row[1],"rating":row[2],"link":row[3]}}
