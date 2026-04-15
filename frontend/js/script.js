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
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ nome, email, senha })
        });

        const data = await response.json();

        if (response.ok) {
            alert("✅ " + data.mensagem);
            window.location.href = "login.html";
        } else {
            alert("❌ " + data.erro);
        }

    } catch (error) {
        console.error(error);
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
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ email, senha })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("usuario", JSON.stringify(data.usuario));
            window.location.href = "dashboard.html";
        } else {
            alert("❌ " + data.erro);
        }

    } catch (error) {
        console.error(error);
        alert("Erro ao conectar com servidor");
    }
}

// 👀 VERIFICAR LOGIN + BUSCAR PLANO
async function verificarLogin() {
    const usuario = localStorage.getItem("usuario");

    if (!usuario) {
        window.location.href = "login.html";
        return;
    }

    const dados = JSON.parse(usuario);

    // Nome
    const nomeEl = document.getElementById("nomeUsuario");
    if (nomeEl) nomeEl.innerText = dados.nome;

    // 🔥 IMPORTANTE: aguardar resposta corretamente
    try {
        const response = await fetch(`${API_URL}/usuarios/${dados.id}`);

        if (!response.ok) {
            throw new Error("Erro ao buscar usuário");
        }

        const data = await response.json();

        const planoEl = document.getElementById("planoAtual");

        if (planoEl) {
            if (data.plano_nome) {
                planoEl.innerText = "Plano: " + data.plano_nome;
            } else {
                planoEl.innerText = "Nenhum plano selecionado";
            }
        }

    } catch (error) {
        console.error("Erro ao buscar plano:", error);
    }
}

// ✏️ ATUALIZAR
async function atualizarUsuario() {
    const usuario = JSON.parse(localStorage.getItem("usuario"));

    const nome = document.getElementById("editNome").value;
    const email = document.getElementById("editEmail").value;
    const senha = document.getElementById("editSenha").value;

    try {
        const response = await fetch(`${API_URL}/atualizar/${usuario.id}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ nome, email, senha })
        });

        const data = await response.json();

        if (response.ok) {
            alert("✅ " + data.mensagem);

            usuario.nome = nome;
            usuario.email = email;
            localStorage.setItem("usuario", JSON.stringify(usuario));

            location.reload();
        } else {
            alert("❌ " + data.erro);
        }

    } catch (error) {
        console.error(error);
        alert("Erro ao atualizar usuário");
    }
}

// 🗑️ DELETAR
async function deletarUsuario() {
    const usuario = JSON.parse(localStorage.getItem("usuario"));

    if (!confirm("Tem certeza que deseja excluir?")) return;

    try {
        const response = await fetch(`${API_URL}/deletar/${usuario.id}`, {
            method: "DELETE"
        });

        const data = await response.json();

        if (response.ok) {
            alert("✅ " + data.mensagem);
            localStorage.removeItem("usuario");
            window.location.href = "login.html";
        } else {
            alert("❌ " + data.erro);
        }

    } catch (error) {
        console.error(error);
        alert("Erro ao deletar usuário");
    }
}

// 🚪 LOGOUT
function logout() {
    localStorage.removeItem("usuario");
    window.location.href = "login.html";
}

// 🏠 HOME
function irHome() {
    window.location.href = "index.html";
}

// 📋 LISTAR USUÁRIOS
async function listarUsuarios() {
    try {
        const response = await fetch(`${API_URL}/listar`);
        const usuarios = await response.json();

        const lista = document.getElementById("lista");
        lista.innerHTML = "";

        usuarios.forEach(user => {
            const li = document.createElement("li");
            li.innerHTML = `<strong>${user.nome}</strong> - ${user.email}`;
            lista.appendChild(li);
        });

    } catch (error) {
        console.error(error);
        alert("Erro ao carregar usuários");
    }
}

// 🔁 IR PARA PLANOS
function irPlanos() {
    window.location.href = "planos.html";
}

// 💳 ESCOLHER PLANO (CORRIGIDO)
async function escolherPlano(plano_id) {
    const usuario = JSON.parse(localStorage.getItem("usuario"));

    if (!usuario) {
        alert("Usuário não logado");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/usuarios/${usuario.id}/plano`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ plano_id })
        });

        if (!response.ok) {
            throw new Error("Erro na requisição");
        }

        const data = await response.json();

        alert("✅ " + data.mensagem);

        window.location.href = "dashboard.html";

    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao conectar com servidor");
    }
}

// 🔙 VOLTAR
function voltarDashboard() {
    window.location.href = "dashboard.html";
}