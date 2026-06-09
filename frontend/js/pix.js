window.onload = function() {

    const plano = localStorage.getItem("planoNome");
    const valor = localStorage.getItem("planoValor");

    document.getElementById("nomePlanoPix").innerHTML =
        `${plano}<br><strong>${valor}</strong>`;
};


function copiarPix() {

    const codigo =
        document.getElementById("codigoPix");

    codigo.select();

    navigator.clipboard.writeText(
        codigo.value
    );

    alert("✅ Código PIX copiado!");
}


async function confirmarPagamento() {

    const usuario = JSON.parse(
        localStorage.getItem("usuario")
    );

    const plano_id =
        localStorage.getItem("planoId");

    let valor = 0;

    if (plano_id == "1") valor = 49;
    if (plano_id == "2") valor = 79;
    if (plano_id == "3") valor = 119;

    try {

        // SALVA NA TABELA PAGAMENTOS
        const pagamento = await fetch(
            "http://localhost:5000/pagar",
            {
                method: "POST",
                headers: {
                    "Content-Type":"application/json"
                },
                body: JSON.stringify({
                    usuario_id: usuario.id,
                    plano_id: plano_id,
                    valor: valor
                })
            }
        );

        if (!pagamento.ok) {

            alert("Erro ao registrar pagamento");
            return;
        }

        // ATIVA O PLANO
        const ativarPlano = await fetch(
            "http://localhost:5000/pagar-plano",
            {
                method: "POST",
                headers: {
                    "Content-Type":"application/json"
                },
                body: JSON.stringify({
                    usuario_id: usuario.id,
                    plano_id: plano_id
                })
            }
        );

        if (!ativarPlano.ok) {

            alert("Erro ao ativar plano");
            return;
        }

        alert("✅ Pagamento confirmado!");

        window.location.href =
            "dashboard.html";

    } catch(err){

        console.error(err);

        alert("Erro ao confirmar pagamento");
    }
}