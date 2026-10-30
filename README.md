# 🏋️ Olympus Gym — Sistema de Gerenciamento de Academia

## 📖 Sobre o Projeto

O **Olympus Gym** é um sistema web de gerenciamento de academia, desenvolvido como projeto acadêmico. Seu objetivo é oferecer aos alunos uma plataforma para acompanhar sua rotina de atividades físicas, gerenciar planos, realizar agendamentos e monitorar sua evolução.

O sistema reúne funcionalidades de cadastro, autenticação, contratação de planos, pagamentos simulados, agendamento de aulas, treinos, progresso físico, desafios, check-in de presença e notificações.

A aplicação possui uma interface com identidade visual em preto e dourado, desenvolvida para transmitir modernidade, força e sofisticação.

---

## 🎯 Objetivos do Sistema

- Facilitar o gerenciamento das atividades dos alunos.
- Permitir que os usuários consultem e escolham planos.
- Organizar os agendamentos de aulas.
- Registrar treinos concluídos.
- Acompanhar a evolução física e a frequência.
- Incentivar a participação por meio de desafios e metas.
- Centralizar avisos e notificações dentro da plataforma.

---

## 🚀 Tecnologias Utilizadas

### Backend
- Python 3
- Flask
- Flask-CORS
- MySQL Connector Python

### Frontend
- HTML5
- CSS3
- JavaScript

### Banco de Dados
- MySQL 8

### Infraestrutura
- Docker
- Docker Compose

### Ferramentas utilizadas
- Visual Studio Code
- MySQL
- Docker Desktop
- Git e GitHub
- Postman (para testes de API)

---

# 📁 Estrutura do Projeto

```text
gerenciador_academia/
│
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.py
├── README.md
│
├── backend/
│   ├── app.py
│   ├── database.py
│   └── models.py
│
└── frontend/
    │
    ├── index.html
    ├── login.html
    ├── cadastro.html
    ├── dashboard.html
    ├── planos.html
    ├── pagamento-pix.html
    ├── pagamentos.html
    ├── agendamentos.html
    ├── avaliar-aula.html
    ├── treinos.html
    ├── progresso.html
    ├── calculadora.html
    ├── quiz-treino.html
    ├── streak.html
    ├── desafios.html
    ├── checkin.html
    ├── notificacoes.html
    │
    ├── css/
    │   └── style.css
    │
    ├── js/
    │   ├── script.js
    │   ├── agendamentos.js
    │   ├── avaliar-aula.js
    │   ├── calculadora.js
    │   ├── desafios.js
    │   ├── pagamentos.js
    │   ├── pix.js
    │   ├── progresso.js
    │   ├── quiz-treino.js
    │   ├── streak.js
    │   └── treinos.js
    │
    └── img/
        ├── academia.jpeg
        ├── app.png
        ├── hero.jpeg
        ├── logo.png
        └── treino.jpeg
```

*Observação: a estrutura representa os arquivos do projeto identificados durante o desenvolvimento. Caso algum arquivo tenha sido renomeado ou ainda não esteja na pasta, ajuste a listagem para refletir a versão atual do repositório.*

---

# 🖥️ Como o Sistema Funciona

O Olympus Gym utiliza uma arquitetura dividida em três partes:

### 1. Frontend

É a parte visual do sistema, com a qual o usuário interage.

Desenvolvida em HTML, CSS e JavaScript, apresenta as páginas, formulários, botões, cartões e informações do aluno.

### 2. Backend

É responsável pelo processamento das informações.

Desenvolvido em Python com Flask, recebe as solicitações do frontend, valida os dados, executa operações no banco e retorna respostas em JSON.

### 3. Banco de Dados

Utiliza MySQL para armazenar as informações dos usuários, planos, pagamentos, aulas, agendamentos, treinos, avaliações, desafios, check-ins e notificações.

### Fluxo de funcionamento

```text
        USUÁRIO
           |
           v
       FRONTEND
     HTML / CSS / JS
           |
           v
       API FLASK
        PYTHON
           |
           v
       MYSQL
      BANCO DE DADOS
           |
           v
     RESPOSTA EM JSON
           |
           v
       FRONTEND
    ATUALIZA A TELA
```

---

# 📱 Funcionalidades do Sistema

## 1. Página Inicial — Home

Arquivo: `index.html`

É a página de apresentação da Olympus Gym.

Apresenta a identidade visual da academia, imagens, informações institucionais e opções de navegação.

Permite ao visitante:
- Conhecer a academia.
- Visualizar informações sobre a Olympus.
- Consultar os planos.
- Acessar a tela de login.
- Realizar um novo cadastro.

## 2. Cadastro de Usuário

Arquivo: `cadastro.html`

Permite que novos alunos criem uma conta na plataforma.

O usuário informa:
- Nome.
- E-mail.
- Senha.

O JavaScript envia os dados para o backend, que realiza a validação e salva o cadastro no MySQL.

Rota utilizada:

`POST /cadastrar`

## 3. Login

Arquivo: `login.html`

Permite que o aluno entre no sistema utilizando seu e-mail e senha.

O backend verifica as informações no banco de dados.

Quando o login é realizado com sucesso:
- O sistema recebe os dados do usuário.
- O JavaScript armazena os dados retornados no `localStorage`.
- O usuário é direcionado ao dashboard.

Rota utilizada:

`POST /login`

## 4. Dashboard — Painel do Aluno

Arquivo: `dashboard.html`

É o painel principal do usuário após realizar o login.

Centraliza o acesso às funcionalidades da plataforma.

O dashboard apresenta:
- Treinos.
- Agendamentos.
- Progresso.
- Calculadora física.
- Planos.
- Quiz de treino ideal.
- Sequência de treinos.
- Desafios.
- Check-in.
- Notificações.
- Edição de perfil.
- Exclusão de conta.
- Logout.

Também apresenta o nome do aluno e as informações do plano contratado.

## 5. Planos

Arquivo: `planos.html`

Permite que o aluno conheça e escolha um dos planos disponíveis.

O sistema trabalha com três opções:

| Plano | Valor mensal | Benefícios |
|---|---:|---|
| Básico | R$ 49,00 | Acesso limitado à academia |
| Intermediário | R$ 79,00 | Acesso e aulas em grupo |
| Premium | R$ 119,00 | Acesso total e personal trainer |

Ao selecionar um plano, o JavaScript armazena temporariamente a escolha e encaminha o usuário para a página de pagamento.

A escolha do plano é vinculada ao cadastro do aluno no banco de dados.

## 6. Pagamentos

Arquivos:
- `pagamentos.html`
- `pagamento-pix.html`
- `js/pagamentos.js`
- `js/pix.js`

O módulo de pagamentos permite registrar operações relacionadas aos planos.

O fluxo de pagamento PIX é simulado para fins acadêmicos.

O funcionamento previsto é:
1. O aluno seleciona um plano.
2. O sistema apresenta os dados do pagamento.
3. A interface disponibiliza o QR Code e/ou código PIX.
4. O usuário realiza a confirmação simulada.
5. O sistema registra ou atualiza as informações correspondentes.

Rotas utilizadas:

- `POST /pagar`
- `GET /pagamentos/<usuario_id>`
- `POST /pagar-plano`

**Importante:** o projeto não possui integração bancária ou confirmação real junto a uma instituição financeira. O pagamento é uma simulação dentro da aplicação.

## 7. Agendamentos de Aulas

Arquivo: `agendamentos.html`

Permite que os alunos consultem as aulas disponíveis e realizem agendamentos.

O sistema apresenta modalidades como:

- Dança.
- Yoga.
- Alongamento.
- HIIT.
- Pilates.
- Funcional.
- Jump.
- Abdômen.
- Mobilidade.
- Sertanejo.

O aluno pode:
1. Consultar as aulas.
2. Escolher uma modalidade.
3. Realizar o agendamento.
4. Consultar seus agendamentos.
5. Cancelar um agendamento.

O backend registra o vínculo entre o usuário e a aula escolhida.

Rotas utilizadas:

- `GET /aulas`
- `POST /agendar`
- `GET /meus-agendamentos/<usuario_id>`
- `DELETE /cancelar-agendamento`

## 8. Avaliação de Aulas

Arquivo: `avaliar-aula.html`

Permite que o aluno avalie uma aula que tenha agendado.

O usuário pode:
- Atribuir uma nota de 1 a 5 estrelas.
- Escrever um comentário.
- Consultar suas avaliações anteriores.

O backend verifica se o usuário possui agendamento para aquela aula e impede que a mesma aula seja avaliada novamente pelo mesmo usuário.

Rotas utilizadas:

- `POST /avaliar-aula`
- `GET /minhas-avaliacoes/<usuario_id>`

## 9. Treinos

Arquivo: `treinos.html`

Apresenta os treinos disponibilizados na plataforma.

O aluno pode iniciar uma atividade e registrar sua conclusão.

Quando o treino é concluído, o backend:
- Registra o treino no histórico.
- Atualiza a quantidade de treinos concluídos.
- Atualiza o percentual de progresso.
- Verifica os desafios ativos do usuário.
- Pode gerar notificações relacionadas à conclusão e às metas.

Rotas utilizadas:

- `POST /concluir-treino`
- `GET /historico-treinos/<usuario_id>`

## 10. Progresso

Arquivo: `progresso.html`

Permite que o aluno acompanhe sua evolução física e seus resultados.

O módulo trabalha com informações como:
- Peso corporal.
- Massa muscular.
- Gordura corporal.
- Quantidade de treinos concluídos.
- Percentual de progresso.

O histórico de treinos concluídos alimenta o acompanhamento da evolução.

Rota utilizada:

- `GET /progresso/<usuario_id>`

O progresso é armazenado no banco de dados para que as informações possam ser consultadas posteriormente.

## 11. Calculadora Física — IMC e TMB

Arquivo: `calculadora.html`

Permite que o usuário informe seus dados físicos para obter cálculos de referência.

Dados utilizados:
- Peso.
- Altura.
- Idade.
- Gênero.

O sistema calcula:

**IMC — Índice de Massa Corporal**

Utilizado para apresentar uma classificação de acordo com o resultado calculado.

**TMB — Taxa Metabólica Basal**

Calculada utilizando a fórmula de Mifflin-St Jeor.

O sistema também apresenta uma recomendação geral de atividade física conforme a classificação obtida.

Os resultados são armazenados na tabela de avaliações físicas.

Rotas utilizadas:

- `POST /calcular-imc`
- `GET /avaliacao-fisica/<usuario_id>`

*Os resultados são informativos e não substituem uma avaliação realizada por um profissional de saúde.*

## 12. Quiz — Descubra seu Treino Ideal

Arquivo: `quiz-treino.html`

É uma funcionalidade interativa que ajuda o aluno a encontrar uma modalidade de treino de acordo com suas respostas.

O quiz considera:
- Objetivo do aluno.
- Preferência de atividade.
- Nível de experiência.

Com base nas respostas, o backend define uma modalidade recomendada e apresenta uma orientação.

Entre as possibilidades estão:
- Musculação.
- HIIT.
- Funcional.
- Cardio.
- Yoga e Pilates.

O resultado é armazenado para consulta posterior.

Rotas utilizadas:

- `POST /quiz-treino`
- `GET /quiz-treino/<usuario_id>`

## 13. Sequência de Treinos — Streak

Arquivo: `streak.html`

A funcionalidade de sequência acompanha os dias consecutivos em que o aluno concluiu treinos.

O sistema consulta as datas registradas no histórico de treinos e calcula a sequência atual.

A intenção é incentivar a regularidade e a disciplina dos alunos.

Rota utilizada:

- `GET /streak/<usuario_id>`

O cálculo utiliza os registros da tabela `treinos_concluidos`, não uma tabela independente de sequência.

## 14. Desafios

Arquivo: `desafios.html`

Permite que os alunos participem de desafios de atividade física.

Os desafios possuem informações como:
- Título.
- Descrição.
- Meta.
- Tipo.
- Pontuação.
- Status.

O aluno pode entrar em um desafio e acompanhar seu progresso.

O backend atualiza o progresso com base nos registros de treinos e na sequência de atividades.

Quando a meta é atingida:
- O desafio é marcado como concluído.
- A data de conclusão é registrada.
- Uma notificação de conclusão pode ser criada.

O sistema não utiliza apenas o valor enviado pelo navegador como comprovação de conclusão: o backend recalcula o progresso utilizando os dados armazenados no banco.

Rotas utilizadas:

- `GET /desafios`
- `POST /desafios/participar`
- `GET /meus-desafios/<usuario_id>`
- `PUT /desafios/progresso`

## 15. Check-in de Presença

Arquivo: `checkin.html`

Permite que o aluno registre sua presença na academia.

Ao clicar em **Registrar meu check-in**, o sistema:
1. Identifica o usuário conectado.
2. Envia a solicitação ao backend.
3. Verifica se já existe um check-in naquele dia.
4. Registra a data e o horário da presença.
5. Atualiza o histórico e os indicadores.

O sistema permite um check-in por usuário por dia.

A página apresenta:
- Botão para registrar presença.
- Total de presenças no mês.
- Total geral de presenças.
- Histórico de frequência.

Rotas utilizadas:

- `POST /checkin`
- `GET /checkins/<usuario_id>`

## 16. Notificações

Arquivo: `notificacoes.html`

Centraliza os avisos relacionados às atividades do aluno dentro da plataforma.

As notificações são armazenadas no banco de dados e podem ser consultadas pelo usuário.

A página apresenta:
- Título da notificação.
- Mensagem.
- Data e horário.
- Status de leitura.

O sistema permite:
- Consultar notificações.
- Identificar notificações não lidas.
- Marcar uma notificação como lida.
- Marcar todas como lidas.
- Visualizar o contador de notificações não lidas no dashboard.

### Notificações automáticas já integradas ao backend

- Agendamento de aula realizado.
- Treino concluído.
- Participação em desafio.
- Desafio concluído.
- Meta de cinco treinos concluídos e seus múltiplos.

**Observação:** as notificações são internas à plataforma. Não há envio de SMS, WhatsApp, e-mail ou notificações push. O check-in e os pagamentos também não estão integrados a gatilhos automáticos de notificação no código atual.

Rotas utilizadas:

- `GET /notificacoes/<usuario_id>`
- `PUT /notificacoes/<notificacao_id>/lida`
- `PUT /notificacoes/usuario/<usuario_id>/ler-todas`

## 17. Gerenciamento do Perfil

O aluno pode editar seus dados pessoais diretamente pelo dashboard.

Informações disponíveis:
- Nome.
- E-mail.
- Senha.

Também existe a opção de excluir a conta.

Rotas utilizadas:

- `PUT /atualizar/<id>`
- `DELETE /deletar/<id>`

## 18. Logout

A função de logout encerra a sessão mantida no navegador, removendo os dados do usuário do `localStorage` e redirecionando para a tela de login.

---

# 🗄️ Banco de Dados — MySQL

O projeto utiliza o banco de dados:

```sql
academia
```

O banco armazena as informações necessárias para o funcionamento das funcionalidades da aplicação.

## Principais tabelas

| Tabela | Finalidade |
|---|---|
| `usuarios` | Armazena os dados dos alunos e o plano associado. |
| `planos` | Armazena os planos disponíveis. |
| `aulas` | Armazena as modalidades e horários das aulas. |
| `agendamentos` | Relaciona os alunos às aulas agendadas. |
| `pagamentos` | Armazena os registros de pagamentos. |
| `progresso` | Armazena informações de evolução e treinos concluídos. |
| `treinos_concluidos` | Mantém o histórico dos treinos realizados. |
| `avaliacoes_aulas` | Armazena notas e comentários sobre as aulas. |
| `avaliacao_fisica` | Armazena os resultados de IMC e TMB. |
| `quiz_treino` | Armazena as respostas e recomendações do quiz. |
| `desafios` | Armazena os desafios disponíveis. |
| `usuario_desafios` | Relaciona os alunos aos desafios e registra o progresso. |
| `checkins` | Registra as presenças dos alunos. |
| `notificacoes` | Armazena as notificações e seus status de leitura. |

## Relacionamento entre as tabelas

O banco utiliza identificadores para relacionar os dados.

Exemplos:

- Um usuário pode possuir um plano.
- Um usuário pode realizar diversos agendamentos.
- Um agendamento está relacionado a uma aula.
- Um usuário pode possuir vários registros de pagamentos.
- Um usuário pode concluir vários treinos.
- Um usuário pode participar de vários desafios.
- Um usuário pode possuir vários check-ins.
- Um usuário pode receber várias notificações.

### Consultar as tabelas

```sql
USE academia;

SHOW TABLES;
```

### Consultar usuários

```sql
SELECT * FROM usuarios;
```

### Consultar planos

```sql
SELECT * FROM planos;
```

### Consultar agendamentos com nome do aluno e aula

```sql
SELECT
    u.nome AS aluno,
    a.nome AS aula,
    a.horario
FROM agendamentos ag
INNER JOIN usuarios u
    ON ag.usuario_id = u.id
INNER JOIN aulas a
    ON ag.aula_id = a.id;
```

### Consultar notificações

```sql
SELECT
    n.id,
    u.nome AS aluno,
    n.tipo,
    n.titulo,
    n.mensagem,
    n.lida,
    n.data_criacao
FROM notificacoes n
INNER JOIN usuarios u
    ON n.usuario_id = u.id
ORDER BY n.data_criacao DESC;
```

### Consultar check-ins

```sql
SELECT
    u.nome AS aluno,
    c.data_hora
FROM checkins c
INNER JOIN usuarios u
    ON c.usuario_id = u.id
ORDER BY c.data_hora DESC;
```

---

# 🔗 Rotas da API — Flask

O backend disponibiliza rotas REST para comunicação entre o frontend e o banco de dados.

## Usuários

| Método | Rota | Função |
|---|---|---|
| GET | `/` | Verifica se a API está funcionando. |
| POST | `/cadastrar` | Cadastra um usuário. |
| POST | `/login` | Realiza o login. |
| GET | `/listar` | Lista os usuários. |
| GET | `/usuarios/<id>` | Consulta um usuário e seu plano. |
| PUT | `/usuarios/<id>/plano` | Atualiza o plano do usuário. |
| PUT | `/atualizar/<id>` | Atualiza os dados do usuário. |
| DELETE | `/deletar/<id>` | Exclui o usuário. |

## Aulas e agendamentos

| Método | Rota | Função |
|---|---|---|
| GET | `/aulas` | Lista as aulas. |
| POST | `/agendar` | Realiza um agendamento. |
| GET | `/meus-agendamentos/<usuario_id>` | Consulta os agendamentos do aluno. |
| DELETE | `/cancelar-agendamento` | Cancela um agendamento. |

## Pagamentos

| Método | Rota | Função |
|---|---|---|
| POST | `/pagar` | Registra um pagamento. |
| GET | `/pagamentos/<usuario_id>` | Consulta os pagamentos. |
| POST | `/pagar-plano` | Atualiza o plano do usuário após a confirmação simulada. |

## Treinos e progresso

| Método | Rota | Função |
|---|---|---|
| POST | `/concluir-treino` | Registra um treino concluído. |
| GET | `/historico-treinos/<usuario_id>` | Consulta o histórico de treinos. |
| GET | `/progresso/<usuario_id>` | Consulta o progresso do aluno. |
| GET | `/streak/<usuario_id>` | Calcula a sequência de treinos. |

## Avaliações físicas

| Método | Rota | Função |
|---|---|---|
| POST | `/calcular-imc` | Calcula e salva IMC e TMB. |
| GET | `/avaliacao-fisica/<usuario_id>` | Consulta a última avaliação física. |

## Avaliação de aulas

| Método | Rota | Função |
|---|---|---|
| POST | `/avaliar-aula` | Registra uma avaliação. |
| GET | `/minhas-avaliacoes/<usuario_id>` | Consulta as avaliações do aluno. |

## Quiz

| Método | Rota | Função |
|---|---|---|
| POST | `/quiz-treino` | Salva as respostas e recomendação. |
| GET | `/quiz-treino/<usuario_id>` | Consulta o último resultado. |

## Desafios

| Método | Rota | Função |
|---|---|---|
| GET | `/desafios` | Lista os desafios ativos. |
| POST | `/desafios/participar` | Registra a participação. |
| GET | `/meus-desafios/<usuario_id>` | Consulta os desafios do aluno. |
| PUT | `/desafios/progresso` | Recalcula e atualiza o progresso. |

## Check-in

| Método | Rota | Função |
|---|---|---|
| POST | `/checkin` | Registra a presença. |
| GET | `/checkins/<usuario_id>` | Consulta o histórico de presença. |

## Notificações

| Método | Rota | Função |
|---|---|---|
| GET | `/notificacoes/<usuario_id>` | Lista as notificações e o contador de não lidas. |
| PUT | `/notificacoes/<notificacao_id>/lida` | Marca uma notificação como lida. |
| PUT | `/notificacoes/usuario/<usuario_id>/ler-todas` | Marca todas como lidas. |

---

# 🐳 Como Executar o Projeto

## Pré-requisitos

Antes de iniciar, é necessário ter instalado:

- Python 3.
- Docker Desktop.
- Docker Compose.
- Visual Studio Code.
- Navegador atualizado.

## 1. Clonar o repositório

```bash
git clone https://github.com/gabrielly-soares-marinho/gerenciador_academia.git
```

Entrar na pasta:

```bash
cd gerenciador_academia
```

## 2. Iniciar os containers

Na raiz do projeto, execute:

```bash
docker-compose up --build
```

Esse comando constrói a imagem do backend e inicia os serviços configurados no Docker Compose.

O projeto utiliza dois containers principais:

- `olympus_backend`: executa a API Flask.
- `olympus_db`: executa o banco MySQL.

## 3. Verificar os containers

```bash
docker ps
```

Confira se os containers estão em execução.

## 4. Testar o backend

Abra no navegador:

```text
http://localhost:5000
```

Resposta esperada:

```text
API rodando 🚀
```

## 5. Abrir o frontend

Abra a pasta `frontend` no Visual Studio Code.

A página inicial é:

```text
frontend/index.html
```

Uma opção prática é utilizar a extensão Live Server do VS Code para abrir as páginas HTML no navegador.

O backend deverá permanecer em execução para que as funcionalidades que consultam a API funcionem.

## 6. Acessar o MySQL

Para entrar no banco pelo terminal:

```bash
docker exec -it olympus_db mysql -u root -p
```

Senha configurada no ambiente local:

```text
root
```

Selecionar o banco:

```sql
USE academia;
```

Listar as tabelas:

```sql
SHOW TABLES;
```

---

# 🧪 Testes das Funcionalidades

Após iniciar o projeto, é possível testar os principais recursos seguindo esta ordem:

### Teste 1 — Cadastro e login
1. Acesse a página inicial.
2. Clique em cadastro.
3. Crie um usuário.
4. Faça login.
5. Confira se o dashboard é aberto.

### Teste 2 — Planos e pagamento
1. Acesse Planos.
2. Escolha uma opção.
3. Confira os dados do pagamento simulado.
4. Realize a confirmação.
5. Verifique o plano associado ao usuário.

### Teste 3 — Agendamentos
1. Acesse Agendamentos.
2. Consulte as aulas.
3. Escolha uma modalidade.
4. Realize o agendamento.
5. Consulte seus agendamentos.
6. Teste o cancelamento.

### Teste 4 — Treinos e progresso
1. Acesse Treinos.
2. Escolha uma atividade.
3. Conclua o treino.
4. Consulte o histórico.
5. Acesse Progresso.
6. Confira a atualização da quantidade de treinos.

### Teste 5 — Calculadora
1. Acesse a Calculadora.
2. Informe os dados físicos solicitados.
3. Realize o cálculo.
4. Confira os resultados de IMC e TMB.

### Teste 6 — Quiz
1. Acesse Treino Ideal.
2. Responda às perguntas.
3. Confira a modalidade recomendada.
4. Consulte o resultado salvo.

### Teste 7 — Sequência de treinos
1. Conclua treinos em datas diferentes.
2. Acesse Minha Sequência.
3. Confira o cálculo dos dias consecutivos.

### Teste 8 — Desafios
1. Acesse Desafios.
2. Escolha um desafio disponível.
3. Participe.
4. Conclua treinos que contribuam para a meta.
5. Confira a atualização do progresso.

### Teste 9 — Check-in
1. Acesse Check-in.
2. Clique em Registrar meu check-in.
3. Confira a confirmação.
4. Consulte o histórico.
5. Tente registrar novamente no mesmo dia para verificar a proteção contra duplicidade.

### Teste 10 — Notificações
1. Realize um agendamento.
2. Conclua um treino.
3. Entre em um desafio.
4. Acesse Notificações.
5. Confira as mensagens geradas.
6. Marque uma notificação como lida.
7. Teste a opção de marcar todas como lidas.

### Teste 11 — Perfil
1. Acesse o dashboard.
2. Informe os novos dados.
3. Clique em Atualizar.
4. Confira as alterações.
5. Teste o logout.

---

# 🔐 Segurança e Limitações Conhecidas

O Olympus Gym é um projeto acadêmico em desenvolvimento.

Alguns pontos importantes da implementação atual:

- O login utiliza consulta de e-mail e senha no banco.
- Os dados do usuário são mantidos no `localStorage` do navegador.
- A implementação atual não utiliza autenticação JWT.
- As senhas são armazenadas diretamente no banco na versão analisada, sem hash. Isso deve ser corrigido antes de qualquer uso em produção.
- As rotas utilizam o identificador do usuário enviado pelo frontend; ainda é necessário implementar autenticação e autorização robustas no servidor.
- O pagamento PIX é simulado e não possui confirmação bancária real.
- As notificações são exibidas dentro do sistema e não são enviadas por serviços externos.
- O check-in permite um registro por dia por usuário.
- Os lembretes antecipados de aulas ainda não estão implementados, pois o cadastro atual de aulas utiliza horários, sem um calendário de sessões com datas específicas.

As credenciais configuradas no Docker são destinadas ao ambiente local de desenvolvimento e devem ser substituídas por configurações seguras em produção.

---

# 🔮 Melhorias Futuras

Algumas melhorias que podem ampliar o sistema:

- Criar painel administrativo para gerenciamento de alunos.
- Implementar autenticação JWT.
- Armazenar senhas utilizando hash seguro.
- Implementar recuperação de senha.
- Integrar o pagamento a um provedor real.
- Criar calendário com datas e horários das aulas.
- Implementar lembretes automáticos de agendamentos.
- Criar notificações de vencimento de planos.
- Permitir o envio de comunicados para todos os alunos.
- Criar relatórios de frequência e desempenho.
- Melhorar os gráficos de evolução física.
- Implementar notificações push.
- Criar controle de permissões para alunos e administradores.

---

# 👩‍💻 Desenvolvedores

Projeto acadêmico desenvolvido por:

- **Emilly Silva Eduardo Pereira** — RA 2403751
- **Gabrielly Soares Marinho** — RA 2403430
- **Maurício Monteiro Filho** — RA 2302967

**Olympus Gym — Sistema de Gerenciamento de Academia**

Desenvolvido utilizando Python, Flask, MySQL, HTML, CSS, JavaScript e Docker.
