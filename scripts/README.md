# Scripts de Desenvolvimento

Esta pasta contém scripts úteis para desenvolvimento e teste do projeto.

## 🧪 testar_backend.py

Script para testar a conexão com o backend e criar dados de exemplo.

### Como usar:

1. **Certifique-se que o backend está rodando:**
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

2. **Execute o script de teste:**
   ```bash
   python scripts/testar_backend.py
   ```

### O que o script faz:

- ✅ Testa se o backend está acessível
- 🧑‍💼 Cria jogadores de exemplo (se não existirem)
- 🏟️ Cria uma pelada de teste (se não existir)
- ⚽ Cria uma partida de teste (se não existir)
- 🔍 Testa os endpoints específicos que o frontend usa

### Dados criados:

- **Jogadores**: João Silva, Pedro Santos, Carlos Oliveira, Marco Antonio
- **Pelada**: "Pelada de Teste" no "Campo do Bairro"
- **Partida**: "Partida de Teste" entre "Time Azul" vs "Time Vermelho"

### Quando usar:

- 🆕 Primeiro setup do projeto
- 🐛 Debug de problemas na API
- 🧹 Após limpar o banco de dados
- 🔧 Verificar se tudo está funcionando
