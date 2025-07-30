
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import db

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome_usuario = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    
    # Relacionamentos :)
    listas = db.relationship('Lista', backref='dono', lazy=True)
    tarefas = db.relationship('Tarefa', backref='usuario', lazy=True)
    comentarios = db.relationship('Comentario', backref='usuario', lazy=True)
    
    def __init__(self, nome_usuario, email, senha):
        """Construtor da classe Usuario"""
        self.nome_usuario = nome_usuario
        self.email = email
        self.definir_senha(senha)

# Codificando a senha    
    def definir_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

# Verificando se a senha está correta 
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)
    
    def __repr__(self):
        return f'<Usuario {self.nome_usuario}>'