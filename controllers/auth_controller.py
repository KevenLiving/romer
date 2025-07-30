
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.database import db
from models.usuario import Usuario
from forms.auth_forms import LoginForm, RegistroForm


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se o usuário já está logado, redireciona para página principal
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    # Se o formulário foi enviado e é válido
    if form.validate_on_submit():
        # Busca o usuário no banco de dados
        usuario = Usuario.query.filter_by(nome_usuario=form.nome_usuario.data).first()
        
        # Verifica se o usuário existe e a senha está correta
        if usuario and usuario.verificar_senha(form.senha.data):
            # Faz o login do usuário (cria sessão e cookies)
            login_user(usuario, remember=True)
            flash('Login realizado com sucesso!', 'success')
            
            # Redireciona para a página que o usuário tentou acessar antes
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Nome de usuário ou senha incorretos', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página e função de registro de novo usuário"""
    # Se o usuário já está logado, redireciona para página principal
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistroForm()
    
    # Se o formulário foi enviado e é válido
    if form.validate_on_submit():
        # Cria novo usuário
        novo_usuario = Usuario(
            nome_usuario=form.nome_usuario.data,
            email=form.email.data,
            senha=form.senha.data
        )
        
        # Salva no banco de dados
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Conta criada com sucesso! Você pode fazer login agora.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar conta. Tente novamente.', 'error')
    
    return render_template('auth/registro.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Função para fazer logout"""
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('auth.login'))