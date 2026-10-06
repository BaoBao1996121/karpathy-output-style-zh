'use strict';
const fs=require('node:fs');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const html=fs.readFileSync(__dirname+'/top-k-explainer.html','utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const elements=new Map();
function element(id){
 const attrs={},handlers={},classes=new Set();
 return {id,attrs,handlers,classes,textContent:'',innerHTML:'',value:id==='speed'?'6000':'',disabled:false,style:{},dataset:{},
  classList:{toggle(name,on){if(on)classes.add(name);else classes.delete(name);}},
  setAttribute(name,value){attrs[name]=value;},removeAttribute(name){delete attrs[name];},
  addEventListener(name,fn){handlers[name]=fn;}};
}
for(const id of html.matchAll(/\bid="([^"]+)"/g))elements.set(id[1],element(id[1]));
const buttons=Array.from({length:5},(_,i)=>{const e=element('step'+i);e.dataset.step=String(i);return e;});
const intervals=new Map();let intervalId=0;
const document={hidden:false,handlers:{},getElementById:id=>elements.get(id),querySelectorAll:()=>buttons,addEventListener(name,fn){this.handlers[name]=fn;}};
const context=vm.createContext({document,console,setInterval(fn,delay){const id=++intervalId;intervals.set(id,{fn,delay});return id;},clearInterval(id){intervals.delete(id);}});
vm.runInContext(script,context,{filename:'embedded-script.js'});
const get=id=>elements.get(id);
const click=id=>get(id).handlers.click();
const selected=()=>[...get('ranks').innerHTML.matchAll(/class="rank selected/g)].length+[...get('ranks').innerHTML.matchAll(/class="rank key selected/g)].length;
assert.equal(get('step-label').textContent,'第 1 / 5 步');assert.equal(selected(),0);
for(const [stage,k,b] of [[1,3,'缺证据'],[2,6,'缺证据'],[3,6,'缺证据'],[4,8,'6 个月']]){
 click('next');assert.equal(selected(),k);assert.equal(get('b-value').textContent,b);
 assert.equal(get('step-label').textContent,`第 ${stage+1} / 5 步`);
}
assert.equal(get('next').disabled,true);
for(let k=1;k<=8;k++){
 get('k').value=String(k);get('k').handlers.input();assert.equal(selected(),k);
 assert.equal(get('b-value').textContent,k===8?'6 个月':'缺证据');
 assert.equal(intervals.size,0);assert.equal(get('k-output').value,String(k));
}
click('reset');assert.equal(selected(),0);assert.equal(get('prev').disabled,true);
click('play');assert.equal(intervals.size,1);assert.equal(get('play').attrs['aria-pressed'],'true');
[...intervals.values()][0].fn();assert.equal(selected(),3);
click('play');assert.equal(intervals.size,0);
click('play');get('speed').value='4000';get('speed').handlers.change();
assert.equal([...intervals.values()][0].delay,4000);
for(let i=0;i<3;i++)[...intervals.values()][0].fn();
assert.equal(selected(),8);assert.equal(intervals.size,0);assert.equal(get('play').attrs['aria-pressed'],'false');
click('play');assert.equal(selected(),0);assert.equal(intervals.size,1);
get('k').value='6';get('k').handlers.input();assert.equal(selected(),6);assert.equal(intervals.size,0);
buttons[2].handlers.click();assert.equal(selected(),6);
assert.equal(buttons[2].attrs['aria-current'],'step');
click('play');document.hidden=true;document.handlers.visibilitychange();assert.equal(intervals.size,0);
assert.ok(!/<(?:script|img|link|iframe|source)[^>]+(?:src|href)\s*=\s*["'][^"']*(?:https?:|\/\/)/i.test(html));
assert.ok(!/\b(?:fetch|XMLHttpRequest|WebSocket|EventSource)\s*\(/.test(script));
assert.ok(!/@import\b|url\s*\(/i.test(html.match(/<style>([\s\S]*?)<\/style>/)[1]));
assert.ok(html.includes("connect-src 'none'"));
assert.ok(html.includes('@media(prefers-reduced-motion:reduce)'));
assert.ok(html.includes('@media(max-width:720px)'));
const result={
 method:'Node vm with minimal DOM stand-in; does not verify browser rendering, native keyboard behavior, or actual network traffic',
 manual_steps:'passed',slider_values_1_to_8:'passed',autoplay_pause_speed_terminal_stop:'passed',
 replay:'passed',slider_pauses_playback:'passed',background_tab_pauses_playback:'passed',
 jump_to_step:'passed',static_no_external_assets:'passed',static_no_network_API_calls:'passed',
 content_security_policy:'connect-src none; default-src none; inline script/style only',
 responsive_and_reduced_motion_css:'present; not browser-verified',
 browser_validation:'not performed by this script; the original browser attempt was blocked by environment socket permissions',
 model_version:'unavailable',html_bytes:Buffer.byteLength(html),node:process.version
};
fs.writeFileSync(__dirname+'/logic-checks.json',JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify(result,null,2));
