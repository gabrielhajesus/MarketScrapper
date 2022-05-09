import time
from posixpath import split
from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


#definindo o navegador do drive como invisivel
options= webdriver.ChromeOptions()

#Executando drive do google
driver = webdriver.Chrome(service = Service('/Users/Gabriel/drivechrome/chromedriver') , options= options)
driver.maximize_window() # For maximizing window

print ("Chrome Initialized")

# Declarando variável cards
cards = []

#SCROLL_PAUSE_TIME = 2

# Declarando variável cards
cards = []

# Obtendo o HTML

driver.get('https://www.pichau.com.br/promocao/trabalhador?utm_source=home&utm_medium=banner&utm_campaign=trabalhador_2022')


# Pegando o tamanho do scroll
"""last_height = driver.execute_script("return document.body.scrollHeight")

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
"""
soup = BeautifulSoup(driver.page_source, 'html.parser')
print('pegando o html da pagina completa')


# Obtendo as TAGs de interesse
anuncios = soup.find('div', {'class':"infinite-scroll-component__outerdiv"}).find('div',{'class':"MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-3"}).findAll('div', {"class":"MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-6 MuiGrid-grid-lg-4 MuiGrid-grid-xl-3"})


# Coletando as informações dos CARDS
for anuncio in anuncios:
    card = {}

    conteudoTexto = anuncio.find(class_ = "MuiCardContent-root").getText()
    #Placa de Video Asrock Radeon RX 6700 XT Challenger D 12GB GDDR6 OC 192-bit, 90-GA31ZZ-00UANFde R$ 7.840,80 por:
    # à vistaR$5.299,90no PIX com 12% descontoR$ 6.022,61em até 12x de 501,88sem juros no cartão
    
    card['Conteudo Texto'] = anuncio.find(class_ = "MuiCardContent-root").getText()
    
    #conteudoTexto.split(',')[0]

    # Preços
    #card['Precos'] = conteudoTexto.split()

    # Adicionando resultado a lista cards
    cards.append(card)

    # Adicionando as imagens ao nosso programa
    #image = anuncio.find('img')
    #urlretrieve(image.get('src'), './src/img/pichau/' + image.get('src').split('/')[-1] )

dataset = pd.DataFrame(cards)
dataset.to_csv('./data/pichau/dataset/promoçõespichau.csv', sep=';', index = False, encoding ='utf-8-sig')