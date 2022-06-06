from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from urllib.request import Request, URLopener
import pandas as pd
import time
from banco import Banco


#Conexão com o Mongodb
banco_de_dados = Banco.inicia_banco()
pichau = Banco.pichau(banco_de_dados)

#Definindo o navegador do drive como Chrome
options= webdriver.ChromeOptions()

#Executando drive do google
driver = webdriver.Chrome(service = Service('/Users/Gabriel/drivechrome/chromedriver') , options= options)
driver.maximize_window()
print ("Chrome Inicializado")

# Obtendo a campanha de promoção atual
driver.get("https://www.pichau.com.br/")
paginaprincipal = BeautifulSoup(driver.page_source, 'html.parser')
campanhaAtual = paginaprincipal.main.div.div.div.div.ul.li.a.get('href')
nomecampanha = paginaprincipal.main.div.div.div.div.ul.li.a.get('title')

# Indo para a campanha atual
driver.get(campanhaAtual)
print('Pegou a campanha Atual')

# Pegando o tamanho do scroll
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")
print(range(last_height))
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        print(range(last_height))
        for i in range(1000):
            driver.execute_script("window.scrollTo(0, "+ str(i*250) +");")
        break
    last_height = new_height

depoisdoscroll = BeautifulSoup(driver.page_source, 'html.parser')
print('Pagina completa')

#Fechando o Driver
driver.quit()

# Obtendo as TAGs de interesse
anuncios = depoisdoscroll.find('main').find('div', {'class' : "infinite-scroll-component__outerdiv"}).find('div').find('div').findAll('a')

# Declarando variável cards e imagens
cards = []
imagens = []
erros = []

# Coletando as informações dos CARDS
for anuncio in anuncios:
    card = {} 
    
    # Nome
    card['name'] = anuncio.find('div', {'class':'MuiCardContent-root'}).find('h2').getText()  

    try:
        # Valor antigo
        preco_antigo = anuncio.find('div', {'class':'MuiCardContent-root'}).find('div').find('div').find('div').find('div').getText()
        preco_antigo = preco_antigo.split(' ')
        preco_antigo.pop()
        del preco_antigo[0]
        preco_antigo = " ".join(preco_antigo)

        card['old_price_card'] = preco_antigo

        # Valor Completo
        preco = anuncio.find('div', {'class':'MuiCardContent-root'}).div.div.div.div.find_next_sibling().find_next_sibling().getText()
        
        card['price_card'] = preco

        #Preço parcelado
        desconto = anuncio.find('div', {'class':'MuiCardContent-root'}).div.div.div.span.find_next_sibling().find_next_sibling().getText()
        preco_parcelado = anuncio.find('div', {'class':'MuiCardContent-root'}).div.div.find_next_sibling().find_next_sibling().div.div.getText()
        parcelado = anuncio.find('div', {'class':'MuiCardContent-root'}).div.div.find_next_sibling().find_next_sibling().div.span.getText()
        card['price_text_card'] = preco_parcelado + ' ' + parcelado + ' e avista ' + desconto

        #Tag da Promocao
        card['tag_campanha'] = nomecampanha
        
        #Link do produto
        card['link_produto'] = 'https://www.pichau.com.br' + anuncio.get('href')

        #Loja da pichau
        card['loja'] = 'Pichau'

        cards.append(card)
    except:
        continue

    # Adicionando as imagens a lista
    try:
        imagem = anuncio.find('div', {"class":"lazyload-wrapper"}).img['src']
        imagens.append({'imagem' : imagem, 'nome': card['name']})
    except:
        erros.append([card['name'] , anuncio.find('div', {"class":"lazyload-wrapper"}).img])

#Definindo um header para o download das imagens
opener = URLopener()
opener.addheader('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36')

with open("saida_texto.txt", "w", encoding= "utf-8") as arquivo:
        arquivo.write(imagem)

for imagem in imagens:
    nome = imagem['nome']
    nome = Banco.convertenome(nome)
    filename, headers = opener.retrieve(imagem['imagem'], './data/pichau/img/'+ nome + '.jpg')


#Inserindo o resultado no banco de dados
pichau.insert_many(cards)