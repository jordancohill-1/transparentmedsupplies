// intialize swup
const swup = new Swup();

// find navbar toggler and menu
const navbarToggler = document.getElementsByClassName('navbar-toggler')
const navbarMenu = document.querySelector('.navbar-collapse')

// toggle mobile menu on page change
document.addEventListener('swup:clickLink', event => {
  if (screen.width < 576 && navbarMenu.classList.contains('show')) {
    navbarToggler[0].click()
  }
});

// scroll to top of page before replacing content
document.addEventListener('swup:willReplaceContent', event => {
  document.body.style.scrollBehavior = "auto";
  window.scrollTo(0, 0);
  document.body.style.scrollBehavior = "smooth";
});

