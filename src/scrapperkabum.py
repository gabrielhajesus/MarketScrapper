from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import pandas as pd

cards = []


url = 'https://www.kabum.com.br/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}

req = Request(url, headers = headers)
response = urlopen(req)
html = response.read()
html = html.decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

anuncios = soup.find('div',{"class":"sc-edUIhV fMjDrq"})
print(anuncios)
#with open("saida_texto.txt", "w", encoding= "utf-8") as arquivo:
 #       arquivo.write(anuncios.decode('utf-8'))
