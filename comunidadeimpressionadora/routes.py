from flask import render_template, redirect, url_for, flash, request
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.forms import FormCadastro, FormLogin, FormEditarPerfil
from comunidadeimpressionadora.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required

lista_usuarios = ['Marcos', 'Evilly', 'Andressa', 'Caio']


@app.route('/') # url da página principal
def home():
    return render_template('home.html')



@app.route('/contato') # url da página contato
def contato():
    return render_template('contato.html')



@app.route('/usuarios')
@login_required
def usuarios():

    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:           #se tiver 2 form na mesma pagina: importa request e cod: if form_login.validate_on_submit() and 'botao_submit_login' in request.form:  #ver o nome do id do botao no inspecionar da pag
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            parametro_next = request.args.get('next')
            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login. E-mail ou senha incorretos.', 'alert-danger')
    return render_template('login.html', form_login=form_login)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form_cadastro = FormCadastro()

    if form_cadastro.validate_on_submit() and 'botao_submit_cadastro' in request.form:
        #criar conta
        senha_crypt = bcrypt.generate_password_hash(form_cadastro.senha.data)
        usuario = Usuario(username=form_cadastro.username.data, email=form_cadastro.email.data, senha=senha_crypt)
        #adicionar a sessão
        database.session.add(usuario)
        #commit na sessão
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_cadastro.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('cadastro.html', form_cadastro=form_cadastro)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso.', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('criarpost.html')


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        bio = form.bio.data
        database.session.commit()
        flash(f'Perfil atualizado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)



