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
    confirmacao_senha = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_cadastro = SubmitField('Create account')

    #se quiser fazer o username ser único, criar outra função dessa com validade_username
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('An account is already registered with this email address.')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Remember-me')
    botao_submit_login = SubmitField('Login')



class FormEditarPerfil(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])

    curso_javascrip = BooleanField('JAVASCRIPT')
    curso_python = BooleanField('PYTHON')
    curso_sql = BooleanField('SQL')
    curso_powerbi = BooleanField('C++')
    curso_html = BooleanField('HTML E CSS')
    curso_php = BooleanField('PHP')


    botao_submit_editarperfil = SubmitField('Confirm edit')


def validate_email(self, email):
    if current_user.email != email.data:
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('An account with this email already exists.')



class FormCriarPost(FlaskForm):
    titulo = StringField('Post title', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Type your post here', validators=[DataRequired()])
    botao_submit = SubmitField('Create Post')