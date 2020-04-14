let user = null;
let persons = [];

async function getUser() {
  let response = await fetch(`/validate/`);
  user = await response.json();

  if (user) {
    let data = await fetch('/persons/');
    persons = await data.json();
    persons = Object.values(persons);
  }

  onValidate();
}

function onValidate() {}

getUser();