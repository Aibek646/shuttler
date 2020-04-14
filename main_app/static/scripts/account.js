const csrfToken = Cookies.get('csrftoken');
const getParams = new URLSearchParams(window.location.search);
const redirect = getParams.get('redirect');

const loginForm = {
  username: document.querySelector('#username'),
  userWarn: document.querySelector('#userWarn'),
  password: document.querySelector('#password'),
  passWarn: document.querySelector('#passWarn'),
  loginFail: document.querySelector('#loginFail'),
  login: document.querySelector('#login'),
  logout: document.querySelector('#logout'),
  csrf: document.querySelector('[name="csrfmiddlewaretoken"]')
}

const display = {
  fullName: document.querySelector('#full-name'),
}

const warnings = {
  none: '&nbsp;',
  user: 'You must enter a username',
  pass: 'You must enter a password',
  auth: 'Invalid credentials entered',
}

if (loginForm.login) {
  loginForm.login.addEventListener('click', login);
}
if (loginForm.logout) {
  loginForm.logout.addEventListener('click', logout);
}
if (loginForm.username) {
  loginForm.username.focus();
}

async function login(event) {
  event.preventDefault();
  let fail = false;
  let username = loginForm.username.value;
  if (username.length === 0) {
    loginForm.userWarn.innerHTML = warnings.user;
    loginForm.username.focus();
    fail = true;
  }
  else {
    loginForm.userWarn.innerHTML = warnings.none;
  }

  let password = loginForm.password.value;
  if (password.length === 0) {
    loginForm.passWarn.innerHTML = warnings.pass;
    if (!fail) {
      loginForm.password.focus();
      fail = true;
    }
  }
  else {
    loginForm.passWarn.innerHTML = warnings.none;
  }
  if (!fail) {
    try {
      let response = await fetch(
        '/login/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrfToken
          },
          body: JSON.stringify({
            username: loginForm.username.value,
            password: loginForm.password.value,
          })
        }
      )
      let login = await response.json();
      console.log('Log In');
      if (login.login === true) {
        if (redirect) {
          window.location.href = redirect;
          return;
        }
        window.location.href = `/account/`;
      }
      else {
        loginForm.userWarn.innerHTML = warnings.none;
        loginForm.passWarn.innerHTML = warnings.none;
        loginForm.loginFail.innerHTML = warnings.auth;
        loginForm.username.focus();
      }
    }
    catch (err) {
      console.log(`Login Error:`, err);
    }
  }
}

async function logout(event) {
  event.preventDefault();
  console.log('Log Out');
  try {
    let response = await fetch(
      '/logout/', {
        method: 'DELETE',
        headers: {
          'X-CSRFToken': csrfToken
        },
      }
    )
    await response.text();
    window.location.href = `/account/`;
  }
  catch (err) {
    console.log(`Logout Error:`, err);
  }
}

function onValidate() {
  if (user) {
    display.fullName.innerText = `${user.firstName} ${user.lastName}`
  }
}