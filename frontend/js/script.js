const API_URL = "http://localhost:5000";

// 👤 CADASTRO
async function cadastrar(event) {
    event.preventDefault();

    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    try {
        const response = await fetch(`${API_URL}/usuarios`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nome, email, senha })
        });

        const data = await response.json();

        if (response.ok) {
            alert("✅ " + data.mensagem);
            window.location.href = "login.html";
        } else {
            alert("❌ " + data.erro);
        }

    } catch {
        alert("Erro ao conectar com servidor");
    }
}


// 🔐 LOGIN
async function login(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, senha })
        });

        const data = await response.json();

        if (response.ok) {
            // 💾 salva usuário
            localStorage.setItem("usuario", JSON.stringify(data.usuario));

            // 🚀 redireciona
            window.location.href = "dashboard.html";
        } else {
            alert("❌ " + data.erro);
        }

    } catch {
        alert("Erro ao conectar");
    }
}


// 👀 VERIFICAR LOGIN
function verificarLogin() {
    const usuario = localStorage.getItem("usuario");

    if (!usuario) {
        // se não estiver logado → volta pro login
        window.location.href = "login.html";
    } else {
        const dados = JSON.parse(usuario);

        const nomeEl = document.getElementById("nomeUsuario");
        if (nomeEl) {
            nomeEl.innerText = dados.nome;
        }
    }
}


// 🚪 LOGOUT
function logout() {
    localStorage.removeItem("usuario");
    window.location.href = "login.html";
}