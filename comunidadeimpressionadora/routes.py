from flask import render_template, redirect, url_for, flash, request, abort
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormCadastro, FormLogin, FormEditarPerfil, FormCriarPost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image



@app.route('/') # url da página principal
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)



@app.route('/contato') # url da página contato
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

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:           #se tiver 2 form na mesma pagina: importa request e cod: if form_login.validate_on_submit() and 'botao_submit_login' in request.form:  #ver o nome do id do botao no inspecionar da pag
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode('utf-8'), form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Successfully login on email:  {form_login.email.data}', 'alert-success')
            parametro_next = request.args.get('next')
            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Login Failed: Your e-mail or password is incorrect', 'alert-danger')
    return render_template('login.html', form_login=form_login)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form_cadastro = FormCadastro()

    if form_cadastro.validate_on_submit() and 'botao_submit_cadastro' in request.form:
        #criar conta
        senha_cript = bcrypt.generate_password_hash(form_cadastro.senha.data).decode('utf-8')
        usuario = Usuario(username=form_cadastro.username.data, email=form_cadastro.email.data, senha=senha_cript)
        #adicionar a sessão
        database.session.add(usuario)
        #commit na sessão
        database.session.commit()
        flash(f'Account created successfully on email: {form_cadastro.email.data}', 'alert-success')
        usuario = Usuario.query.filter_by(email=form_cadastro.email.data).first()
        return redirect(url_for('home'))


    return render_template('cadastro.html', form_cadastro=form_cadastro)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'You have successfully logged out.', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)



@app.route('/post/criar', methods=['GET','POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post successfully created!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)



def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso' in campo.name:
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
            nome_imagem = salvar_imagem((form.foto_perfil.data))
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash(f'Profile successfully updated!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)



@app.route('/post/<post_id>', methods=['GET','POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post successfully updated!','alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)


@app.route('/post/<post_id>/excluir', methods=['GET','POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post successfully deleted.', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)
