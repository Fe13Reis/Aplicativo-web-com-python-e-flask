import sqlite3
from flask import Flask, render_template, redirect, request, session, flash, \
url_for
from werkzeug.exceptions import abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


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

#recuperar todos os eventos do firebase
#events = db.child('events').order_by_child('date').get()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agenda')
def agenda():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('login')))
    #return render_template('agenda.html', email = session['usuario_logado'], events = events)
    return render_template('agenda.html', email = session['usuario_logado'], events = events)

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
          flash('Email e/ou senha inválidos, tente novamente')
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

'''
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
'''
#Gravar um agendamento
@app.route('/agendar-espaco', methods=('GET', 'POST'))
def agendarEspaco():
    if request.method == 'POST':
        title = request.form['data']
        content = request.form['espaco']

        if not title:
            flash('Escolhe a data, por favor!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('agenda'))

    return render_template('agenda.html')

#Recuperar todos os agendamentos
@app.route('/dataMarcada')
def dataMarcada():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('datas-marcadas.html',  posts=posts)

#Possibilitar acessar a um registro (post)
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

#Acessar a um registro (post) para editar   
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('A data é obligatória!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('dataMarcada'))

    return render_template('edit.html', post=post)

#Deletar um agendamento
@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" O agendamento foi deletado!'.format(post['title']))
    return redirect(url_for('dataMarcada'))

@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/visitantes')
def visitantes():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('login')))
    #return render_template('agenda.html', email = session['usuario_logado'], events = events)
    return render_template('visitantes.html')


app.run(debug=True)