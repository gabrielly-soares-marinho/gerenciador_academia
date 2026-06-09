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

# ▶️ SEMPRE POR ÚLTIMO
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)