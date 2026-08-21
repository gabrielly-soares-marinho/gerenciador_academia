const API_URL = "http://localhost:5000";


// ==========================================================
// CALCULAR IMC / TMB
// ==========================================================

async function calcularIMC() {

    const usuario = JSON.parse(
        localStorage.getItem("usuario")
    );


    // ==========================
    // VERIFICAR LOGIN
    // ==========================

    if (!usuario) {

        alert("Você precisa estar logado!");

        window.location.href = "login.html";

        return;
    }


    // ==========================
    // PEGAR DADOS
    // ==========================

    const peso = parseFloat(
        document.getElementById("peso").value
    );

    const altura = parseFloat(
        document.getElementById("altura").value
    );

    const idade = parseInt(
        document.getElementById("idade").value
    );

    const genero =
        document.getElementById("genero").value;


    // ==========================
    // VALIDAÇÃO
    // ==========================

    if (!peso || !altura || !idade || !genero) {

        alert(
            "⚠️ Preencha todos os campos."
        );

        return;
    }


    if (peso <= 0 || altura <= 0 || idade <= 0) {

        alert(
            "⚠️ Informe valores válidos."
        );

        return;
    }


    try {

        // ==========================
        // ENVIAR PARA O BACKEND
        // ==========================

        const response = await fetch(
            `${API_URL}/calcular-imc`,
            {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    usuario_id:
                        usuario.id,

                    peso: peso,

                    altura: altura,

                    idade: idade,

                    genero: genero

                })

            }
        );


        const data =
            await response.json();


        // ==========================
        // ERRO
        // ==========================

        if (!response.ok) {

            alert(
                "❌ " +
                (
                    data.erro ||
                    "Erro ao realizar cálculo"
                )
            );

            return;
        }


        // ==========================
        // MOSTRAR RESULTADO
        // ==========================

        document.getElementById(
            "resultado"
        ).innerHTML = `

            <div
                style="
                    border: 2px solid #ffd700;
                    border-radius: 15px;
                    padding: 20px;
                    margin-top: 20px;
                "
            >

                <h2>
                    📊 Seu Resultado
                </h2>

                <p>
                    <strong>IMC:</strong>
                    ${data.imc}
                </p>

                <p>
                    <strong>Classificação:</strong>
                    ${data.classificacao}
                </p>

                <p>
                    <strong>TMB:</strong>
                    ${data.tmb} kcal/dia
                </p>

                <p>
                    <strong>💪 Recomendação:</strong>
                </p>

                <p>
                    ${data.recomendacao}
                </p>

            </div>

        `;


        alert(
            "✅ Avaliação calculada e salva!"
        );


    } catch (error) {

        console.error(
            "Erro:",
            error
        );

        alert(
            "❌ Erro ao conectar com o servidor."
        );
    }
}