from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import time

from bs4 import BeautifulSoup

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# открытие браузера и запрос + сохранил код 
def open_browser(text):
    driver = webdriver.Chrome('/Users/Dima/Desktop/Parser/chromedriver_v105')
    driver.get('https://yandex.ru/') # открываем браузер
    
    element = driver.find_element(By.ID, "text") # ищем строку поиска
    element.send_keys(text) # заполняем поле запроса

    find_button= driver.find_element(By.CLASS_NAME, "search2__button") # ицем кнопку поиска
    find_button.click()# выполняем поиск
    
    time.sleep(2)
     # сохраняем код, чтобы распарсить
    HTML_code = driver.page_source
    fileToWrite = open("HTML_code.html", "w")
    fileToWrite.write(HTML_code)
    fileToWrite.close()
print( open_browser("конденсатор"))
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# сохранение ссылок
def save_links():

    # чтение файла
    with open("HTML_code.html", "r") as f:
        contents = f.read()

    soup = BeautifulSoup(contents, features="html.parser")
    
    # сбор ссылок по результату запроса
    result_links = []
    for link in soup.find_all(class_ = "Link Link_theme_outer Path-Item link path__item link organic__greenurl"):
        result_links.append(link.get('href'))
    return result_links

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# парсинг найденных ссылок
def find_text(links):
    driver = webdriver.Chrome('/Users/Dima/Desktop/Parser/chromedriver_v104')
    link_for_show = []
    text_in = []
    for link in links:
        driver.get(link) # открываем ccылку
        
        time.sleep(0.5)
        
        # сохраняем код
        HTML_code = driver.page_source
        fileToWrite = open("HTML_code.html", "w")
        fileToWrite.write(HTML_code)
        fileToWrite.close()
        
        # парсим код (поиск читаемого текста)
        with open("HTML_code.html", "r") as f:
            contents = f.read()
        soup = BeautifulSoup(contents, features="html.parser")
        pars_text = soup.get_text("", strip = False)

        # Анализ
        link_for_show.append(link)
        if ("Цена: " or "Цена " or "Стоимость " or "руб.") in pars_text:
            text_in.append("1")
        else:
            text_in.append("0")
        result = [link_for_show, text_in]
    return result
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# обобщение
def all_parse(search):
    open_browser(search)
    result = find_text(save_links())
    return result
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
search = "пгу"
all_parse(search)
