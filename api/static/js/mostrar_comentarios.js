// Función para mostrar el elemento
    function mostrarFeedback() {
            var feedbackSection = document.getElementById('feedbackSection');
    if (feedbackSection.style.display === 'none') {
        feedbackSection.style.display = 'block';
            }
        }

    // Función para ocultar el elemento
    function ocultarFeedback() {
            var feedbackSection = document.getElementById('feedbackSection');
    if (feedbackSection.style.display === 'block') {
        feedbackSection.style.display = 'none';
            }
        }