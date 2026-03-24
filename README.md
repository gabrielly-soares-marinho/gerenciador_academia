# 🏋️‍♂️ Olympus Gym - Sistema de Gerenciamento de Academia

Sistema web desenvolvido com **Flask + MySQL + Docker**, com funcionalidades de cadastro, login e dashboard de usuários.

---

# 🚀 Tecnologias Utilizadas

- Python (Flask)
- MySQL
- Docker & Docker Compose
- HTML, CSS, JavaScript
- Flask-CORS

---

# 📁 Estrutura do Projeto

gerenciador_academia/

├── backend/  
│   ├── app.py  
│   ├── requirements.txt  

├── frontend/  
│   ├── cadastro.html  
│   ├── login.html  
│   ├── dashboard.html  
│   ├── js/  
│   │   └── script.js  
│   ├── css/  
│   │   └── style.css  

├── docker-compose.yml  
└── Dockerfile  

---

# ⚙️ Como Rodar o Projeto

## 🔥 1. Clonar o repositório

git clone <seu-repositorio>  
cd gerenciador_academia  

---

## 🐳 2. Subir o Docker

docker-compose up --build  

---

## 🌐 3. Acessar o sistema

Abra no navegador:

http://localhost:5500/frontend/login.html  

(ou use Live Server no VS Code)

---

# 🧠 Funcionalidades

## 👤 Cadastro de Usuário
- Nome, email e senha
- Dados salvos no banco MySQL

## 🔐 Login
- Validação de credenciais
- Retorno de dados do usuário
- Armazenamento no localStorage

## 🏠 Dashboard
- Exibe nome do usuário logado
- Simula funcionalidades:
  - Treinos
  - Agendamentos
  - Progresso
  - Planos

## 🚪 Logout
- Remove usuário da sessão
- Redireciona para login

## 🔒 Proteção de Rotas
- Dashboard só acessível se estiver logado

---

# 🔗 Rotas da API

## 📍 Rota Inicial
GET /

Resposta:
API rodando 🚀

---

## 👤 Criar Usuário
POST /usuarios

Body:
{
  "nome": "Gabi",
  "email": "gabi@email.com",
  "senha": "123"
}

Resposta:
{
  "mensagem": "Usuário cadastrado com sucesso!"
}

---

## 📋 Listar Usuários
GET /usuarios

Resposta:
[
  {
    "id": 1,
    "nome": "Gabi",
    "email": "gabi@email.com"
  }
]

👉 Como acessar no navegador:
http://localhost:5000/usuarios

---

## 🔐 Login
POST /login

Body:
{
  "email": "gabi@email.com",
  "senha": "123"
}

Resposta:
{
  "mensagem": "Login realizado com sucesso!",
  "usuario": {
    "id": 1,
    "nome": "Gabi",
    "email": "gabi@email.com"
  }
}

---

# 🗄️ Banco de Dados (MySQL)

## Criar banco:
CREATE DATABASE academia;

## Criar tabela:
USE academia;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    senha VARCHAR(100)
);

---

# ⚠️ Observações

- Backend roda na porta 5000
- Frontend pode ser aberto com Live Server
- Banco roda via Docker
- Não precisa instalar MySQL localmente

---

# 🧪 Testes

- Cadastro → Login → Dashboard
- Pode usar Postman para testar API

---

# 💡 Melhorias Futuras

- Autenticação com JWT
- Criptografia de senha
- CRUD completo
- Dashboard com gráficos

---

Membros do projeto
------------------

- Emilly Silva Eduardo Pereira - RA 2403751
- Gabrielly Soares Marinho - RA 2403430
- Maurício Monteiro Filho - RA 2302967
