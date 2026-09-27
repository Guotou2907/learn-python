import requests
import time
import random
import json

all_movies = []

from bs4 import BeautifulSoup

session = requests.Session()

session.headers.update({
    "User-Agent":(
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept":(
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.douban.com/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
})

for i in range(10):          
    start = i * 25           
    url = f"https://movie.douban.com/top250?start={start}"

    response = session.get(url,timeout = 10)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text,"html.parser")

    movies = soup.find_all("div",class_ = "item")

    for movie in movies:
        name = movie.find("span", class_="title").text
        rating = movie.find("span", class_="rating_num").text
        link = movie.find("a")["href"]
        movie_data = {
            "name" : name,
            "rating" : rating,
            "link" : link
        }
        all_movies.append(movie_data)
    
        #print(f"电影：{name}，评分：{rating}，链接：{link}")
                       
    time.sleep(random.uniform(1, 3))
        
print(f"一共找到了{len(all_movies)}部电影")
with open("douban_top250.json","w",encoding = "utf-8") as f:
    json.dump(all_movies,f,ensure_ascii = False,indent = 2)
print("全部爬取完毕，已保存到 douban_top250.json")
