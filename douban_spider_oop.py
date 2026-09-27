import requests
import time
import random
import json
from bs4 import BeautifulSoup

class DoubanSpider:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.douban.com/",
        })
        self.all_movies = []

    def fetch_page(self,start):
        url = f"https://movie.douban.com/top250?start={start}"
        response = self.session.get(url,timeout = 10)
        response.encoding = "utf-8"
        return response.text

    def parse_page(self,html):
        soup = BeautifulSoup(html,"html.parser")
        movies = soup.find_all("div",class_="item")
        for movie in movies:
            name = movie.find("span", class_="title").text
            rating = movie.find("span", class_="rating_num").text
            link = movie.find("a")["href"]

            self.all_movies.append({
                "name": name,
                "rating": rating,
                "link": link
            })

    def save_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.all_movies, f, ensure_ascii=False, indent=2)
        print(f"已保存到 {filename}，共 {len(self.all_movies)} 部电影")

    def run(self):
        for i in range(10):
            start = i*25;
            print(f"现在在寻找第{i+1}页的电影")
            html = self.fetch_page(start)
            self.parse_page(html)
            time.sleep(random.uniform(1, 3))
        self.save_to_file("douban_top250_oop.json")

if __name__ == "__main__":
    spider = DoubanSpider()
    spider.run()
