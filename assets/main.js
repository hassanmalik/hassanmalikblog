const menuButton=document.querySelector('.mobile-toggle');
const navLinks=document.querySelector('.nav-links');
if(menuButton&&navLinks){menuButton.addEventListener('click',()=>{const open=navLinks.classList.toggle('open');menuButton.setAttribute('aria-expanded',String(open));});}
document.querySelectorAll('[data-year]').forEach(n=>n.textContent=new Date().getFullYear());
