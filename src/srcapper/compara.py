from pymongo import MongoClient
from banco import Banco

banco_de_dados = Banco.inicia_banco()
kabum = Banco.kabum(banco_de_dados)
pichau = Banco.pichau(banco_de_dados)
produtos = Banco.produtos(banco_de_dados)

todos_kabum = kabum.find()
todos_pichau = pichau.find()

iguais = []


for kabum in todos_kabum:
    for pichau in todos_pichau:
        kabum_name = Banco.convertenome(kabum['name'])
        pichua_name = Banco.convertenome(pichau['name'])
        if kabum_name == pichua_name:
            iguais.append(kabum_name)

print(str(iguais))