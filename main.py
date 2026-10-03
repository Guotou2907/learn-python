from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sqlite3

class UTF8JSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"

app = FastAPI(default_response_class=UTF8JSONResponse)

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
