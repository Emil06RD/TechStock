
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('loginForm');
  const usernameInput = document.getElementById('username');
  const passwordInput = document.getElementById('password');
  const loginBtn = document.getElementById('loginBtn');

  if (form) {
    form.addEventListener('submit', function (e) {
      let valid = true;


      usernameInput.classList.remove('is-invalid');
      passwordInput.classList.remove('is-invalid');

      if (!usernameInput.value.trim()) {
        usernameInput.classList.add('is-invalid');
        valid = false;
      }

      if (!passwordInput.value.trim()) {
        passwordInput.classList.add('is-invalid');
        valid = false;
      }

      if (!valid) {
        e.preventDefault();
      } else {
        loginBtn.disabled = true;
        loginBtn.textContent = 'Iniciando...';
      }
    });
  }
});
