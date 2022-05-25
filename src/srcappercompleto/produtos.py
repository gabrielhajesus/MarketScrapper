from pymongo import MongoClient
from banco import Banco

banco_de_dados = Banco.inicia_banco()
kabum = Banco.kabum(banco_de_dados)
pichau = Banco.pichau(banco_de_dados)


todos_kabum = kabum.find()
nomes_kabum = []
for item in todos_kabum:
    nome = item.get('name')
    nome = nome.replace(',',' ')
    nome = nome.replace('-',' ')
    nome = nome.replace(' ','_').lower()
    nomes_kabum.append(nome)
with open("nomes_kabum.txt", "w", encoding= "utf-8") as arquivo:
    arquivo.write(str(nomes_kabum))


todos_pichau = pichau.find()
nomes_pichau = []
for item in todos_pichau:
    nome = item.get('name')
    nome = nome.replace(',',' ')
    nome = nome.replace('-',' ')
    nome = nome.replace(' ','_').lower()
    nomes_pichau.append(nome)
with open("nomes_pichau.txt", "w", encoding= "utf-8") as arquivo:
    arquivo.write(str(nomes_pichau))

comparaproduto = []
for itemk in nomes_kabum:
    comparaproduto.append({'qtd' : 1, 'nome': itemk})

with open("nomes_produtos1.txt", "w", encoding= "utf-8") as arquivo:
    arquivo.write(str(comparaproduto))
i= 0
qtd = len(comparaproduto)
print(qtd)
for itemp in nomes_pichau:
    print(i)
    for item in comparaproduto:
        if itemp == item['nome']:
            item['qtd'] = 2
            break
        elif item == comparaproduto[qtd]:
            comparaproduto.append({'qtd': 1, 'nome' : itemp})
    i = i+1

with open("nomes_produtos2.txt", "w", encoding= "utf-8") as arquivo:
    arquivo.write(str(comparaproduto))









"""
for card in cards:
    kabumn = "Memória Corsair Vengeance LPX, 8GB, 2666MHz, DDR4, C16, Preto - CMK8GX4M1A2666C16"
    pichaun = "Memoria Corsair Vengeance LPX 8GB (1x8) DDR4 2666MHz C16 Preta, CMK8GX4M1A2666C16"

    if card['name_card'] == kabumn or card['name_card'] == pichaun:
        produtobanco = produtos.find_one(card['name_card'])
        if produtos.find_one(card['name_card']) != None:
            if produtobanco['menor_preco'] > card['price_card']:
                produtos.update_one({'nome' : card['name_card']}, {'$set': {"menor_preco": card['price_card']}})
            produtos.update_one({'nome' : card['name_card']}, {'$set': {"kabum.preco_kabum": card['price_card' , "kabum.tag_promocao" : 'megamaio']}})  
        else:
            produto = {
                'nome' : card['name_card'],
                'menor_preco' : card['price_card'],
                'categoria' : 'hardware',
                'kabum' :  {'preco_kabum' : card['price_card'] , 'tag_promocao' : '' , 'link_da_promocao' : ''},
                'pichau' : {'preco_pichau' : '' , 'tag_promocao' : '', 'link_da_promocao' : ''}
            }
        produtos.insert_one(produto)
"""