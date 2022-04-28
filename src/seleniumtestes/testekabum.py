from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class chamadaselenium:
    def funsele():
        driver = webdriver.Chrome(service = Service('/Users/Gabriel/drivechrome/chromedriver') , options= webdriver.ChromeOptions())

        driver.get('https://www.kabum.com.br/ofertas/megamaio?pagina=1')

        driver.maximize_window() # For maximizing window
        driver.implicitly_wait(20) # gives an implicit wait for 20 seconds


        elements = driver.find_elements(By.CLASS_NAME,"nameCard")

        for element in elements:
            print(element.text)

        driver.quit()

"""# Code to read data from HTML heref
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,"sc-dFdIVH gPDxyn sc-bPyhqo kgBarW nameCard"))
    )
    print(element.text)
finally:
    driver.quit()"""