"""
Rotas da API para gerenciar jogadores
Aqui definimos todos os endpoints relacionados aos jogadores
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.database import Jogador
from app.schemas import JogadorCreate, JogadorUpdate, JogadorResponse

# Cria o router para agrupar rotas de jogadores
router = APIRouter()

@router.post("/jogadores/", response_model=JogadorResponse, status_code=status.HTTP_201_CREATED)
async def criar_jogador(
    jogador: JogadorCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo jogador
    
    - **nome**: Nome completo do jogador
    - **email**: Email único do jogador
    - **telefone**: Telefone (opcional)
    - **posicao_preferida**: Posição que prefere jogar (opcional)
    - **nivel_habilidade**: Nível de 1-10 (padrão 5)
    """
    
    # Verifica se email já existe
    db_jogador = db.query(Jogador).filter(Jogador.email == jogador.email).first()
    if db_jogador:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Cria novo jogador
    db_jogador = Jogador(**jogador.dict())
    db.add(db_jogador)
    db.commit()
    db.refresh(db_jogador)  # Pega os dados atualizados (como ID)
    
    return db_jogador

@router.get("/jogadores/", response_model=List[JogadorResponse])
async def listar_jogadores(
    skip: int = 0,
    limit: int = 100,
    ativo: bool = True,
    db: Session = Depends(get_db)
):
    """
    Lista todos os jogadores
    
    - **skip**: Quantos registros pular (paginação)
    - **limit**: Quantos registros retornar (máximo 100)
    - **ativo**: Se deve mostrar apenas jogadores ativos
    """
    query = db.query(Jogador)
    
    if ativo:
        query = query.filter(Jogador.ativo == True)
    
    jogadores = query.offset(skip).limit(limit).all()
    return jogadores

@router.get("/jogadores/{jogador_id}", response_model=JogadorResponse)
async def obter_jogador(jogador_id: int, db: Session = Depends(get_db)):
    """
    Obtém um jogador específico pelo ID
    """
    jogador = db.query(Jogador).filter(Jogador.id == jogador_id).first()
    
    if not jogador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jogador não encontrado"
        )
    
    return jogador

@router.put("/jogadores/{jogador_id}", response_model=JogadorResponse)
async def atualizar_jogador(
    jogador_id: int,
    jogador_update: JogadorUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza dados de um jogador
    """
    jogador = db.query(Jogador).filter(Jogador.id == jogador_id).first()
    
    if not jogador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jogador não encontrado"
        )
    
    # Atualiza apenas os campos fornecidos
    update_data = jogador_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(jogador, field, value)
    
    db.commit()
    db.refresh(jogador)
    
    return jogador

@router.delete("/jogadores/{jogador_id}")
async def deletar_jogador(jogador_id: int, db: Session = Depends(get_db)):
    """
    Desativa um jogador (não deleta fisicamente)
    """
    jogador = db.query(Jogador).filter(Jogador.id == jogador_id).first()
    
    if not jogador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jogador não encontrado"
        )
    
    # Desativa ao invés de deletar (soft delete)
    jogador.ativo = False
    db.commit()
    
    return {"message": "Jogador desativado com sucesso"}
