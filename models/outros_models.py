from datetime import datetime
from models.database import db, tarefa_etiqueta

class Lista(db.Model):
    __tablename__ = 'lista'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
    # Colocando um relacionamento com as tarefas
    tarefas = db.relationship('Tarefa', backref='lista', lazy=True)
    
    def __repr__(self):
        return f'<Lista {self.nome}>'

class Etiqueta(db.Model):
    __tablename__ = 'etiqueta'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True, nullable=False)
    
    # Relacionamento de muitos para muitos com tarefas
    tarefas = db.relationship('Tarefa', secondary=tarefa_etiqueta, back_populates='etiquetas')
    
    def __repr__(self):
        return f'<Etiqueta {self.nome}>'



class Tarefa(db.Model):
    __tablename__ = 'tarefa'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    data_limite = db.Column(db.DateTime)
    concluida = db.Column(db.Boolean, default=False)
    prioridade = db.Column(db.String(20), default='Normal')  # Baixa, Normal, Alta, Urgente
    criada_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizada_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Chaves estrangeiras
    lista_id = db.Column(db.Integer, db.ForeignKey('lista.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
    # Relacionamentos 
    etiquetas = db.relationship('Etiqueta', secondary=tarefa_etiqueta, back_populates='tarefas')
    comentarios = db.relationship('Comentario', backref='tarefa', lazy=True)
    
    def __repr__(self):
        return f'<Tarefa {self.titulo}>'




class Comentario(db.Model):
    __tablename__ = 'comentario'
    
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tarefa_id = db.Column(db.Integer, db.ForeignKey('tarefa.id'), nullable=False)
    
    def __repr__(self):
        return f'<Comentario {self.id}>'