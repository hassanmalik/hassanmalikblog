const menuButton=document.querySelector('.mobile-toggle');
const navLinks=document.querySelector('.nav-links');
const closeMenu=()=>{if(menuButton&&navLinks){navLinks.classList.remove('open');menuButton.setAttribute('aria-expanded','false');}};
if(menuButton&&navLinks){
  menuButton.addEventListener('click',()=>{const open=navLinks.classList.toggle('open');menuButton.setAttribute('aria-expanded',String(open));});
  navLinks.querySelectorAll('a').forEach(link=>link.addEventListener('click',closeMenu));
  document.addEventListener('keydown',event=>{if(event.key==='Escape')closeMenu();});
}
document.querySelectorAll('[data-year]').forEach(node=>node.textContent=new Date().getFullYear());

const filterButtons=[...document.querySelectorAll('.filter-button')];
const publicationCards=[...document.querySelectorAll('.publication-card')];
const resultCount=document.querySelector('[data-results-count]');
if(filterButtons.length&&publicationCards.length){
  filterButtons.forEach(button=>button.addEventListener('click',()=>{
    const kind=button.dataset.filterKind;
    const value=button.dataset.filterValue;
    filterButtons.forEach(candidate=>candidate.setAttribute('aria-pressed',String(candidate===button)));
    let visible=0;
    publicationCards.forEach(card=>{
      const matches=kind==='all'||card.dataset[kind]===value;
      card.hidden=!matches;
      if(matches)visible+=1;
    });
    if(resultCount)resultCount.textContent=`Showing ${visible} articles`;
  }));
}
