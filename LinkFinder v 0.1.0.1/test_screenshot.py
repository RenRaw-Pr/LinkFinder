from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from PIL import Image

path = './Cromedrivers'

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('window-size=1920x1080')

driver = webdriver.Chrome(path+'/chromedriver_v105', options=chrome_options)
driver.get('https://ya.ru/')





page = driver.find_element(By.TAG_NAME, "body")
page.screenshot("./Data/screenshot_full.png")

img = Image.open('./Data/screenshot_full.png')
new_img = img.resize((192,108))
new_img.save('./Data/new_screenshot.png')

driver.quit()