from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user

class FormCadastro(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(25)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha= PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirme', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_cadastro = SubmitField('Criar Conta')

    #se quiser fazer o username ser único, criar outra função dessa com validade_username
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar.')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembre-me')
    botao_submit_login = SubmitField('Fazer Login')



class FormEditarPerfil(FlaskForm):
    username = StringField('User:   ', validators=[DataRequired()])
    email = StringField('E-mail: ', validators=[DataRequired(), Email()])
    bio = StringField('Bio:   ', validators=[DataRequired()])
    foto_perfil = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg']),'ERRO!'])
    botao_submit_editarperfil = SubmitField('CONFIRMAR EDIÇÃO')


def validate_email(self, email):
    if current_user.email != email.data:
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Já existe um usuário com esse e-mail.')
