from flask import Flask, render_template, redirect, request, session, flash, \
url_for
app = Flask(__name__)
app.secret_key = 'alura'

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha


usuario1 = Usuario('fernando@gmail.com', 'Fernando', '1234')
usuario2 = Usuario('winzor@gmail.com', 'Winzor', '5678')
usuario3 = Usuario('thiago@gmail.com', 'Tiago', '9101')

usuarios = {usuario1.id: usuario1,
            usuario2.id: usuario2,
            usuario3.id: usuario3}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agenda')
def agenda():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('agenda')))
    return render_template('agenda.html')

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['e-mail'] in usuarios:
        usuario = usuarios[request.form['e-mail']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(url_for('agenda'))
        else:
          flash('Não logado, tente novamente')
          return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

app.run(debug=True)

