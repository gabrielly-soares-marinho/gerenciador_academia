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

    // Buscar informações do usuário e do plano
    try {
        const response = await fetch(`${API_URL}/usuarios/${dados.id}`);

        if (!response.ok) {
            throw new Error("Erro ao buscar usuário");
        }

        const data = await response.json();

        const planoEl = document.getElementById("planoAtual");

        if (planoEl) {

            const statusPlano = document.getElementById("statusPlano");

            if (data.plano_nome) {

                planoEl.innerHTML = "🏆 " + data.plano_nome;

                if (statusPlano) {
                    statusPlano.innerHTML = "✅ Plano Ativo";
                }

            } else {

                planoEl.innerHTML = "Nenhum plano ativo";

                if (statusPlano) {
                    statusPlano.innerHTML = "❌ Sem assinatura";
                }
            }
        }

        // 🔔 Atualizar contador de notificações
        atualizarContadorNotificacoes();

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

async function escolherPlano(plano_id) {

    let planoNome = "";
    let planoValor = "";

    if(plano_id == 1){
        planoNome = "Plano Básico";
        planoValor = "R$ 49,00";
    }

    if(plano_id == 2){
        planoNome = "Plano Intermediário";
        planoValor = "R$ 79,00";
    }

    if(plano_id == 3){
        planoNome = "Plano Premium";
        planoValor = "R$ 119,00";
    }

    localStorage.setItem(
        "planoId",
        plano_id
    );

    localStorage.setItem(
        "planoNome",
        planoNome
    );

    localStorage.setItem(
        "planoValor",
        planoValor
    );

    window.location.href =
        "pagamento-pix.html";
}

// 🔙 VOLTAR
function voltarDashboard() {
    window.location.href = "dashboard.html";
}

function iniciarTreino(nome) {
    alert("Treino " + nome + " iniciado!");
}

function concluirTreino(card){
    card.style.borderColor = "green";
}

// 🎯 QUIZ - DESCOBRIR TREINO IDEAL
function irQuiz() {

    const usuario = JSON.parse(
        localStorage.getItem("usuario")
    );

    if (!usuario) {

        alert("Você precisa estar logado!");

        window.location.href = "login.html";

        return;
    }

    window.location.href =
        "quiz-treino.html";
}

// 🎯 QUIZ - DESCOBRIR TREINO IDEAL

function irQuiz() {

    const usuario = JSON.parse(
        localStorage.getItem("usuario")
    );

    if (!usuario) {
        alert("Você precisa estar logado!");
        window.location.href = "login.html";
        return;
    }

    window.location.href =
        "quiz-treino.html";
}

// ==========================================================
// CHECK-IN DE PRESENÇA
// ==========================================================

function obterUsuarioLogado() {
    try {
        return JSON.parse(localStorage.getItem("usuario"));
    } catch (erro) {
        return null;
    }
}

function formatarDataHora(valor) {
    if (!valor) return "";

    const data = new Date(String(valor).replace(" ", "T"));

    if (Number.isNaN(data.getTime())) return valor;

    return data.toLocaleString("pt-BR", {
        dateStyle: "short",
        timeStyle: "short"
    });
}

async function registrarCheckin() {
    const usuario = obterUsuarioLogado();

    if (!usuario) {
        alert("Faça login para registrar sua presença.");
        window.location.href = "login.html";
        return;
    }

    const botao = document.getElementById("btnCheckin");

    if (botao) botao.disabled = true;

    try {
        const response = await fetch(`${API_URL}/checkin`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ usuario_id: usuario.id })
        });

        const data = await response.json();

        if (response.ok) {
            alert("✅ " + data.mensagem);
            await carregarCheckins();
        } else {
            alert("ℹ️ " + (data.erro || "Não foi possível registrar o check-in."));
            await carregarCheckins();
        }

    } catch (error) {
        console.error("Erro ao registrar check-in:", error);
        alert("Erro ao conectar com o servidor.");

    } finally {
        if (botao) botao.disabled = false;
    }
}

async function carregarCheckins() {
    const usuario = obterUsuarioLogado();

    if (!usuario) return;

    const lista = document.getElementById("listaCheckins");
    const totalMes = document.getElementById("totalCheckinsMes");
    const totalGeral = document.getElementById("totalCheckins");

    try {
        const response = await fetch(`${API_URL}/checkins/${usuario.id}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.erro || "Erro ao buscar presenças.");
        }

        if (totalMes) totalMes.textContent = data.total_mes ?? 0;
        if (totalGeral) totalGeral.textContent = data.total ?? 0;

        if (!lista) return;

        lista.innerHTML = "";

        if (!data.checkins || data.checkins.length === 0) {
            lista.innerHTML = '<p class="estado-vazio">Você ainda não possui presenças registradas.</p>';
            return;
        }

        data.checkins.forEach((item) => {
            const registro = document.createElement("div");
            registro.className = "checkin-item";

            const dataHora = document.createElement("span");
            dataHora.textContent = formatarDataHora(item.data_hora);

            const status = document.createElement("strong");
            status.textContent = "Presença confirmada";

            registro.append(dataHora, status);
            lista.appendChild(registro);
        });

    } catch (error) {
        console.error("Erro ao carregar check-ins:", error);

        if (lista) {
            lista.innerHTML = '<p class="estado-vazio">Não foi possível carregar o histórico.</p>';
        }
    }
}


// ==========================================================
// NOTIFICAÇÕES E LEMBRETES
// ==========================================================

async function atualizarContadorNotificacoes() {
    const usuario = obterUsuarioLogado();
    const contador = document.getElementById("contadorNotificacoes");

    if (!usuario || !contador) return;

    try {
        const response = await fetch(`${API_URL}/notificacoes/${usuario.id}`);
        const data = await response.json();

        if (!response.ok) return;

        const quantidade = Number(data.nao_lidas || 0);

        contador.textContent = quantidade;
        contador.style.display = quantidade > 0 ? "inline-flex" : "none";

    } catch (error) {
        console.error("Erro ao atualizar contador:", error);
    }
}

async function carregarNotificacoes() {
    const usuario = obterUsuarioLogado();

    if (!usuario) return;

    const lista = document.getElementById("listaNotificacoes");
    const resumo = document.getElementById("resumoNotificacoes");

    try {
        const response = await fetch(`${API_URL}/notificacoes/${usuario.id}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.erro || "Erro ao buscar notificações.");
        }

        if (resumo) {
            resumo.textContent =
                `${data.nao_lidas || 0} notificação(ões) não lida(s)`;
        }

        if (!lista) return;

        lista.innerHTML = "";

        if (!data.notificacoes || data.notificacoes.length === 0) {
            lista.innerHTML = '<p class="estado-vazio">Você ainda não possui notificações.</p>';
            return;
        }

        data.notificacoes.forEach((item) => {
            const card = document.createElement("article");

            card.className = `notificacao-item${
                item.lida ? " notificacao-lida" : " notificacao-nao-lida"
            }`;

            const conteudo = document.createElement("div");
            conteudo.className = "notificacao-conteudo";

            const titulo = document.createElement("h3");
            titulo.textContent = item.titulo;

            const mensagem = document.createElement("p");
            mensagem.textContent = item.mensagem;

            const dataHora = document.createElement("small");
            dataHora.textContent = formatarDataHora(item.data_criacao);

            conteudo.append(titulo, mensagem, dataHora);
            card.appendChild(conteudo);

            if (!item.lida) {
                const botao = document.createElement("button");

                botao.type = "button";
                botao.className = "btn-amarelo";
                botao.textContent = "Marcar como lida";

                botao.addEventListener("click", () => {
                    marcarNotificacaoLida(item.id);
                });

                card.appendChild(botao);

            } else {
                const status = document.createElement("span");

                status.className = "status-lida";
                status.textContent = "Lida";

                card.appendChild(status);
            }

            lista.appendChild(card);
        });

        await atualizarContadorNotificacoes();

    } catch (error) {
        console.error("Erro ao carregar notificações:", error);

        if (lista) {
            lista.innerHTML = '<p class="estado-vazio">Não foi possível carregar as notificações.</p>';
        }
    }
}

async function marcarNotificacaoLida(notificacaoId) {
    const usuario = obterUsuarioLogado();

    if (!usuario) return;

    try {
        const response = await fetch(
            `${API_URL}/notificacoes/${notificacaoId}/lida`,
            {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({ usuario_id: usuario.id })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.erro || "Erro ao atualizar notificação.");
        }

        await carregarNotificacoes();

    } catch (error) {
        console.error(error);
        alert("Não foi possível marcar a notificação como lida.");
    }
}

async function marcarTodasNotificacoesLidas() {
    const usuario = obterUsuarioLogado();

    if (!usuario) return;

    try {
        const response = await fetch(
            `${API_URL}/notificacoes/usuario/${usuario.id}/ler-todas`,
            { method: "PUT" }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.erro || "Erro ao atualizar notificações.");
        }

        await carregarNotificacoes();

    } catch (error) {
        console.error(error);
        alert("Não foi possível atualizar as notificações.");
    }
}

function irCheckin() {
    window.location.href = "checkin.html";
}

function irNotificacoes() {
    window.location.href = "notificacoes.html";
}