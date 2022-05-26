from pymongo import MongoClient

class Banco:
    def inicia_banco():
        client = MongoClient('localhost', 27017)
        db = client.sites
        return db
    
    def kabum(db):
        kabum = db.kabum2
        return kabum
    
    def pichau(db):
        pichau = db.pichau2
        return pichau

    def produtos(db):
        produtos = db.produtos
        return produtos
    
    def usuarios(db):

        usuarios = db.usuarios
        return usuarios
    
    def convertenome(nome):
        nome = nome.replace(',','').replace('-','').replace(' ','').replace('(', '').replace(')','').replace('.','').lower()
        return nome