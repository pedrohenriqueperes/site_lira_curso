from flask import render_template, request, redirect, flash, url_for
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta
from comunidadeimpressionadora.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required

lista_usuarios = ['Lira', 'John', 'Pereira', 'Sogra']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario:
            print("Usuário encontrado")
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            print("Senha correta")
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no email: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            print("Falha no login, email ou senha incorretos")
            flash('Falha no login, email ou senha incorretos!', 'alert-danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()

        flash(f'Conta criada com sucesso no email: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout Feito com Sucesso!', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('criarpost.html')
