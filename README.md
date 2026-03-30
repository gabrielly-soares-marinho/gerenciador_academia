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
- Permite criar uma nova conta
- Campos obrigatórios:
    Nome
    Email
    Senha
- Validação de campos vazios
- Salva os dados no banco de dados MySQL
- Redireciona para tela de login após cadastro

## 🔐 Login
- Autentica o usuário com:
    Email
    Senha
- Verifica os dados no banco
- Em caso de sucesso:
    Salva o usuário no localStorage
    Redireciona para o dashboard
- Em caso de erro:
    Exibe mensagem de credenciais inválidas

## 📋 Listar Usuários
- Busca todos os usuários cadastrados no banco
- Exibe na tela ao clicar em "Carregar"
- Mostra:
    Nome
    Email
- Atualiza a lista dinamicamente

## 🏠 Dashboard
- Exibe nome do usuário logado
- Simula funcionalidades:
    Treinos
    Agendamentos
    Progresso
    Planos
- Permite:
    Atualizar dados
    Deletar conta
    Logout

## ✏️ Atualizar Usuário
- Permite editar:
    Nome
    Email
    Senha
- Utiliza o ID do usuário logado
- Atualiza os dados no banco de dados
- Atualiza também os dados no localStorage
- Exibe mensagem de sucesso ou erro

## 🚪 Logout
- Remove usuário da sessão
- Redireciona para login

## 🗑️ Deletar Usuário
- Permite excluir a conta do usuário logado
- Solicita confirmação antes da exclusão
- Remove o usuário do banco de dados
- Em caso de sucesso:
    Remove o usuário do localStorage
   Redireciona para tela de login
- Exibe mensagem de sucesso ou erro

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
POST /cadastrar
http://localhost:5000/cadastrar

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
GET /listar
http://localhost:5000/listar

Resposta:
[
  {
    "id": 1,
    "nome": "Gabi",
    "email": "gabi@email.com"
  }
]

---

## 🔐 Login
POST /login
http://localhost:5000/login

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

## ✏️ Atualizar Usuário
PUT /atualizar/id
http://localhost:5000/atualizar/13

{
  "nome": "Novo Nome",
  "email": "novo@gmail.com",
  "senha": "999999"
}

Resposta:
{
    "mensagem": "Usuário atualizado com sucesso!"
}

## 🗑️ Deletar Usuário
DELETE /deletar/id
http://localhost:5000/deletar/13

Resposta:
{
    "mensagem": "Usuário deletado com sucesso!"
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

- Cadastro → Listar → Login → Dashboard → Atualizar → Deletar
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
