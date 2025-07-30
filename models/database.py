from flask_sqlalchemy import SQLAlchemy

# Conectando a aplicação ao banco de dados
db = SQLAlchemy()



# Relação de muitos para muitos entre Tarefa e Etiqueta
tarefa_etiqueta = db.Table(
    'tarefa_etiqueta',
    db.Column('tarefa_id', db.Integer, db.ForeignKey('tarefa.id'), primary_key=True),
    db.Column('etiqueta_id', db.Integer, db.ForeignKey('etiqueta.id'), primary_key=True)
)