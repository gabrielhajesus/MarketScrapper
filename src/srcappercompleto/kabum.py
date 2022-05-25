from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from urllib.request import Request, urlopen, urlretrieve
import pandas as pd

#Conexão com o Mongodb
client = MongoClient('localhost', 27017)
db = client.sites
promocao = db.kabum

#Definindo o navegador do drive como Chrome
options= webdriver.ChromeOptions()

#Executando drive do google
driver = webdriver.Chrome(service = Service('/Users/Gabriel/drivechrome/chromedriver') , options= options)
driver.maximize_window()
print ("Chrome Initialized")

# Obtendo a campanha de promoção atual
driver.get("https://www.kabum.com.br")
soup = BeautifulSoup(driver.page_source, 'html.parser')
campanhaAtual= soup.find('a' , {'id': "bannerPrincipal"}).get('href')

# Indo para a campanha de promoção atual
driver.get('https://www.kabum.com.br' + campanhaAtual + '?pagina=1')
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Declarando variável cards
cards = []

# Obtendo as paginas
print('pegando as paginas')
page = int(soup.find('div', {'id' : "blocoPaginacao"}).findAll('button')[-3].getText())

#Obtendo o conteudo do site
for i in range(73):

    print('aba ' + str(i))

    ## Obtendo o HTML
    driver.get('https://www.kabum.com.br' + campanhaAtual + '?pagina=' + str(i + 1))
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Obtendo as TAGs de interesse
    anuncios = soup.find('section', {'id':"blocoProdutosListagem"}).findAll('div', {'class':"productCard"})

    # Coletando as informações dos CARDS
    for anuncio in anuncios:
        card = {}

        # Nome
        card['name'] = anuncio.find('span', {'class':"nameCard"}).getText()

        # Valor antigo
        card['old_price_card'] = anuncio.find(class_ = "oldPriceCard").getText()

        # Valor
        card['price_card'] = anuncio.find(class_ = "priceCard").getText()

        #Tipo de Compra
        card['price_text_card'] = anuncio.find(class_ = "priceTextCard").getText()

        # Adicionando resultado a lista cards
        cards.append(card)

        # Adicionando as imagens ao nosso programa
        """image = anuncio.find('img', {'class':'imageCard'})
        nome = image.get('src').split('/')[-1]
        while(len(nome) > 178):
            aux = nome.split('-').pop()
            nome = "-".join(aux)   
        urlretrieve(image.get('src'), './data/kabum/img/' + nome)"""

#Fechando o Driver
driver.quit()

#Inserindo o resultado no banco de dados
promocao.insert_many(cards)