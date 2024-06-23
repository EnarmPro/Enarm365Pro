// Variable para verificar si el script ya se ha ejecutado
var scriptEjecutado = false;
// Función principal
function main() {
    // Si el script no se ha ejecutado previamente
    if (!scriptEjecutado) {
        scriptEjecutado = true; 
        var currentQuestion=1;
        var preguntasContainer = document.getElementById('preguntas-data');
        var totalQuestions = preguntasContainer.getAttribute('data-totalpreguntas');

        // Función para manejar el evento click en las opciones de respuesta
        document.querySelectorAll('.answer_type').forEach(div => {
            div.addEventListener('click', function () {
                const radioId = this.getAttribute('data-radio-id');
                const radioButton = this.querySelector(`input[type="radio"]`);
                if (radioButton) {
                    radioButton.checked = true;
                }
            });
        });

        // Función para mostrar la siguiente pregunta al cargar la página
        var formularios = document.querySelectorAll('.formulario-timer.pregunta');
        var index = 0;

        function mostrarSiguientePregunta() {
            if (index < formularios.length) {
                for (var i = 0; i < formularios.length; i++) {
                    formularios[i].style.display = 'none';
                }
                formularios[index].style.display = 'block';
                index++;
            }
        }
        function updateProgressBar() {
        const progress = (currentQuestion - 1) / totalQuestions * 100;
        document.querySelector('.progress-simulator').style.width = `${progress}%`;
    }

        mostrarSiguientePregunta();

        // Función para manejar el evento click en los botones "Siguiente"
        document.querySelectorAll('.btn-siguiente').forEach(btn => {
            btn.addEventListener('click', function () {
                // Obtener la pregunta y la respuesta seleccionada
                const formularioVisible = document.querySelector('.formulario-timer[data-question-id]:not([style="display: none;"])');
                const preguntaId = formularioVisible.getAttribute('data-question-id');
                const respuestaSeleccionada = formularioVisible.querySelector('input[type="radio"]:checked');
                const respuestaId = respuestaSeleccionada ? respuestaSeleccionada.value : null;

                if (preguntaId && respuestaId) {
                    console.log(`Pregunta ID: ${preguntaId}, Respuesta ID: ${respuestaId}`);
                    enviarRespuestaPorAjax(preguntaId, respuestaId);
                    // Incrementar el número de pregunta actual
                    currentQuestion++;
                    console.log(currentQuestion)
                    if (currentQuestion <= totalQuestions) {
                        updateProgressBar();
                        // Mostrar la siguiente pregunta
                        mostrarSiguientePregunta();
                        
                    } else {
                        // Si no hay más preguntas disponibles, marcar el cuestionario como completado
                        enviarIntento('Enarm')
                        alert('¡Cuestionario completado!');
                    }
                } else {
                    alert('Por favor, selecciona una respuesta antes de continuar.');
                    console.error('No se ha seleccionado ninguna respuesta o no se ha encontrado el ID de la pregunta.');
                }

                
            });
        });
    }
}

// Función para obtener el token CSRF
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

// Función para enviar la respuesta por AJAX
function enviarRespuestaPorAjax(preguntaId, respuestaId) {
    fetch('/registrar_preguntas/', {
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
    })
    .then(data => {
        console.log('Respuesta registrada con éxito:', data);
    })
    .catch(error => {
        console.error('Error al registrar la respuesta:', error);
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
                enviarIntento('Enarm')
                
            }
            
        }, 1000);
    }
    var tiempoContainer = document.getElementById('tiempo-data');
    var tiempo_min = tiempoContainer.getAttribute('data-totaltiempo');
    // Iniciar el cronómetro al cargar la página
    window.onload = function () {
        var fifteenMinutes = 60 * (70*tiempo_min),
            display = document.querySelector('#timer');
        startTimer(fifteenMinutes, display);
    };

// Ejecutar la función principal cuando el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", main);