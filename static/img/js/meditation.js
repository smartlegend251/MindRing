const menu = document.querySelector('.menu');
const toggleBtn = document.querySelector('.toggle-btn');

function toggleMenu() {
  menu.classList.toggle('open');
}

toggleBtn.addEventListener('click', toggleMenu);

menu.addEventListener('click', (e) => {
  if (e.target.tagName === 'A') {
    toggleMenu();
  }
});
const body = document.querySelector('body');
const themeBtn = document.querySelector('#theme-btn');

themeBtn.addEventListener('click', () => {
  body.classList.toggle('dark-mode');
});

function goBack() {
  window.history.back();
}