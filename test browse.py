'''
import requests
from bs4 import BeautifulSoup

search_term = "Компрессорно конденсаторный блок NSK 060"
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
'''
import requests
from bs4 import BeautifulSoup

search_term = "Компрессорно конденсаторный блок NSK 060"
url = "https://www.google.com/search?q=" + search_term

links_found = []    # список для сохранения найденных ссылок
NUM_PAGES = 4       # количество страниц, которые мы хотим обработать
link_count = 0      # счетчик найденных ссылок

for page in range(NUM_PAGES):
    start = page * 10
    search_url = f"{url}&start={start}"
    r = requests.get(search_url)
    soup = BeautifulSoup(r.content)

    links = soup.find_all("a")
    for link in links:
        href = link.get("href")
        if href.startswith("/url?q="):
            href = href.replace("/url?q=", "")
            href = href.split("&")[0]
            if "webcache" not in href and "https://support.google.com/" not in href and "https://accounts.google.com/" not in href:
                links_found.append(href)
                link_count += 1
                if link_count >= 30:    # остановка поиска после достижения нужного количества результатов
                    break
    if link_count >= 30:
        break

for num, link in enumerate(links_found):
    print(num, link)
