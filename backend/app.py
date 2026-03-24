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
@app.route("/usuarios", methods=["POST"])
def criar_usuario():
    try:
        data = request.get_json()

        nome = data.get("nome")
        email = data.get("email")
        senha = data.get("senha")

        # 🔒 validação básica
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
@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, email FROM usuarios")
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()

    resultado = []
    for u in usuarios:
        resultado.append({
            "id": u[0],
            "nome": u[1],
            "email": u[2]
        })

    return jsonify(resultado)


# ▶️ RODAR
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)