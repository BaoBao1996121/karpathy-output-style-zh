// Offline smoke test. Uses a deliberately minimal DOM stub, not a browser.
'use strict';
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const html = fs.readFileSync(path.join(__dirname, 'top-k-maintenance.html'), 'utf8');
const source = html.match(/<script>([\s\S]*?)<\/script>/)[1];
let assertions = 0;
function check(value, message) { assert.ok(value, message); assertions++; }
class Element {
 constructor(tag='div') {this.tagName=tag;this.children=[];this.attributes={};this.listeners={};this.dataset={};this.className='';this.textContent='';this.disabled=false;this.value=0;}
 setAttribute(name,value) {this.attributes[name]=String(value);}
 removeAttribute(name) {delete this.attributes[name];}
 getAttribute(name) {return this.attributes[name];}
 addEventListener(name, callback) {(this.listeners[name]??=[]).push(callback);}
 append(...children) {this.children.push(...children);}
 appendChild(child) {this.append(child);}
 replaceChildren(...children) {this.children=[...children];}
 fire(name,event={}) {for(const fn of this.listeners[name]??[]) fn({target:this,preventDefault(){},...event});}
}
class Input extends Element {}
const ids={};
for(const [,id] of html.matchAll(/\bid="([^"]+)"/g)) ids[id]=id==='progress'?new Input():new Element();
const nav = new Element('nav');
const document={hidden:false,listeners:{},getElementById:id=>ids[id],querySelector:sel=>sel==='.steps'?nav:null,createElement:tag=>new Element(tag),addEventListener:Element.prototype.addEventListener,fire:Element.prototype.fire};
let timerCallback=null;
const context=vm.createContext({document,HTMLInputElement:Input,setInterval(fn){timerCallback=fn;return 1;},clearInterval(){timerCallback=null;},console});
vm.runInContext(source,context,{filename:'top-k-maintenance.inline.js'});
check(nav.children.length===6,'Six navigation steps');
check(ids.rows.children.length===8,'Eight fixed candidate rows');
check(ids.prev.disabled && !ids.next.disabled,'Initial navigation bounds');
check(ids['value-a'].textContent==='？' && ids['value-b'].textContent==='？','Initial pending evidence');
const selected=()=>ids.rows.children.filter(r=>r.dataset.selected==='true').length;
for(let i=0;i<6;i++) {
 nav.children[i].fire('click');
 check(ids.counter.textContent===`${i+1} / 6`,`Step ${i+1} counter`);
 check(nav.children[i].getAttribute('aria-current')==='step',`Step ${i+1} accessible current marker`);
 check(selected()===[0,0,3,6,6,7][i],`Step ${i+1} selected row count`);
}
nav.children[2].fire('click');
check(ids['value-a'].textContent==='每 6 个月','K3 supports A');
check(ids['value-b'].textContent==='仍缺依据','K3 misses B');
nav.children[3].fire('click');
check(ids.rows.children.filter(r=>r.className.includes('newly')).length===3,'K6 adds precisely three rows');
check(ids['value-b'].textContent==='仍缺依据','K6 still misses B');
check(ids.rows.children[6].dataset.selected==='false','Rank7 excluded at K6');
nav.children[4].fire('click');
check(ids.rows.children[6].className.includes('target'),'Missing B evidence highlighted');
check(ids.rows.children[6].dataset.selected==='false','Highlight does not falsely select B');
nav.children[5].fire('click');
check(ids['value-b'].textContent==='每 12 个月','K7 supports B');
check(ids.next.disabled && !ids.prev.disabled,'Final navigation bounds');
ids.reset.fire('click');
check(ids.counter.textContent==='1 / 6','Reset returns to step1');
ids.next.fire('click');check(ids.counter.textContent==='2 / 6','Next control');
ids.prev.fire('click');check(ids.counter.textContent==='1 / 6','Previous control');
ids.progress.value='4';ids.progress.fire('input');check(ids.counter.textContent==='5 / 6','Seek control');
check(ids.progress.getAttribute('aria-valuetext')==='第 5 步：找到缺口','Seek accessible value');
document.fire('keydown',{target:new Element(),key:'End'});check(ids.counter.textContent==='6 / 6','End keyboard control');
document.fire('keydown',{target:new Element(),key:'Home'});check(ids.counter.textContent==='1 / 6','Home keyboard control');
document.fire('keydown',{target:new Element(),key:'ArrowRight'});check(ids.counter.textContent==='2 / 6','Right keyboard control');
document.fire('keydown',{target:new Element(),key:'ArrowLeft'});check(ids.counter.textContent==='1 / 6','Left keyboard control');
document.fire('keydown',{target:new Input(),key:'ArrowRight'});check(ids.counter.textContent==='1 / 6','Global keyboard handler ignores native range input');
ids.play.fire('click');check(timerCallback!==null && ids.play.getAttribute('aria-pressed')==='true','Start playback');
timerCallback();check(ids.counter.textContent==='2 / 6','Playback advances one step');
ids.play.fire('click');check(timerCallback===null && ids.play.getAttribute('aria-pressed')==='false','Pause playback');
ids.play.fire('click');ids.next.fire('click');check(timerCallback===null,'Manual navigation pauses playback');
nav.children[4].fire('click');ids.play.fire('click');timerCallback();check(ids.counter.textContent==='6 / 6' && timerCallback===null,'Playback ends and pauses on final step');
ids.play.fire('click');check(ids.counter.textContent==='1 / 6' && timerCallback!==null,'Playback restarts from final step');
document.hidden=true;document.fire('visibilitychange');check(timerCallback===null,'Hiding document pauses playback');
check(!/https?:\/\/|\bfetch\s*\(|XMLHttpRequest|WebSocket|sendBeacon|@import/.test(html),'No network URL or request API');
check(html.includes("connect-src 'none'"),'CSP blocks network connections');
check(html.includes('prefers-reduced-motion:reduce'),'Reduced-motion styling');
check(html.includes('@media(max-width:760px)'),'Narrow-screen styling');
check(html.includes(':focus-visible'),'Visible keyboard focus');
check(html.includes('教学用模拟数据'),'Simulated data disclosed');
console.log(JSON.stringify({result:'PASS',assertions,scope:'Offline HTML and JavaScript smoke test with minimal DOM stub; not full browser or visual QA.'},null,2));
