# 🏋️‍♂️ Olympus Gym - Sistema de Gerenciamento de Academia

Sistema web desenvolvido com **Flask + MySQL + Docker**, com funcionalidades de cadastro, login, dashboard de usuários e logout.

---

# 🚀 Tecnologias Utilizadas

- Python (Flask)
- MySQL
- Docker & Docker Compose
- HTML, CSS, JavaScript
- Flask-CORS

---

# ⚙️ Como Rodar o Projeto

## 🔥 1. Clonar o repositório

git clone (https://github.com/gabrielly-soares-marinho/gerenciador_academia.git) 
cd gerenciador_academia  

---

## 🐳 2. Subir o Docker

docker-compose up --build  

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
  "email": "gabi@gmail.com",
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
  "email": "gabi@gmail.com",
  "senha": "123"
}

Resposta:
{
  "mensagem": "Login realizado com sucesso!",
  "usuario": {
    "id": 1,
    "nome": "Gabi",
    "email": "gabi@gmail.com"
  }
}

---

# 🗄️ Banco de Dados (MySQL)

Entrar no MYSQL:
docker exec -it olympus_db mysql -u root -p

Digite a senha:
root

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

Testar se funcionou:
SHOW DATABASES;

USE academia;

SHOW TABLES;

Deve aparecer:
usuarios

Inserir um usuario (TESTE):
INSERT INTO usuarios (nome, email, senha)
VALUES ('Gabi', 'gabi@gmail.com', '123456');

Ver dados:
SELECT * FROM usuarios;

Vai aparecer algo assim:

1 | Gabi | gabi@email.com | 123456


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
