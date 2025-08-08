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
    
    from datetime import datetime, timezone
    from app.models.entities import StatusPartida
    
    try:
        partida.horario_inicio = datetime.now(timezone.utc)
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
    
    from datetime import datetime, timezone
    from app.models.entities import StatusPartida
    
    try:
        partida.horario_fim = datetime.now(timezone.utc)
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

# ===== NOVAS APIS PARA TELA DA PARTIDA =====

@router.get("/partidas/{partida_id}/detalhada")
async def obter_partida_detalhada(
    partida_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtém partida com todos os gols e informações detalhadas
    Para a tela da partida ao vivo
    """
    from app.models.entities import Gol, Jogador
    
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    
    if partida is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partida não encontrada"
        )
    
    # Busca todos os gols da partida ordenados por minuto
    gols = db.query(Gol).filter(Gol.partida_id == partida_id).order_by(Gol.minuto).all()
    
    # Busca todos os jogadores para poder marcar gols
    jogadores = db.query(Jogador).all()
    
    return {
        "partida": partida,
        "gols": gols,
        "jogadores": jogadores,
        "placar": f"{partida.gols_time_a} x {partida.gols_time_b}",
        "duracao_minutos": partida.duracao_minutos if partida.horario_inicio else 0,
        "em_andamento": partida.status.value == "em_andamento"
    }

@router.patch("/partidas/{partida_id}/cronometro")
async def atualizar_cronometro(
    partida_id: int,
    acao: str,  # "play", "pause", "reset"
    db: Session = Depends(get_db)
):
    """
    Controla o cronômetro da partida
    
    - **play**: Inicia/retoma o cronômetro
    - **pause**: Pausa o cronômetro
    - **reset**: Reseta o cronômetro
    """
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    
    if partida is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partida não encontrada"
        )
    
    from datetime import datetime, timezone
    from app.models.entities import StatusPartida
    
    try:
        if acao == "play":
            if not partida.horario_inicio:
                partida.horario_inicio = datetime.now(timezone.utc)
            # Sempre colocar como EM_ANDAMENTO, seja primeira vez ou retomando
            partida.status = StatusPartida.EM_ANDAMENTO
            
        elif acao == "pause":
            # Partida pausada mas ainda em andamento (não finalizada)
            partida.status = StatusPartida.EM_ANDAMENTO
            
        elif acao == "reset":
            partida.horario_inicio = None
            partida.horario_fim = None
            partida.status = StatusPartida.AGENDADA
        
        db.commit()
        db.refresh(partida)
        
        return {
            "message": f"Cronômetro {acao} executado com sucesso",
            "partida": partida,
            "duracao_minutos": partida.duracao_minutos
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao controlar cronômetro: {str(e)}"
        )

# Endpoint POST adicional para compatibilidade
@router.post("/partidas/{partida_id}/cronometro")
async def atualizar_cronometro_post(
    partida_id: int,
    dados: dict,  # Recebe {"acao": "play/pause/reset"}
    db: Session = Depends(get_db)
):
    """
    Controla o cronômetro da partida (versão POST)
    Aceita {"acao": "play"/"pause"/"reset"}
    """
    acao = dados.get("acao")
    if not acao or acao not in ["play", "pause", "reset"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ação deve ser 'play', 'pause' ou 'reset'"
        )
    
    # Reutiliza a mesma lógica do endpoint PATCH
    return await atualizar_cronometro(partida_id, acao, db)

@router.post("/partidas/{partida_id}/gol-rapido")
async def marcar_gol_rapido(
    partida_id: int,
    jogador_id: int,
    time: str,  # "A" ou "B"
    db: Session = Depends(get_db)
):
    """
    Marca um gol rapidamente durante a partida ao vivo
    Calcula automaticamente o minuto baseado no tempo da partida
    """
    from app.models.entities import Gol, Jogador
    from datetime import datetime, timezone
    
    # Verifica se a partida existe
    partida = db.query(Partida).filter(Partida.id == partida_id).first()
    if partida is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partida não encontrada"
        )
    
    # Verifica se o jogador existe
    jogador = db.query(Jogador).filter(Jogador.id == jogador_id).first()
    if jogador is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jogador não encontrado"
        )
    
    # Valida o time
    if time not in ["A", "B"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Time deve ser 'A' ou 'B'"
        )
    
    try:
        # Calcula o minuto do gol baseado no tempo da partida
        minuto = 1  # Padrão
        if partida.horario_inicio:
            delta = datetime.now(timezone.utc) - partida.horario_inicio
            minuto = max(1, int(delta.total_seconds() / 60))
        
        # Cria o gol
        gol = Gol(
            partida_id=partida_id,
            jogador_id=jogador_id,
            minuto=minuto,
            time=time,
            descricao=f"Gol aos {minuto}' - {jogador.nome}"
        )
        
        db.add(gol)
        
        # Atualiza o placar
        if time == "A":
            partida.gols_time_a += 1
        else:
            partida.gols_time_b += 1
        
        db.commit()
        db.refresh(gol)
        db.refresh(partida)
        
        return {
            "message": "Gol marcado com sucesso!",
            "gol": gol,
            "placar": f"{partida.gols_time_a} x {partida.gols_time_b}",
            "minuto": minuto
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao marcar gol: {str(e)}"
        )
