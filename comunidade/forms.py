from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired,length,email,EqualTo, ValidationError
from comunidade.models import Usuario
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed




class formCriarConta(FlaskForm):
    username= StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), email()])
    senha = PasswordField('Senha', validators=[DataRequired(), length(6, 20)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    submit_criarconta = SubmitField('Criar Conta')
    
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado. Cadastre-se com outro email, ou faça Login para continuar.')


class formLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), email()])
    senha = PasswordField('Senha', validators=[DataRequired(), length(6, 20)])
    submit_login = SubmitField('Entrar')
    lembrar_dados = BooleanField('esqueci meus dados')

class formEditarConta(FlaskForm):
    username= StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), email()])
    time_futebol = SelectField('Time de Futebol', validators=[DataRequired()], choices=[
    ('atletico_mineiro', 'Atlético Mineiro'),
    ('avai', 'Avaí'),
    ('bahia', 'Bahia'),
    ('botafogo', 'Botafogo'),
    ('botafogo_sp', 'Botafogo-SP'),
    ('brasil_de_pelotas', 'Brasil de Pelotas'),
    ('brusque', 'Brusque'),
    ('ceara', 'Ceará'),
    ('chapecoense', 'Chapecoense'),
    ('confianca', 'Confiança'),
    ('corinthians', 'Corinthians'),
    ('coritiba', 'Coritiba'),
    ('cruzeiro', 'Cruzeiro'),
    ('csa', 'CSA'),
    ('cuiaba', 'Cuiabá'),
    ('flamengo', 'Flamengo'),
    ('fluminense', 'Fluminense'),
    ('fortaleza', 'Fortaleza'),
    ('figueirense', 'Figueirense'),
    ('gremio', 'Grêmio'),
    ('goias', 'Goiás'),
    ('guarani', 'Guarani'),
    ('internacional', 'Internacional'),
    ('juventude', 'Juventude'),
    ('mirassol', 'Mirassol'),
    ('nautico', 'Náutico'),
    ('novorizontino', 'Novorizontino'),
    ('operario', 'Operário'),
    ('palmeiras', 'Palmeiras'),
    ('parana', 'Paraná'),
    ('ponte_preta', 'Ponte Preta'),
    ('remo', 'Remo'),
    ('sampaio_correa', 'Sampaio Corrêa'),
    ('santos', 'Santos'),
    ('sao_paulo', 'São Paulo'),
    ('sport', 'Sport'),
    ('vasco', 'Vasco da Gama'),
    ('vitoria', 'Vitória'),
    ('ypiranga', 'Ypiranga'),
])
    foto_perfil = FileField('Atualizar perfil', validators=[FileAllowed(['jpg', 'png'])])
    submit_editarperfil = SubmitField('Confirmar Conta')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('já existe usuario com esse email')

class formCriarPost(FlaskForm):
    titulo = StringField('Titulo do post', validators=[DataRequired(), length(2, 150)])
    corpo = TextAreaField('Escreva seu Post', validators=[DataRequired()])
    submit_criarpost = SubmitField('Criar Post')
    