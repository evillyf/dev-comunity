from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user



class FormCadastro(FlaskForm):
    username = StringField('Username', validators=[DataRequired(25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha= PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirme Password', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_cadastro = SubmitField('Create account')

    #se quiser fazer o username ser único, criar outra função dessa com validade_username
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Remember-me')
    botao_submit_login = SubmitField('Login')



class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])

    curso_javascrip = BooleanField('CURSO JAVASCRIPT')
    curso_python = BooleanField('CURSO PYHTON')
    curso_sql = BooleanField('CURSO SQL')
    curso_powerbi = BooleanField('CURSO PB')
    curso_html = BooleanField('CURSO HTML')
    curso_php = BooleanField('CURSO PHP')


    botao_submit_editarperfil = SubmitField('Confirmar Edição')


def validate_email(self, email):
    if current_user.email != email.data:
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Já existe um usuário com esse e-mail.')



class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')