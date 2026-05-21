function iniciarTreino(botao, treinoNome) {

    // muda botão
    botao.innerText = "✅ Concluir Treino";

    // muda função do botão
    botao.onclick = function () {
        concluirTreino(botao, treinoNome);
    };

    alert("🔥 Treino " + treinoNome + " iniciado!");
}


function concluirTreino(botao, treinoNome) {

    // pega card
    const card = botao.closest(".treino-card");

    // muda visual
    card.style.border = "2px solid lime";

    // muda botão
    botao.innerText = "🏆 Treino Concluído";

    // desabilita botão
    botao.disabled = true;

    // muda aparência
    botao.style.background = "lime";
    botao.style.color = "black";

    // salva no navegador
    localStorage.setItem(treinoNome, "concluido");

    alert("💪 Treino concluído com sucesso!");
}