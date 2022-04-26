from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import pandas as pd

# Declarando variável cards
cards = []

# Obtendo o HTML
url = 'https://www.pichau.com.br/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}
req = Request(url, headers = headers)
response = urlopen(req)
html = response.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

# Obtendo a campanha de promoção atual

resultado = soup.find('a' , {'class': "jss12 jss27"})
url = resultado['href']
print(url)


req = Request(url, headers = headers)
response = urlopen(req)
html = response.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

paginas = soup.find('div' , {'id': "__next"}).find('div' ,{'class': "jss40"})
with open("saida_texto1.txt", "w", encoding= "utf-8") as arquivo:
        arquivo.write(str(paginas))


"""""
# Obtendo as TAGs de interesse
anuncios = soup.find('div', {'id':"secaoOfertasCampanha"}).find('div',{'class':"slick-slider slick-initialized"}).findAll('div', {"style":"outline:none"})

# Coletando as informações dos CARDS
for anuncio in anuncios:
    card = {}

    # Nome
    card['Nome do produto'] = anuncio.find('h2').getText()

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
    urlretrieve(image.get('src'), './src/img/kabum/' + image.get('src').split('/')[-1] )

dataset = pd.DataFrame(cards)
dataset.to_csv('./src/data/kabum/promoçõeskabum.csv', sep=';', index = False, encoding ='utf-8-sig')
print(dataset)"""