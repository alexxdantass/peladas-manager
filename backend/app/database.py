"""
Configuração da conexão com o banco de dados
Aqui definimos como conectar e criar as tabelas
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.entities import Base

# URL do banco SQLite - arquivo local
# sqlite:/// significa arquivo local
DATABASE_URL = "sqlite:///./peladas.db"

# Engine - objeto que gerencia a conexão com o banco
# check_same_thread=False é necessário para SQLite com FastAPI
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# SessionLocal - classe para criar sessões do banco
# Uma sessão é como uma "conversa" com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """
    Cria todas as tabelas no banco de dados
    Roda apenas se as tabelas não existirem
    """
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Função para obter uma sessão do banco
    Usaremos como dependência no FastAPI
    """
    db = SessionLocal()
    try:
        yield db  # Retorna a sessão
    finally:
        db.close()  # Sempre fecha a conexão
