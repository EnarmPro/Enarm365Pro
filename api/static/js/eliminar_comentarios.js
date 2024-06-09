document.addEventListener('DOMContentLoaded', function () {
    // Obtener todos los botones de eliminación de comentarios
    var deleteButtons = document.querySelectorAll('.delete-comment-btn');

    // Verificar si el script ya se ejecutó
    if (deleteButtons.length > 0 && !deleteButtons[0].closest('[data-js-executed]')) {
        // Agregar un atributo de datos al elemento al que se adjunta el script
        document.body.setAttribute('data-js-executed', 'true');

        // Agregar un evento de clic a todos los botones de eliminación de comentarios
        deleteButtons.forEach(function (button) {
            button.addEventListener('click', function (event) {
                event.preventDefault();

                // Obtener el formulario padre del botón actual
                var form = this.closest('form');

                // Agregar una confirmación antes de eliminar el comentario
                if (confirm('¿Estás seguro de que deseas eliminar este comentario?')) {
                    // Obtener la URL del formulario
                    var url = form.getAttribute('action');

                    // Obtener los datos del formulario
                    var formData = new FormData(form);

                    // Enviar la solicitud AJAX
                    fetch(url, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRFToken': '{{ csrf_token }}'
                        }
                    })
                        .then(function (response) {
                            if (!response.ok) {
                                throw new Error('Network response was not ok.');
                            }
                            // Si la respuesta es exitosa, recargar la página
                            location.reload();
                        })
                        .catch(function (error) {
                            console.error('There has been a problem with your fetch operation:', error);
                        });
                }
            });
        });
    }
});
