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

#auth = firebase.auth()
db = firebase.database()
#storage = firebase.storage()

#Autenticação com Email e Senha
#Login
#email = input("Entrar o seu e-mail: ")
#senha = input("Digite a sua senha: ")
#auth.sign_in_with_email_and_password(email, senha)
#auth.create_user_with_email_and_password(email, senha)
print(db.child('events').get())