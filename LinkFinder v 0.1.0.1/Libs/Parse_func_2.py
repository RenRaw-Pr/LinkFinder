from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
#============================================================================================================
# Промежуточные функции для парсинга

def get_links(driver):
    result_links = []
    for elem in driver.find_elements(By.XPATH, '//*[@id="search-result"]/li'):
        print(elem.get_attribute("href§§222333c"))
    #return result_links


def parse_site(url, driver):
    parse_info = {'load': False, 'url': url, 'img': None, 'price': None}
    driver.get(url)
    # Ждем прогрузки страницы
    try:
        body_wait = WebDriverWait(driver, 4).until(EC.presence_of_element_located(By.TAG_NAME, 'body'))
    # Если страница не прогрузилась
    except Exception as e:
        # Работем с содержимым страницы
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        pars_text = soup.get_text("", strip = False)
        #parse_info['price']
        print(pars_text)
        
    # Если страница прогрузилась
    else:
        parse_info['load'] = True
        # Сохраняем скриншот
        page = driver.find_element(By.TAG_NAME, 'body')
        parse_info['img'] = (page.screenshot_as_base64)[0:4]

        # Работем с содержимым страницы
        soup = BeautifulSoup(driver.page_source, features="html.parser")
        pars_text = soup.get_text("", strip = False)
        parse_info['price'] = pars_text[0:4]
        print(pars_text)
#============================================================================================================

def start_parse(search):
    # Главные настройки парсера / main options of parser
    path = './Cromedrivers'
    browser_url = 'https://ya.ru/'
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument("user-data-dir=./Data/Default")
    driver = webdriver.Chrome(path+'/chromedriver_v109', options=chrome_options)
    # Делаем запрос в поисковую машину
    driver.get(browser_url)
    search_line = driver.find_element(By.XPATH, "//input[@id='text'][@name='text']")
    search_line.send_keys(search) 

    search_button = driver.find_element(By.XPATH, "//button[@class='search3__button mini-suggest__button']")  
    search_button.click()

    # Считываем ссылки из результата поиска и проверяем текст на каждой из них

    #for link in get_links(driver.page_source):
        #parse_site(link, driver)
    get_links(driver)
    driver.close()
start_parse("пгу")