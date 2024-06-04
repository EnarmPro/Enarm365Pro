 // Función para enviar el formulario de actualización del nombre de usuario
 document.getElementById("updateUsernameForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Evitar el envío del formulario
    fetch("/actualizar_datos/", {
        method: "POST",
        body: new FormData(this)
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Muestra el mensaje de éxito o error
            window.location.href = ''
        });
});

// Función para enviar el formulario de actualización del correo electrónico
document.getElementById("updateEmailForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Evitar el envío del formulario
    fetch("/actualizar_datos/", {
        method: "POST",
        body: new FormData(this)
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Muestra el mensaje de éxito o error
            window.location.href = ''
        });
});

// Función para enviar el formulario de actualización de la contraseña
document.getElementById("updatePasswordForm").addEventListener("submit", function (event) {
    event.preventDefault(); // Evitar el envío del formulario
    fetch("/actualizar_datos/", {
        method: "POST",
        body: new FormData(this)
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Muestra el mensaje de éxito o error
            window.location.href = ''
        });
});
