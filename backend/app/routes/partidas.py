"""
Rotas da API para gerenciar partidas
Aqui definimos todos os endpoints relacionados às partidas
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.entities import Partida, Pelada
from app.schemas import PartidaCreate, PartidaUpdate, PartidaResponse

# Cria o router para agrupar rotas de partidas
router = APIRouter()

@router.post("/partidas/", response_model=PartidaResponse, status_code=status.HTTP_201_CREATED)
async def criar_partida(
    partida: PartidaCreate,
    db: Session = Depends(get_db)
):
    """
    Cria uma nova partida
    
    - **pelada_id**: ID da pelada à qual pertence
    - **nome**: Nome da partida (opcional)
    - **horario_previsto**: Horário agendado
    - **nome_time_a**: Nome do time A (padrão "Time A")
    - **nome_time_b**: Nome do time B (padrão "Time B")
    - **observacoes**: Observações opcionais
    """
    # Verifica se a pelada existe
    pelada = db.query(Pelada).filter(Pelada.id == partida.pelada_id).first()
    if pelada is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pelada não encontrada"
        )
    
    try:
        # Cria nova instância do modelo
        db_partida = Partida(**partida.dict())
        
        # Adiciona ao banco
        db.add(db_partida)
        db.commit()
        db.refresh(db_partida)
        
        return db_partida
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar partida: {str(e)}"
        )

@router.get("/partidas/", response_model=List[PartidaResponse])
async def listar_partidas(
    pelada_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista partidas
    
    - **pelada_id**: Filtrar por pelada específica (opcional)
    - **skip**: Quantos registros pular
    - **limit**: Quantos registros retornar
    """
    query = db.query(Partida)
    
    if pelada_id:
        query = query.filter(Partida.pelada_id == pelada_id)
    
    partidas = query.offset(skip).limit(limit).all()
    return partidas

@router.get("/partidas/{partida_id}", response_model=PartidaResponse)
async def obter_partida(
    partida_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtém uma partida específica pelo ID
    """
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    
    if partida is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partida não encontrada"
        )
    
    return partida

@router.put("/partidas/{partida_id}", response_model=PartidaResponse)
async def atualizar_partida(
    partida_id: int,
    partida_update: PartidaUpdate,
    db: Session = Depends(get_db)
):
    """
    Atualiza uma partida existente
    """
    # Busca a partida
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    
    if partida is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partida não encontrada"
        )
    
    try:
        # Atualiza apenas os campos fornecidos
        update_data = partida_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(partida, field, value)
        
        db.commit()
        db.refresh(partida)
        
        return partida
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao atualizar partida: {str(e)}"
        )

@router.delete("/partidas/{partida_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_partida(
    partida_id: int,
    db: Session = Depends(get_db)
):
    """
    Deleta uma partida
    
    Atenção: Isso também deletará todos os gols relacionados!
    """
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    
    if partida is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partida não encontrada"
        )
    
    try:
        db.delete(partida)
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao deletar partida: {str(e)}"
        )

# Endpoints específicos para controle de partida
@router.patch("/partidas/{partida_id}/iniciar")
async def iniciar_partida(
    partida_id: int,
    db: Session = Depends(get_db)
):
    """
    Inicia uma partida (marca horário de início e status)
    """
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    
    if partida is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partida não encontrada"
        )
    
    from datetime import datetime
    from app.models.entities import StatusPartida
    
    try:
        partida.horario_inicio = datetime.utcnow()
        partida.status = StatusPartida.EM_ANDAMENTO
        
        db.commit()
        db.refresh(partida)
        
        return {"message": "Partida iniciada com sucesso", "partida": partida}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao iniciar partida: {str(e)}"
        )

@router.patch("/partidas/{partida_id}/finalizar")
async def finalizar_partida(
    partida_id: int,
    db: Session = Depends(get_db)
):
    """
    Finaliza uma partida (marca horário de fim e status)
    """
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    
    if partida is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partida não encontrada"
        )
    
    from datetime import datetime
    from app.models.entities import StatusPartida
    
    try:
        partida.horario_fim = datetime.utcnow()
        partida.status = StatusPartida.FINALIZADA
        
        db.commit()
        db.refresh(partida)
        
        return {"message": "Partida finalizada com sucesso", "partida": partida}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao finalizar partida: {str(e)}"
        )
