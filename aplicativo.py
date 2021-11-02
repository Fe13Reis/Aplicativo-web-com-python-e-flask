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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/churras')
def churras():
    return render_template('agenda-churras.html')

@app.route('/piscina')
def piscina():
    return render_template('agenda-piscina.html')

@app.route('/salao')
def salao():
    return render_template('agenda-salao.html')

@app.route('/agenda')
def agenda():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('agenda')))
    return render_template('agenda.html', email = session['usuario_logado'])

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', 'GET'])
def autenticar():
    if request.method == 'POST':
        email = request.form.get('e-mail')
        senha = request.form.get('senha')
        try:
            auth.sign_in_with_email_and_password(email, senha)
            session['usuario_logado'] = email
            flash('Bem vinv@: '+ email + '!')
            proxima_pagina = request.form['proxima']
            return redirect(url_for('agenda'))
        except:
          flash('Email e/ou senha, tente novamente')
          return redirect(url_for('login'))

@app.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar():
    if request.method == 'POST':
        email = request.form.get('e-mail')
        senha = request.form.get('senha')
        try:
            auth.create_user_with_email_and_password(email, senha)
            session['usuario_logado'] = email
            flash('Bem vinv@: '+ email + '!')
            proxima_pagina = request.form['proxima']
            return redirect(url_for('agenda'))
        except:
          flash('Erro no Cadastro, tente novamente')
          return redirect(url_for('cadastro'))
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

app.run(debug=True)