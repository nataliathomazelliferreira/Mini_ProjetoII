from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, text
from datetime import datetime
import time
from functools import wraps


def medir_tempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()
        duracao = fim - inicio
        print(f"Função '{func.__name__}' executada em {duracao:.6f} segundos.")
        return resultado
    return wrapper


engine = create_engine("postgresql+psycopg2://alunos:AlunoFatec@200.19.224.150:5432/atividade2", echo=False)
metadata = MetaData()

usuarios = Table(
    'usuarios', metadata,
    Column('id', Integer, primary_key=True),
    Column('nome', String(50), nullable=False, index=True),
    Column('cpf', String(14), nullable=False),
    Column('email', String(100), nullable=False, unique=True),
    Column('telefone', String(20), nullable=False),
    Column('data_nascimento', Date, nullable=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)

metadata.create_all(engine)


def anonimizar_nome(nome):
    partes = nome.split()
    return ' '.join(p[0] + '*' * (len(p) - 1) for p in partes)


def anonimizar_cpf(cpf):
    return cpf[:4] + '*' * (len(cpf) - 4)


def anonimizar_email(email):
    usuario, dominio = email.split('@')
    return usuario[0] + '*' * (len(usuario) - 1) + '@' + dominio


def anonimizar_telefone(telefone):
    digitos = ''.join(filter(str.isdigit, telefone))
    return digitos[-4:]


@medir_tempo
def LGPD(row):
    id_, nome, cpf, email, telefone, data_nascimento, created_on, updated_on = row
    return (
        id_,
        anonimizar_nome(nome),
        anonimizar_cpf(cpf),
        anonimizar_email(email),
        anonimizar_telefone(telefone),
        data_nascimento,
        created_on,
        updated_on
    )

users = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios LIMIT 5;"))
    for row in result:
        row = LGPD(row)
        users.append(row)

for user in users:
    print(user)