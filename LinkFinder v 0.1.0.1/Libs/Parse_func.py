from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time

from bs4 import BeautifulSoup



def start_parse(search):
    # Главные настройки парсера / main options of parser
    path = './Cromedrivers'
    browser_url = 'https://ya.ru/'
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('window-size=1920x1080')

    driver = webdriver.Chrome(path+'/chromedriver_v105', options=chrome_options)
    
    # Делаем запрос в поисковую машину
    driver.get(browser_url)
    search_line = driver.find_element(By.ID, "test")
    search_line.send_keys(search) 

    search_button = driver.find_element(By.CLASS_NAME, "search3__button mini-suggest__button")  
    search_button.click()

start_parse('пгу')