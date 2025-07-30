# forms/auth_forms.py - Formulários para autenticação
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models.usuario import Usuario

class LoginForm(FlaskForm):
    """Formulário de login"""
    nome_usuario = StringField('Nome de Usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class RegistroForm(FlaskForm):
    """Formulário de registro de novo usuário"""
    nome_usuario = StringField(
        'Nome de Usuário', 
        validators=[DataRequired(), Length(min=4, max=20)]
    )
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email()]
    )
    senha = PasswordField(
        'Senha', 
        validators=[DataRequired(), Length(min=6)]
    )
    confirmar_senha = PasswordField(
        'Confirmar Senha', 
        validators=[DataRequired(), EqualTo('senha')]
    )
    submit = SubmitField('Registrar')
    
    def validate_nome_usuario(self, nome_usuario):
        """Valida se o nome de usuário já existe"""
        usuario = Usuario.query.filter_by(nome_usuario=nome_usuario.data).first()
        if usuario:
            raise ValidationError('Este nome de usuário já está em uso. Escolha outro.')
    
    def validate_email(self, email):
        """Valida se o email já está registrado"""
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este email já está registrado. Use outro email.')