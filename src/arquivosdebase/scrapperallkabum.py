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

# Obtendo a campanha de promoção atual

#resultado = soup.find('a' , {'id': "bannerPrincipal"})
#driver.get("https://www.kabum.com.br"+resultado))

# Obtendo as paginas

driver.get('https://www.kabum.com.br/ofertas/megamaio?pagina=1' )
soup = BeautifulSoup(driver.page_source, 'html.parser')

print('pegando as paginas')
page = int(soup.find('div', {'id' : "blocoPaginacao"}).findAll('button')[-3].getText())

for i in range(page):

    print('aba ' + str(i))

    ## Obtendo o HTML
    driver.get('https://www.kabum.com.br/ofertas/megamaio?pagina=' + str(i + 1))
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Obtendo as TAGs de interesse
    anuncios = soup.find('section', {'id':"blocoProdutosListagem"}).findAll('div', {'class':"productCard"})

    # Coletando as informações dos CARDS
    for anuncio in anuncios:
        card = {}

        # Nome
        card['Nome do produto'] = anuncio.find('span', {'class':"nameCard"}).getText()

        # Valor antigo
        card['Preço Antigo do produto'] = anuncio.find(class_ = "oldPriceCard").getText()

        # Valor
        card['Preço do produto'] = anuncio.find(class_ = "priceCard").getText()

        #Tipo de Compra
        card['Tipo de Compra'] = anuncio.find(class_ = "priceTextCard").getText()

        # Adicionando resultado a lista cards
        cards.append(card)

        # Adicionando as imagens ao nosso programa
        image = anuncio.find('img', {'class':'imageCard'})
        urlretrieve(image.get('src'), './data/kabum/img/' + image.get('src').split('/')[-1] )

driver.quit()

dataset = pd.DataFrame(cards)
dataset.to_csv('./data/kabum/dataset/promoçõeskabum.csv', sep=';', index = False, encoding ='utf-8-sig')