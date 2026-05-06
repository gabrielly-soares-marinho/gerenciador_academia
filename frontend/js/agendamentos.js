const API = "http://localhost:5000";

// 🔹 CARREGAR AULAS DISPONÍVEIS
async function carregarAulas() {
    try {
        const res = await fetch(`${API}/aulas`);
        const aulas = await res.json();

        const div = document.getElementById("aulas");
        div.innerHTML = "";

        aulas.forEach(aula => {
            div.innerHTML += `
                <div class="item-agenda">
                    <span>${aula.nome} - ${aula.horario}</span>
                    <button onclick="agendar(${aula.id})">Agendar</button>
                </div>
            `;
        });

    } catch (error) {
        console.error("Erro ao carregar aulas:", error);
    }
}


// 🔹 AGENDAR AULA
async function agendar(aula_id) {
    try {
        const usuario = JSON.parse(localStorage.getItem("usuario"));

        if (!usuario) {
            alert("Você precisa estar logado!");
            window.location.href = "login.html";
            return;
        }

        const res = await fetch(`${API}/agendar`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                usuario_id: usuario.id,
                aula_id: aula_id
            })
        });

        const data = await res.json();

        if (res.ok) {
            alert("✅ " + data.mensagem);
            carregarMeusAgendamentos();
        } else {
            alert("❌ " + data.erro);
        }

    } catch (error) {
        console.error("Erro ao agendar:", error);
        alert("Erro ao conectar com servidor");
    }
}


// 🔹 CARREGAR MEUS AGENDAMENTOS
async function carregarMeusAgendamentos() {
    try {
        const usuario = JSON.parse(localStorage.getItem("usuario"));

        if (!usuario) return;

        const res = await fetch(`${API}/meus-agendamentos/${usuario.id}`);
        const dados = await res.json();

        const div = document.getElementById("meus");
        div.innerHTML = "";

        if (dados.length === 0) {
            div.innerHTML = "<p style='text-align:center'>Nenhum agendamento ainda</p>";
            return;
        }

        dados.forEach(a => {
            div.innerHTML += `
                <div class="item-agenda">
                    <span>${a.nome} - ${a.horario}</span>
                    <button onclick="cancelar(${a.id})">Cancelar</button>
                </div>
            `;
        });

    } catch (error) {
        console.error("Erro ao carregar agendamentos:", error);
    }
}


// 🔥 INICIAR PÁGINA
window.onload = () => {
    carregarAulas();
    carregarMeusAgendamentos();
};


async function cancelar(aula_id) {
    try {
        const usuario = JSON.parse(localStorage.getItem("usuario"));

        const res = await fetch("http://localhost:5000/cancelar-agendamento", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                usuario_id: usuario.id,
                aula_id: aula_id
            })
        });

        const data = await res.json();

        alert(data.mensagem);

        carregarMeusAgendamentos();

    } catch (error) {
        console.error("Erro ao cancelar:", error);
    }
}