# forms/task_forms.py - Formulários para tarefas
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length
from models.outros_models import Lista
from flask_login import current_user

class EditarTarefaForm(FlaskForm):
    """Formulário para editar tarefa"""
    titulo = StringField(
        'Título da Tarefa', 
        validators=[DataRequired(), Length(min=1, max=200)]
    )
    descricao = TextAreaField(
        'Descrição',
        validators=[Length(max=500)]
    )
    lista_id = SelectField(
        'Lista', 
        validators=[DataRequired()],
        coerce=int
    )
    prioridade = SelectField(
        'Prioridade',
        choices=[
            ('Baixa', 'Baixa'),
            ('Normal', 'Normal'),
            ('Alta', 'Alta'),
            ('Urgente', 'Urgente')
        ],
        default='Normal'
    )
    data_limite = DateField(
        'Data Limite',
        validators=[]
    )
    submit = SubmitField('Salvar Alterações')
    
    def __init__(self, *args, **kwargs):
        super(EditarTarefaForm, self).__init__(*args, **kwargs)
        # Carrega as listas do usuário atual para o campo select
        if current_user.is_authenticated:
            self.lista_id.choices = [
                (lista.id, lista.nome) 
                for lista in Lista.query.filter_by(usuario_id=current_user.id).all()
            ]