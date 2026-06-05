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

    try {

        const response = await fetch(
            `http://localhost:5000/pagar-plano`,
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

        const data = await response.json();

        alert(data.mensagem);

        window.location.href =
            "dashboard.html";

    } catch(err){

        alert("Erro ao confirmar pagamento");
    }
}


function voltarPlanos() {

    window.location.href =
        "planos.html";
}