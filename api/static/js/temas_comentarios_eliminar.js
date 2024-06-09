
var scriptExecuted = false;

function executeScript() {
    if (!scriptExecuted) {
        document.querySelectorAll('.delete-item-btn').forEach(function (button) {
            button.addEventListener('click', function (event) {
                event.preventDefault();

                // Agregar una confirmación antes de eliminar el tema
                if (confirm('¿Estás seguro de que deseas eliminar este tema?')) {
                    var form = this.closest('.delete-item-form');
                    var url = form.getAttribute('action');
                    var formData = new FormData(form);

                    fetch(url, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRFToken': '{{ csrf_token }}'
                        }
                    })
                        .then(response => {
                            if (response.ok) {
                                return response.json();
                            }
                            throw new Error('Network response was not ok.');
                        })
                        .then(data => {
                            if (data.success) {
                                // Eliminar la fila del tema de la tabla
                                var topicRow = form.closest('tr');
                                topicRow.parentNode.removeChild(topicRow);
                            } else {
                                console.error(data.error);
                            }
                        })
                        .catch(error => {
                            console.error('There has been a problem with your fetch operation:', error);
                        });
                }
            });
        });

        scriptExecuted = true;
    }
}

document.addEventListener('DOMContentLoaded', executeScript);
