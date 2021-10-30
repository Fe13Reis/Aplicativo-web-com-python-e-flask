from flask import Flask, render_template, redirect, request, session, flash, \
url_for


import pyrebase

firebaseConfig = {
  'apiKey': "AIzaSyAtmOiQQWMkSWMrpx5oafa5crw8yD7BaBk",
  'authDomain': "pji110-sa-g002.firebaseapp.com",
  'projectId': "pji110-sa-g002",
  'storageBucket': "pji110-sa-g002.appspot.com",
  'messagingSenderId': "758005852528",
  'appId': "1:758005852528:web:f491f93e6bec2ddf3f87b5",
  'measurementId': "G-J41KXNEZFL",
  'databaseURL': "https://pji110-sa-g002-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

app = Flask(__name__)
app.secret_key = 'alura'
'''
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
'''
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

    '''
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
    '''
    if request.method == 'POST':
        email = request.form.get('e-mail')
        senha = request.form.get('senha')
        try:
            auth.sign_in_with_email_and_password(email, senha)
            flash(email + ' logou com sucesso!')
            #proxima_pagina = request.form['proxima']
            return redirect(url_for('agenda'))
        except:
          flash('Não logado, tente novamente')
          return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

app.run(debug=True)