
document.addEventListener('DOMContentLoaded', (event) => {
    document.body.addEventListener('copy', (e) => e.preventDefault());
    document.body.addEventListener('cut', (e) => e.preventDefault());
    document.body.addEventListener('paste', (e) => e.preventDefault());
});
