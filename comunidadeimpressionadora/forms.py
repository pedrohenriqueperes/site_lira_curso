from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer Login')
    

class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    curso_excel = BooleanField('Excel Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_ppt = BooleanField('Apresentações Impressionadoras')
    curso_sql = BooleanField('SQL Impressionador')
    botao_submit_editarperfil = SubmitField('Confirmar Edição')
    
    def validate_email(self, email):
        if current_user.email != email.data: 
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuario com esse e-mail. Cadastre outro e-mail.')
            
            
 
 
 
 
class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[DataRequired(), Length(2, 140)])  
    corpo =  TextAreaField('Escreva seu Post', validators=[DataRequired()])  
    botao_submit = SubmitField('Criar Post')