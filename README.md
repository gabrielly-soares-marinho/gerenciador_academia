# 🏋️ Olympus Gym - Sistema de Gerenciamento de Academia

## 📖 Sobre o Projeto

O Olympus Gym e um sistema web desenvolvido para auxiliar no gerenciamento de uma academia.

O sistema permite que usuarios realizem:

- Cadastro
- Login
- Atualizacao de perfil
- Contratacao de planos
- Pagamento via PIX (simulado)
- Agendamento de aulas
- Controle de treinos
- Acompanhamento de progresso

O projeto foi desenvolvido utilizando Flask no backend, MySQL como banco de dados e HTML, CSS e JavaScript no frontend.

---

# 🚀 Tecnologias Utilizadas

## Backend

- Python 3.10
- Flask
- Flask-CORS
- MySQL Connector Python

## Banco de Dados

- MySQL 8

## Frontend

- HTML5
- CSS3
- JavaScript

## Containerizacao

- Docker
- Docker Compose

---

# 📁 Estrutura do Projeto

```text
gerenciador_academia/

│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py
│
├── backend
│   ├── app.py
│   ├── database.py
│   └── models.py
│
└── frontend
    │
    ├── index.html
    ├── login.html
    ├── cadastro.html
    ├── dashboard.html
    ├── planos.html
    ├── pagamentos.html
    ├── pagamento-pix.html
    ├── agendamentos.html
    ├── treinos.html
    ├── progresso.html
    │
    ├── css
    │   └── style.css
    │
    ├── js
    │   ├── script.js
    │   ├── agendamentos.js
    │   ├── pagamentos.js
    │   ├── pix.js
    │   ├── progresso.js
    │   └── treinos.js
    │
    └── img
        ├── academia.jpeg
        ├── hero.jpeg
        ├── treino.jpeg
        ├── logo.png
        ├── app.png
        └── imgqrcode-pix.png
```

---

# ⚙️ Como Executar o Projeto

## Pre-Requisitos

Instalar:

- Git
- Docker Desktop
- Docker Compose

---

## Clonar o Repositorio

```bash
git clone https://github.com/gabrielly-soares-marinho/gerenciador_academia.git

cd gerenciador_academia
```

---

## Construir e Executar os Containers

```bash
docker-compose up --build
```

---

## Verificar Containers

```bash
docker ps
```

Devera aparecer algo semelhante:

```text
olympus_backend
olympus_db
```

---

## Backend

Disponivel em:

```text
http://localhost:5000
```

Teste:

```text
http://localhost:5000
```

Resposta esperada:

```text
API rodando
```

---

## Frontend

Abrir os arquivos HTML da pasta frontend.

Pagina inicial:

```text
frontend/index.html
```

---

# 🗄️ Banco de Dados

Banco utilizado:

```sql
academia
```

---
Entrar no banco:
docker exec -it olympus_db mysql -u root -p
Senha: root
SHOW DATABASES;
USE academia
SHOW TABLES;

## Criar Banco

```sql
DROP DATABASE IF EXISTS academia;

CREATE DATABASE academia;

USE academia;

```

SHOW TABLES;
---

## Tabela Usuarios 

SELECT * FROM usuarios;

```sql
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    senha VARCHAR(100),
    plano_id INT
);
```

---

## Tabela Planos

SELECT * FROM planos;

```sql
CREATE TABLE planos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50),
    descricao VARCHAR(100)
);
```

---

## Tabela Aulas

SELECT * FROM aulas;

```sql
CREATE TABLE aulas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    horario VARCHAR(20)
);
```

---

## Tabela Agendamentos

SELECT * FROM agendamentos;

```sql
CREATE TABLE agendamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    aula_id INT,

    FOREIGN KEY (usuario_id)
    REFERENCES usuarios(id),

    FOREIGN KEY (aula_id)
    REFERENCES aulas(id)
);
```

---

## Tabela Pagamentos

SELECT * FROM pagamentos;

```sql
CREATE TABLE pagamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,

    usuario_id INT NOT NULL,
    plano_id INT NOT NULL,

    valor DECIMAL(10,2) NOT NULL,

    status VARCHAR(20)
    DEFAULT 'Pendente',

    data_pagamento DATETIME,

    FOREIGN KEY (usuario_id)
    REFERENCES usuarios(id),

    FOREIGN KEY (plano_id)
    REFERENCES planos(id)
);
```

---

## Tabela Progresso

SELECT * FROM progresso;

```sql
CREATE TABLE progresso (
    id INT AUTO_INCREMENT PRIMARY KEY,

    usuario_id INT,

    peso DECIMAL(5,2),
    gordura DECIMAL(5,2),
    massa DECIMAL(5,2),

    treinos_concluidos INT DEFAULT 0,

    FOREIGN KEY (usuario_id)
    REFERENCES usuarios(id)
);
```

---

## Tabela Treinos Concluidos

SELECT * FROM treinos_concluidos;

```sql
CREATE TABLE treinos_concluidos (
    id INT AUTO_INCREMENT PRIMARY KEY,

    usuario_id INT,

    treino_nome VARCHAR(100),

    data_conclusao DATETIME,

    FOREIGN KEY (usuario_id)
    REFERENCES usuarios(id)
);
```

---

# 📅 Inserir Aulas

```sql
INSERT INTO aulas (nome, horario) VALUES
('Danca', '08:00'),
('Yoga', '10:00'),
('Alongamento', '14:00'),
('HIIT', '18:00'),
('Pilates', '09:00'),
('Funcional', '11:00'),
('Jump', '15:00'),
('Abdomen', '16:00'),
('Mobilidade', '17:00'),
('Sertanejo', '19:00');
```

---

# 💳 Inserir Planos

```sql
INSERT INTO planos (nome, descricao)
VALUES
('Basico','Acesso limitado a academia'),
('Intermediario','Acesso + aulas em grupo'),
('Premium','Acesso total + personal trainer');
```

---

# 🎯 Funcionalidades

## Usuarios

- Cadastro de usuarios
- Login
- Atualizacao de perfil
- Exclusao de conta

---

## Planos

- Escolha de plano
- Plano ativo no dashboard
- Visualizacao do plano contratado

---

## Pagamentos

- Pagamento PIX simulado
- QR Code PIX
- Copiar codigo PIX
- Confirmacao de pagamento
- Ativacao automatica do plano

---

## Agendamentos

- Listagem de aulas
- Agendamento de aulas
- Cancelamento de agendamentos
- Consulta de agendamentos do usuario

---

## Treinos

- Treinos personalizados
- Iniciar treino
- Concluir treino
- Registro de treinos concluidos

---

## Progresso

- Registro de peso
- Controle de gordura corporal
- Controle de massa muscular
- Quantidade de treinos concluidos
- Historico de evolucao

---

# 🔗 Rotas da API

## Usuarios

```http
POST /cadastrar
```

```http
POST /login
```

```http
GET /listar
```

```http
GET /usuarios/<id>
```

```http
PUT /atualizar/<id>
```

```http
DELETE /deletar/<id>
```

---

## Planos

```http
PUT /usuarios/<id>/plano
```

---

## Aulas

```http
GET /aulas
```

---

## Agendamentos

```http
POST /agendar
```

```http
GET /meus-agendamentos/<usuario_id>
```

```http
DELETE /cancelar-agendamento
```

---

## Pagamentos

```http
POST /pagar
```

```http
POST /pagar-plano
```

---

# 🧪 Testando o Projeto

## Cadastro

1. Abrir cadastro.html
2. Criar um usuario
3. Verificar no banco:

```sql
SELECT * FROM usuarios;
```

---

## Login

1. Fazer login
2. Acessar dashboard

---

## Planos

1. Selecionar um plano
2. Realizar pagamento PIX simulado
3. Confirmar pagamento
4. Verificar plano ativo

---

## Agendamentos

1. Abrir tela de agendamentos
2. Escolher uma aula
3. Agendar
4. Verificar no banco:

```sql
SELECT * FROM agendamentos;
```

---

## Treinos

1. Iniciar treino
2. Concluir treino
3. Verificar progresso

---

# 🔮 Melhorias Futuras

- JWT Authentication
- Upload de foto de perfil
- Recuperacao de senha
- Dashboard administrativo
- Relatorios PDF
- Integracao com PIX real
- Integracao com Mercado Pago
- Graficos de progresso
- Notificacoes de vencimento de plano

---

# 👩‍💻 Desenvolvido por

- Emilly Silva Eduardo Pereira - RA 2403751
- Gabrielly Soares Marinho - RA 2403430
- Maurício Monteiro Filho - RA 2302967

Projeto academico desenvolvido para gerenciamento de academia utilizando Flask, MySQL, Docker e JavaScript.
------------------

