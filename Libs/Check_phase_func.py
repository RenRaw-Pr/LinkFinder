from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import traceback

# Функция проверки драйвера последней версии
def try_driver_last_version():
    path = './Cromedrivers'
    
    file = open(path+'/Driver_versions.txt', 'r')
    last_driver_version = file.readline()
    file.close()

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(service = Service(path+'/chromedriver_v'+last_driver_version), options=chrome_options)
        driver.quit()
    except Exception as e:
        browser_version = traceback.format_exc().split('Current browser version is ')[1].split(' ')[0]
        return browser_version
    
# Функция поиска подходящего драйвера 
def find_drivers(browser_version):
    path = './Cromedrivers/'

    file = open(path+'/Driver_versions.txt', 'r')
    text = file.read()
    file.close()
    if browser_version == None:
        return text[0:3]
    else:
        if browser_version[0:3] in text:
            return browser_version[0:3]
        else:
            return ("warning", browser_version)
        
try_driver_last_version()