"""
Script para testar a conexão e criar dados de exemplo
"""
import requests
import json

# URLs da API
BASE_URL = "http://localhost:8000/api"

def testar_conexao():
    """Testa se o backend está rodando"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"✅ Backend está rodando! Status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Backend não está rodando!")
        return False

def criar_dados_teste():
    """Cria dados de teste se não existirem"""
    try:
        # 1. Criar alguns jogadores
        jogadores = [
            {"nome": "João Silva", "posicao": "Atacante"},
            {"nome": "Pedro Santos", "posicao": "Meio-campo"},
            {"nome": "Carlos Oliveira", "posicao": "Defensor"},
            {"nome": "Marco Antonio", "posicao": "Goleiro"}
        ]
        
        print("Criando jogadores...")
        for jogador in jogadores:
            try:
                response = requests.post(f"{BASE_URL}/jogadores/", json=jogador)
                if response.status_code == 201:
                    print(f"✅ Jogador criado: {jogador['nome']}")
                else:
                    print(f"⚠️ Jogador já existe ou erro: {jogador['nome']}")
            except Exception as e:
                print(f"❌ Erro ao criar jogador {jogador['nome']}: {e}")
        
        # 2. Verificar se existe uma pelada
        print("Verificando peladas...")
        response = requests.get(f"{BASE_URL}/peladas/")
        if response.status_code != 200:
            print(f"❌ Erro ao buscar peladas: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return
            
        peladas = response.json()
        print(f"Peladas encontradas: {len(peladas)}")
        
        if not peladas:
            # Criar uma pelada de teste
            print("Criando pelada de teste...")
            pelada_data = {
                "nome": "Pelada de Teste",
                "local": "Campo do Bairro",
                "descricao": "Pelada para testar o sistema"
            }
            response = requests.post(f"{BASE_URL}/peladas/", json=pelada_data)
            if response.status_code == 201:
                print("✅ Pelada criada")
                pelada_id = response.json()["id"]
            else:
                print(f"❌ Erro ao criar pelada: {response.status_code}")
                print(f"   Resposta: {response.text}")
                return
        else:
            pelada_id = peladas[0]["id"]
            print(f"✅ Usando pelada existente: ID {pelada_id}")
        
        # 3. Verificar se já existe uma partida
        print("Verificando partidas...")
        response = requests.get(f"{BASE_URL}/partidas/")
        if response.status_code != 200:
            print(f"❌ Erro ao buscar partidas: {response.status_code}")
            return
            
        partidas = response.json()
        print(f"Partidas encontradas: {len(partidas)}")
        
        if partidas:
            partida_id = partidas[0]["id"] 
            print(f"✅ Usando partida existente: ID {partida_id}")
        else:
            # 3. Criar uma partida de teste
            print("Criando partida de teste...")
            from datetime import datetime, timedelta
            
            partida_data = {
                "pelada_id": pelada_id,
                "nome": "Partida de Teste",
                "horario_previsto": (datetime.now() + timedelta(hours=1)).isoformat(),
                "nome_time_a": "Time Azul",
                "nome_time_b": "Time Vermelho"
            }
            
            response = requests.post(f"{BASE_URL}/partidas/", json=partida_data)
            if response.status_code == 201:
                partida_id = response.json()["id"]
                print(f"✅ Partida criada: ID {partida_id}")
            else:
                print(f"❌ Erro ao criar partida: {response.status_code}")
                print(f"   Resposta: {response.text}")
                return
        
        # Testar endpoint específico que o frontend usa
        print(f"Testando endpoint detalhada para partida {partida_id}...")
        response = requests.get(f"{BASE_URL}/partidas/{partida_id}/detalhada")
        if response.status_code == 200:
            print("✅ Endpoint detalhada funcionando!")
            dados = response.json()
            print(f"   Partida: {dados['partida']['nome_time_a']} vs {dados['partida']['nome_time_b']}")
            print(f"   Gols encontrados: {len(dados['gols'])}")
        else:
            print(f"❌ Erro no endpoint detalhada: {response.status_code}")
            print(f"   Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")

if __name__ == "__main__":
    print("🧪 Testando o backend...")
    
    if testar_conexao():
        print("\n📝 Criando dados de teste...")
        criar_dados_teste()
        print("\n✅ Teste concluído! Verifique o frontend agora.")
    else:
        print("\n💡 Inicie o backend primeiro:")
        print("   cd backend")
        print("   python -m uvicorn app.main:app --reload")
