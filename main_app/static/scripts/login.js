console.log('Login Form Ready');
const form = {
  username: document.querySelector('#username'),
  password: document.querySelector('#password'),
  submit: document.querySelector('#login'),
}

form.submit.addEventListener('click', login);

function login() {
  console.log(form.username.value);
}