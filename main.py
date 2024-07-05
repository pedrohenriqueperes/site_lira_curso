from flask import Flask, render_template, url_for
from forms import *


app = Flask(__name__)


app.config['SECRET_KEY'] = 'c70d27fa2912b9b0dda5cd10b19c0cc1'

lista_usuarios = ['Lira', 'John', 'Pereira', 'Sogra']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login')
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)

if __name__ == '__main__':
    app.run(debug=True)