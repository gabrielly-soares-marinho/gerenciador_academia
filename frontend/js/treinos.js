function iniciarTreino(botao, treinoNome) {

    botao.innerText = "✅ Concluir Treino";

    botao.onclick = function () {
        concluirTreino(botao, treinoNome);
    };

    alert("🔥 Treino " + treinoNome + " iniciado!");
}

function concluirTreino(botao, treinoNome) {

    const usuario = JSON.parse(
        localStorage.getItem("usuario")
    );

    const card = botao.closest(".treino-card");

    card.style.border = "2px solid lime";

    botao.innerText = "🏆 Treino Concluído";

    botao.disabled = true;

    botao.style.background = "lime";
    botao.style.color = "black";

    // =========================
    // TOTAL TREINOS
    // =========================

    let totalTreinos =
        localStorage.getItem(
            `totalTreinos_${usuario.id}`
        );

    if (!totalTreinos) {
        totalTreinos = 0;
    }

    totalTreinos++;

    localStorage.setItem(
        `totalTreinos_${usuario.id}`,
        totalTreinos
    );

    // =========================
    // ÚLTIMO TREINO
    // =========================

    localStorage.setItem(
        `ultimoTreino_${usuario.id}`,
        treinoNome
    );

    // =========================
    // HISTÓRICO
    // =========================

    let historico =
        JSON.parse(
            localStorage.getItem(
                `historicoTreinos_${usuario.id}`
            )
        ) || [];

    historico.push({
        treino: treinoNome,
        data: new Date().toLocaleString()
    });

    localStorage.setItem(
        `historicoTreinos_${usuario.id}`,
        JSON.stringify(historico)
    );

    // =========================
    // BANCO DE DADOS
    // =========================

    fetch("http://localhost:5000/concluir-treino", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            usuario_id: usuario.id,
            treino: treinoNome
        })

    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error(error);
    });

    alert("💪 Treino concluído com sucesso!");
}