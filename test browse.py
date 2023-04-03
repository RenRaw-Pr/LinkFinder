import requests
from bs4 import BeautifulSoup

search_term = "Светодиодный светильник 33 Вт, IP65l"
url = "https://www.google.com/search?q=" + search_term

r = requests.get(url)
soup = BeautifulSoup(r.content)

links = soup.find_all("a")
for link in links:
    href = link.get("href")
    if href.startswith("/url?q="):
        href = href.replace("/url?q=", "")
        href = href.split("&")[0]
        if "webcache" not in href:
            print(href)
