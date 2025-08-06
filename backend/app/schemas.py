"""
Schemas Pydantic para validação de dados
Definem como os dados devem ser estruturados nas requisições/respostas da API
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

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
    data_hora: datetime
    local: str
    max_jogadores: int = 20
    valor_por_pessoa: float = 0.0

class PeladaCreate(PeladaBase):
    """Schema para criar pelada"""
    pass

class PeladaUpdate(BaseModel):
    """Schema para atualizar pelada"""
    nome: Optional[str] = None
    descricao: Optional[str] = None
    data_hora: Optional[datetime] = None
    local: Optional[str] = None
    max_jogadores: Optional[int] = None
    valor_por_pessoa: Optional[float] = None
    ativa: Optional[bool] = None

class PeladaResponse(PeladaBase):
    """Schema para resposta da API"""
    id: int
    ativa: bool
    data_criacao: datetime
    # participantes: List[JogadorResponse] = []  # Adicionaremos depois
    
    class Config:
        from_attributes = True

# Schemas para Participação
class ParticipacaoCreate(BaseModel):
    """Schema para inscrever jogador em pelada"""
    jogador_id: int
    pelada_id: int

class ParticipacaoResponse(BaseModel):
    """Schema para resposta de participação"""
    id: int
    jogador_id: int
    pelada_id: int
    confirmado: bool
    time: Optional[str] = None
    data_inscricao: datetime
    
    class Config:
        from_attributes = True

# Schema para confirmação de presença
class ConfirmarPresenca(BaseModel):
    """Schema para confirmar presença em pelada"""
    confirmado: bool
