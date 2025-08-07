# Peladas Manager

Um sistema web para organização de peladas (jogos de futebol).

## Tecnologias Utilizadas

### Backend
- Python 3.11+
- FastAPI (framework web moderno e rápido)
- SQLAlchemy (ORM para banco de dados)
- Pydantic (validação de dados)
- SQLite (banco de dados)

### Frontend
- React 18
- TypeScript
- Tailwind CSS
- Vite (build tool)

## Estrutura do Projeto

```
peladas-manager/
├── backend/              # API Python
│   ├── app/
│   │   ├── models/       # Modelos do banco de dados
│   │   ├── routes/       # Rotas da API
│   │   └── main.py       # Arquivo principal
│   ├── requirements.txt  # Dependências Python
│   └── database.db       # Banco SQLite
├── frontend/             # Interface React
│   ├── src/
│   │   ├── components/   # Componentes React
│   │   ├── pages/        # Páginas da aplicação
│   │   └── App.tsx       # Componente principal
│   └── package.json      # Dependências Node.js
└── README.md            # Este arquivo
```

## Funcionalidades Planejadas

- [ ] Cadastro de jogadores
- [ ] Criação de peladas
- [ ] Confirmação de presença
- [ ] Divisão automática de times
- [ ] Histórico de jogos
- [ ] Sistema de avaliação de jogadores

## Como executar

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
