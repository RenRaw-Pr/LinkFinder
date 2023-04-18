import requests as req
from bs4 import BeautifulSoup

# функция для получения url - адресов возможных сайтов
def get_urls(search_term, url_max_count):
    res = []
    url = "https://www.google.com/search?q=" + search_term
    PAGES_COUNT = url_max_count//10 + 2
    for page in range(PAGES_COUNT):
        start = page*10
        search_url = f"{url}&start={start}"
        for link in BeautifulSoup(req.get(search_url).content, features="html.parser").find_all("a"):
            href = link.get("href")
            if href.startswith("/url?q="):
                href = href.replace("/url?q=", "")
                href = href.split("&")[0]
                if "webcache" not in href and "https://support.google.com/" not in href and "https://accounts.google.com/" not in href:
                    res.append(href)
                    if len(res) >= url_max_count:    # остановка поиска после достижения нужного количества результатов
                        break
        if len(res) >= url_max_count:
            break
    return res

'''
for num, elem in enumerate(get_urls("Компрессорно конденсаторный блок NSK 060", 20)):
    print(num ,elem, end=' ')
    try:
        response = req.get(elem, timeout=1)
        soup = BeautifulSoup(response.text, "html.parser")
        text = list(soup.get_text().splitlines())
        for i in range(len(text)):
            text[i] = text[i].replace('\xa0', '').replace('\t', '').replace("  ","")
        text = list(filter(None, text))
        
        print("Connected")

    except req.exceptions.Timeout: print("Timeout")
    except req.exceptions.ConnectionError: print("Lost connection")
'''
# функция для проверки сайта по его url - адресу