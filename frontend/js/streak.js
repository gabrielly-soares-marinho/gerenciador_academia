const API_URL = "http://localhost:5000";

async function carregarStreak() {

    const usuarioSalvo = localStorage.getItem("usuario");

    if (!usuarioSalvo) {
        window.location.href = "login.html";
        return;
    }

    const usuario = JSON.parse(usuarioSalvo);

    try {

        const response = await fetch(
            `${API_URL}/streak/${usuario.id}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.erro || "Erro ao buscar sequência");
        }

        const streak = data.streak || 0;

        document.getElementById("streakNumero").innerText =
            streak;

        document.getElementById("streakAtual").innerText =
            `${streak} ${streak === 1 ? "dia" : "dias"}`;

        document.getElementById("streakMensagem").innerText =
            data.mensagem || "Continue treinando!";

        if (streak === 0) {

            document.getElementById("streakStatus").innerText =
                "Comece uma nova sequência!";

        } else if (streak < 3) {

            document.getElementById("streakStatus").innerText =
                "Boa! Continue treinando!";

        } else if (streak < 7) {

            document.getElementById("streakStatus").innerText =
                "🔥 Você está mantendo o ritmo!";

        } else {

            document.getElementById("streakStatus").innerText =
                "🏆 Sequência incrível!";

        }

    } catch (error) {

        console.error(
            "Erro ao carregar sequência:",
            error
        );

        document.getElementById("streakMensagem").innerText =
            "Não foi possível carregar sua sequência.";

    }
}

document.addEventListener(
    "DOMContentLoaded",
    carregarStreak
);