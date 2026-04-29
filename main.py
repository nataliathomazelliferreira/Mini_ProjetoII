from sqlalchemy import create_engine, MetaData, Table, Column, Integer
from sqlalchemy import String, Date, DateTime, text
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

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

def LGPD(row):
    id, nome, cpf, email, telefone, data_nasc, created, updated = row

    partes_nome = nome.split(" ")
    primeiro_nome = partes_nome[0]
    sobrenome = " ".join(partes_nome[1:]) if len(partes_nome) > 1 else ""

    nome_anon = primeiro_nome[0] + "*" * (len(primeiro_nome) - 1)
    if sobrenome:
        nome_anon += " " + sobrenome

    cpf_anon = cpf[:3] + ".***.***-**"

    usuario, dominio = email.split("@")
    email_anon = usuario[0] + "*" * (len(usuario) - 1) + "@" + dominio

    telefone_anon = telefone[-4:]

    return (
        id,
        nome_anon,
        cpf_anon,
        email_anon,
        telefone_anon,
        data_nasc,
        created,
        updated
    )

users = []

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM usuarios LIMIT 10;"))
    
    for row in result:
        row = LGPD(row)
        users.append(row)

for u in users:
    print(u)