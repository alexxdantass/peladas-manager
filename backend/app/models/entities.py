"""
Entidades/Modelos de banco de dados usando SQLAlchemy
Aqui definimos como os dados serão estruturados no banco
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Date, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

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


# ===== NOVAS ENTIDADES PARA SISTEMA DE PELADAS =====

class StatusPelada(enum.Enum):
    """Status possíveis de uma pelada"""
    PLANEJADA = "planejada"      # Ainda sendo organizada
    CONFIRMADA = "confirmada"    # Confirmada, jogadores podem se inscrever
    EM_ANDAMENTO = "em_andamento"  # Happening now
    FINALIZADA = "finalizada"    # Acabou
    CANCELADA = "cancelada"      # Foi cancelada


class Pelada(Base):
    """
    Entidade Pelada - Um evento esportivo
    
    Uma pelada é como um "campeonato de um dia" que pode ter várias partidas
    Exemplo: "Pelada do Sábado - Parque Ibirapuera"
    """
    __tablename__ = "peladas"

    # Campos básicos
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, index=True)  # "Pelada do Sábado"
    descricao = Column(Text, nullable=True)  # Descrição opcional
    
    # Data e local
    data_evento = Column(Date, nullable=False, index=True)  # Dia da pelada
    local = Column(String(200), nullable=False)  # "Parque Ibirapuera - Campo 2"
    
    # Configurações
    max_jogadores = Column(Integer, default=22)  # Máximo de jogadores (11 x 11)
    valor_por_jogador = Column(Integer, default=0)  # Em centavos (ex: 2000 = R$ 20,00)
    
    # Status e timestamps
    status = Column(Enum(StatusPelada), default=StatusPelada.PLANEJADA, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    partidas = relationship("Partida", back_populates="pelada", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Pelada(id={self.id}, nome='{self.nome}', data='{self.data_evento}')>"


class StatusPartida(enum.Enum):
    """Status possíveis de uma partida"""
    AGENDADA = "agendada"        # Agendada mas ainda não começou
    EM_ANDAMENTO = "em_andamento"  # Rolando agora
    FINALIZADA = "finalizada"    # Acabou
    CANCELADA = "cancelada"      # Foi cancelada


class Partida(Base):
    """
    Entidade Partida - Um jogo individual
    
    Uma partida é um jogo específico dentro de uma pelada
    Exemplo: "Jogo 1: Time A vs Time B - 14h às 15h"
    """
    __tablename__ = "partidas"

    # Campos básicos
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=True)  # "Jogo 1", "Final", etc (opcional)
    
    # Relacionamento com pelada
    pelada_id = Column(Integer, ForeignKey("peladas.id"), nullable=False)
    
    # Horários
    horario_inicio = Column(DateTime, nullable=True)  # Quando começou de fato
    horario_fim = Column(DateTime, nullable=True)     # Quando terminou
    horario_previsto = Column(DateTime, nullable=False)  # Horário agendado
    
    # Times (por enquanto, só nomes. Depois podemos melhorar)
    nome_time_a = Column(String(50), default="Time A")
    nome_time_b = Column(String(50), default="Time B")
    
    # Placar
    gols_time_a = Column(Integer, default=0)
    gols_time_b = Column(Integer, default=0)
    
    # Observações
    observacoes = Column(Text, nullable=True)  # "Jogo adiado por chuva", etc
    
    # Status
    status = Column(Enum(StatusPartida), default=StatusPartida.AGENDADA, nullable=False)
    
    # Timestamps
    data_criacao = Column(DateTime, default=datetime.utcnow, nullable=False)
    data_atualizacao = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    pelada = relationship("Pelada", back_populates="partidas")
    gols = relationship("Gol", back_populates="partida", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Partida(id={self.id}, {self.nome_time_a} {self.gols_time_a} x {self.gols_time_b} {self.nome_time_b})>"
    
    @property
    def placar(self) -> str:
        """Retorna o placar formatado"""
        return f"{self.gols_time_a} x {self.gols_time_b}"
    
    @property
    def duracao_minutos(self) -> int:
        """Calcula duração da partida em minutos"""
        if self.horario_inicio and self.horario_fim:
            delta = self.horario_fim - self.horario_inicio
            return int(delta.total_seconds() / 60)
        return 0


class Gol(Base):
    """
    Entidade Gol - Um gol marcado durante uma partida
    
    Registra quem fez o gol e quando
    """
    __tablename__ = "gols"

    # Campos básicos
    id = Column(Integer, primary_key=True, index=True)
    
    # Relacionamentos
    partida_id = Column(Integer, ForeignKey("partidas.id"), nullable=False)
    jogador_id = Column(Integer, ForeignKey("jogadores.id"), nullable=False)
    
    # Dados do gol
    minuto = Column(Integer, nullable=False)  # Minuto do jogo (1-90+)
    time = Column(String(1), nullable=False)  # "A" ou "B"
    
    # Observações
    descricao = Column(String(200), nullable=True)  # "Chute de fora da área", etc
    
    # Timestamps
    data_criacao = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relacionamentos
    partida = relationship("Partida", back_populates="gols")
    jogador = relationship("Jogador")  # Referência ao jogador que fez o gol
    
    def __repr__(self):
        return f"<Gol(jogador_id={self.jogador_id}, minuto={self.minuto})>"
