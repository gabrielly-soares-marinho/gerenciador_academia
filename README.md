# Gerenciador de Academia (MVP)

Projeto inicial — backend em Flask, banco MySQL (via Docker) e frontend estático simples.

Como executar (local, sem Docker - rápido para desenvolvimento):

1. Crie e ative um ambiente virtual

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure o banco de dados e migrações

```powershell
$env:DATABASE_URI = "sqlite:///dev.db"
$env:FLASK_APP = "run.py"
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

3. Rode a aplicação

```powershell
python run.py
```

4. Acesse http://localhost:5000

Como executar com Docker (app + MySQL):

```bash
docker compose up --build
```

Endpoints principais:
- `GET /api/health` - health check
- `GET /api/members` - listar membros
- `POST /api/members` - criar membro (json: {name, email, phone})

Próximos passos sugeridos:
- Configurar migrations (`flask db init/migrate/upgrade`) e instruções no README
- Implementar autenticação e autorização
- Adicionar testes e CI

Membros do projeto
------------------

- Emilly Silva Eduardo Pereira - RA 2403751
- Gabrielly Soares Marinho - RA 2403430
- Maurício Monteiro Filho - RA 2302967
