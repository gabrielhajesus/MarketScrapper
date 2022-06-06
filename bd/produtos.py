from hashlib import new
from pymongo import MongoClient
from banco import Banco

banco_de_dados = Banco.inicia_banco()
kabum = Banco.kabum(banco_de_dados)
pichau = Banco.pichau(banco_de_dados)
produtos = Banco.produtos(banco_de_dados)

todos_kabum = kabum.find()
todos_pichau = pichau.find()


def inserirnobanco(item = {}, produtos = produtos):
    nome_de_busca = Banco.convertenome(item['name'])
    if produtos.find_one(nome_de_busca)!= None:
        produtobanco = produtos.find_one(nome_de_busca)
        if produtobanco['menor_preco'] > item['price_card']:
            produtos.update_one({'nome' : item['name']}, {'$set': {"menor_preco": item['price_card'], "desconto": desconto(item['old_price_card'], item['price_card'], item['loja'])}})
        if item['loja'] == 'Kabum':
            produtos.update_one({'nome' : item['name']}, 
            {'$set': 
            {'kabum.old_price': item['old_price_card'],
            "kabum.preco_kabum" : item['price_card'],
            'kabum.price_text_card' : item['price_text_card'],
            "kabum.tag_campanha" : item['tag_campanha'],
            "kabum.link_produto" : item['link_produto']}})
        if item['loja'] == 'Pichau':
            produtos.update_one({'nome' : item['name']}, 
            {'$set': 
            {'pichau.old_price': item['old_price_card'],
            "pichau.preco_kabum" : item['price_card'],
            'pichau.price_text_card' : item['price_text_card'],
            "pichau.tag_campanha" : item['tag_campanha'],
            "pichau.link_produto" : item['link_produto']}}) 
    else:
        if item['loja'] == 'Kabum':
            produto = {
                'name' : item['name'],
                'search_name': nome_de_busca,
                'old_price': item['old_price_card'],
                'menor_preco' : item['price_card'],
                'link': item['link_produto'],
                'desconto': desconto(item['old_price_card'], item['price_card'], item['loja']),
                'categoria' : definindocategoria(item['name']),
                'kabum' :  {'old_price': item['old_price_card'],
                            'price' : item['price_card'],
                            'price_text_card' : item['price_text_card'],
                            'tag_campanha' : item['tag_campanha'],
                            'link' : item['link_produto']},
                'pichau' : None
            }
        if item['loja'] == 'Pichau':
            produto = {
                'name' : item['name'],
                'search_name': nome_de_busca,
                'old_price': item['old_price_card'],
                'menor_preco' : item['price_card'],
                'link': item['link_produto'],
                'desconto': desconto(item['old_price_card'], item['price_card'], item['loja']),
                'categoria' : definindocategoria(item['name']),
                'kabum' :  None,
                'pichau' : {'old_price': item['old_price_card'],
                            'price' : item['price_card'] ,
                            'price_text_card' : item['price_text_card'],
                            'tag_campanha' : item['tag_campanha'] ,
                            'link' : item['link_produto']}
            }
        produtos.insert_one(produto)

def definindocategoria(nomec):
    catHardware = ['processador', 'placa', 'memoria', 'SSD', 'fonte', 'fan', 'ddr3', 'ddr4']
    contadorHardware = 0
    catPeriferico = ['headset', 'mouse', 'teclado' , 'gabinete', 'mousepad', 'mochila']
    contadorPeriferico = 0
    catComputador = ['computador', 'notebook', 'linux', 'windows']
    contadorComputador = 0
    catCadeira = ['cadeira']
    contadorCadeira = 0
    catTV = ['tv', 'smart', '43', '70', '55', 'monitor', '23']
    contadorTV = 0
    catSmartfone = ['smartphone', 'iphone', 'apple']
    contadorSmartfone = 0
    contadorOutros = 0

    categoria = []
    nomec = nomec.replace(',',' ').replace('-',' ').replace('_',' ').replace('´',' ').lower().split(' ')
    for nome in nomec:
        if nome in catHardware:
            contadorHardware = contadorHardware + 1
            contadorOutros = 1
        if nome in catPeriferico:
            contadorPeriferico = contadorPeriferico + 1
            contadorOutros = 1
        if nome in catComputador:
            contadorComputador = contadorComputador + 1
            contadorOutros = 1
        if nome in catCadeira:
            contadorCadeira = contadorCadeira + 1
            contadorOutros = 1
        if nome in catTV:
            contadorTV = contadorTV + 1
            contadorOutros = 1
        if nome in catSmartfone:
            contadorSmartfone = contadorSmartfone + 1
            contadorOutros = 1
    
    if contadorSmartfone >= 1:
        categoria.append('Celular/Smartphone')
    if contadorCadeira >= 1:
        categoria.append('Cadeira')
    if contadorComputador >= 1 :
        categoria.append('Computador/Notebook')
    if contadorHardware > contadorPeriferico and contadorHardware > contadorTV and contadorHardware < 3:
        categoria.append('Hardware')
    if contadorPeriferico > contadorHardware:
        categoria.append('Periferico')
    if contadorTV > contadorPeriferico:
        categoria.append('TV/Monitor')
    if contadorOutros == 0:
        categoria.append('Outros')

    return categoria

def desconto(old_price, new_price, loja):
    old_price = old_price.replace('R$', '').replace('\xa0','').replace('.','').replace(',','')
    new_price = new_price.replace('R$', '').replace('\xa0','').replace('.','').replace(',','')
    desconto = int((float(old_price) - float(new_price) ) * 100 / float(old_price))
    return desconto



tagKabum = ''
tagPichau = ''

for item in todos_kabum :
    tagKabum = item['tag_campanha']
    inserirnobanco(item, produtos)

for item in todos_pichau :
    tagPichau = item['tag_campanha']
    inserirnobanco(item, produtos)

todos_produtos = produtos.find()

for item in todos_produtos:

    if item['kabum'] != None: 
        if item['kabum']['tag_campanha'] != tagKabum:
            produtos.update_one({'nome' : item['name']}, {'$set': {"kabum" : None}})

    if item['pichau'] != None:
        if item['pichau']['tag_campanha'] != tagPichau:
            produtos.update_one({'nome' : item['name']}, {'$set': {"pichau" : None}})


    if item['kabum'] == None and item['pichau'] == None:
        produtos.deleteOne({{'nome' : item['name']}})
