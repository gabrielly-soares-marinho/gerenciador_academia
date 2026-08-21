const API_URL = "http://localhost:5000";

let respostas = {
    objetivo: "",
    preferencia: "",
    experiencia: ""
};


// ==========================================
// RESPONDER PERGUNTA
// ==========================================

function responder(tipo, resposta) {

    respostas[tipo] = resposta;

    // PERGUNTA 1 → PERGUNTA 2
    if (tipo === "objetivo") {

        document.getElementById("pergunta1").style.display = "none";
        document.getElementById("pergunta2").style.display = "block";

        document.getElementById("numeroPergunta").innerText =
            "Pergunta 2 de 3";

        return;
    }


    // PERGUNTA 2 → PERGUNTA 3
    if (tipo === "preferencia") {

        document.getElementById("pergunta2").style.display = "none";
        document.getElementById("pergunta3").style.display = "block";

        document.getElementById("numeroPergunta").innerText =
            "Pergunta 3 de 3";

        return;
    }


    // PERGUNTA 3 → RESULTADO
    if (tipo === "experiencia") {

        calcularResultado();

    }
}


// ==========================================
// CALCULAR RESULTADO
// ==========================================

async function calcularResultado() {

    let modalidade = "";
    let recomendacao = "";


    // MUSCULAÇÃO
    if (
        respostas.objetivo === "musculacao" ||
        respostas.preferencia === "academia"
    ) {

        modalidade = "💪 MUSCULAÇÃO";

        recomendacao =
            "A musculação é indicada para seu perfil. " +
            "Priorize exercícios de força e treinos progressivos, " +
            "respeitando seu nível de experiência.";
    }


    // CARDIO
    else if (
        respostas.objetivo === "emagrecimento" ||
        respostas.preferencia === "cardio"
    ) {

        modalidade = "🏃 CARDIO";

        recomendacao =
            "Treinos cardiovasculares combinam com seus objetivos. " +
            "Corrida, caminhada, bicicleta e HIIT podem ajudar " +
            "a melhorar seu condicionamento.";
    }


    // FUNCIONAL
    else if (
        respostas.objetivo === "condicionamento" ||
        respostas.preferencia === "aulas"
    ) {

        modalidade = "🔥 TREINO FUNCIONAL";

        recomendacao =
            "O treinamento funcional combina com seu perfil. " +
            "Ele trabalha força, resistência, coordenação " +
            "e condicionamento de forma dinâmica.";
    }


    // PILATES / MOBILIDADE
    else if (
        respostas.objetivo === "flexibilidade" ||
        respostas.preferencia === "tranquilo"
    ) {

        modalidade = "🧘 PILATES / MOBILIDADE";

        recomendacao =
            "Pilates e exercícios de mobilidade são indicados " +
            "para melhorar flexibilidade, equilíbrio " +
            "e controle corporal.";
    }


    // RESULTADO PADRÃO
    else {

        modalidade = "🏋️ TREINO FUNCIONAL";

        recomendacao =
            "O treino funcional é uma ótima opção para começar, " +
            "pois trabalha diferentes capacidades físicas.";
    }


    // ESCONDER PERGUNTA 3
    document.getElementById("pergunta3").style.display = "none";


    // ALTERAR TEXTO DO PROGRESSO
    document.getElementById("numeroPergunta").innerText =
        "Resultado";


    // MOSTRAR RESULTADO
    document.getElementById("resultadoQuiz").style.display = "block";


    // PREENCHER RESULTADO
    document.getElementById("modalidadeResultado").innerText =
        modalidade;

    document.getElementById("recomendacaoResultado").innerText =
        recomendacao;


    // SALVAR NO BANCO
    await salvarQuiz(modalidade, recomendacao);
}


// ==========================================
// SALVAR QUIZ NO BANCO
// ==========================================

async function salvarQuiz(modalidade, recomendacao) {

    const usuarioSalvo = localStorage.getItem("usuario");

    if (!usuarioSalvo) {

        alert("Usuário não encontrado.");

        window.location.href = "login.html";

        return;
    }


    const usuario = JSON.parse(usuarioSalvo);


    try {

        const response = await fetch(
            `${API_URL}/quiz-treino`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    usuario_id: usuario.id,

                    objetivo: respostas.objetivo,

                    preferencia: respostas.preferencia,

                    experiencia: respostas.experiencia,

                    modalidade_recomendada: modalidade,

                    recomendacao: recomendacao
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            console.error(
                "Erro ao salvar quiz:",
                data
            );

            alert("Erro ao salvar resultado do quiz.");

            return;
        }


        console.log(
            "Quiz salvo com sucesso:",
            data
        );

    } catch (error) {

        console.error(
            "Erro ao conectar com API:",
            error
        );

        alert(
            "Não foi possível salvar o resultado."
        );
    }
}


// ==========================================
// VOLTAR
// ==========================================

function voltarDashboard() {

    window.location.href = "dashboard.html";
}