import requests as req
from bs4 import BeautifulSoup
import multiprocessing as mp


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

def analyze_url(url):
    try:
        response = req.get(url, timeout=1)
        soup = BeautifulSoup(response.text, "html.parser")
        text = list(soup.get_text().splitlines())
        for i in range(len(text)):
            text[i] = text[i].replace('\xa0', '').replace('\t', '').replace("  ","")
        text = list(filter(None, text))
        
        return "Connected"

    except req.exceptions.Timeout: return "Timeout"
    except req.exceptions.ConnectionError: return "Lost connection"

class Search_process():
    def __init__(self, progress_queue):
        self.progress_queue = progress_queue
    
    def run(self, search_term, url_max_count, step):
        for num, elem in enumerate(get_urls(search_term, url_max_count)):
            progress = num
            self.progress_queue.put(progress)
            print(num, elem, analyze_url(elem))