from flask import Flask, render_template, request, redirect, session, flash, url_for
from pymongo import MongoClient
from banco import Banco

bancoflask = Banco.inicia_banco()
kabum = Banco.kabum(bancoflask)
pichau = Banco.kabum(bancoflask)
usuarios = Banco.usuarios(bancoflask)

app = Flask(__name__)
app.secret_key = 'promohunter'

@app.route('/')
def home():
    logado = 'false'
    try:
        if session['usuario_logado'] != None:
            logado = 'true'
            return render_template('home.html', titulo='Promo Hunter', resultados = kabum.find().limit(8), logado = logado)
        else:
            session['usuario_logado'] = None
            return render_template('home.html', titulo='Promo Hunter', resultados = kabum.find().limit(8), logado = logado)
    except:
        session['usuario_logado'] = None
        return render_template('home.html', titulo='Promo Hunter', resultados = kabum.find().limit(8), logado = logado)

@app.route('/registrar')
def registrar():
#    if session['usuario_logado'] != None:
#        return redirect(url_for('home'))
    proxima = request.args.get('proxima')
    return render_template('registrar.html', proxima=proxima)

@app.route('/registra', methods= ['POST', ])
def registra():
    if usuarios.find_one({'nickname': request.form.get('nickname')}) != None:
        flash('Usuario registrado')
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            nome = request.form.get('nome')
            nickname = request.form.get('nickname')
            email = request.form.get('email')
            senha = request.form.get('senha')
            usuarios.insert_one({ 'nome' : nome, 'nickname' : nickname , 'email' : email , 'senha' : senha})
            session['usuario_logado'] = nickname
            flash(str(nickname) + ' logado com sucesso!')
            proxima_pagina = request.form.get('proxima')
            if proxima_pagina == 'None':
                proxima_pagina = "/"
            return redirect(proxima_pagina)      

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if usuarios.find_one({"nickname": request.form['usuario']}) != None:
        usuario = usuarios.find_one({"nickname": request.form['usuario']})
        if request.form['senha'] == usuario.get('senha'):
            session['usuario_logado'] = usuario.get('nickname')
            flash(usuario.get('nickname') + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            if proxima_pagina == 'None':
                proxima_pagina = "/"
            return redirect(proxima_pagina)
        else:
            flash('senha incorreta')
            return redirect(url_for('login'))
    else:
        flash('Nickname não encontrado')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('home'))

@app.route('/perfil')
def perfil():
    return render_template('perfil.html', usuarios = usuarios.find())

@app.route('/procura')
def procura():
    return render_template('procura.html', titulo='Titulo')

@app.route('/resultado', methods = ['POST', ])
def resultado():
    item = request.form.get('nome')
    resultado1 = kabum.find({"$text": {"$search": item}})
    resultado2 = pichau.find({"$text": {"$search": item}})
    return render_template('resultado.html', titulo='Resultado da Busca',  resultados = kabum.find({"$text": {"$search": item}}))

app.run(debug=True)