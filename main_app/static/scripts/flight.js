const elems = {
  seatsTotal: document.querySelector('#seats-total'),
  seatsRemain: document.querySelector('#seats-remain'),
  bookButton: document.querySelector('#book-flight'),
  loginButton: document.querySelector('#log-in'),
  username: document.querySelector('#username'),
  passengers: document.querySelector('#passengers'),
}

const FLIGHT_NUM = window.location.pathname.split('/')[2];

let seats = 0;
let passengers = [];
let persons = [];
let row = 0;

function onValidate() {
  if (user) {
    elems.bookButton.classList.remove('d-none');
    elems.bookButton.addEventListener('click', removeBookButton);
    elems.username.value = user;
  }
  else {
    elems.loginButton.classList.remove('d-none');
    elems.loginButton.addEventListener('click', login);
  }
}

function login() {
  window.location.href = `/account/?redirect=${window.location.pathname}`
}

function removeBookButton() {
  elems.bookButton.classList.add('d-none');
}

async function getSeats() {
  let data = await fetch(`/seats/${FLIGHT_NUM}`);
  seats = await data.json();
  elems.seatsTotal.innerText = `Total seats: ${seats.total}`;
  elems.seatsRemain.innerText = `Remaining seats: ${seats.remaining}`;
  passengers = Object.values(seats.passengers);
  seats = seats.remaining;
}

async function getPersons() {
  let data = await fetch('/persons/');
  persons = await data.json();
  persons = Object.values(persons);

  let options = '';


  for (row = 0; row < passengers.length; row++) {
    elems.passengers.insertAdjacentHTML('beforeend', `
      <tr id="row-${row}">
        <td colspan="2" class="name">
          <select id="seat-${row}" class="form-control">
            <option selected value="none">---------</option>
          </select>
        </td>
        <td>
          <i class="btn btn-small m-1 btn-outline-none form-control fas fa-minus" id="remove-${row}"></i>
        </td>
      </tr>`);
    let options = document.querySelector(`#seat-${row}`);
    for (let j = 0; j < persons.length; j++) {
      let selected = '';
      if (persons[j].id == passengers[row].person_id) {
        selected = 'selected';
      }
      options.insertAdjacentHTML('beforeend', `
        <option value="${persons[j].id}" ${selected}>${persons[j].first_name} ${persons[j].last_name}</option>
      `);
    }
    let removeButton = document.querySelector(`#row-${row} i`);
    let removeRow = document.querySelector(`#row-${row}`);
    removeButton.addEventListener('click', () => {
      removePassenger(removeRow);
    });
  }

  if (passengers.length <= seats) {
    elems.passengers.insertAdjacentHTML('beforeend', `
      <tr id="row-new">
        <td colspan="2" class="name">
        </td>
        <td>
          <i class="btn btn-small m-1 btn-outline-none form-control fas fa-plus" id="add"></i>
        </td>
      </tr>`)
    let addButton = document.querySelector('#row-new i');
    addButton.addEventListener('click', addPassenger);
  }
}

async function buildPage() {
  await getSeats();
  await getPersons();
}

function addPassenger() {
  row++;
  let newRow = document.querySelector('#row-new');
  newRow.insertAdjacentHTML('beforebegin', `
    <tr id="row-${row}">
      <td colspan="2" class="name">
        <select id="seat-${row}" class="form-control">
          <option selected value="none">---------</option>
        </select>
      </td>
      <td>
        <i class="btn btn-small m-1 btn-outline-none form-control fas fa-minus" id="remove-${row}"></i>
      </td>
    </tr>`);
  let options = document.querySelector(`#seat-${row}`);
  for (let j = 0; j < persons.length; j++) {
    options.insertAdjacentHTML('beforeend', `
      <option value="${persons[j].id}">${persons[j].first_name} ${persons[j].last_name}</option>
    `);
  }
  let removeButton = document.querySelector(`#row-${row} i`);
  let removeRow = document.querySelector(`#row-${row}`);
  removeButton.addEventListener('click', () => {
    removePassenger(removeRow);
  });
}

function removePassenger(removeRow) {
  console.log(removeRow);
  removeRow.remove();
}

buildPage().catch(console.log);