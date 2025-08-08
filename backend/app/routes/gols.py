"""
Rotas da API para gerenciar gols
Aqui definimos todos os endpoints relacionados aos gols
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.entities import Gol, Partida, Jogador
from app.schemas import GolCreate, GolUpdate, GolResponse

# Cria o router para agrupar rotas de gols
router = APIRouter()

@router.post("/gols/", response_model=GolResponse, status_code=status.HTTP_201_CREATED)
async def criar_gol(
    gol: GolCreate,
    db: Session = Depends(get_db)
):
    """
    Registra um novo gol
    
    - **partida_id**: ID da partida onde foi o gol
    - **jogador_id**: ID do jogador que fez o gol
    - **minuto**: Minuto do jogo
    - **time**: Time que marcou ("A" ou "B")
    - **descricao**: Descrição opcional do gol
    """
    # Verifica se a partida existe
    partida = db.query(Partida).filter(Partida.id == gol.partida_id).first()
    if partida is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partida não encontrada"
        )
    
    # Verifica se o jogador existe
    jogador = db.query(Jogador).filter(Jogador.id == gol.jogador_id).first()
    if jogador is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jogador não encontrado"
        )
    
    # Valida o time
    if gol.time not in ["A", "B"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Time deve ser 'A' ou 'B'"
        )
    
    try:
        # Cria nova instância do modelo
        db_gol = Gol(**gol.dict())
        
        # Adiciona ao banco
        db.add(db_gol)
        
        # Atualiza o placar da partida
        if gol.time == "A":
            partida.gols_time_a += 1
        else:
            partida.gols_time_b += 1
        
        db.commit()
        db.refresh(db_gol)
        
        return db_gol
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao registrar gol: {str(e)}"
        )

@router.get("/gols/", response_model=List[GolResponse])
async def listar_gols(
    partida_id: int = None,
    jogador_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista gols
    
    - **partida_id**: Filtrar por partida específica (opcional)
    - **jogador_id**: Filtrar por jogador específico (opcional)
    - **skip**: Quantos registros pular
    - **limit**: Quantos registros retornar
    """
    query = db.query(Gol)
    
    if partida_id:
        query = query.filter(Gol.partida_id == partida_id)
    
    if jogador_id:
        query = query.filter(Gol.jogador_id == jogador_id)
    
    gols = query.offset(skip).limit(limit).all()
    return gols

@router.get("/gols/{gol_id}", response_model=GolResponse)
async def obter_gol(
    gol_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtém um gol específico pelo ID
    """
    gol = db.query(Gol).filter(Gol.id == gol_id).first()
    
    if gol is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gol não encontrado"
        )
    
    return gol

@router.put("/gols/{gol_id}", response_model=GolResponse)
async def atualizar_gol(
    gol_id: int,
    gol_update: GolUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza um gol existente
    """
    # Busca o gol
    gol = db.query(Gol).filter(Gol.id == gol_id).first()
    
    if gol is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gol não encontrado"
        )
    
    try:
        # Se mudou o time, precisa atualizar o placar
        old_time = gol.time
        
        # Atualiza apenas os campos fornecidos
        update_data = gol_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(gol, field, value)
        
        # Se mudou o time, atualiza o placar
        if "time" in update_data and update_data["time"] != old_time:
            partida = db.query(Partida).filter(Partida.id == gol.partida_id).first()
            
            # Remove do time antigo
            if old_time == "A":
                partida.gols_time_a -= 1
            else:
                partida.gols_time_b -= 1
            
            # Adiciona no time novo
            if gol.time == "A":
                partida.gols_time_a += 1
            else:
                partida.gols_time_b += 1
        
        db.commit()
        db.refresh(gol)
        
        return gol
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao atualizar gol: {str(e)}"
        )

@router.delete("/gols/{gol_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_gol(
    gol_id: int,
    db: Session = Depends(get_db)
):
    """
    Deleta um gol e atualiza o placar da partida
    """
    gol = db.query(Gol).filter(Gol.id == gol_id).first()
    
    if gol is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gol não encontrado"
        )
    
    try:
        # Atualiza o placar da partida
        partida = db.query(Partida).filter(Partida.id == gol.partida_id).first()
        if gol.time == "A":
            partida.gols_time_a -= 1
        else:
            partida.gols_time_b -= 1
        
        # Deleta o gol
        db.delete(gol)
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao deletar gol: {str(e)}"
        )
