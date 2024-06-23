// Variable para verificar si el script ya se ha ejecutado
var scriptEjecutado = false;

// Función principal
function main() {
    if (!scriptEjecutado) {
        scriptEjecutado = true; 

        var currentQuestion = 1;
        var preguntasContainer = document.getElementById('preguntas-data');
        var totalQuestions = preguntasContainer.getAttribute('data-totalpreguntas');

        document.querySelectorAll('.answer_type').forEach(div => {
            div.addEventListener('click', function () {
                const radioId = this.getAttribute('data-radio-id');
                const radioButton = this.querySelector(`input[type="radio"]`);
                if (radioButton) {
                    radioButton.checked = true;
                }
            });
        });

        var formularios = document.querySelectorAll('.formulario-timer.pregunta');
        var index = 0;

        function mostrarSiguientePregunta() {
            if (index < formularios.length) {
                formularios.forEach((form, i) => {
                    form.style.display = i === index ? 'block' : 'none';
                });
                index++;
            }
        }

        function updateProgressBar() {
            const progress = (currentQuestion - 1) / totalQuestions * 100;
            document.querySelector('.progress-simulator').style.width = `${progress}%`;
        }

        mostrarSiguientePregunta();

        document.querySelectorAll('.btn-siguiente').forEach(btn => {
            btn.addEventListener('click', function () {
                const formularioVisible = document.querySelector('.formulario-timer[data-question-id]:not([style="display: none;"])');
                const preguntaId = formularioVisible.getAttribute('data-question-id');
                const justificacion = formularioVisible.getAttribute('data-justificacion');
                const respuestaSeleccionada = formularioVisible.querySelector('input[type="radio"]:checked');
                const respuestaId = respuestaSeleccionada ? respuestaSeleccionada.value : null;

                if (preguntaId && respuestaId) {
                    enviarRespuestaPorAjax(preguntaId, respuestaId)
                        .then(data => {
                            Swal.fire({
                                icon: 'success',
                                title: 'Respuesta registrada',
                                html: `
                                    Respuesta registrada con éxito.<br>
                                    La respuesta correcta es: ${data.respuesta_correcta}<br><br>
                                    <strong>Justificación:</strong> ${justificacion}
                                    `
                            }).then(() => {
                                currentQuestion++;
                                if (currentQuestion <= totalQuestions) {
                                    updateProgressBar();
                                    mostrarSiguientePregunta();
                                } else {
                                    enviarIntento('Gratuito')
                                        .then(() => {
                                            Swal.fire({
                                                icon: 'success',
                                                title: '¡Cuestionario completado!',
                                                text: '¡Has completado el cuestionario!'
                                            }).then(() => {
                                                window.location.href = '/';
                                            });
                                        });
                                }
                            });
                        })
                        .catch(error => {
                            console.error('Error al registrar la respuesta:', error);
                        });
                } else {
                    console.error('No se ha seleccionado ninguna respuesta o no se ha encontrado el ID de la pregunta.');
                }
            });
        });
    }
}

function obtenerCSRFToken() {
    var csrfToken = null;
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.startsWith('csrftoken=')) {
            csrfToken = cookie.substring('csrftoken='.length, cookie.length);
            break;
        }
    }
    return csrfToken;
}

function enviarRespuestaPorAjax(preguntaId, respuestaId) {
    return fetch('/registrar_preguntas/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': obtenerCSRFToken()
        },
        body: JSON.stringify({
            pregunta_id: preguntaId,
            respuesta_id: respuestaId,
            intento: 1
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al registrar la respuesta');
        }
        return response.json();
    });
}

function enviarIntento(categoria) {
    return fetch('/registrar_intento/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': obtenerCSRFToken()
        },
        body: JSON.stringify({
            categoria_id: categoria
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al registrar el intento');
        }
        return response.json();
    });
}

function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
            enviarIntento('Gratuito');
        }
    }, 1000);
}

window.onload = function () {

    var tiempo_min = 1;

    var cantidad_preguntas = 15;
    var fifteenMinutes = 60 * (tiempo_min * cantidad_preguntas);
    var display = document.querySelector('#timer');
    startTimer(fifteenMinutes, display);
};

document.addEventListener("DOMContentLoaded", main);
