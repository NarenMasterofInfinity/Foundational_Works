// Dependency-free Node 22+ CDP verification of the self-contained reading edition.
// node verify_browser.mjs /absolute/repository/root /tmp/profile/DevToolsActivePort
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';
const root=resolve(process.argv[2]||join(import.meta.dirname,'../..'));
const port=readFileSync(process.argv[3]||'/tmp/system-design-atlas-chrome/DevToolsActivePort','utf8').split('\n')[0];
const targets=await(await fetch(`http://127.0.0.1:${port}/json`)).json();
const ws=new WebSocket(targets.find(t=>t.type==='page').webSocketDebuggerUrl);
await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j;});
let serial=0;const pending=new Map(),errors=[],network=[];
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails);if(m.method==='Network.requestWillBeSent')network.push(m.params.request.url);if(m.id&&pending.has(m.id)){const {resolve,reject,timer}=pending.get(m.id);clearTimeout(timer);pending.delete(m.id);m.error?reject(Error(JSON.stringify(m.error))):resolve(m.result);}};
function call(method,params={}){return new Promise((resolve,reject)=>{const id=++serial,timer=setTimeout(()=>{pending.delete(id);reject(Error('CDP timeout: '+method));},30000);pending.set(id,{resolve,reject,timer});ws.send(JSON.stringify({id,method,params}));});}
async function evaluate(expression){const r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result?.value;}
async function change(selector,value,event='input'){await evaluate(`(()=>{const el=document.querySelector(${JSON.stringify(selector)});el.value=${JSON.stringify(value)};el.dispatchEvent(new Event(${JSON.stringify(event)},{bubbles:true}));})()`);}
const click=s=>evaluate(`document.querySelector(${JSON.stringify(s)}).click()`);
async function page(path,ready='Boolean(window.SYSTEM_ATLAS_READY)'){
 const [file,hash]=path.split('#'),url=pathToFileURL(join(root,file));if(hash)url.hash=hash;
 await call('Page.navigate',{url:url.href});
 for(let i=0;i<80;i++){if(await evaluate(ready))return;await new Promise(r=>setTimeout(r,50));}
 throw Error('Page not ready: '+path);
}
const qa='/tmp/system-design-atlas-qa';mkdirSync(qa,{recursive:true});
async function screenshot(name,anchor){await evaluate(anchor?`document.getElementById(${JSON.stringify(anchor)}).scrollIntoView({block:'start',behavior:'instant'})`:'scrollTo(0,0)');await new Promise(r=>setTimeout(r,150));const r=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});writeFileSync(join(qa,name+'.png'),Buffer.from(r.data,'base64'));}
async function navigate(id){await evaluate(`SystemAtlas.navigate('#'+${JSON.stringify(id)})`);assert.equal(await evaluate('SystemAtlas.activePanel'),id);assert.equal(await evaluate('document.querySelectorAll(".panel:not([hidden])").length'),1);}
await call('Runtime.enable');await call('Page.enable');await call('Network.enable');
await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false});
try{
 await page('system-design/index.html');
 if(process.argv.includes('--pdf-only')){
  await evaluate('dispatchEvent(new Event("beforeprint"))');
  await call('Emulation.setEmulatedMedia',{media:'print'});
  const pdf=await call('Page.printToPDF',{printBackground:true,preferCSSPageSize:true,displayHeaderFooter:false});
  writeFileSync(join(root,'system-design/System-Design-Atlas-Foundations.pdf'),Buffer.from(pdf.data,'base64'));
  await evaluate('dispatchEvent(new Event("afterprint"))');
  await call('Emulation.setEmulatedMedia',{media:''});
  console.log('Regenerated foundations PDF: '+Buffer.from(pdf.data,'base64').length+' bytes.');
 }else if(process.argv.includes('--figures-only')){
  for(const f of await evaluate('AtlasData.figures')){
   await evaluate(`SystemAtlas.navigate('#'+${JSON.stringify(f.id)})`);
   const clip=await evaluate(`(()=>{const r=document.getElementById(${JSON.stringify(f.id)}).getBoundingClientRect();return {x:r.x+scrollX,y:r.y+scrollY,width:r.width,height:r.height,scale:1}})()`);
   const r=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip});writeFileSync(join(qa,f.id+'.png'),Buffer.from(r.data,'base64'));
  }
  console.log('Captured 16 complete figures for visual review.');
  process.exitCode=0;
 }else{
 assert.equal(await evaluate('document.querySelectorAll(".chapter").length'),4);
 assert.equal(await evaluate('document.querySelectorAll(".chapter .figure").length'),16);
 assert.equal(await evaluate('document.querySelectorAll(".lab").length'),4);
 assert.equal(await evaluate('document.querySelectorAll(".exercise").length'),11);
 assert.equal(await evaluate('document.querySelectorAll(".solution").length'),11);
 assert.equal(await evaluate('document.querySelectorAll("script[src],link[rel=stylesheet],img[src^=http]").length'),0);
 assert.equal(await evaluate('document.querySelectorAll(".planned-chapter").length'),95);
 await screenshot('overview-desktop');
 await navigate('ch-1-1');
 // The policy with early acknowledgment must exhibit acknowledged write loss.
 await change('#crash-policy','early','change');for(let i=0;i<3;i++)await click('#crash-next');
 await click('#crash-restart');assert.match(await evaluate('document.querySelector("#crash-state").innerText'),/Promise broken/);
 await change('#crash-policy','durable','change');for(let i=0;i<4;i++)await click('#crash-next');
 await click('#crash-restart');assert.match(await evaluate('document.querySelector("#crash-state").innerText'),/Task recovered/);
 await change('#crash-policy','durable','change');for(let i=0;i<3;i++)await click('#crash-next');
 await click('#crash-restart');assert.match(await evaluate('document.querySelector("#crash-state").innerText'),/No successful response was received/);
 assert.equal(await evaluate('document.querySelector("#crash-next").disabled'),true);
 await change('#crash-policy','memory','change');for(let i=0;i<3;i++)await click('#crash-next');await click('#crash-restart');assert.match(await evaluate('document.querySelector("#crash-state").innerText'),/Promise broken/);
 await click('#crash-reset');assert.equal(await evaluate('document.querySelectorAll("#crash-trace li").length'),0);
 await screenshot('chapter-desktop');
 await navigate('ch-1-2');await change('#change-scenario','retry','change');assert.match(await evaluate('document.querySelector("#change-result").innerText'),/Caller protocol/);
 await change('#change-scenario','format','change');assert.match(await evaluate('document.querySelector("#change-result").innerText'),/Input adapter/);
 await navigate('ch-1-3');
 const scores=await evaluate('SystemAtlas.decisionScores([5,1,1])');assert.equal(scores.embedded,4);assert.ok(Math.abs(scores.separate-18/7)<1e-12);
 for(const id of ['simple','growth','independent'])await change('#weight-'+id,0);assert.match(await evaluate('document.querySelector("#decision-result").innerText'),/All weights are zero/);
 await change('#weight-growth',5);assert.match(await evaluate('document.querySelector("#decision-result").innerText'),/Separate database ranks higher/);
 await change('#weight-simple',5);await change('#weight-growth',1);await change('#weight-independent',1);
 await screenshot('decisions-desktop');
 await screenshot('requirement-figure','fig-1-3-1');
 await navigate('ch-1-4');for(const v of ['container','component','code','context']){await click(`[data-view="${v}"]`);assert.equal(await evaluate(`document.querySelector('[data-view="${v}"]').getAttribute('aria-pressed')`),'true');}
 await screenshot('sequence-figure','fig-1-4-3');
 await navigate('ch-1-2');await screenshot('dependency-figure','fig-1-2-3');
 await navigate('overview');await change('#atlas-search','captive dependencies');assert.match(await evaluate('document.querySelector("#search-results").innerText'),/Planned/);
 await change('#atlas-search','<img src=x onerror=alert(1)>');assert.equal(await evaluate('document.querySelectorAll("#search-results img").length'),0);
 await change('#atlas-search','promise');await click('#search-results a');await new Promise(r=>setTimeout(r,100));assert.equal(await evaluate('SystemAtlas.activePanel'),'ch-1-1');
 await navigate('glossary');await change('#glossary-search','unfindable-term');assert.equal(await evaluate('document.querySelector("#glossary-empty").hidden'),false);await change('#glossary-search','durability');
 await navigate('sources');await change('#source-search','raft');assert.match(await evaluate('document.querySelector("#source-count").innerText'),/^1 of/);await change('#source-search','unfindable-term');assert.equal(await evaluate('document.querySelector("#source-empty").hidden'),false);await change('#source-search','');
 await navigate('ch-1-1');const wasRead=await evaluate('document.querySelector("[data-read=ch-1-1]").getAttribute("aria-pressed")');await click('[data-read="ch-1-1"]');const isRead=wasRead==='false'?'true':'false';assert.equal(await evaluate('document.querySelector("[data-read=ch-1-1]").getAttribute("aria-pressed")'),isRead);
 await page('system-design/index.html#ch-1-1');assert.equal(await evaluate('document.querySelector("[data-read=ch-1-1]").getAttribute("aria-pressed")'),isRead);
 await page('system-design/index.html#fig-1-4-3');assert.equal(await evaluate('SystemAtlas.activePanel'),'ch-1-4');
 await page('system-design/index.html#solution-S1');assert.equal(await evaluate('SystemAtlas.activePanel'),'solutions');
 // Every panel must fit each reading width. Large SVGs and code scroll locally.
 const ids=await evaluate('[...document.querySelectorAll(".panel")].map(x=>x.id)');
 for(const width of [1440,1024,768,390,360]){
  await call('Emulation.setDeviceMetricsOverride',{width,height:1100,deviceScaleFactor:1,mobile:width<701});
  for(const id of ids){await navigate(id);const dims=await evaluate('({w:innerWidth,scroll:document.documentElement.scrollWidth})');assert.ok(dims.scroll<=dims.w+1,`${id} overflows at ${width}: ${dims.scroll}`);}
 }
 await navigate('overview');await screenshot('overview-mobile');await click('#menu-toggle');assert.equal(await evaluate('document.querySelector("#menu-toggle").getAttribute("aria-expanded")'),'true');await click('.nav-chapter');await new Promise(r=>setTimeout(r,100));assert.equal(await evaluate('document.querySelector("#menu-toggle").getAttribute("aria-expanded")'),'false');
 await navigate('ch-1-3');await screenshot('chapter-mobile');
 await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false});
 await navigate('glossary');await change('#glossary-search','durability');await change('#source-search','raft');
 await evaluate('dispatchEvent(new Event("beforeprint"))');await call('Emulation.setEmulatedMedia',{media:'print'});
 assert.equal(await evaluate('[...document.querySelectorAll(".chapter")].every(x=>getComputedStyle(x).display!=="none")'),true);
 assert.equal(await evaluate('[...document.querySelectorAll(".planned-chapter")].every(x=>getComputedStyle(x).display==="none")'),true);
 assert.equal(await evaluate('document.querySelectorAll(".chapter details:not([open])").length'),0);
 const pdf=await call('Page.printToPDF',{printBackground:true,preferCSSPageSize:true,displayHeaderFooter:false});
 writeFileSync(join(root,'system-design/System-Design-Atlas-Foundations.pdf'),Buffer.from(pdf.data,'base64'));
 await evaluate('dispatchEvent(new Event("afterprint"))');await call('Emulation.setEmulatedMedia',{media:''});assert.equal(await evaluate('document.querySelector("#glossary-search").value'),'durability');assert.equal(await evaluate('document.querySelector("#source-search").value'),'raft');
 await page('index.html','Boolean(document.querySelector("#system-design-unit"))');
 await change('#unit-search','system design');assert.equal(await evaluate('document.querySelector("#system-design-unit").hidden'),false);assert.equal(await evaluate('document.querySelector("#retrieval-unit").hidden'),true);
 await change('#unit-search','rank fusion');assert.equal(await evaluate('document.querySelector("#retrieval-unit").hidden'),false);assert.equal(await evaluate('document.querySelector("#system-design-unit").hidden'),true);
 await change('#unit-search','nothing matches');assert.equal(await evaluate('document.querySelector("#no-units").hidden'),false);await click('#reset-search');assert.match(await evaluate('document.querySelector("#unit-count").innerText'),/02 \/ 02/);
 for(const width of [1440,390,360]){await call('Emulation.setDeviceMetricsOverride',{width,height:1100,deviceScaleFactor:1,mobile:width<701});assert.ok(await evaluate('document.documentElement.scrollWidth<=innerWidth+1'));}await screenshot('library-mobile');
 // Readability with JavaScript disabled is an intentional product property.
 await call('Emulation.setScriptExecutionDisabled',{value:true});await call('Page.navigate',{url:pathToFileURL(join(root,'system-design/index.html')).href});await new Promise(r=>setTimeout(r,400));await call('Emulation.setScriptExecutionDisabled',{value:false});
 assert.equal(await evaluate('document.querySelectorAll(".chapter:not([hidden])").length'),4);
 assert.deepEqual(errors,[],'No runtime exceptions');assert.deepEqual(network.filter(u=>/^https?:/.test(u)),[],'No external reading requests');
 console.log(JSON.stringify({ok:true,panels:ids.length,widths:[1440,1024,768,390,360],chapters:4,chapterFigures:16,workbenches:4,questions:11,solutions:11,plannedChapters:95,pdfBytes:Buffer.from(pdf.data,'base64').length,screenshots:qa,checks:'failure histories, decision arithmetic, filtering, deep links, progress persistence, all-panel layout, complete produced-edition printing, no-JS reading, offline file loading, library search'},null,2));
 }
}finally{ws.close();}
