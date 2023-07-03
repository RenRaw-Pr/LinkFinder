import requests as req
from bs4 import BeautifulSoup

# функция для получения url - адресов возможных сайтов
def get_urls(search_term, url_max_count):
    _cancel_list = [
        "webcache",
        "https://support.google.com/",
        "https://accounts.google.com/",
        "https://www.youtube.com/"
    ]
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
                tag=True
                for cancel in _cancel_list:
                    if cancel in href:
                        tag=False 
                if tag==True:
                    res.append(href)
                    if len(res) >= url_max_count:    # остановка поиска после достижения нужного количества результатов
                        break
        if len(res) >= url_max_count:
            break
    return res

def analyze_url(url, search_term, compare=0.8):
    try:
        response = req.get(url, timeout=1)
        soup = BeautifulSoup(response.text, "html.parser")
        # Получение текста
        text = soup.get_text().replace('\n', '').replace('\xa0', '').replace('\t', '').replace("  ","")
        # Сравнение с запросом
        text_words = text.split()
        term_words = search_term.split()
        matching_words = sum(1 for word in term_words if word in text_words)
        if matching_words / len(term_words) > compare:
            return "Connected", f"Compare > {compare*100}% Sucess"
        else:
            return "Connected", f"Compare < {compare*100}% Error"

    except req.exceptions.Timeout: return "Timeout"
    except req.exceptions.ConnectionError: return "Lost connection"







for num, url in enumerate(get_urls("Компрессорно-конденсаторный блок NSK 060", 10)):
    print(num, url, analyze_url(url, "Компрессорно-конденсаторный блок NSK 060"))