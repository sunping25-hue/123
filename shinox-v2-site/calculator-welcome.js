'use strict';
(()=> {
 const dialog=document.getElementById('calculator-welcome');
 if(!dialog||!dialog.showModal)return;
 const key='shinox-calculator-welcome-seen-v1';
 let seen=false;
 try{seen=sessionStorage.getItem(key)==='1'}catch(_){}
 function dismiss(){
   if(dialog.open)dialog.close();
   try{sessionStorage.setItem(key,'1')}catch(_){}
 }
 dialog.querySelector('.calculator-welcome-close').addEventListener('click',dismiss);
 dialog.querySelector('.calculator-welcome-later').addEventListener('click',dismiss);
 dialog.addEventListener('cancel',()=>{try{sessionStorage.setItem(key,'1')}catch(_){}});
 dialog.addEventListener('click',e=>{if(e.target===dialog)dismiss()});
 // Close welcome first, then allow calculator-gate.js to display its password prompt.
 dialog.querySelectorAll('[data-calculator-url]').forEach(a=>a.addEventListener('click',dismiss,{capture:true}));
 if(!seen)window.addEventListener('load',()=>dialog.showModal(),{once:true});
})();
