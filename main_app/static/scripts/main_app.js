let user = null;

async function getUser() {
  let response = await fetch(`/validate/`);
  user = await response.text();
  console.log(user);
}

getUser();