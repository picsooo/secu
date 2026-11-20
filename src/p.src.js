(function(){
var b=document.body;
function stop(e){e.preventDefault();return false}
document.addEventListener('contextmenu',stop);
document.addEventListener('dragstart',stop);
document.addEventListener('copy',stop);
document.addEventListener('keydown',function(e){
  var k=(e.key||'').toLowerCase(),m=e.ctrlKey||e.metaKey;
  if(e.key==='F12'||(m&&['s','u','p','c'].indexOf(k)>-1)||(m&&e.shiftKey&&['i','j','c'].indexOf(k)>-1)){e.preventDefault();return false}
  if(e.key==='PrintScreen'){b.classList.add('blur');try{navigator.clipboard.writeText('')}catch(x){}setTimeout(function(){b.classList.remove('blur')},1500)}
});
window.addEventListener('blur',function(){b.classList.add('blur')});
window.addEventListener('focus',function(){b.classList.remove('blur')});
document.addEventListener('visibilitychange',function(){if(document.hidden)b.classList.add('blur')});
setInterval(function(){if(window.outerWidth-window.innerWidth>200||window.outerHeight-window.innerHeight>260){b.classList.add('blur')}},1500);
var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{threshold:.12});
document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});
})();
