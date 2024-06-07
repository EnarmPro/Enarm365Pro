document.addEventListener('DOMContentLoaded', function () {
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.querySelector('input[type="password"]');
    const eyeIcon = document.getElementById('eyeIcon');

    if (togglePassword) {
        togglePassword.addEventListener('click', function (e) {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            eyeIcon.textContent = type === 'password' ? '👁️' : '🚫';
        });
    }
});
