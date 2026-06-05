function iniciarTreino(botao, treinoNome) {

    botao.innerText = "✅ Concluir Treino";

    botao.onclick = function () {
        concluirTreino(botao, treinoNome);
    };

    alert("🔥 Treino " + treinoNome + " iniciado!");
}



function concluirTreino(botao, treinoNome) {

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

    // pega total atual
    let totalTreinos =
        localStorage.getItem("totalTreinos");

    // se não existir
    if (!totalTreinos) {
        totalTreinos = 0;
    }

    // soma +1
    totalTreinos++;

    // salva novo total
    localStorage.setItem(
        "totalTreinos",
        totalTreinos
    );



    // =========================
    // SALVAR ÚLTIMO TREINO
    // =========================

    localStorage.setItem(
        "ultimoTreino",
        treinoNome
    );



    // =========================
    // HISTÓRICO
    // =========================

    let historico =
        JSON.parse(
            localStorage.getItem("historicoTreinos")
        ) || [];

    historico.push({
        treino: treinoNome,
        data: new Date().toLocaleString()
    });

    localStorage.setItem(
        "historicoTreinos",
        JSON.stringify(historico)
    );



    alert("💪 Treino concluído com sucesso!");
}