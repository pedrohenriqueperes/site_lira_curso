from flask import render_template, request, redirect, flash, url_for, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image






@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
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
    foto_perfil = url_for('static', filename= 'fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com sucesso!!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)


# def salvar_imagem(imagem):
#     #adicionar um codigo aleatorio no nome da imagem
#     codigo = secrets.token_hex(8)
#     nome, extensao = os.path.splitext(imagem.filename)
#     nome_arquivo = nome + "_" + codigo + extensao
#     caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
#     #reduzir o tamanho da imagem
#     tamanho = (200, 200)
#     imagem_reduzida = Image.open(imagem)
#     imagem_reduzida.thumbnail(tamanho)
#     #salvar a imagem na pasta fotos_perfil
#     imagem_reduzida.save(caminho_completo)
#     return nome_arquivo

def salvar_imagem(imagem):
    try:
        # Adicionar um código aleatório no nome da imagem
        codigo = secrets.token_hex(8)
        nome, extensao = os.path.splitext(imagem.filename)
        nome_arquivo = nome + "_" + codigo + extensao
        caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
        
        # Certificar-se de que o diretório de destino existe
        if not os.path.exists(os.path.join(app.root_path, 'static/fotos_perfil')):
            os.makedirs(os.path.join(app.root_path, 'static/fotos_perfil'))
        
        # Reduzir o tamanho da imagem
        tamanho = (200, 200)
        imagem_reduzida = Image.open(imagem)
        imagem_reduzida.thumbnail(tamanho)
        
        # Converter a imagem para RGB se necessário
        if imagem_reduzida.mode in ("RGBA", "P"):
            imagem_reduzida = imagem_reduzida.convert("RGB")
        
        # Salvar a imagem na pasta fotos_perfil
        imagem_reduzida.save(caminho_completo)
        return nome_arquivo
    except Exception as e:
        print(f"Ocorreu um erro ao salvar a imagem: {e}")
        return None


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_'in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)        
            

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data 
        if form.foto_perfil.data:
            #mudar o campo foto_perfil do usuario para o novo nome da imagem
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos =  atualizar_cursos(form)  
            
        database.session.commit()
        flash('Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename= 'fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = None
    if current_user.is_authenticated and current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash("Post Atualizado com Sucesso!", "alert-success")
            return redirect(url_for('home'))
    return render_template('post.html', post=post, form=form)




@app.route('/post/<int:post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluido com sucesso!', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)
        