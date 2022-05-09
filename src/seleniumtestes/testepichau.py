import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(service = Service('/Users/Gabriel/drivechrome/chromedriver') , options= webdriver.ChromeOptions())

driver.get('https://www.pichau.com.br/promocao/trabalhador?utm_source=home&utm_medium=banner&utm_campaign=trabalhador_2022')

driver.maximize_window() # For maximizing window

SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

driver.implicitly_wait(20)

elements = driver.find_elements(By.CLASS_NAME,"MuiTypography-h6")

print(elements)

driver.quit()