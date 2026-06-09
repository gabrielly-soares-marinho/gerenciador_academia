const API_URL = "http://localhost:5000";

window.onload = function () {

    const planoId =
        localStorage.getItem("planoSelecionado");

    const nomePlano =
        document.getElementById("nomePlano");

    const valorPlano =
        document.getElementById("valorPlano");

    if (!planoId) {

        nomePlano.innerText =
            "Nenhum plano selecionado";

        valorPlano.innerText =
            "R$ 0,00";

        return;
    }

    if (planoId == "1") {

        nomePlano.innerText =
            "🥉 Plano Básico";

        valorPlano.innerText =
            "R$ 49,00";
    }

    if (planoId == "2") {

        nomePlano.innerText =
            "🥈 Plano Intermediário";

        valorPlano.innerText =
            "R$ 79,00";
    }

    if (planoId == "3") {

        nomePlano.innerText =
            "🥇 Plano Premium";

        valorPlano.innerText =
            "R$ 119,00";
    }
};

async function realizarPagamento() {

    const usuario =
        JSON.parse(
            localStorage.getItem("usuario")
        );

    const plano_id =
        localStorage.getItem(
            "planoSelecionado"
        );

    if (!usuario || !plano_id) {

        alert(
            "Erro ao localizar plano."
        );

        return;
    }

    let valor = 0;

    if (plano_id == "1") valor = 49;
    if (plano_id == "2") valor = 79;
    if (plano_id == "3") valor = 119;

    try {

        const pagamento =
            await fetch(
                `${API_URL}/pagar`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                        "application/json"
                    },
                    body: JSON.stringify({
                        usuario_id: usuario.id,
                        plano_id: plano_id,
                        valor: valor
                    })
                }
            );

        if (!pagamento.ok) {

            alert(
                "Erro ao registrar pagamento"
            );

            return;
        }

        const ativarPlano =
            await fetch(
                `${API_URL}/pagar-plano`,
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                        "application/json"
                    },
                    body: JSON.stringify({
                        usuario_id: usuario.id,
                        plano_id: plano_id
                    })
                }
            );

        if (!ativarPlano.ok) {

            alert(
                "Erro ao ativar plano"
            );

            return;
        }

        document.getElementById(
            "statusPagamento"
        ).innerHTML =
            "✔ Plano ativado com sucesso";

        localStorage.removeItem(
            "planoSelecionado"
        );

        alert(
            "✅ Pagamento realizado com sucesso!"
        );

        setTimeout(() => {

            window.location.href =
                "dashboard.html";

        }, 1500);

    } catch (error) {

        console.error(error);

        alert(
            "Erro ao processar pagamento"
        );
    }
}