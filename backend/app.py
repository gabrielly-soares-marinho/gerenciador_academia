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


# ▶️ SEMPRE POR ÚLTIMO
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)