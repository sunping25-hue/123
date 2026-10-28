/* Display-copy localization only: no password, destination or validation changes. */
(()=>{
 const english=document.documentElement.lang.startsWith('en'),dict=window.SHINOX_EN||{};
 const base=new URL('.',document.currentScript.src);
 function t(value){
  if(!english||typeof value!=='string'||!/[\u3400-\u9fff]/.test(value))return value;
  const key=value.trim(),translated=dict[key];
  if(translated!==undefined)return value.slice(0,value.indexOf(key))+translated+value.slice(value.indexOf(key)+key.length);
  let result=value;
  Object.keys(dict).filter(k=>k.length>3&&/[\u3400-\u9fff]/.test(k)).sort((a,b)=>b.length-a.length).forEach(k=>{if(result.includes(k))result=result.split(k).join(dict[k])});
  return result;
 }
 window.ShinoXLocale={language:english?'en':'zh-Hant',t};if(!english)return;
 function apply(node){
  const parent=node.nodeType===Node.ELEMENT_NODE?node:node.parentElement;
  if(!parent||parent.closest('script,style,textarea,[data-locale-link="zh-Hant"]'))return;
  if(node.nodeType===Node.TEXT_NODE){const value=t(node.nodeValue);if(value!==node.nodeValue)node.nodeValue=value;return}
  if(node.nodeType!==Node.ELEMENT_NODE)return;
  for(const attr of ['aria-label','title','alt','placeholder','data-calculator-title']){const value=node.getAttribute(attr);if(value){const translated=t(value);if(value!==translated)node.setAttribute(attr,translated)}}
  if(node.matches('a.calculator-contact'))node.href=new URL('en/contact.html',base).href;
  [...node.childNodes].forEach(apply);
 }
 apply(document.body);
 new MutationObserver(entries=>entries.forEach(e=>{if(e.type==='characterData'||e.type==='attributes')apply(e.target);else e.addedNodes.forEach(apply)})).observe(document.body,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['aria-label','title','alt','placeholder','data-calculator-title']});
})();
