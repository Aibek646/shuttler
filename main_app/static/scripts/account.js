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
  table: document.querySelector('#person-list'),
  body: document.querySelector('#person-list tbody'),
  add: document.querySelector('#add-person'),
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
    display.fullName.innerText = `${user.firstName} ${user.lastName}`;
    for (let i = 0; i < persons.length; i++) {
      addPassengerRow(i, persons);
    }

    function addPassengerRow(i, persons) {
      let personRow = document.createElement('tr');
      personRow.id = `row-${persons[i].id}`;

      let firstNameCell = document.createElement('td');
      let firstNameEdit = document.createElement('input');
      let firstNameDisp = document.createElement('p');
      firstNameEdit.type = 'text';
      firstNameEdit.innerText = persons[i].first_name;
      firstNameDisp.innerText = persons[i].first_name;
      firstNameEdit.classList.add('form-control', 'd-none');
      firstNameCell.appendChild(firstNameEdit);
      firstNameCell.appendChild(firstNameDisp);

      let lastNameCell = document.createElement('td');
      let lastNameEdit = document.createElement('input');
      let lastNameDisp = document.createElement('p')
      lastNameEdit.type = 'text';
      lastNameEdit.innerText = persons[i].last_name;
      lastNameDisp.innerText = persons[i].last_name;
      lastNameEdit.classList.add('form-control', 'd-none');
      lastNameCell.appendChild(lastNameEdit);
      lastNameCell.appendChild(lastNameDisp);

      let buttonCell = document.createElement('td');

      let ex = document.createElement('i');
      ex.classList.add('btn', 'btn-small', 'btn-outline-none', 'd-none', 'fas', 'fa-times');
      ex.id = `cancel-${persons[i].id}`

      let check = document.createElement('i');
      check.classList.add('btn', 'btn-small', 'btn-outline-none', 'd-none', 'fas', 'fa-check');
      check.id = `confirm-${persons[i].id}`

      let pen = document.createElement('i');
      pen.classList.add('btn', 'btn-small', 'btn-outline-none', 'fas', 'fa-pen');
      pen.id = `edit-${persons[i].id}`

      let minus = document.createElement('button');
      minus.classList.add('btn', 'btn-small', 'btn-outline-none', 'fas', 'fa-minus');
      minus.id = `remove-${persons[i].id}`;

      buttonCell.appendChild(ex);
      buttonCell.appendChild(check);
      buttonCell.appendChild(pen);
      buttonCell.appendChild(minus);

      personRow.appendChild(firstNameCell);
      personRow.appendChild(lastNameCell);
      personRow.appendChild(buttonCell);
      display.body.appendChild(personRow);

      ex.addEventListener('click', () => {
        cancel();
        check.removeEventListener('click', removePerson);
        check.removeEventListener('click', updatePerson);
        check.removeEventListener('click', createPerson);
      })

      // display.add.addEventListener('click', () => {
      //   verify();
      //   check.addEventListener('click', createPerson);
      // })

      pen.addEventListener('click', () => {
        verify();
        firstNameDisp.classList.add('d-none');
        firstNameEdit.classList.remove('d-none');
        check.addEventListener('click', updatePerson);
      })

      minus.addEventListener('click', () => {
        verify();
        check.addEventListener('click', removePerson);
      })

      function verify() {
        ex.classList.remove('d-none');
        check.classList.remove('d-none');
        pen.classList.add('d-none');
        minus.classList.add('d-none');
      }

      function cancel() {
        ex.classList.add('d-none');
        check.classList.add('d-none');
        pen.classList.remove('d-none');
        minus.classList.remove('d-none');
      }

      async function removePerson() {
        try {
          let data = await fetch(
            `/persons/${persons[i].id}/`, {
              method: "DELETE",
              headers: {
                'X-CSRFToken': csrfToken
              },
            }
          );
          let success = await data.json();
          if (success.deleted) {
            personRow.remove();
          }
        }
        catch (err) {
          console.log(err);
        }
      }

      async function createPerson() {
        try {
          let data = await fetch(
            `/persons/`, {
              method: "POST",
              body: {
                action: 'create',
                first_name: 'Seanny',
                last_name: 'Phoenix',
              },
              headers: {
                'X-CSRFToken': csrfToken
              },
            }
          );
          let success = await data.json();
          if (success.created) {
            addPassengerRow(0, [success.created]);
          }
        }
        catch (err) {
          console.log(err);
        }
      }

      async function updatePerson() {
        try {
          let data = await fetch(
            `/persons/`, {
              method: "POST",
              body: JSON.stringify({
                action: 'update',
                id: persons[i].id,
                first_name: firstNameEdit.value,
                last_name: lastNameEdit.value,
              }),
              headers: {
                'X-CSRFToken': csrfToken
              },
            }
          );
        }
        catch (err) {
          console.log(err);
        }
      }
    }
  }
}