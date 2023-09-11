from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, event
import os

# importando os elemetos definidos no modelo
from model.base import Base
from model.grupo import Grupo
from model.grupo import SubGrupo
from model.lancamento import Lancamento
from model.load_db import carga_inicial

db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
  # então cria o diretório
  os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

#cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# cria o banco se ele não existir
if not database_exists(engine.url):
  create_database(engine.url)

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)


# faz a carga inicial automaticamente se não tiver nenhum grupo
with Session(engine) as session:
  count = session.query(Grupo).count()
  if not count:
    carga_inicial(session)
    session.commit()
