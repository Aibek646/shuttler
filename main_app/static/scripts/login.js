const csrfToken = Cookies.get('csrftoken');

const form = {
  username: document.querySelector('#username'),
  userWarn: document.querySelector('#userWarn'),
  password: document.querySelector('#password'),
  passWarn: document.querySelector('#passWarn'),
  loginFail: document.querySelector('#loginFail'),
  login: document.querySelector('#login'),
  logout: document.querySelector('#logout'),
  csrf: document.querySelector('[name="csrfmiddlewaretoken"]')
}

const warnings = {
  none: '&nbsp;',
  user: 'You must enter a username',
  pass: 'You must enter a password',
  auth: 'Invalid credentials entered',
}

if (form.login) {
  form.login.addEventListener('click', login);
}
if (form.logout) {
  form.logout.addEventListener('click', logout);
}
if (form.username) {
  form.username.focus();
}

async function login(event) {
  event.preventDefault();
  let fail = false;
  let username = form.username.value;
  if (username.length === 0) {
    form.userWarn.innerHTML = warnings.user;
    form.username.focus();
    fail = true;
  }
  else {
    form.userWarn.innerHTML = warnings.none;
  }

  let password = form.password.value;
  if (password.length === 0) {
    form.passWarn.innerHTML = warnings.pass;
    if (!fail) {
      form.password.focus();
      fail = true;
    }
  }
  else {
    form.passWarn.innerHTML = warnings.none;
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
            username: form.username.value,
            password: form.password.value,
          })
        }
      )
      let login = await response.json();
      console.log(login.login);
      if (login.login === true) {
        window.location.href = `/account/`;
      }
      else {
        form.userWarn.innerHTML = warnings.none;
        form.passWarn.innerHTML = warnings.none;
        form.loginFail.innerHTML = warnings.auth;
        form.username.focus();
      }
    }
    catch (err) {
      console.log(`Login Error:`, err);
    }
  }
}

async function logout(event) {
  event.preventDefault();
  console.log('Logout');
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