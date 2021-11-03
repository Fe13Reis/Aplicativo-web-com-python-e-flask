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
db = firebase.database();

app = Flask(__name__)
app.secret_key = 'alura'

events = [
    {
        'todo' : 'Casa Cintia - Churrasco', 
        'date' : '2021-11-02',
    },
    {
        'todo' : 'Casa Eric - Cerveja', 
        'date' : '2021-11-10',
    },
    {
        'todo' : 'Casa Bruno - Piscina', 
        'date' : '2021-11-15',
    },
    {
        'todo' : 'Dia de Piscina', 
        'date' : '2021-11-20',
    }
]

#events = db.child('events').get()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/churras')
def churras():
    return render_template('agenda-churras.html', events = events)

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

#data={'name' : 'Teste', 'numero':123, 'lgpd': True}
#db.push(data)
@app.route('/agendar-espaco', methods=['POST', 'GET'])
def agendarEspaco():
    if request.method == 'POST':
        data = request.form.get('data')
        espaco = request.form.get('espaco')
        dataEvent={'date' : data, 'todo': espaco}
        try:
            db.child('events').push(dataEvent)
            flash('Agendado com sucesso')
            return redirect(url_for('churras'))
        except:
          flash('Falha no Agendamento, tente novamente!')
          return redirect(url_for('churras'))
#print(db.child('events').get())
app.run(debug=True)