# PromoHunter

O objetivo do projeto é fazer scrapping de sites de compras e mostrar produtos em promoção em um site local.

# Tópicos

- arquitetura do projeto
- dependencias necessarias
- como usar

# Arquitetura do projeto

![Alt text](./Users/Gabriel/Pictures/arquitetura.jpg?raw=true "Title")

# dependencias necessarias

Beautiful Soup
```
pip install beautifulsoup4 
```

Selenium
```
pip install selenium
```
O selenium necessita que o driver do google chrome seja baixado, o driver deve ser compativel com a versão do navegador ulilizado.

Link para download do driver:
https://chromedriver.chromium.org/downloads

O arquivo deve ser extraido em uma pasta e essa pasta deve ser definida como PATH do sistema.
O caminho da pasta deve ser colocado no arquivo inicia_selenium.py.
```
driver = webdriver.Chrome(service = Service('your path') , options= options)
```

pymongo
```
pip install pymongo
```
flask
```
pip install  flask
```
webdriver_manager
```
pip install webdriver_manager 
```

## Documentação

Documentação das bibliotecas

| Docs | links |
| ------ | ------ |
| Beautiful Soup | https://www.crummy.com/software/BeautifulSoup/bs4/doc/ |
| selenium | https://selenium-python.readthedocs.io/index.html  |
| pymongo | https://pymongo.readthedocs.io/en/stable/tutorial.html  |
| flask | https://pythonbasics.org/what-is-flask-python/ |

# Como usar


- Após instalar todas as dependências necessárias,
- podemos adicionar um novo site a base de sites ou executar os já existentes,
- devemos criar as coleções dos sites no banco de dados e a coleção de produtos,
- executar o scraping dos sites,
- executar produtos.py
- executar promohunter.py
- no seu navegador entrar no endereço http://127.0.0.1:5000/
