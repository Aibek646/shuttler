let user = null;

async function getUser() {
  let response = await fetch(`/validate/`);
  user = await response.json();
  onValidate();
}

function onValidate() {}

getUser();