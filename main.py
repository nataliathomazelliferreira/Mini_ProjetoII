from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, DateTime, insert, text
from datetime import datetime
import csv

import time
from functools import wraps

#atividade 4
def medir_tempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        fim = time.perf_counter()
        duracao = fim - inicio

        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("log.txt", "a", encoding="utf-8") as log:
            log.write(f"{agora} | {func.__name__} | {duracao:.6f} segundos\n")

        print(f"{func.__name__}: {duracao:.6f} segundos")
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

#atividade 1
def LGPD(row):
    nome = row[1]
    partes = nome.split(" ")
    primeiro = partes[0]
    resto = " ".join(partes[1:]) if len(partes) > 1 else ""
    nome_anon = primeiro[0] + "*" * (len(primeiro) - 1)
    if resto:
        nome_anon += " " + resto

    cpf = row[2]
    cpf_anon = cpf[:3] + ".***.***-**"

    email = row[3]
    usuario, dominio = email.split("@")
    email_anon = usuario[0] + "*" * (len(usuario) - 1) + "@" + dominio

    telefone = row[4]
    telefone_limpo = "".join([c for c in telefone if c.isdigit()])
    telefone_anon = telefone_limpo[-4:]

    return (
        row[0],
        nome_anon,
        cpf_anon,
        email_anon,
        telefone_anon,
        row[5],
        row[6],
        row[7]
    )
#atividade 2
@medir_tempo
def atividade2():
    dados_por_ano = {}

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM usuarios"))
        for row in result:
            ano = row[5].year

            if ano not in dados_por_ano:
                dados_por_ano[ano] = []

            dados_por_ano[ano].append(LGPD(row))

    for ano, registros in dados_por_ano.items():
        with open(f"{ano}.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(registros)

#atividade 3
@medir_tempo
def atividade3():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT nome, cpf FROM usuarios"))

        with open("todos.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(result)

users = []
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios LIMIT 5;"))
    for row in result:
        row = LGPD(row)
        users.append(row)

for user in users:
    print(user)

atividade2()
atividade3()