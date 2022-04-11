import bs4
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import pandas

urll = 'https://www.kabum.com.br/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}

def trata_saida(input):
    html = input.decode('utf-8')
    soup = bs4.BeautifulSoup(html, 'html.parser')
    with open("saida_texto.txt", "w", encoding= "utf-8") as arquivo:
        arquivo.write(soup.decode('utf-8'))
    return


try:
    req = Request(urll, headers = headers)
    response = urlopen(req)
    html = response.read()
    trata_saida(html)
      
except HTTPError as e:
    print(e.status, e.reason)

except URLError as e:
    print(e.reason)