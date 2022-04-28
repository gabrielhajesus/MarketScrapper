from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service = Service('/Users/Gabriel/drivechrome/chromedriver') , options= webdriver.ChromeOptions())

driver.get('https://quotes.toscrape.com/js')

# Code to read data from HTML heref
element = driver.find_element(By.CLASS_NAME,"author")
print(element.text)

elements = driver.find_elements(By.CLASS_NAME,"author")

for element in elements:
    print(element.text)

driver.implicitly_wait(20)

driver.quit()