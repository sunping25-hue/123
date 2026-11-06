(function(){
var mv=document.querySelector('.n9v-3d');if(!mv)return;
var base=mv.getAttribute('src').replace(/[^/]*$/,'');
self.ModelViewerElement=self.ModelViewerElement||{};self.ModelViewerElement.meshoptDecoderLocation=base+'meshopt_decoder.js';
var loaded=false;function load(){if(loaded)return;loaded=true;var s=document.createElement('script');s.type='module';s.src=base+'model-viewer.min.js';document.head.appendChild(s)}
if('IntersectionObserver'in window){var io=new IntersectionObserver(function(e){if(e.some(function(x){return x.isIntersecting})){load();io.disconnect()}},{rootMargin:'400px'});io.observe(mv)}else load();
var C={blue:[.03,.12,.55],red:[.6,.012,.012],orange:[.85,.22,.01],yellow:[.85,.62,.01],green:[.02,.42,.09],black:[.012,.012,.015]};
var btns=document.querySelectorAll('.n9v-3d-swatches button'),cur='blue';
function apply(){var m=mv.model&&mv.model.getMaterialByName('MetallicBlue');if(m)m.pbrMetallicRoughness.setBaseColorFactor(C[cur].concat(1))}
btns.forEach(function(b){b.addEventListener('click',function(){cur=b.dataset.c;btns.forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false')});apply()})});
mv.addEventListener('load',apply);
var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches,sway=!reduce,t0=0;
mv.addEventListener('camera-change',function(e){if(e.detail&&e.detail.source==='user-interaction')sway=false});
function tick(t){if(!t0)t0=t;if(sway&&mv.loaded&&!window.__noSway){mv.cameraOrbit=(30+35*Math.sin((t-t0)/2600)).toFixed(2)+'deg 78deg '+mv.getCameraOrbit().radius+'m'}requestAnimationFrame(tick)}
if(sway)requestAnimationFrame(tick);
})();
