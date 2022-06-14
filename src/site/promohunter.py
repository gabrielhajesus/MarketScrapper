from flask import Flask, render_template, request, redirect, session, flash, url_for
from pymongo import MongoClient
from banco import Banco

bancoflask = Banco.inicia_banco()
kabum = Banco.kabum(bancoflask)
pichau = Banco.kabum(bancoflask)
produtos = Banco.produtos(bancoflask)

app = Flask(__name__ , template_folder='./templates/')
app.secret_key = 'promohunter'
app.static_folder='./static/'

@app.route('/')
def home():
    return render_template('home.html', titulo='Promo Hunter', resultados = produtos.find().limit(8))

@app.route('/resultado', methods = ['POST', ])
def resultado():
    filtro = request.form.get('checkbox')
    item = request.form.get('nome')
    if filtro == None or filtro == 'Null':
        resultados = produtos.find({"$text": {"$search": item}})
    else:
        resultados = produtos.find({"categoria": { '$elemMatch' : {'$eq': filtro }}})

    return render_template('resultado.html', titulo='Resultado da Busca',  resultados = resultados)

@app.route('/busca/<resultado_produto>')
def produto(resultado_produto):
    return render_template('produto.html', titulo='Produto',  resultado = produtos.find_one({'search_name':resultado_produto}))

app.run(debug=True, port=5000)