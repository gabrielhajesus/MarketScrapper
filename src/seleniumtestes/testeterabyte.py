import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options= webdriver.ChromeOptions()

options.add_argument("--disable-popup-blocking")

driver = webdriver.Chrome(service = Service('/Users/Gabriel/drivechrome/chromedriver') , options= options )

driver.get('https://www.terabyteshop.com.br/promocoes?utm_source=terabyte-site&utm_medium=banner-desktop&utm_campaign=work-week-25-04-22-q2')

driver.maximize_window() # For maximizing window

SCROLL_PAUSE_TIME = 50

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    driver.find_elements(By.XPATH,"/html/body/div[7]/div/div/div/button").click()

    """"<div class="footer-content">
            <a id="pdmore" class="arrow-down btn btn-pdmore" href="/promocoes" data-pg="2" data-manufacturer="0" data-order="ordem_asc" role="button">
                <span class="hidden-xs hidden-sm">CLIQUE PARA</span> VER MAIS PRODUTOS
            </a>"""

    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"div.footer-content a.pdmore.arrow-down.btn.btn-pdmore[role='button']"))).click()

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height



driver.implicitly_wait(20)

elements = driver.find_elements(By.CLASS_NAME,"MuiTypography-h6")

lista = []

for element in elements :
    lista.append(element.text)

with open("saida_texto2.txt", "w", encoding= "utf-8") as arquivo:
        arquivo.write(str(lista))


driver.quit()