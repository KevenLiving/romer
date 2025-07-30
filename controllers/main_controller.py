from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.database import db
from models.outros_models import Lista, Tarefa


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@login_required
def index():
    # Busca as listas e tarefas do usuário atual
    listas = Lista.query.filter_by(usuario_id=current_user.id).all()
    tarefas_recentes = Tarefa.query.filter_by(usuario_id=current_user.id).order_by(Tarefa.criada_em.desc()).limit(5).all()
    
    # Conta algumas estatísticas básicas
    total_tarefas = Tarefa.query.filter_by(usuario_id=current_user.id).count()
    tarefas_concluidas = Tarefa.query.filter_by(usuario_id=current_user.id, concluida=True).count()
    tarefas_pendentes = total_tarefas - tarefas_concluidas
    
    return render_template('main/dashboard.html', 
                         listas=listas, 
                         tarefas_recentes=tarefas_recentes,
                         total_tarefas=total_tarefas,
                         tarefas_concluidas=tarefas_concluidas,
                         tarefas_pendentes=tarefas_pendentes)



@main_bp.route('/listas')
@login_required
def listas():
    """Página para gerenciar listas"""
    listas_usuario = Lista.query.filter_by(usuario_id=current_user.id).all()
    return render_template('main/listas.html', listas=listas_usuario)


@main_bp.route('/nova-lista', methods=['POST'])
@login_required
def nova_lista():
    nome_lista = request.form.get('nome')
    
    if nome_lista:
        nova_lista = Lista(nome=nome_lista, usuario_id=current_user.id)
        try:
            db.session.add(nova_lista)
            db.session.commit()
            flash('Lista criada com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar lista.', 'error')
    else:
        flash('Nome da lista é obrigatório.', 'error')
    
    return redirect(url_for('main.listas'))




@main_bp.route('/tarefa/<int:tarefa_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_tarefa(tarefa_id):
    from forms.task_forms import EditarTarefaForm
    from datetime import datetime
    
    # Busca a tarefa do usuário atual
    tarefa = Tarefa.query.filter_by(id=tarefa_id, usuario_id=current_user.id).first()
    
    if not tarefa:
        flash('Tarefa não encontrada.', 'error')
        return redirect(url_for('main.tarefas'))
    
    form = EditarTarefaForm()
    
    if form.validate_on_submit():
        # Atualiza os dados da tarefa
        tarefa.titulo = form.titulo.data
        tarefa.descricao = form.descricao.data
        tarefa.lista_id = form.lista_id.data
        tarefa.prioridade = form.prioridade.data
        tarefa.data_limite = form.data_limite.data
        tarefa.atualizada_em = datetime.utcnow()
        
        try:
            db.session.commit()
            flash(f'Tarefa "{tarefa.titulo}" foi atualizada com sucesso!', 'success')
            return redirect(url_for('main.tarefas'))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar tarefa.', 'error')
    
    # Preenche o formulário com os dados atuais da tarefa
    elif request.method == 'GET':
        form.titulo.data = tarefa.titulo
        form.descricao.data = tarefa.descricao
        form.lista_id.data = tarefa.lista_id
        form.prioridade.data = tarefa.prioridade
        form.data_limite.data = tarefa.data_limite
    
    return render_template('main/editar_tarefa.html', form=form, tarefa=tarefa)

@main_bp.route('/lista/<int:lista_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_lista(lista_id):
    lista = Lista.query.filter_by(id=lista_id, usuario_id=current_user.id).first()
    
    if not lista:
        flash('Lista não encontrada.', 'error')
        return redirect(url_for('main.listas'))
    
    if request.method == 'POST':
        novo_nome = request.form.get('nome')
        if novo_nome:
            lista.nome = novo_nome
            try:
                db.session.commit()
                flash(f'Lista renomeada para "{novo_nome}" com sucesso!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Erro ao renomear lista.', 'error')
        else:
            flash('Nome da lista é obrigatório.', 'error')
    
    return redirect(url_for('main.listas'))

@main_bp.route('/tarefas')
@login_required
def tarefas():
    tarefas_usuario = Tarefa.query.filter_by(usuario_id=current_user.id).all()
    listas_usuario = Lista.query.filter_by(usuario_id=current_user.id).all()
    return render_template('main/tarefas.html', tarefas=tarefas_usuario, listas=listas_usuario)

@main_bp.route('/nova-tarefa', methods=['POST'])
@login_required
def nova_tarefa():
    from flask import request
    from datetime import datetime

    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao', '')
    lista_id = request.form.get('lista_id')
    prioridade = request.form.get('prioridade', 'Normal')
    data_limite_str = request.form.get('data_limite')

    # Converte a data limite se fornecida
    data_limite = None
    if data_limite_str:
        try:
            data_limite = datetime.strptime(data_limite_str, '%Y-%m-%d')
        except ValueError:
            flash('Formato de data inválido.', 'error')
            return redirect(url_for('main.tarefas'))

    if titulo and lista_id:
        nova_tarefa = Tarefa(
            titulo=titulo,
            descricao=descricao,
            data_limite=data_limite,
            prioridade=prioridade,
            lista_id=lista_id,
            usuario_id=current_user.id
        )

        try:
            db.session.add(nova_tarefa)
            db.session.commit()
            flash('Tarefa criada com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar tarefa.', 'error')
    else:
        flash('Título e lista são obrigatórios.', 'error')

    return redirect(url_for('main.tarefas'))


@main_bp.route('/tarefa/<int:tarefa_id>/concluir', methods=['POST'])
@login_required
def concluir_tarefa(tarefa_id):
    tarefa = Tarefa.query.filter_by(id=tarefa_id, usuario_id=current_user.id).first()
    
    if tarefa:
        # Alterna o status de conclusão
        tarefa.concluida = not tarefa.concluida
        try:
            db.session.commit()
            status = 'concluída' if tarefa.concluida else 'reaberta'
            flash(f'Tarefa "{tarefa.titulo}" foi {status}!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar tarefa.', 'error')
    else:
        flash('Tarefa não encontrada.', 'error')
    
    # Redireciona para a página de origem
    return redirect(request.referrer or url_for('main.tarefas'))

@main_bp.route('/tarefa/<int:tarefa_id>/excluir', methods=['POST'])
@login_required
def excluir_tarefa(tarefa_id):
    tarefa = Tarefa.query.filter_by(id=tarefa_id, usuario_id=current_user.id).first()
    
    if tarefa:
        titulo_tarefa = tarefa.titulo
        try:
            db.session.delete(tarefa)
            db.session.commit()
            flash(f'Tarefa "{titulo_tarefa}" foi excluída!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Erro ao excluir tarefa.', 'error')
    else:
        flash('Tarefa não encontrada.', 'error')
    
    # Redireciona para a página de origem
    return redirect(request.referrer or url_for('main.tarefas'))

@main_bp.route('/lista/<int:lista_id>/excluir', methods=['POST'])
@login_required
def excluir_lista(lista_id):
    lista = Lista.query.filter_by(id=lista_id, usuario_id=current_user.id).first()
    
    if lista:
        nome_lista = lista.nome
        try:
            # Primeiro exclui todas as tarefas da lista
            Tarefa.query.filter_by(lista_id=lista_id).delete()
            # Depois exclui a lista
            db.session.delete(lista)
            db.session.commit()
            flash(f'Lista "{nome_lista}" e todas suas tarefas foram excluídas!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Erro ao excluir lista.', 'error')
    else:
        flash('Lista não encontrada.', 'error')
    
    return redirect(url_for('main.listas'))
    
    if titulo and lista_id:
        nova_tarefa = Tarefa(
            titulo=titulo,
            descricao=descricao,
            data_limite=data_limite,
            prioridade=prioridade,
            lista_id=lista_id,
            usuario_id=current_user.id
        )
        
        try:
            db.session.add(nova_tarefa)
            db.session.commit()
            flash('Tarefa criada com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Erro ao criar tarefa.', 'error')
    else:
        flash('Título e lista são obrigatórios.', 'error')
    
    return redirect(url_for('main.tarefas'))