# models/database.py - Configuração do banco de dados
from flask_sqlalchemy import SQLAlchemy

# Criando instância do SQLAlchemy
db = SQLAlchemy()

# Tabela de associação many-to-many entre Tarefa e Etiqueta
tarefa_etiqueta = db.Table(
    'tarefa_etiqueta',
    db.Column('tarefa_id', db.Integer, db.ForeignKey('tarefa.id'), primary_key=True),
    db.Column('etiqueta_id', db.Integer, db.ForeignKey('etiqueta.id'), primary_key=True)
)