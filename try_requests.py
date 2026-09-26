import requests
from bs4 import BeautifulSoup

response = requests.get("https://baidu.com")
response.encoding = "utf-8"

soup = BeautifulSoup(response.text,"html.parser")

title = soup.title.string
print(f"网页标题是：{title}")

links = soup.find_all("a")
print(f"这个页面有{len(links)}个超链接")

for link in links[:3]:
    print(f"连接文字是：{link.text}")
