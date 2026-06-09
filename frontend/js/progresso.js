async function carregarProgresso() {

    const usuario =
        JSON.parse(
            localStorage.getItem("usuario")
        );

    try {

        const response =
            await fetch(
                `http://localhost:5000/progresso/${usuario.id}`
            );

        const data =
            await response.json();

        document.getElementById(
            "totalTreinos"
        ).innerText =
            data.treinos;

        document.getElementById(
            "ultimoTreino"
        ).innerText =
            "Ver histórico abaixo";

        document.getElementById(
            "metaTexto"
        ).innerText =
            data.treinos + " / 20";

        document.getElementById(
            "barraProgresso"
        ).style.width =
            data.percentual + "%";

    } catch (error) {

        console.error(error);

    }

    carregarHistorico();
}

async function carregarHistorico() {

    const usuario =
        JSON.parse(
            localStorage.getItem("usuario")
        );

    try {

        const response =
            await fetch(
                `http://localhost:5000/historico-treinos/${usuario.id}`
            );

        const historico =
            await response.json();

        let html = "";

        historico.forEach(item => {

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

    } catch (error) {

        console.error(error);

    }
}