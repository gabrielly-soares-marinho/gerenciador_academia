const API_URL = "http://localhost:5000";

let notaSelecionada = 0;


// ==========================================================
// CARREGAR AULA
// ==========================================================

function carregarAulaParaAvaliar() {

    const usuario = JSON.parse(
        localStorage.getItem("usuario")
    );

    if (!usuario) {

        window.location.href = "login.html";

        return;
    }


    const aula = JSON.parse(
        localStorage.getItem("aulaParaAvaliar")
    );


    if (!aula) {

        document.getElementById(
            "nomeAula"
        ).innerText =
            "Nenhuma aula selecionada";

        document.getElementById(
            "horarioAula"
        ).innerText =
            "";

        return;
    }


    document.getElementById(
        "nomeAula"
    ).innerText =
        "📚 " + aula.nome;


    document.getElementById(
        "horarioAula"
    ).innerText =
        "🕐 Horário: " + aula.horario;
}


// ==========================================================
// SELECIONAR NOTA
// ==========================================================

function selecionarNota(nota) {

    notaSelecionada = nota;


    const estrelas =
        document.querySelectorAll(
            ".estrelas button"
        );


    estrelas.forEach(
        (estrela, index) => {

            if (index < nota) {

                estrela.classList.add(
                    "estrela-selecionada"
                );

            } else {

                estrela.classList.remove(
                    "estrela-selecionada"
                );

            }

        }
    );


    const textos = {

        1: "😞 Muito ruim",

        2: "😕 Ruim",

        3: "😐 Regular",

        4: "😊 Boa",

        5: "🤩 Excelente"

    };


    document.getElementById(
        "textoNota"
    ).innerText =
        textos[nota];
}


// ==========================================================
// ENVIAR AVALIAÇÃO
// ==========================================================

async function enviarAvaliacao() {

    const usuario = JSON.parse(
        localStorage.getItem("usuario")
    );


    const aula = JSON.parse(
        localStorage.getItem("aulaParaAvaliar")
    );


    const comentario =
        document.getElementById(
            "comentario"
        ).value.trim();


    if (!usuario) {

        alert(
            "Usuário não encontrado."
        );

        window.location.href =
            "login.html";

        return;
    }


    if (!aula) {

        alert(
            "Nenhuma aula selecionada."
        );

        return;
    }


    if (notaSelecionada === 0) {

        alert(
            "⭐ Selecione uma nota de 1 a 5."
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/avaliar-aula`,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        usuario_id:
                            usuario.id,

                        aula_id:
                            aula.id,

                        nota:
                            notaSelecionada,

                        comentario:
                            comentario

                    })

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                "❌ " +
                (
                    data.erro ||
                    "Erro ao enviar avaliação"
                )
            );

            return;
        }


        document.getElementById(
            "mensagemAvaliacao"
        ).innerText =
            "✅ " + data.mensagem;


        alert(
            "⭐ Avaliação enviada com sucesso!"
        );


        localStorage.removeItem(
            "aulaParaAvaliar"
        );


        setTimeout(
            function () {

                window.location.href =
                    "agendamentos.html";

            },
            1000
        );


    } catch (error) {

        console.error(
            "ERRO:",
            error
        );

        alert(
            "❌ Erro ao conectar com o servidor."
        );
    }
}