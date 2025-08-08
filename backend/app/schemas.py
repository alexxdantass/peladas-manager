"""
Schemas Pydantic para validação de dados
Definem como os dados devem ser estruturados nas requisições/respostas da API
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, List
from enum import Enum

# Enums para status
class StatusPeladaEnum(str, Enum):
    PLANEJADA = "planejada"
    CONFIRMADA = "confirmada"
    EM_ANDAMENTO = "em_andamento"
    FINALIZADA = "finalizada"
    CANCELADA = "cancelada"

class StatusPartidaEnum(str, Enum):
    AGENDADA = "agendada"
    EM_ANDAMENTO = "em_andamento"
    FINALIZADA = "finalizada"
    CANCELADA = "cancelada"

# Schemas para Jogador
class JogadorBase(BaseModel):
    """Schema base do jogador - campos comuns"""
    nome: str
    email: str  # EmailStr valida formato de email automaticamente
    telefone: Optional[str] = None
    posicao_preferida: Optional[str] = None
    nivel_habilidade: int = 5  # Padrão 5

class JogadorCreate(JogadorBase):
    """Schema para criar jogador - herda do base"""
    pass  # Por enquanto, mesmos campos do base

class JogadorUpdate(BaseModel):
    """Schema para atualizar jogador - todos os campos opcionais"""
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    posicao_preferida: Optional[str] = None
    nivel_habilidade: Optional[int] = None
    ativo: Optional[bool] = None

class JogadorResponse(JogadorBase):
    """Schema para resposta da API - inclui campos do banco"""
    id: int
    ativo: bool
    data_cadastro: datetime
    
    class Config:
        """Configuração para trabalhar com objetos SQLAlchemy"""
        from_attributes = True  # Permite criar Pydantic de objetos ORM

# Schemas para Pelada
class PeladaBase(BaseModel):
    """Schema base da pelada"""
    nome: str
    descricao: Optional[str] = None
    data_evento: date
    local: str
    max_jogadores: int = 22
    valor_por_jogador: int = 0  # Em centavos

class PeladaCreate(PeladaBase):
    """Schema para criar pelada"""
    pass

class PeladaUpdate(BaseModel):
    """Schema para atualizar pelada"""
    nome: Optional[str] = None
    descricao: Optional[str] = None
    data_evento: Optional[date] = None
    local: Optional[str] = None
    max_jogadores: Optional[int] = None
    valor_por_jogador: Optional[int] = None
    status: Optional[StatusPeladaEnum] = None

class PeladaResponse(PeladaBase):
    """Schema para resposta da API"""
    id: int
    status: StatusPeladaEnum
    data_criacao: datetime
    data_atualizacao: datetime
    
    class Config:
        from_attributes = True

# Schemas para Partida
class PartidaBase(BaseModel):
    """Schema base da partida"""
    nome: Optional[str] = None
    horario_previsto: datetime
    nome_time_a: str = "Time A"
    nome_time_b: str = "Time B"
    observacoes: Optional[str] = None

class PartidaCreate(PartidaBase):
    """Schema para criar partida"""
    pelada_id: int

class PartidaUpdate(BaseModel):
    """Schema para atualizar partida"""
    nome: Optional[str] = None
    horario_inicio: Optional[datetime] = None
    horario_fim: Optional[datetime] = None
    horario_previsto: Optional[datetime] = None
    nome_time_a: Optional[str] = None
    nome_time_b: Optional[str] = None
    gols_time_a: Optional[int] = None
    gols_time_b: Optional[int] = None
    observacoes: Optional[str] = None
    status: Optional[StatusPartidaEnum] = None

class PartidaResponse(PartidaBase):
    """Schema para resposta da API"""
    id: int
    pelada_id: int
    horario_inicio: Optional[datetime] = None
    horario_fim: Optional[datetime] = None
    gols_time_a: int
    gols_time_b: int
    status: StatusPartidaEnum
    data_criacao: datetime
    data_atualizacao: datetime
    
    class Config:
        from_attributes = True

# Schemas para Gol
class GolBase(BaseModel):
    """Schema base do gol"""
    minuto: int
    time: str  # "A" ou "B"
    descricao: Optional[str] = None

class GolCreate(GolBase):
    """Schema para criar gol"""
    partida_id: int
    jogador_id: int

class GolUpdate(BaseModel):
    """Schema para atualizar gol"""
    minuto: Optional[int] = None
    time: Optional[str] = None
    descricao: Optional[str] = None

class GolResponse(GolBase):
    """Schema para resposta da API"""
    id: int
    partida_id: int
    jogador_id: int
    data_criacao: datetime
    
    class Config:
        from_attributes = True
