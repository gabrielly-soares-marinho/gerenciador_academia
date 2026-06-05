function carregarProgresso() {

    // =========================
    // TOTAL TREINOS
    // =========================

    let total =
        localStorage.getItem("totalTreinos");

    if (!total) {
        total = 0;
    }

    document.getElementById(
        "totalTreinos"
    ).innerText = total;



    // =========================
    // ÚLTIMO TREINO
    // =========================

    let ultimo =
        localStorage.getItem("ultimoTreino");

    if (!ultimo) {
        ultimo = "Nenhum treino";
    }

    document.getElementById(
        "ultimoTreino"
    ).innerText = ultimo;



    // =========================
    // META
    // =========================

    const meta = 20;

    document.getElementById(
        "metaTexto"
    ).innerText =
        total + " / " + meta;



    // porcentagem
    let porcentagem =
        (total / meta) * 100;

    if (porcentagem > 100) {
        porcentagem = 100;
    }

    document.getElementById(
        "barraProgresso"
    ).style.width =
        porcentagem + "%";



    // =========================
    // HISTÓRICO
    // =========================

    let historico =
        JSON.parse(
            localStorage.getItem("historicoTreinos")
        ) || [];

    let html = "";

    historico.reverse().forEach(item => {

        html += `
            <div class="historico-item">
                ✅ ${item.treino}
                <br>
                <small>${item.data}</small>
            </div>
        `;
    });

    document.getElementById(
        "historico"
    ).innerHTML = html;
}