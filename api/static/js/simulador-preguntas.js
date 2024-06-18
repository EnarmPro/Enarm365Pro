document.querySelectorAll('.answer_type').forEach(div => {
    div.addEventListener('click', function () {
        const radioId = this.getAttribute('data-radio-id');
        const radioButton = this.querySelector(`input[type="radio"]`);
        if (radioButton) {
            radioButton.checked = true;
        }
    });
});
   

var scriptEjecutado = false;

function main() {
    if (!scriptEjecutado) {
        scriptEjecutado = true;

        document.querySelectorAll('.btn-siguiente').forEach(btn => {
            btn.addEventListener('click', function () {
                nextQuestion();
            });
        });

        let currentQuestion = 1;

        var preguntasContainer = document.getElementById('preguntas-data');
        var totalQuestions = preguntasContainer.getAttribute('data-totalpreguntas');

        function showQuestion(questionNumber) {
            document.querySelectorAll('.pregunta').forEach(div => {
                div.style.display = 'none';
            });
            document.querySelector(`.formulario-gratuito[data-question-id="${questionNumber}"]`).style.display = 'block';
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

        function enviarIntento(Categoria) {
            fetch('/registrar_intento/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': obtenerCSRFToken()
                },
                body: JSON.stringify({
                    categoria_id: Categoria
                    
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error al registrar la respuesta');
                }
                return response.json();
            })
            .then(data => {
                console.log('Respuesta registrada con éxito:', data);
                window.location.href = '/'
            })
            .catch(error => {
                console.error('Error al registrar la respuesta:', error);
            });
        }
         // Función para enviar los resultados de la encuesta
        function enviarResultados() {
            // Aquí puedes enviar los resultados de la encuesta hasta donde se haya llegado
            enviarIntento('Gratuito')
            
        }
        function cambiarpagina(){
            window.location.reload();
        }
         // Función para iniciar el cronómetro
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
                    // Llamar a la función para enviar los resultados
                    enviarResultados();
                    
                }
                
            }, 1000);
        }

        // Iniciar el cronómetro al cargar la página
        window.onload = function () {
            var fifteenMinutes = 60 * 15,
                display = document.querySelector('#timer');
            startTimer(fifteenMinutes, display);
        };
    

        function nextQuestion() {
            const formularioVisible = document.querySelector('.formulario-gratuito[data-question-id]:not([style="display: none;"])');
            const preguntaId = formularioVisible.getAttribute('data-question-id');
            const justificacion = formularioVisible.getAttribute('data-justificacion');
            const respuestaSeleccionada = formularioVisible.querySelector('input[type="radio"]:checked');
            const respuestaId = respuestaSeleccionada ? respuestaSeleccionada.value : null;
            
            if (preguntaId && respuestaId) {
                // Registrar la respuesta actual
                enviarRespuestaPorAjax(preguntaId, respuestaId)
                .then(data => {
                    
                    // Mostrar la respuesta correcta en un SweetAlert
                    Swal.fire({
                        icon: 'success',
                        title: 'Respuesta registrada',
                        html: `
                        Respuesta registrada con éxito.<br>
                        La respuesta correcta es: ${data.respuesta_correcta}<br><br>
                        <strong>Justificación:</strong> ${justificacion}
                        `
                    }).then(() => {
                        // Incrementar el número de pregunta actual
                        currentQuestion++;
        
                        if (currentQuestion <= totalQuestions) {
                            showQuestion(currentQuestion);
                            updateProgressBar();
                        } else {
                            enviarIntento('Gratuito');
                            Swal.fire({
                                icon: 'success',
                                title: '¡Cuestionario completado!',
                                text: '¡Has completado el cuestionario!'
                            }).then(() => {
                                cambiarpagina();
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
        }
        
        
        
        
        

        function updateProgressBar() {
            const progress = (currentQuestion - 1) / totalQuestions * 100;
            document.querySelector('.progress-simulator').style.width = `${progress}%`;
        }

        showQuestion(currentQuestion);
    }
}

document.addEventListener("DOMContentLoaded", main);
