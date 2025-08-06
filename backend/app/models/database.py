"""
Modelos de banco de dados usando SQLAlchemy
Aqui definimos como os dados serão estruturados no banco
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

# Base para todos os modelos - padrão SQLAlchemy
Base = declarative_base()

class Jogador(Base):
    """
    Modelo para representar um jogador
    Cada jogador tem informações básicas e estatísticas
    """
    __tablename__ = "jogadores"  # Nome da tabela no banco
    
    # Campos da tabela
    id = Column(Integer, primary_key=True, index=True)  # Chave primária
    nome = Column(String(100), nullable=False)  # Nome obrigatório, máx 100 chars
    email = Column(String(255), unique=True, nullable=False)  # Email único
    telefone = Column(String(20), nullable=True)  # Telefone opcional
    posicao_preferida = Column(String(50), nullable=True)  # Goleiro, Atacante, etc.
    nivel_habilidade = Column(Integer, default=5)  # 1-10, padrão 5
    ativo = Column(Boolean, default=True)  # Se o jogador está ativo
    data_cadastro = Column(DateTime, default=datetime.utcnow)  # Quando foi cadastrado
    
    # Relacionamentos (definiremos depois)
    # participacoes = relationship("Participacao", back_populates="jogador")
    
    def __repr__(self):
        """Representação em string do objeto - útil para debug"""
        return f"<Jogador(nome='{self.nome}', email='{self.email}')>"

class Pelada(Base):
    """
    Modelo para representar uma pelada/jogo
    """
    __tablename__ = "peladas"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(200), nullable=False)  # "Pelada de Terça", etc.
    descricao = Column(String(500), nullable=True)  # Descrição opcional
    data_hora = Column(DateTime, nullable=False)  # Quando vai acontecer
    local = Column(String(200), nullable=False)  # Onde vai ser
    max_jogadores = Column(Integer, default=20)  # Máximo de jogadores
    valor_por_pessoa = Column(Float, default=0.0)  # Custo por pessoa
    ativa = Column(Boolean, default=True)  # Se a pelada está ativa
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    # participacoes = relationship("Participacao", back_populates="pelada")
    
    def __repr__(self):
        return f"<Pelada(nome='{self.nome}', data='{self.data_hora}')>"

class Participacao(Base):
    """
    Modelo para relacionar jogadores com peladas
    Tabela de ligação entre Jogador e Pelada
    """
    __tablename__ = "participacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    jogador_id = Column(Integer, ForeignKey("jogadores.id"), nullable=False)
    pelada_id = Column(Integer, ForeignKey("peladas.id"), nullable=False)
    confirmado = Column(Boolean, default=False)  # Se confirmou presença
    time = Column(String(1), nullable=True)  # 'A' ou 'B' quando dividir times
    data_inscricao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    # jogador = relationship("Jogador", back_populates="participacoes")
    # pelada = relationship("Pelada", back_populates="participacoes")
    
    def __repr__(self):
        return f"<Participacao(jogador_id={self.jogador_id}, pelada_id={self.pelada_id})>"
