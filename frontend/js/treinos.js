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

    // visual concluído
    card.style.border = "2px solid lime";

    botao.innerText = "🏆 Treino Concluído";

    botao.disabled = true;

    botao.style.background = "lime";
    botao.style.color = "black";



    // =========================
    // SALVAR TREINO CONCLUÍDO
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
    // SALVAR ÚLTIMO TREINO
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



    alert("💪 Treino concluído com sucesso!");
}