const API_URL = "http://localhost:5000";


// ==========================================
// CARREGAR DESAFIOS
// ==========================================

async function carregarDesafios() {

    const usuario = JSON.parse(
        localStorage.getItem("usuario")
    );

    if (!usuario) {
        window.location.href = "login.html";
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/desafios`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.erro || "Erro ao carregar desafios"
            );
        }

        const container =
            document.getElementById("listaDesafios");

        container.innerHTML = "";

        data.forEach(desafio => {

            const card =
                document.createElement("div");

            card.className = "desafio-card";

            card.innerHTML = `

                <h2>
                    🏆 ${desafio.titulo}
                </h2>

                <p>
                    ${desafio.descricao}
                </p>

                <p>
                    🎯 Meta:
                    <strong>${desafio.meta}</strong>
                    ${desafio.tipo === "treinos"
                        ? " treinos"
                        : " dias consecutivos"}
                </p>

                <p>
                    ⭐ ${desafio.pontos} pontos
                </p>

                <button
                    class="btn-amarelo"
                    onclick="participarDesafio(${desafio.id})">

                    PARTICIPAR DO DESAFIO

                </button>

            `;

            container.appendChild(card);

        });

    } catch (error) {

        console.error(
            "Erro ao carregar desafios:",
            error
        );

        document.getElementById(
            "listaDesafios"
        ).innerHTML = `

            <p style="
                color: #ff3366;
                text-align: center;
                font-size: 18px;
            ">

                ❌ Não foi possível carregar os desafios.

            </p>

        `;
    }
}


// ==========================================
// PARTICIPAR DO DESAFIO
// ==========================================

async function participarDesafio(desafioId) {

    const usuario = JSON.parse(
        localStorage.getItem("usuario")
    );

    if (!usuario) {

        alert(
            "Você precisa estar logado."
        );

        window.location.href =
            "login.html";

        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/desafios/participar`,
            {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    usuario_id:
                        usuario.id,

                    desafio_id:
                        desafioId

                })

            }
        );

        const data =
            await response.json();

        if (response.ok) {

            alert(
                "🏆 Você entrou no desafio!"
            );

            carregarDesafios();

        } else {

            alert(
                "❌ " +
                (data.erro ||
                    "Não foi possível participar.")
            );
        }

    } catch (error) {

        console.error(error);

        alert(
            "Erro ao conectar com o servidor."
        );
    }
}


// ==========================================
// VOLTAR
// ==========================================

function voltarDashboard() {

    window.location.href =
        "dashboard.html";
}


// ==========================================
// LOGOUT
// ==========================================

function logout() {

    localStorage.removeItem(
        "usuario"
    );

    window.location.href =
        "login.html";
}


// ==========================================
// INICIAR
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    carregarDesafios
);