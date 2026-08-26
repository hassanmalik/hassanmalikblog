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

const reducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)');
const finePointer=window.matchMedia('(pointer: fine)');
const publicationHero=document.querySelector('.publication-hero');
const systemsBoard=document.querySelector('.architecture-board:has(.systems-field)');
const motionCueSelectors=['.section-head','.evidence-item','.recruiting-path','.delivery-step','.featured-post','.pillar-card','.article-card','.experience-lens article'];
const motionCues=[...document.querySelectorAll(motionCueSelectors.join(','))];
motionCues.forEach((element,index)=>{
  element.setAttribute('data-motion-cue',String(index));
  element.style.setProperty('--cue-delay',`${Math.min(index%4,3)*55}ms`);
});
const revealPassedCues=()=>{
  motionCues.forEach(element=>{
    if(element.getBoundingClientRect().top<innerHeight*.94)element.classList.add('is-visible');
  });
};

if(reducedMotion.matches){
  motionCues.forEach(element=>element.classList.add('is-visible'));
}else{
  document.documentElement.classList.add('motion-ready');
  const cueObserver=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){
        entry.target.classList.add('is-visible');
        cueObserver.unobserve(entry.target);
      }
    });
  },{rootMargin:'0px 0px -8%',threshold:.12});
  motionCues.forEach(element=>cueObserver.observe(element));
  revealPassedCues();
  let cueTicking=false;
  addEventListener('scroll',()=>{
    if(!cueTicking){
      cueTicking=true;
      requestAnimationFrame(()=>{revealPassedCues();cueTicking=false;});
    }
  },{passive:true});
}

if(systemsBoard&&!reducedMotion.matches&&finePointer.matches){
  let targetX=0,targetY=0,currentX=0,currentY=0,tracking=false;
  const moveField=()=>{
    currentX+=(targetX-currentX)*.09;
    currentY+=(targetY-currentY)*.09;
    systemsBoard.style.setProperty('--field-x',currentX.toFixed(4));
    systemsBoard.style.setProperty('--field-y',currentY.toFixed(4));
    if(Math.abs(targetX-currentX)>.001||Math.abs(targetY-currentY)>.001)requestAnimationFrame(moveField);
    else tracking=false;
  };
  const track=()=>{if(!tracking){tracking=true;requestAnimationFrame(moveField);}};
  systemsBoard.addEventListener('pointermove',event=>{
    const bounds=systemsBoard.getBoundingClientRect();
    targetX=Math.max(-1,Math.min(1,((event.clientX-bounds.left)/bounds.width-.5)*2));
    targetY=Math.max(-1,Math.min(1,((event.clientY-bounds.top)/bounds.height-.5)*2));
    track();
  });
  systemsBoard.addEventListener('pointerleave',()=>{targetX=0;targetY=0;track();});
}

if(publicationHero){
  let scrollTicking=false;
  const publishHeroProgress=()=>{
    const bounds=publicationHero.getBoundingClientRect();
    const progress=Math.max(0,Math.min(1,-bounds.top/Math.max(bounds.height,1)));
    publicationHero.style.setProperty('--hero-progress',progress.toFixed(4));
    scrollTicking=false;
  };
  addEventListener('scroll',()=>{
    if(!scrollTicking){scrollTicking=true;requestAnimationFrame(publishHeroProgress);}
  },{passive:true});
  publishHeroProgress();
}
