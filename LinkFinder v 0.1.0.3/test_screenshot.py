from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from PIL import Image

from io import BytesIO

import base64

path = './Cromedrivers'

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('window-size=1920x1080')

driver = webdriver.Chrome(path+'/chromedriver_v107', options=chrome_options)
driver.get('https://ya.ru/')


page = driver.find_element(By.TAG_NAME, "body")
img_b64 = page.screenshot_as_base64
print(img_b64)

'''img = Image.open('./Data/screenshot_full.png')
new_img = img.resize((192,108))
new_img.save('./Data/new_screenshot.png')

driver.quit()
'''