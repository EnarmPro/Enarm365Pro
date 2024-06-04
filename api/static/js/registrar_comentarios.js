let formSubmitInProgress = false;  // Variable para verificar si el formulario ya se está enviando

document.getElementById('updateUsernameForm').addEventListener('submit', function (event) {
    event.preventDefault();  // Evitar la recarga de la página

    if (formSubmitInProgress) return;  // Si el formulario ya se está enviando, no hacer nada

    formSubmitInProgress = true;  // Marcar que el formulario está en proceso de envío

    const comentario = document.getElementById('comentario').value;
    const puntuacion = document.querySelector('input[name="puntuacion"]').value;
    const csrfToken = document.querySelector('input[name="csrf-token"]').value;

    fetch("/update_username_form/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            comentario: comentario,
            puntuacion: puntuacion
        })
    })
    .then(response => response.json())
    .then(data => {
        formSubmitInProgress = false;  // Permitir nuevos envíos
        if (data.success) {
            // Manejar el éxito, por ejemplo, mostrar un mensaje o redirigir
            alert('Comentario registrado exitosamente');
            window.location.href = '/';  // Redirigir después del éxito
        } else {
            // Manejar errores
            alert('Hubo un error al registrar tu comentario');
        }
    })
    .catch(error => {
        formSubmitInProgress = false;  // Permitir nuevos envíos en caso de error
        console.error('Error:', error);
    });
});