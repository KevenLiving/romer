# app.py - Arquivo principal da aplicação Flask
from flask import Flask
from flask_login import LoginManager
from models.database import db
from models.usuario import Usuario
from controllers.auth_controller import auth_bp
from controllers.main_controller import main_bp

def create_app():
    # Criando a aplicação Flask
    app = Flask(__name__)
    
    # Configurações básicas da aplicação
    app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'  # Mude isso para produção
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_app.db'  # Banco SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializando extensões
    db.init_app(app)
    
    # Configurando Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Página de login
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    
    # Função para carregar usuário (necessária para Flask-Login)
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    # Registrando blueprints (controllers)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    # Criando tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    return app

# Rodando a aplicação
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)  # debug=True apenas para desenvolvimento