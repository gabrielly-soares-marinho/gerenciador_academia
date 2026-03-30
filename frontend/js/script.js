const API_URL = "http://localhost:5000";

// 👤 CADASTRO
async function cadastrar(event) {
    event.preventDefault();

    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    try {
        const response = await fetch(`${API_URL}/cadastrar`, {
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
            localStorage.setItem("usuario", JSON.stringify(data.usuario));
            window.location.href = "dashboard.html";
        } else {
            alert("❌ " + data.erro);
        }

    } catch {
        alert("Erro ao conectar");
    }
}


// ✏️ ATUALIZAR USUÁRIO
async function atualizarUsuario() {
    const usuario = JSON.parse(localStorage.getItem("usuario"));

    const nome = document.getElementById("editNome").value;
    const email = document.getElementById("editEmail").value;
    const senha = document.getElementById("editSenha").value;

    try {
        const response = await fetch(`${API_URL}/atualizar/${usuario.id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nome, email, senha })
        });

        const data = await response.json();

        if (response.ok) {
            alert("✅ " + data.mensagem);

            // 🔄 atualiza localStorage
            usuario.nome = nome;
            usuario.email = email;
            localStorage.setItem("usuario", JSON.stringify(usuario));

            location.reload();
        } else {
            alert("❌ " + data.erro);
        }

    } catch {
        alert("Erro ao atualizar usuário");
    }
}


// 👀 VERIFICAR LOGIN
function verificarLogin() {
    const usuario = localStorage.getItem("usuario");

    if (!usuario) {
        window.location.href = "login.html";
    } else {
        const dados = JSON.parse(usuario);

        const nomeEl = document.getElementById("nomeUsuario");
        if (nomeEl) {
            nomeEl.innerText = dados.nome;
        }
    }
}

// 🗑️ DELETAR USUÁRIO
async function deletarUsuario() {
    const usuario = JSON.parse(localStorage.getItem("usuario"));

    const confirmar = confirm("Tem certeza que deseja excluir sua conta? 😢");

    if (!confirmar) return;

    try {
        const response = await fetch(`${API_URL}/deletar/${usuario.id}`, {
            method: "DELETE"
        });

        const data = await response.json();

        if (response.ok) {
            alert("✅ " + data.mensagem);

            // limpa sessão
            localStorage.removeItem("usuario");

            // volta pro login
            window.location.href = "login.html";
        } else {
            alert("❌ " + data.erro);
        }

    } catch {
        alert("Erro ao deletar usuário");
    }
}
// 🏠 IR PARA HOME
function irHome() {
    window.location.href = "index.html";
}
// 🚪 LOGOUT
function logout() {
    localStorage.removeItem("usuario");
    window.location.href = "login.html";
}

// 📋 LISTAR USUÁRIOS
async function listarUsuarios() {
    try {
        const response = await fetch(`${API_URL}/listar`);
        const usuarios = await response.json();

        const lista = document.getElementById("lista");
        lista.innerHTML = ""; // limpa antes

        usuarios.forEach(user => {
            const li = document.createElement("li");

            li.innerHTML = `
                <strong>${user.nome}</strong> - ${user.email}
            `;

            lista.appendChild(li);
        });

    } catch (error) {
        alert("Erro ao carregar usuários");
        console.error(error);
    }
}
