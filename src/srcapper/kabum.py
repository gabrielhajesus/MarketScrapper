from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from urllib.request import Request, urlopen, urlretrieve
import pandas as pd
from banco import Banco

#Conexão com o Mongodb
banco_de_dados = Banco.inicia_banco()
kabum = Banco.kabum(banco_de_dados)

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
nomecampanha = campanhaAtual.split('/')
nomecampanha = nomecampanha[-1]

# Indo para a campanha de promoção atual
driver.get('https://www.kabum.com.br' + campanhaAtual + '?pagina=1')
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Declarando variável cards
cards = []

# Obtendo as paginas
print('pegando as paginas')
page = int(soup.find('div', {'id' : "blocoPaginacao"}).findAll('button')[-3].getText())

#Obtendo o conteudo do site
for i in range(page):

    print('aba ' + str(i+1))

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

        #Tag da Promocao
        card['tag_campanha'] = nomecampanha
        
        #Link do produto
        card['link_produto'] = 'https://www.kabum.com.br' + anuncio.find('a').get('href')

        #Loja da kabum
        card['loja'] = 'Kabum'

        # Adicionando resultado a lista cards 
        cards.append(card)

        # Adicionando as imagens ao nosso programa
        image = anuncio.find('img', {'class':'imageCard'})
        nome = card['name']
        nome = Banco.convertenome(nome)
        """while(len(nome) > 178):
            aux = nome.split('-').pop()
            nome = "".join(aux)"""
        urlretrieve(image.get('src'), './data/kabum/img/' + nome + '.jpg')

#Fechando o Driver
driver.quit()

#Inserindo o resultado no banco de dados
kabum.insert_many(cards)