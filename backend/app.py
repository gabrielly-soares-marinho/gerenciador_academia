from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)

# 🔥 Libera acesso do frontend
CORS(app)

# 🔗 Conexão com MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="db",
        user="root",
        password="root",
        database="academia"
    )

# 🚀 Rota inicial
@app.route("/")
def home():
    return "API rodando 🚀"


# 👤 CADASTRO
@app.route("/cadastrar", methods=["POST"])
def criar_usuario():
    try:
        data = request.get_json()

        nome = data.get("nome")
        email = data.get("email")
        senha = data.get("senha")

        if not nome or not email or not senha:
            return jsonify({"erro": "Preencha todos os campos"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha)
            VALUES (%s, %s, %s)
        """, (nome, email, senha))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensagem": "Usuário cadastrado com sucesso!"}), 201

    except Exception as e:
        print("ERRO:", e)
        return jsonify({"erro": "Erro ao cadastrar"}), 500


# 🔐 LOGIN
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        email = data.get("email")
        senha = data.get("senha")

        if not email or not senha:
            return jsonify({"erro": "Preencha email e senha"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, nome, email FROM usuarios WHERE email=%s AND senha=%s",
            (email, senha)
        )

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario:
            return jsonify({
                "mensagem": "Login realizado com sucesso!",
                "usuario": {
                    "id": usuario[0],
                    "nome": usuario[1],
                    "email": usuario[2]
                }
            }), 200
        else:
            return jsonify({"erro": "Email ou senha inválidos"}), 401

    except Exception as e:
        print("ERRO:", e)
        return jsonify({"erro": "Erro no login"}), 500


# 📋 LISTAR USUÁRIOS
@app.route("/listar", methods=["GET"])
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, email FROM usuarios")
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify([
        {"id": u[0], "nome": u[1], "email": u[2]}
        for u in usuarios
    ])


# 🔍 BUSCAR USUÁRIO COM PLANO
@app.route("/usuarios/<int:id>", methods=["GET"])
def buscar_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT u.id, u.nome, u.email, u.plano_id, p.nome, p.descricao
        FROM usuarios u
        LEFT JOIN planos p ON u.plano_id = p.id
        WHERE u.id = %s
    """, (id,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({
            "id": user[0],
            "nome": user[1],
            "email": user[2],
            "plano_id": user[3],
            "plano_nome": user[4],
            "plano_descricao": user[5]
        })

    return jsonify({"erro": "Usuário não encontrado"}), 404


# 🎯 ESCOLHER PLANO (AGORA FUNCIONA)
@app.route("/usuarios/<int:id>/plano", methods=["PUT"])
def escolher_plano(id):
    try:
        data = request.get_json()
        plano_id = data.get("plano_id")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE usuarios SET plano_id = %s WHERE id = %s
        """, (plano_id, id))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"mensagem": "Plano atualizado!"})

    except Exception as e:
        print("ERRO:", e)
        return jsonify({"erro": "Erro ao atualizar plano"}), 500


# ✏️ ATUALIZAR USUÁRIO
@app.route('/atualizar/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    try:
        data = request.get_json()

        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')

        if not nome or not email or not senha:
            return jsonify({"erro": "Preencha todos os campos"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE usuarios
            SET nome = %s,
                email = %s,
                senha = %s
            WHERE id = %s
        """, (nome, email, senha, id))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"mensagem": "Usuário atualizado com sucesso!"})

    except Exception as e:
        print("ERRO:", e)
        return jsonify({"erro": "Erro ao atualizar usuário"}), 500


# 🗑️ DELETAR USUÁRIO
@app.route('/deletar/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"mensagem": "Usuário deletado com sucesso!"})

    except Exception as e:
        print("ERRO:", e)
        return jsonify({"erro": "Erro ao deletar usuário"}), 500

# 📚 LISTAR AULAS
@app.route("/aulas", methods=["GET"])
def listar_aulas():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM aulas")
    aulas = cursor.fetchall()

    cursor.close()
    conn.close()

    resultado = []
    for a in aulas:
        resultado.append({
            "id": a[0],
            "nome": a[1],
            "horario": a[2]
        })

    return jsonify(resultado)


# 📅 AGENDAR AULA
@app.route("/agendar", methods=["POST"])
def agendar():
    data = request.get_json()

    usuario_id = data.get("usuario_id")
    aula_id = data.get("aula_id")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO agendamentos (usuario_id, aula_id)
        VALUES (%s, %s)
    """, (usuario_id, aula_id))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensagem": "Agendamento realizado com sucesso!"})


# 📋 MEUS AGENDAMENTOS
@app.route("/meus-agendamentos/<int:usuario_id>", methods=["GET"])
def meus_agendamentos(usuario_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT a.nome, a.horario, a.id
        FROM agendamentos ag
        JOIN aulas a ON ag.aula_id = a.id
        WHERE ag.usuario_id = %s
    """, (usuario_id,))

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    resultado = []
    for d in dados:
        resultado.append({
            "id": d[2],
            "nome": d[0],
            "horario": d[1]
        })

    return jsonify(resultado)

@app.route("/cancelar-agendamento", methods=["DELETE"])
def cancelar_agendamento():
    data = request.get_json()

    usuario_id = data.get("usuario_id")
    aula_id = data.get("aula_id")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM agendamentos
        WHERE usuario_id = %s AND aula_id = %s
    """, (usuario_id, aula_id))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"mensagem": "Agendamento cancelado com sucesso!"})

# 💳 REALIZAR PAGAMENTO
@app.route("/pagar", methods=["POST"])
def pagar():

    try:

        data = request.get_json()

        usuario_id = data.get("usuario_id")
        plano_id = data.get("plano_id")
        valor = data.get("valor")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO pagamentos
            (usuario_id, plano_id, valor, status, data_pagamento)

            VALUES
            (%s, %s, %s, 'Pago', NOW())
        """,
        (
            usuario_id,
            plano_id,
            valor
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "mensagem": "Pagamento realizado com sucesso!"
        })

    except Exception as e:

        print("ERRO:", e)

        return jsonify({
            "erro": "Erro ao processar pagamento"
        }), 500

# 📋 LISTAR PAGAMENTOS
@app.route("/pagamentos/<int:usuario_id>", methods=["GET"])
def listar_pagamentos(usuario_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.id,
            p.valor,
            p.status,
            p.data_pagamento,
            pl.nome

        FROM pagamentos p

        JOIN planos pl
        ON p.plano_id = pl.id

        WHERE p.usuario_id = %s
    """, (usuario_id,))

    pagamentos = cursor.fetchall()

    cursor.close()
    conn.close()

    resultado = []

    for p in pagamentos:

        resultado.append({
            "id": p[0],
            "valor": float(p[1]),
            "status": p[2],
            "data": str(p[3]),
            "plano": p[4]
        })

    return jsonify(resultado)

# 💳 CONFIRMAR PAGAMENTO
@app.route("/pagar-plano", methods=["POST"])
def pagar_plano():

    try:

        data = request.get_json()

        usuario_id = data.get("usuario_id")
        plano_id = data.get("plano_id")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE usuarios
            SET plano_id = %s
            WHERE id = %s
        """, (plano_id, usuario_id))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "mensagem":
            "Pagamento confirmado e plano ativado!"
        })

    except Exception as e:

        print(e)

        return jsonify({
            "erro":"Erro ao processar pagamento"
        }), 500


# 📊 BUSCAR PROGRESSO
@app.route("/progresso/<int:usuario_id>", methods=["GET"])
def buscar_progresso(usuario_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            treinos_concluidos,
            percentual
        FROM progresso
        WHERE usuario_id = %s
    """, (usuario_id,))

    progresso = cursor.fetchone()

    cursor.close()
    conn.close()

    if progresso:

        return jsonify({
            "treinos": progresso[0],
            "percentual": progresso[1]
        })

    return jsonify({
        "treinos": 0,
        "percentual": 0
    })

# 💪 CONCLUIR TREINO
@app.route("/concluir-treino", methods=["POST"])
def concluir_treino():
    try:
        data = request.get_json() or {}

        usuario_id = data.get("usuario_id")
        treino = data.get("treino")

        if not usuario_id or not treino:
            return jsonify({
                "erro": "Usuário e treino são obrigatórios"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Salva o treino real no histórico.
        cursor.execute("""
            INSERT INTO treinos_concluidos
            (usuario_id, treino_nome)
            VALUES (%s, %s)
        """, (
            usuario_id,
            treino
        ))

        # Atualiza o progresso geral do usuário.
        cursor.execute("""
            SELECT id, treinos_concluidos
            FROM progresso
            WHERE usuario_id = %s
        """, (usuario_id,))

        progresso = cursor.fetchone()

        if progresso:
            novo_total = progresso[1] + 1

            percentual = int((novo_total / 20) * 100)

            if percentual > 100:
                percentual = 100

            cursor.execute("""
                UPDATE progresso
                SET treinos_concluidos = %s,
                    percentual = %s
                WHERE usuario_id = %s
            """, (
                novo_total,
                percentual,
                usuario_id
            ))

        else:
            cursor.execute("""
                INSERT INTO progresso
                (
                    usuario_id,
                    treinos_concluidos,
                    carga_total,
                    peso,
                    percentual
                )
                VALUES
                (
                    %s,
                    1,
                    0,
                    0,
                    5
                )
            """, (usuario_id,))

        # IMPORTANTE: os desafios são atualizados automaticamente
        # a partir dos treinos realmente registrados no banco.
        desafios_atualizados = atualizar_desafios_automaticamente(
            cursor,
            usuario_id
        )

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "mensagem": "Treino salvo com sucesso!",
            "desafios_atualizados": desafios_atualizados
        }), 200

    except Exception as e:
        print("ERRO AO CONCLUIR TREINO:", e)

        return jsonify({
            "erro": "Erro ao salvar treino"
        }), 500


# HISTORICO DE TREINOS
@app.route("/historico-treinos/<int:usuario_id>", methods=["GET"])
def historico_treinos(usuario_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT treino_nome, data_conclusao
        FROM treinos_concluidos
        WHERE usuario_id = %s
        ORDER BY data_conclusao DESC
    """, (usuario_id,))

    treinos = cursor.fetchall()

    cursor.close()
    conn.close()

    resultado = []

    for treino in treinos:

        resultado.append({
            "treino": treino[0],
            "data": str(treino[1])
        })

    return jsonify(resultado)

# ==========================================================
# ⭐ AVALIAR AULA
# ==========================================================

@app.route("/avaliar-aula", methods=["POST"])
def avaliar_aula():

    try:

        data = request.get_json()

        usuario_id = data.get("usuario_id")
        aula_id = data.get("aula_id")
        nota = data.get("nota")
        comentario = data.get("comentario")

        # Verifica dados obrigatórios
        if not usuario_id or not aula_id or not nota:

            return jsonify({
                "erro": "Preencha todos os campos obrigatórios"
            }), 400

        # Verifica se a nota é válida
        if int(nota) < 1 or int(nota) > 5:

            return jsonify({
                "erro": "A nota deve estar entre 1 e 5"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verifica se o usuário realmente agendou essa aula
        cursor.execute("""
            SELECT id
            FROM agendamentos
            WHERE usuario_id = %s
            AND aula_id = %s
        """, (
            usuario_id,
            aula_id
        ))

        agendamento = cursor.fetchone()

        if not agendamento:

            cursor.close()
            conn.close()

            return jsonify({
                "erro": "Você precisa ter agendado esta aula para avaliá-la."
            }), 403

        # Verifica se já avaliou
        cursor.execute("""
            SELECT id
            FROM avaliacoes_aulas
            WHERE usuario_id = %s
            AND aula_id = %s
        """, (
            usuario_id,
            aula_id
        ))

        avaliacao_existente = cursor.fetchone()

        if avaliacao_existente:

            cursor.close()
            conn.close()

            return jsonify({
                "erro": "Você já avaliou esta aula."
            }), 409

        # Salva avaliação
        cursor.execute("""
            INSERT INTO avaliacoes_aulas
            (
                usuario_id,
                aula_id,
                nota,
                comentario,
                data_avaliacao
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                NOW()
            )
        """, (
            usuario_id,
            aula_id,
            nota,
            comentario
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "mensagem": "Avaliação enviada com sucesso!"
        }), 201

    except Exception as e:

        print("ERRO AO AVALIAR AULA:", e)

        return jsonify({
            "erro": "Erro ao salvar avaliação"
        }), 500


# ==========================================================
# ⭐ LISTAR AVALIAÇÕES DO USUÁRIO
# ==========================================================

@app.route("/minhas-avaliacoes/<int:usuario_id>", methods=["GET"])
def minhas_avaliacoes(usuario_id):

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                av.id,
                av.nota,
                av.comentario,
                av.data_avaliacao,
                a.nome,
                a.horario

            FROM avaliacoes_aulas av

            JOIN aulas a
            ON av.aula_id = a.id

            WHERE av.usuario_id = %s

            ORDER BY av.data_avaliacao DESC
        """, (
            usuario_id,
        ))

        avaliacoes = cursor.fetchall()

        cursor.close()
        conn.close()

        resultado = []

        for a in avaliacoes:

            resultado.append({

                "id": a[0],

                "nota": a[1],

                "comentario": a[2],

                "data": str(a[3]),

                "aula": a[4],

                "horario": a[5]
            })

        return jsonify(resultado)

    except Exception as e:

        print("ERRO AO BUSCAR AVALIAÇÕES:", e)

        return jsonify({
            "erro": "Erro ao buscar avaliações"
        }), 500

# ==========================================================
# CALCULADORA IMC / TMB
# ==========================================================

@app.route("/calcular-imc", methods=["POST"])
def calcular_imc():

    try:

        dados = request.get_json()

        usuario_id = dados.get("usuario_id")
        peso = float(dados.get("peso"))
        altura = float(dados.get("altura"))
        idade = int(dados.get("idade"))
        genero = dados.get("genero")

        # ==========================
        # VALIDAÇÕES
        # ==========================

        if not usuario_id:
            return jsonify({
                "erro": "Usuário não informado"
            }), 400

        if peso <= 0:
            return jsonify({
                "erro": "Peso inválido"
            }), 400

        if altura <= 0:
            return jsonify({
                "erro": "Altura inválida"
            }), 400

        if idade <= 0:
            return jsonify({
                "erro": "Idade inválida"
            }), 400

        if genero not in ["masculino", "feminino"]:
            return jsonify({
                "erro": "Gênero inválido"
            }), 400

        # ==========================
        # IMC
        # ==========================

        altura_metros = altura / 100

        imc = peso / (altura_metros ** 2)

        imc = round(imc, 2)

        # ==========================
        # CLASSIFICAÇÃO
        # ==========================

        if imc < 18.5:

            classificacao = "Abaixo do peso"

            recomendacao = (
                "Treinos de musculação com foco em ganho de massa "
                "e fortalecimento muscular."
            )

        elif imc < 25:

            classificacao = "Peso ideal"

            recomendacao = (
                "Treinos de musculação combinados com exercícios "
                "cardiorrespiratórios para manutenção e condicionamento."
            )

        elif imc < 30:

            classificacao = "Sobrepeso"

            recomendacao = (
                "Treinos de musculação combinados com exercícios "
                "cardiorrespiratórios de intensidade moderada."
            )

        else:

            classificacao = "Obesidade"

            recomendacao = (
                "Treinos de baixo impacto, caminhada e musculação "
                "progressiva, respeitando os limites individuais."
            )

        # ==========================
        # TMB
        # Fórmula de Mifflin-St Jeor
        # ==========================

        if genero == "masculino":

            tmb = (
                (10 * peso)
                + (6.25 * altura)
                - (5 * idade)
                + 5
            )

        else:

            tmb = (
                (10 * peso)
                + (6.25 * altura)
                - (5 * idade)
                - 161
            )

        tmb = round(tmb, 2)

        # ==========================
        # SALVAR NO BANCO
        # ==========================

        conn = mysql.connector.connect(
            host="db",
            user="root",
            password="root",
            database="academia"
        )

        cursor = conn.cursor()

        sql = """
            INSERT INTO avaliacao_fisica
            (
                usuario_id,
                peso,
                altura,
                idade,
                genero,
                imc,
                classificacao,
                tmb,
                recomendacao
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            usuario_id,
            peso,
            altura,
            idade,
            genero,
            imc,
            classificacao,
            tmb,
            recomendacao
        )

        cursor.execute(sql, valores)

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({

            "mensagem": "Avaliação calculada e salva com sucesso",

            "imc": imc,

            "classificacao": classificacao,

            "tmb": tmb,

            "recomendacao": recomendacao

        }), 200

    except Exception as e:

        print("ERRO CALCULADORA:", e)

        return jsonify({
            "erro": "Erro ao calcular avaliação física"
        }), 500


# ==========================================================
# BUSCAR ÚLTIMA AVALIAÇÃO FÍSICA
# ==========================================================

@app.route("/avaliacao-fisica/<int:usuario_id>", methods=["GET"])
def buscar_avaliacao_fisica(usuario_id):

    try:

        conn = mysql.connector.connect(
            host="db",
            user="root",
            password="root",
            database="academia"
        )

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                peso,
                altura,
                idade,
                genero,
                imc,
                classificacao,
                tmb,
                recomendacao,
                data_calculo
            FROM avaliacao_fisica
            WHERE usuario_id = %s
            ORDER BY id DESC
            LIMIT 1
        """, (usuario_id,))

        avaliacao = cursor.fetchone()

        cursor.close()
        conn.close()

        if not avaliacao:

            return jsonify({
                "mensagem": "Nenhuma avaliação encontrada"
            }), 404

        return jsonify(avaliacao), 200

    except Exception as e:

        print("ERRO AO BUSCAR AVALIAÇÃO:", e)

        return jsonify({
            "erro": "Erro ao buscar avaliação física"
        }), 500

# ==========================================================
# 🎯 QUIZ - DESCUBRA SEU TREINO IDEAL
# ==========================================================

@app.route("/quiz-treino", methods=["POST"])
def salvar_quiz_treino():

    try:

        data = request.get_json()

        usuario_id = data.get("usuario_id")
        objetivo = data.get("objetivo")
        preferencia = data.get("preferencia")
        experiencia = data.get("experiencia")

        # ==================================================
        # VALIDAR DADOS
        # ==================================================

        if not usuario_id:
            return jsonify({
                "erro": "Usuário não identificado."
            }), 400

        if not objetivo or not preferencia or not experiencia:
            return jsonify({
                "erro": "Responda todas as perguntas."
            }), 400

        # ==================================================
        # DEFINIR MODALIDADE
        # ==================================================

        modalidade = ""
        recomendacao = ""

        # --------------------------------------------------
        # OBJETIVO: GANHAR MASSA
        # --------------------------------------------------

        if objetivo == "massa":

            modalidade = "Musculação"

            if experiencia == "iniciante":

                recomendacao = (
                    "Treinos de musculação para iniciantes, "
                    "com foco em adaptação, técnica e ganho "
                    "gradual de massa muscular."
                )

            elif experiencia == "intermediario":

                recomendacao = (
                    "Treinos de musculação com foco em "
                    "hipertrofia e progressão de cargas."
                )

            else:

                recomendacao = (
                    "Treinos avançados de musculação com foco "
                    "em hipertrofia, força e progressão de cargas."
                )

        # --------------------------------------------------
        # OBJETIVO: EMAGRECER
        # --------------------------------------------------

        elif objetivo == "emagrecer":

            if preferencia == "dinamico":

                modalidade = "HIIT"

                recomendacao = (
                    "Treinos rápidos e intensos para aumentar "
                    "o gasto calórico e melhorar o condicionamento."
                )

            else:

                modalidade = "Funcional"

                recomendacao = (
                    "Treinos funcionais que combinam força, "
                    "resistência e gasto calórico."
                )

        # --------------------------------------------------
        # OBJETIVO: CONDICIONAMENTO
        # --------------------------------------------------

        elif objetivo == "condicionamento":

            if preferencia == "dinamico":

                modalidade = "Funcional"

                recomendacao = (
                    "Treinos funcionais dinâmicos para melhorar "
                    "resistência, força, agilidade e condicionamento."
                )

            else:

                modalidade = "Cardio"

                recomendacao = (
                    "Treinos cardiovasculares para melhorar "
                    "resistência e condicionamento físico."
                )

        # --------------------------------------------------
        # OBJETIVO: RELAXAMENTO / MOBILIDADE
        # --------------------------------------------------

        elif objetivo == "relaxamento":

            modalidade = "Yoga / Pilates"

            recomendacao = (
                "Treinos focados em mobilidade, flexibilidade, "
                "equilíbrio e bem-estar."
            )

        # --------------------------------------------------
        # CASO NÃO IDENTIFICADO
        # --------------------------------------------------

        else:

            modalidade = "Funcional"

            recomendacao = (
                "Treino funcional completo para desenvolver "
                "força, resistência e condicionamento."
            )

        # ==================================================
        # CONECTAR AO BANCO
        # ==================================================

        conn = get_db_connection()
        cursor = conn.cursor()

        # ==================================================
        # SALVAR RESULTADO
        # ==================================================

        cursor.execute("""
            INSERT INTO quiz_treino
            (
                usuario_id,
                objetivo,
                preferencia,
                experiencia,
                modalidade_recomendada,
                recomendacao,
                data_quiz
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                NOW()
            )
        """, (
            usuario_id,
            objetivo,
            preferencia,
            experiencia,
            modalidade,
            recomendacao
        ))

        conn.commit()

        cursor.close()
        conn.close()

        # ==================================================
        # RETORNAR RESULTADO
        # ==================================================

        return jsonify({

            "mensagem": "Quiz realizado com sucesso!",

            "resultado": {

                "modalidade": modalidade,

                "recomendacao": recomendacao

            }

        }), 201

    except Exception as e:

        print("ERRO AO SALVAR QUIZ:", e)

        return jsonify({
            "erro": "Erro ao salvar o resultado do quiz."
        }), 500


# ==========================================================
# 🎯 BUSCAR ÚLTIMO RESULTADO DO QUIZ
# ==========================================================

@app.route("/quiz-treino/<int:usuario_id>", methods=["GET"])
def buscar_ultimo_quiz(usuario_id):

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                objetivo,
                preferencia,
                experiencia,
                modalidade_recomendada,
                recomendacao,
                data_quiz
            FROM quiz_treino
            WHERE usuario_id = %s
            ORDER BY data_quiz DESC
            LIMIT 1
        """, (usuario_id,))

        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        # ==================================================
        # NENHUM RESULTADO
        # ==================================================

        if not resultado:

            return jsonify({
                "mensagem": "Nenhum quiz realizado."
            }), 404

        # ==================================================
        # RETORNAR RESULTADO
        # ==================================================

        return jsonify({

            "id": resultado[0],

            "objetivo": resultado[1],

            "preferencia": resultado[2],

            "experiencia": resultado[3],

            "modalidade_recomendada": resultado[4],

            "recomendacao": resultado[5],

            "data_quiz": str(resultado[6])

        }), 200

    except Exception as e:

        print("ERRO AO BUSCAR QUIZ:", e)

        return jsonify({
            "erro": "Erro ao buscar resultado do quiz."
        }), 500

# ==========================================================
# 🔥 SEQUÊNCIA DE TREINOS - STREAK
# ==========================================================

@app.route("/streak/<int:usuario_id>", methods=["GET"])
def buscar_streak(usuario_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT DATE(data_conclusao)
            FROM treinos_concluidos
            WHERE usuario_id = %s
            ORDER BY DATE(data_conclusao) DESC
        """, (usuario_id,))

        dias = cursor.fetchall()

        cursor.close()
        conn.close()

        if not dias:
            return jsonify({
                "streak": 0,
                "mensagem": "Você ainda não possui uma sequência."
            }), 200

        datas = [d[0] for d in dias]

        from datetime import date, timedelta

        hoje = date.today()

        # Verifica se treinou hoje
        if datas[0] == hoje:
            dia_atual = datas[0]

        # Se não treinou hoje, permite considerar ontem
        elif datas[0] == hoje - timedelta(days=1):
            dia_atual = datas[0]

        else:
            return jsonify({
                "streak": 0,
                "mensagem": "Sua sequência foi encerrada. Comece uma nova!"
            }), 200

        streak = 1

        for i in range(1, len(datas)):
            esperado = dia_atual - timedelta(days=i)

            if datas[i] == esperado:
                streak += 1
            else:
                break

        return jsonify({
            "streak": streak,
            "mensagem": f"🔥 Você está há {streak} dia(s) treinando!"
        }), 200

    except Exception as e:
        print("ERRO AO BUSCAR STREAK:", e)

        return jsonify({
            "erro": "Erro ao calcular sequência de treinos"
        }), 500

# ==========================================================
# 🏆 SISTEMA DE DESAFIOS
# ==========================================================

from datetime import date, timedelta


def calcular_streak_desafio(cursor, usuario_id, data_inicio):
    """
    Calcula a sequência atual de dias consecutivos do usuário,
    considerando somente os treinos feitos depois que ele entrou
    no desafio.
    """

    cursor.execute("""
        SELECT DISTINCT DATE(data_conclusao)
        FROM treinos_concluidos
        WHERE usuario_id = %s
        AND data_conclusao >= %s
        ORDER BY DATE(data_conclusao) DESC
    """, (usuario_id, data_inicio))

    registros = cursor.fetchall()

    if not registros:
        return 0

    datas = [registro[0] for registro in registros]
    hoje = date.today()

    # A sequência pode estar ativa hoje ou ter sido mantida até ontem.
    if datas[0] == hoje:
        dia_atual = datas[0]
    elif datas[0] == hoje - timedelta(days=1):
        dia_atual = datas[0]
    else:
        return 0

    streak = 1

    for i in range(1, len(datas)):
        esperado = dia_atual - timedelta(days=i)

        if datas[i] == esperado:
            streak += 1
        else:
            break

    return streak


def atualizar_desafios_automaticamente(cursor, usuario_id):
    """
    Atualiza os desafios do usuário usando somente informações
    registradas no banco. O usuário não consegue informar
    manualmente que concluiu um desafio.
    """

    cursor.execute("""
        SELECT
            ud.id,
            ud.desafio_id,
            ud.data_inicio,
            ud.progresso,
            ud.concluido,
            d.titulo,
            d.meta,
            d.tipo,
            d.pontos
        FROM usuario_desafios ud
        JOIN desafios d
            ON ud.desafio_id = d.id
        WHERE ud.usuario_id = %s
        AND d.ativo = 1
        ORDER BY d.id
    """, (usuario_id,))

    participacoes = cursor.fetchall()
    atualizados = []

    for participacao in participacoes:
        (
            usuario_desafio_id,
            desafio_id,
            data_inicio,
            progresso_atual,
            concluido_atual,
            titulo,
            meta,
            tipo,
            pontos
        ) = participacao

        # Desafio já concluído não precisa ser recalculado.
        if concluido_atual:
            continue

        if tipo == "streak":
            progresso = calcular_streak_desafio(
                cursor,
                usuario_id,
                data_inicio
            )
        else:
            # Desafios do tipo "treinos" contam apenas os treinos
            # concluídos depois da entrada do usuário no desafio.
            cursor.execute("""
                SELECT COUNT(*)
                FROM treinos_concluidos
                WHERE usuario_id = %s
                AND data_conclusao >= %s
            """, (usuario_id, data_inicio))

            resultado = cursor.fetchone()
            progresso = resultado[0] if resultado else 0

        if progresso > meta:
            progresso = meta

        if progresso < 0:
            progresso = 0

        foi_concluido = progresso >= meta

        if foi_concluido:
            cursor.execute("""
                UPDATE usuario_desafios
                SET
                    progresso = %s,
                    concluido = 1,
                    data_conclusao = NOW()
                WHERE id = %s
            """, (
                progresso,
                usuario_desafio_id
            ))

            atualizados.append({
                "id": desafio_id,
                "titulo": titulo,
                "progresso": progresso,
                "meta": meta,
                "pontos": pontos,
                "concluido": True
            })

        else:
            # Atualiza mesmo quando ainda não concluiu, para a tela
            # mostrar o progresso correto.
            cursor.execute("""
                UPDATE usuario_desafios
                SET progresso = %s
                WHERE id = %s
            """, (
                progresso,
                usuario_desafio_id
            ))

    return atualizados


# LISTAR TODOS OS DESAFIOS DISPONÍVEIS
@app.route("/desafios", methods=["GET"])
def listar_desafios():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                id,
                titulo,
                titulo AS nome,
                descricao,
                meta,
                tipo,
                pontos,
                pontos AS recompensa,
                ativo
            FROM desafios
            WHERE ativo = 1
            ORDER BY id
        """)

        desafios = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(desafios), 200

    except Exception as e:
        print("ERRO AO LISTAR DESAFIOS:", e)

        return jsonify({
            "erro": "Erro ao carregar desafios"
        }), 500


# PARTICIPAR DE UM DESAFIO
@app.route("/desafios/participar", methods=["POST"])
def participar_desafio():
    try:
        data = request.get_json() or {}

        usuario_id = data.get("usuario_id")
        desafio_id = data.get("desafio_id")

        if not usuario_id or not desafio_id:
            return jsonify({
                "erro": "Usuário e desafio são obrigatórios"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verifica se o desafio existe e está ativo.
        cursor.execute("""
            SELECT id, titulo, meta, tipo, pontos
            FROM desafios
            WHERE id = %s
            AND ativo = 1
        """, (desafio_id,))

        desafio = cursor.fetchone()

        if not desafio:
            cursor.close()
            conn.close()

            return jsonify({
                "erro": "Desafio não encontrado ou inativo"
            }), 404

        # Verifica se já participa.
        cursor.execute("""
            SELECT id, concluido
            FROM usuario_desafios
            WHERE usuario_id = %s
            AND desafio_id = %s
        """, (
            usuario_id,
            desafio_id
        ))

        existente = cursor.fetchone()

        if existente:
            cursor.close()
            conn.close()

            if existente[1]:
                return jsonify({
                    "erro": "Você já concluiu este desafio."
                }), 409

            return jsonify({
                "erro": "Você já participa deste desafio."
            }), 409

        # Cria a participação. A partir deste momento, somente
        # treinos realizados depois desta data contam para o desafio.
        cursor.execute("""
            INSERT INTO usuario_desafios
            (
                usuario_id,
                desafio_id,
                progresso,
                concluido,
                data_inicio
            )
            VALUES
            (
                %s,
                %s,
                0,
                0,
                NOW()
            )
        """, (
            usuario_id,
            desafio_id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "mensagem": "Você entrou no desafio!",
            "desafio": desafio[1],
            "meta": desafio[2],
            "tipo": desafio[3],
            "pontos": desafio[4]
        }), 201

    except Exception as e:
        print("ERRO AO PARTICIPAR DO DESAFIO:", e)

        return jsonify({
            "erro": "Erro ao participar do desafio"
        }), 500


# MEUS DESAFIOS
@app.route("/meus-desafios/<int:usuario_id>", methods=["GET"])
def meus_desafios(usuario_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Recalcula o progresso antes de mostrar a tela.
        atualizar_desafios_automaticamente(cursor, usuario_id)
        conn.commit()

        cursor.close()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                d.id,
                d.titulo,
                d.titulo AS nome,
                d.descricao,
                d.meta,
                d.tipo,
                d.pontos,
                d.pontos AS recompensa,
                ud.progresso,
                ud.concluido,
                ud.data_inicio,
                ud.data_conclusao
            FROM usuario_desafios ud
            JOIN desafios d
                ON ud.desafio_id = d.id
            WHERE ud.usuario_id = %s
            ORDER BY ud.concluido ASC, d.id
        """, (usuario_id,))

        desafios = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(desafios), 200

    except Exception as e:
        print("ERRO AO BUSCAR MEUS DESAFIOS:", e)

        return jsonify({
            "erro": "Erro ao carregar seus desafios"
        }), 500


# ATUALIZAR/VALIDAR PROGRESSO DO DESAFIO
# Esta rota foi mantida para não quebrar o frontend existente.
# O valor enviado pelo navegador NÃO é usado como prova de conclusão.
# O servidor recalcula o progresso diretamente pelo banco.
@app.route("/desafios/progresso", methods=["PUT"])
def atualizar_progresso_desafio():
    try:
        data = request.get_json() or {}

        usuario_id = data.get("usuario_id")
        desafio_id = data.get("desafio_id")

        if not usuario_id or not desafio_id:
            return jsonify({
                "erro": "Usuário e desafio são obrigatórios"
            }), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verifica se o usuário participa do desafio.
        cursor.execute("""
            SELECT ud.id
            FROM usuario_desafios ud
            WHERE ud.usuario_id = %s
            AND ud.desafio_id = %s
        """, (
            usuario_id,
            desafio_id
        ))

        participacao = cursor.fetchone()

        if not participacao:
            cursor.close()
            conn.close()

            return jsonify({
                "erro": "Você ainda não participa deste desafio"
            }), 403

        # Recalcula TODOS os desafios pelo banco.
        atualizar_desafios_automaticamente(cursor, usuario_id)
        conn.commit()

        cursor.execute("""
            SELECT
                d.titulo,
                d.meta,
                d.pontos,
                ud.progresso,
                ud.concluido
            FROM usuario_desafios ud
            JOIN desafios d
                ON ud.desafio_id = d.id
            WHERE ud.usuario_id = %s
            AND ud.desafio_id = %s
        """, (
            usuario_id,
            desafio_id
        ))

        resultado = cursor.fetchone()

        cursor.close()
        conn.close()

        if not resultado:
            return jsonify({
                "erro": "Desafio não encontrado"
            }), 404

        return jsonify({
            "mensagem": (
                "🏆 Desafio concluído!"
                if resultado[4]
                else "Progresso atualizado automaticamente!"
            ),
            "titulo": resultado[0],
            "progresso": resultado[3],
            "meta": resultado[1],
            "pontos": resultado[2],
            "concluido": bool(resultado[4])
        }), 200

    except Exception as e:
        print("ERRO AO ATUALIZAR DESAFIO:", e)

        return jsonify({
            "erro": "Erro ao atualizar progresso"
        }), 500

    # ==========================================================
# TABELAS E FUNÇÃO DE NOTIFICAÇÕES
# ==========================================================

def garantir_tabelas_novas(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS checkins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id INT NOT NULL,
            data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_checkins_usuario_data (usuario_id, data_hora)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notificacoes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id INT NOT NULL,
            tipo VARCHAR(40) NOT NULL,
            titulo VARCHAR(150) NOT NULL,
            mensagem VARCHAR(500) NOT NULL,
            referencia_id INT NULL,
            lida TINYINT(1) NOT NULL DEFAULT 0,
            data_criacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_notificacoes_usuario_data (usuario_id, data_criacao),
            INDEX idx_notificacoes_usuario_lida (usuario_id, lida)
        )
    """)


def criar_notificacao(cursor, usuario_id, tipo, titulo, mensagem,
                      referencia_id=None, evitar_duplicada=False):

    garantir_tabelas_novas(cursor)

    if evitar_duplicada and referencia_id is not None:
        cursor.execute("""
            SELECT id
            FROM notificacoes
            WHERE usuario_id = %s
              AND tipo = %s
              AND referencia_id = %s
            LIMIT 1
        """, (usuario_id, tipo, referencia_id))

        if cursor.fetchone():
            return

    cursor.execute("""
        INSERT INTO notificacoes
            (usuario_id, tipo, titulo, mensagem, referencia_id, lida)
        VALUES (%s, %s, %s, %s, %s, 0)
    """, (usuario_id, tipo, titulo, mensagem, referencia_id))

# ==========================================================
# CHECK-IN DE PRESENÇA
# ==========================================================

@app.route("/checkin", methods=["POST"])
def registrar_checkin():
    try:
        data = request.get_json() or {}
        usuario_id = data.get("usuario_id")

        if not usuario_id:
            return jsonify({"erro": "Usuário não informado"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        garantir_tabelas_novas(cursor)

        cursor.execute(
            "SELECT id FROM usuarios WHERE id = %s",
            (usuario_id,)
        )

        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({"erro": "Usuário não encontrado"}), 404

        cursor.execute("""
            SELECT id, data_hora
            FROM checkins
            WHERE usuario_id = %s
              AND DATE(data_hora) = CURDATE()
            ORDER BY data_hora DESC
            LIMIT 1
        """, (usuario_id,))

        checkin_existente = cursor.fetchone()

        if checkin_existente:
            cursor.close()
            conn.close()

            return jsonify({
                "erro": "Seu check-in de hoje já foi registrado.",
                "data_hora": str(checkin_existente[1])
            }), 409

        cursor.execute("""
            INSERT INTO checkins (usuario_id, data_hora)
            VALUES (%s, NOW())
        """, (usuario_id,))

        checkin_id = cursor.lastrowid
        conn.commit()

        cursor.execute("""
            SELECT data_hora
            FROM checkins
            WHERE id = %s
        """, (checkin_id,))

        registro = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({
            "mensagem": "Check-in realizado com sucesso!",
            "id": checkin_id,
            "data_hora": str(registro[0])
        }), 201

    except Exception as e:
        print("ERRO AO REGISTRAR CHECK-IN:", e)
        return jsonify({"erro": "Erro ao registrar check-in"}), 500


@app.route("/checkins/<int:usuario_id>", methods=["GET"])
def listar_checkins(usuario_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        garantir_tabelas_novas(cursor)

        cursor.execute("""
            SELECT id, data_hora
            FROM checkins
            WHERE usuario_id = %s
            ORDER BY data_hora DESC
        """, (usuario_id,))

        registros = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*)
            FROM checkins
            WHERE usuario_id = %s
              AND YEAR(data_hora) = YEAR(CURDATE())
              AND MONTH(data_hora) = MONTH(CURDATE())
        """, (usuario_id,))

        total_mes = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return jsonify({
            "total_mes": total_mes,
            "total": len(registros),
            "checkins": [
                {
                    "id": item[0],
                    "data_hora": str(item[1])
                }
                for item in registros
            ]
        }), 200

    except Exception as e:
        print("ERRO AO LISTAR CHECK-INS:", e)
        return jsonify({
            "erro": "Erro ao carregar histórico de presença"
        }), 500


# ==========================================================
# NOTIFICAÇÕES
# ==========================================================

@app.route("/notificacoes/<int:usuario_id>", methods=["GET"])
def listar_notificacoes(usuario_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        garantir_tabelas_novas(cursor)

        cursor.execute("""
            SELECT id, tipo, titulo, mensagem, lida, data_criacao
            FROM notificacoes
            WHERE usuario_id = %s
            ORDER BY data_criacao DESC, id DESC
        """, (usuario_id,))

        registros = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*)
            FROM notificacoes
            WHERE usuario_id = %s AND lida = 0
        """, (usuario_id,))

        nao_lidas = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return jsonify({
            "nao_lidas": nao_lidas,
            "total": len(registros),
            "notificacoes": [
                {
                    "id": item[0],
                    "tipo": item[1],
                    "titulo": item[2],
                    "mensagem": item[3],
                    "lida": bool(item[4]),
                    "data_criacao": str(item[5])
                }
                for item in registros
            ]
        }), 200

    except Exception as e:
        print("ERRO AO LISTAR NOTIFICAÇÕES:", e)
        return jsonify({
            "erro": "Erro ao carregar notificações"
        }), 500


@app.route("/notificacoes/<int:notificacao_id>/lida", methods=["PUT"])
def marcar_notificacao_lida(notificacao_id):
    try:
        data = request.get_json() or {}
        usuario_id = data.get("usuario_id")

        if not usuario_id:
            return jsonify({"erro": "Usuário não informado"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        garantir_tabelas_novas(cursor)

        cursor.execute("""
            UPDATE notificacoes
            SET lida = 1
            WHERE id = %s AND usuario_id = %s
        """, (notificacao_id, usuario_id))

        alteradas = cursor.rowcount

        conn.commit()
        cursor.close()
        conn.close()

        if not alteradas:
            return jsonify({
                "erro": "Notificação não encontrada"
            }), 404

        return jsonify({
            "mensagem": "Notificação marcada como lida."
        }), 200

    except Exception as e:
        print("ERRO AO MARCAR NOTIFICAÇÃO:", e)
        return jsonify({
            "erro": "Erro ao atualizar notificação"
        }), 500


@app.route("/notificacoes/usuario/<int:usuario_id>/ler-todas", methods=["PUT"])
def marcar_todas_notificacoes_lidas(usuario_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        garantir_tabelas_novas(cursor)

        cursor.execute("""
            UPDATE notificacoes
            SET lida = 1
            WHERE usuario_id = %s AND lida = 0
        """, (usuario_id,))

        quantidade = cursor.rowcount

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "mensagem": "Todas as notificações foram marcadas como lidas.",
            "atualizadas": quantidade
        }), 200

    except Exception as e:
        print("ERRO AO MARCAR TODAS AS NOTIFICAÇÕES:", e)
        return jsonify({
            "erro": "Erro ao atualizar notificações"
        }), 500


# ▶️ SEMPRE POR ÚLTIMO
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)