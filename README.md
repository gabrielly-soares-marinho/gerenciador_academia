# Gerenciador de Academia (MVP)

Projeto inicial — backend em Flask, banco MySQL (via Docker) e frontend estático simples.

Como executar (local, sem Docker - rápido para desenvolvimento):

1. Crie e ative um ambiente virtual

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure o banco de dados e migrações (mesmo para local ou docker)

```powershell
#& ".\.venv\Scripts\flask.exe" db migrate -m "initial migration"
# se usando local com MySQL rodando na porta 3307 (docker-compose atual)
$env:DATABASE_URI = "mysql+pymysql://root:password@localhost:3307/academia"
$env:FLASK_APP = "run.py"
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

3. Opção A: Rode a aplicação local (sem Docker)

```powershell
python run.py
```

- URL local (app flask): http://localhost:5000
- Endpoints locais:
  - http://localhost:5000/api/health
  - http://localhost:5000/api/db-check
  - http://localhost:5000/api/members

4. Opção B: Rode com Docker (app + MySQL)

```bash
docker compose up --build -d
# aguarde o container iniciar e então:
docker compose exec app flask db upgrade
```

- URL docker: http://localhost:5001
- Endpoints docker:
  - http://localhost:5001/api/health
  - http://localhost:5001/api/db-check
  - http://localhost:5001/api/members

5. Testar cadastro

```powershell
curl.exe -X POST "http://localhost:5001/api/members" `
  -H "Content-Type: application/json" `
  -d '{"name":"NOME","email":"email@x.com","phone":"123456"}'

curl.exe "http://localhost:5001/api/members"
```

6. Verificar dados no MySQL

```bash
docker compose exec db mysql -uroot -ppassword -e "USE academia; SELECT * FROM member;"
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
