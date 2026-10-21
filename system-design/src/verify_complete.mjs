// Node 22+; dedicated local Chrome profile; no third-party browser library.
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {join,resolve} from 'node:path';
import {pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';
const root=resolve(process.argv[2]||join(import.meta.dirname,'../..'));
const manifest=JSON.parse(readFileSync(join(root,'system-design/completion-manifest.json'),'utf8'));
const profile=process.argv[3]||'/tmp/system-design-atlas-chrome/DevToolsActivePort';
const port=readFileSync(profile,'utf8').split('\n')[0];
const targets=await(await fetch(`http://127.0.0.1:${port}/json`)).json();
const ws=new WebSocket(targets.find(t=>t.type==='page').webSocketDebuggerUrl);
await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j;});let serial=0;const pending=new Map(),errors=[],network=[];
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails);if(m.method==='Network.requestWillBeSent')network.push(m.params.request.url);if(m.id&&pending.has(m.id)){const {resolve,reject,timer}=pending.get(m.id);clearTimeout(timer);pending.delete(m.id);m.error?reject(Error(JSON.stringify(m.error))):resolve(m.result);}};
function call(method,params={},timeout=30000){return new Promise((resolve,reject)=>{const id=++serial,timer=setTimeout(()=>{pending.delete(id);reject(Error('CDP timeout: '+method));},timeout);pending.set(id,{resolve,reject,timer});ws.send(JSON.stringify({id,method,params}));});}
async function evaluate(expression){const r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result?.value;}
async function load(path,ready='Boolean(window.SYSTEM_ATLAS_READY)'){
 const [file,hash]=path.split('#'),url=pathToFileURL(join(root,file));if(hash)url.hash=hash;
 await call('Page.navigate',{url:url.href});for(let i=0;i<150;i++){if(await evaluate(ready))return;await new Promise(r=>setTimeout(r,50));}throw Error('Page failed to initialize: '+path);
}
const change=async(s,v,event='input')=>evaluate(`(()=>{let e=document.querySelector(${JSON.stringify(s)});e.value=${JSON.stringify(v)};e.dispatchEvent(new Event(${JSON.stringify(event)},{bubbles:true}));})()`);
const click=s=>evaluate(`document.querySelector(${JSON.stringify(s)}).click()`);
const text=s=>evaluate(`document.querySelector(${JSON.stringify(s)}).innerText`);
async function navigate(id){await evaluate(`SystemAtlas.navigate('#'+${JSON.stringify(id)})`);assert.equal(await evaluate('SystemAtlas.activePanel'),id);assert.equal(await evaluate('document.querySelectorAll(".panel:not([hidden])").length'),1);}
const qa='/tmp/system-design-complete-qa';mkdirSync(qa,{recursive:true});
async function capture(name){await evaluate('scrollTo({top:0,behavior:"instant"})');const result=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});writeFileSync(join(qa,name+'.png'),Buffer.from(result.data,'base64'));}
async function exportPDF(){
 await evaluate('dispatchEvent(new Event("beforeprint"))');await call('Emulation.setEmulatedMedia',{media:'print'});
 assert.equal(await evaluate('[...document.querySelectorAll(".chapter")].filter(e=>getComputedStyle(e).display!=="none").length'),99);
 assert.equal(await evaluate('document.querySelectorAll("details:not([open])").length'),0);
 const pdf=await call('Page.printToPDF',{printBackground:true,preferCSSPageSize:true,generateDocumentOutline:true,generateTaggedPDF:true,displayHeaderFooter:false},180000);
 const bytes=Buffer.from(pdf.data,'base64');writeFileSync(join(root,'system-design/System-Design-Atlas-Complete.pdf'),bytes);
 await evaluate('dispatchEvent(new Event("afterprint"))');await call('Emulation.setEmulatedMedia',{media:''});
 console.log('Complete PDF exported: '+bytes.length+' bytes');return bytes.length;
}
await call('Runtime.enable');await call('Page.enable');await call('Network.enable');
await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false});
try{
 await load('system-design/index.html');
 if(process.argv.includes('--pdf-only')){await exportPDF();}
 else if(process.argv.includes('--figures-only')){
  const figures=manifest.figures.filter(f=>['fig-4-0-1','fig-6-0-2','fig-10-0-1','fig-12-0-2','fig-14-0-1','fig-18-0-1','fig-22-9-2','fig-22-11-3','fig-22-12-3','fig-2-0-2'].includes(f.id));
  for(const f of figures){await evaluate(`SystemAtlas.navigate('#'+${JSON.stringify(f.id)})`);const clip=await evaluate(`(()=>{const r=document.getElementById(${JSON.stringify(f.id)}).getBoundingClientRect();return {x:r.x+scrollX,y:r.y+scrollY,width:r.width,height:r.height,scale:1}})()`);const result=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip});writeFileSync(join(qa,f.id+'.png'),Buffer.from(result.data,'base64'));}console.log('Captured '+figures.length+' representative complete figures.');
 }else{
  assert.equal(await evaluate('document.querySelectorAll(".chapter").length'),99);
  assert.equal(await evaluate('document.querySelectorAll(".planned-chapter").length'),0);
  assert.equal(await evaluate('document.querySelectorAll(".chapter .figure").length'),manifest.units.flatMap(u=>u.chapters).reduce((s,c)=>s+c.illustrations.length,0));
  assert.equal(await evaluate('document.querySelectorAll("figure.figure").length'),manifest.counts.figures_produced+1);
  assert.equal(await evaluate('document.querySelectorAll(".exercise").length'),242);
  assert.equal(await evaluate('document.querySelectorAll(".solution").length'),242);
  assert.equal(await evaluate('document.querySelectorAll(".case-section").length'),264);
  assert.equal(await evaluate('document.querySelectorAll(".pattern-lesson").length'),26);
  assert.equal(await evaluate('document.querySelectorAll("script[src],link[rel=stylesheet],img[src^=http]").length'),0);
  assert.equal(await evaluate('document.querySelectorAll(".lab").length'),13);
  await capture('complete-overview-desktop');
  await navigate('ch-2-4');const capacity=await evaluate('SystemAtlas.capacityModel(1e7,50,5,600,.6)');assert.equal(capacity.active,81);assert.equal(capacity.failure,82);assert.ok(Math.abs(capacity.avg-5787.037037)<1e-5);
  assert.match(await text('#model-capacity-result'),/81/);await change('#model-users',0);assert.match(await text('#model-capacity-result'),/0/);await change('#model-users',10000000);
  await navigate('ch-4-4');assert.deepEqual(await evaluate('SystemAtlas.queueModel(150,100,60,100)'),{arrived:9000,done:6000,waiting:100,rejected:2900});
  await navigate('ch-10-4');assert.match(await text('#model-ticket-result'),/Two callers/);await change('#model-ticket-policy','conditional','change');assert.match(await text('#model-ticket-result'),/sole owner/);
  await navigate('ch-11-4');assert.match(await text('#model-lru-result'),/evict B/);await change('#model-cache-access','<img src=x>,A,<img src=x>');assert.equal(await evaluate('document.querySelectorAll("#model-lru-result img").length'),0);await change('#model-cache-access','A,B,C,A,D');
  await navigate('ch-12-4');assert.equal(await evaluate('(()=>{for(let k=0;k<1000;k++){let a=SystemAtlas.hashOwner(k,["A","B","C"]),b=SystemAtlas.hashOwner(k,["A","B","C","D"]);if(a!==b&&b!=="D")return false;}return true})()'),true);
  await navigate('ch-13-4');assert.match(await text('#model-pipeline-result'),/Reject/);await change('#model-pipeline-scenario','valid','change');assert.match(await text('#model-pipeline-result'),/Accept/);await change('#model-pipeline-scenario','deleted','change');assert.match(await text('#model-pipeline-result'),/Reject/);
  await navigate('ch-14-4');assert.match(await text('#model-quorum-result'),/must intersect/);await change('#model-quorum-r',1);assert.match(await text('#model-quorum-result'),/Disjoint/);await change('#model-quorum-r',2);await change('#model-quorum-w',4);assert.match(await text('#model-quorum-result'),/between one and N/);await change('#model-quorum-w',2);
  await navigate('ch-22-2');for(let i=0;i<11;i++)await click('#model-bucket-spend');assert.match(await text('#model-bucket-result'),/admitted: 10.*rejected: 1/);await click('#model-bucket-advance');assert.match(await text('#model-bucket-result'),/tokens: 6/);await click('#model-bucket-reset');
  await navigate('ch-21-4');assert.match(await text('#model-cost-result'),/0\.002473/);await change('#model-outcomes',0);assert.match(await text('#model-cost-result'),/range/);await change('#model-outcomes',150000);
  await navigate('ch-1-1');await change('#crash-policy','early','change');for(let i=0;i<3;i++)await click('#crash-next');await click('#crash-restart');assert.match(await text('#crash-state'),/Promise broken/);await change('#crash-policy','durable','change');for(let i=0;i<4;i++)await click('#crash-next');await click('#crash-restart');assert.match(await text('#crash-state'),/Task recovered/);
  await navigate('overview');await change('#atlas-search','fencing');assert.match(await text('#search-results'),/Produced/);await change('#atlas-search','');
  await navigate('glossary');await change('#glossary-search','unfindable-complete-atlas-term');assert.equal(await evaluate('document.querySelector("#glossary-empty").hidden'),false);await change('#glossary-search','');
  await navigate('sources');await change('#source-search','raft.github.io');assert.match(await text('#source-count'),/^1 of/);await change('#source-search','');
  await load('system-design/index.html#topic-15-12');assert.equal(await evaluate('SystemAtlas.activePanel'),'ch-15-3');
  await load('system-design/index.html#pattern-visitor');assert.equal(await evaluate('SystemAtlas.activePanel'),'ch-6-6');
  await load('system-design/index.html#solution-22-S2');assert.equal(await evaluate('SystemAtlas.activePanel'),'solutions');
  await navigate('ch-22-12');await click('[data-read="ch-22-12"]');const marked=await evaluate('document.querySelector("[data-read=ch-22-12]").getAttribute("aria-pressed")');await load('system-design/index.html#ch-22-12');assert.equal(await evaluate('document.querySelector("[data-read=ch-22-12]").getAttribute("aria-pressed")'),marked);assert.match(await text('#reading-progress'),/of 99/);
  await capture('document-design-desktop');
  const ids=await evaluate('[...document.querySelectorAll(".panel")].map(e=>e.id)');
  const clipped=[];
  for(const width of [1440,1024,768,390,360]){
   await call('Emulation.setDeviceMetricsOverride',{width,height:1100,deviceScaleFactor:1,mobile:width<701});
   for(const id of ids){await navigate(id);const dims=await evaluate('({w:innerWidth,scroll:document.documentElement.scrollWidth})');assert.ok(dims.scroll<=dims.w+1,`${id} overflows ${width}: ${dims.scroll}`);
    if(width===1440){const bad=await evaluate(`(()=>{let out=[];for(let svg of document.querySelector('#'+${JSON.stringify(id)}).querySelectorAll('.figure svg')){const v=svg.viewBox.baseVal;for(let t of svg.querySelectorAll('text')){const b=t.getBBox();if(b.x < -2||b.y < -2||b.x+b.width>v.width+3||b.y+b.height>v.height+3)out.push({figure:svg.closest('figure').id,text:t.textContent,box:[b.x,b.y,b.width,b.height],view:[v.width,v.height]});}}return out})()`);clipped.push(...bad);}
   }
   console.log('All '+ids.length+' views fit '+width+' px.');
  }
  writeFileSync(join(qa,'svg-text-bounds.json'),JSON.stringify(clipped,null,2));assert.deepEqual(clipped,[],'SVG text must fit its viewBox');
  await navigate('overview');await capture('complete-overview-mobile');await click('#menu-toggle');assert.equal(await evaluate('document.querySelector("#menu-toggle").getAttribute("aria-expanded")'),'true');await click('a[href="#ch-22-9"]');await new Promise(r=>setTimeout(r,60));assert.equal(await evaluate('SystemAtlas.activePanel'),'ch-22-9');assert.equal(await evaluate('document.querySelector("#menu-toggle").getAttribute("aria-expanded")'),'false');await capture('payment-design-mobile');
  await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1100,deviceScaleFactor:1,mobile:false});
  await navigate('sources');await change('#source-search','raft');await change('#glossary-search','durability');
  await evaluate('dispatchEvent(new Event("beforeprint"))');await call('Emulation.setEmulatedMedia',{media:'print'});assert.equal(await evaluate('[...document.querySelectorAll(".chapter")].filter(e=>getComputedStyle(e).display!=="none").length'),99);await evaluate('dispatchEvent(new Event("afterprint"))');await call('Emulation.setEmulatedMedia',{media:''});assert.equal(await evaluate('document.querySelector("#source-search").value'),'raft');assert.equal(await evaluate('document.querySelector("#glossary-search").value'),'durability');
  await load('index.html','Boolean(document.querySelector("#system-design-unit"))');await change('#unit-search','system design');assert.equal(await evaluate('document.querySelector("#system-design-unit").hidden'),false);assert.equal(await evaluate('document.querySelector("#retrieval-unit").hidden'),true);await change('#unit-search','rank fusion');assert.equal(await evaluate('document.querySelector("#retrieval-unit").hidden'),false);await change('#unit-search','');
  for(const width of [1440,390,360]){await call('Emulation.setDeviceMetricsOverride',{width,height:1100,deviceScaleFactor:1,mobile:width<701});assert.ok(await evaluate('document.documentElement.scrollWidth<=innerWidth+1'));}
  await call('Emulation.setScriptExecutionDisabled',{value:true});await call('Page.navigate',{url:pathToFileURL(join(root,'system-design/index.html')).href});await new Promise(r=>setTimeout(r,500));await call('Emulation.setScriptExecutionDisabled',{value:false});assert.equal(await evaluate('document.querySelectorAll(".chapter:not([hidden])").length'),99);
  assert.deepEqual(errors,[],'No browser exceptions');assert.deepEqual(network.filter(u=>/^https?:/.test(u)),[],'Offline reading loads no external resources');
  console.log(JSON.stringify({ok:true,panels:ids.length,chapters:99,figures:manifest.counts.figures_produced,questions:242,solutions:242,caseSections:264,workbenches:13,widths:[1440,1024,768,390,360],svgTextBounds:'all fit',offline:true,noJavaScriptReading:true,screenshots:qa},null,2));
 }
}finally{ws.close();}
