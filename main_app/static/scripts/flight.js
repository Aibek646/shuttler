const elems = {
  bookButton: document.querySelector('#book-flight')
}

if (user) {
  elems.bookButton.innerText = 'Book Flight';
}
else {
  elems.bookButton.innerText = 'Log in to book flight';
}