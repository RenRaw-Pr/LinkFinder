from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import traceback

def try_driver_last_version():
    path = '/Users/Dima/Desktop/LinkFinder v 0.1.0.1/Cromedrivers/'
    
    file = open(path+'Driver_versions.txt', 'r')
    last_driver_version = file.readline()[-4::].replace('\n', '')
    file.close()

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(path+'chromedriver_v'+last_driver_version, options=chrome_options)
    except Exception as e:
        browser_version = traceback.format_exc().split('Current browser version is ')[1].split(' ')[0]
        return browser_version
    
def find_drivers(browser_version):
    path = '/Users/Dima/Desktop/LinkFinder v 0.1.0.1/Cromedrivers/'
    file = open(path+'Driver_versions.txt', 'r')
    text = file.read()
    file.close()
    if browser_version == None:
        return text[14:17]
    else:
        if browser_version[0:3] in text:
            return browser_version[0:3]
        else:
            return ("warning", browser_version)