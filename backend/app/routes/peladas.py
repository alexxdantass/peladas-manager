"""
Rotas da API para gerenciar peladas
Aqui definimos todos os endpoints relacionados às peladas
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.entities import Pelada
from app.schemas import PeladaCreate, PeladaUpdate, PeladaResponse

# Cria o router para agrupar rotas de peladas
router = APIRouter()

@router.post("/peladas/", response_model=PeladaResponse, status_code=status.HTTP_201_CREATED)
async def criar_pelada(
    pelada: PeladaCreate,
    db: Session = Depends(get_db)
):
    """
    Cria uma nova pelada
    
    - **nome**: Nome da pelada (ex: "Pelada do Sábado")
    - **descricao**: Descrição opcional
    - **data_evento**: Data do evento
    - **local**: Local onde será realizada
    - **max_jogadores**: Máximo de jogadores (padrão 22)
    - **valor_por_jogador**: Valor em centavos (padrão 0)
    """
    try:
        # Cria nova instância do modelo
        db_pelada = Pelada(**pelada.dict())
        
        # Adiciona ao banco
        db.add(db_pelada)
        db.commit()
        db.refresh(db_pelada)
        
        return db_pelada
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar pelada: {str(e)}"
        )

@router.get("/peladas/", response_model=List[PeladaResponse])
async def listar_peladas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista todas as peladas
    
    - **skip**: Quantos registros pular (paginação)
    - **limit**: Quantos registros retornar (máximo 100)
    """
    peladas = db.query(Pelada).offset(skip).limit(limit).all()
    return peladas

@router.get("/peladas/{pelada_id}", response_model=PeladaResponse)
async def obter_pelada(
    pelada_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtém uma pelada específica pelo ID
    """
    pelada = db.query(Pelada).filter(Pelada.id == pelada_id).first()
    
    if pelada is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pelada não encontrada"
        )
    
    return pelada

@router.put("/peladas/{pelada_id}", response_model=PeladaResponse)
async def atualizar_pelada(
    pelada_id: int,
    pelada_update: PeladaUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza uma pelada existente
    """
    # Busca a pelada
    pelada = db.query(Pelada).filter(Pelada.id == pelada_id).first()
    
    if pelada is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pelada não encontrada"
        )
    
    try:
        # Atualiza apenas os campos fornecidos
        update_data = pelada_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(pelada, field, value)
        
        db.commit()
        db.refresh(pelada)
        
        return pelada
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao atualizar pelada: {str(e)}"
        )

@router.delete("/peladas/{pelada_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_pelada(
    pelada_id: int,
    db: Session = Depends(get_db)
):
    """
    Deleta uma pelada
    
    Atenção: Isso também deletará todas as partidas e gols relacionados!
    """
    pelada = db.query(Pelada).filter(Pelada.id == pelada_id).first()
    
    if pelada is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pelada não encontrada"
        )
    
    try:
        db.delete(pelada)
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao deletar pelada: {str(e)}"
        )
