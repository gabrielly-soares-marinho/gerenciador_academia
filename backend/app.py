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

        data = request.get_json()

        usuario_id = data.get("usuario_id")
        treino = data.get("treino")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO treinos_concluidos
            (usuario_id, treino_nome)
            VALUES (%s, %s)
        """, (
            usuario_id,
            treino
        ))

        cursor.execute("""
            SELECT id, treinos_concluidos
            FROM progresso
            WHERE usuario_id = %s
        """, (usuario_id,))

        progresso = cursor.fetchone()

        if progresso:

            novo_total = progresso[1] + 1

            percentual = int(
                (novo_total / 20) * 100
            )

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

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({
            "mensagem":
            "Treino salvo com sucesso!"
        })

    except Exception as e:

        print("ERRO:", e)

        return jsonify({
            "erro":
            "Erro ao salvar treino"
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

# ▶️ SEMPRE POR ÚLTIMO
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)