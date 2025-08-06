"""
Arquivo principal da aplicação FastAPI
Este é o ponto de entrada do nosso backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa as rotas
from app.routes import jogadores
from app.database import create_tables

# Cria a instância principal do FastAPI
app = FastAPI(
    title="Peladas Manager API",
    description="API para gerenciamento de peladas",
    version="1.0.0"
)

# Cria as tabelas do banco na inicialização
create_tables()

# Configuração de CORS - permite que o frontend acesse a API
# CORS = Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL do frontend React
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Permite todos os headers
)

# Rota de teste - primeira rota da nossa API
@app.get("/")
async def root():
    """
    Rota raiz da API - apenas para testar se está funcionando
    """
    return {
        "message": "Peladas Manager API está funcionando!",
        "version": "1.0.0"
    }

# Rota de health check - boa prática para APIs
@app.get("/health")
async def health_check():
    """
    Endpoint para verificar se a API está saudável
    Útil para monitoramento em produção
    """
    return {"status": "healthy"}

# Inclui as rotas da API
app.include_router(jogadores.router, prefix="/api", tags=["jogadores"])

# Quando criarmos outras rotas:
# app.include_router(peladas.router, prefix="/api", tags=["peladas"])
