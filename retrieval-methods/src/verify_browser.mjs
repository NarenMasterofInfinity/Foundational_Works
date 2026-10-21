// Node 22+, no dependencies. Use a dedicated Chrome debugging session.
// node verify_browser.mjs /absolute/site/root /tmp/profile/DevToolsActivePort
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {resolve,join} from 'node:path';
import {pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
const root=resolve(process.argv[2]||join(import.meta.dirname,'../..'));
const referenceCases=JSON.parse(execFileSync('python3',[join(import.meta.dirname,'math_reference.py')],{encoding:'utf8',env:{...process.env,PYTHONDONTWRITEBYTECODE:'1'}}));
const port=readFileSync(process.argv[3]||'/tmp/retrieval-intuition-chrome/DevToolsActivePort','utf8').split('\n')[0];
const targets=await (await fetch(`http://127.0.0.1:${port}/json`)).json();
const ws=new WebSocket(targets.find(t=>t.type==='page').webSocketDebuggerUrl);
await new Promise((r,j)=>{ws.onopen=r;ws.onerror=j;});
let serial=0;const pending=new Map(),errors=[];let network=[];
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails);if(m.method==='Network.requestWillBeSent')network.push(m.params.request.url);if(m.id&&pending.has(m.id)){const {resolve,reject,timer}=pending.get(m.id);clearTimeout(timer);pending.delete(m.id);m.error?reject(Error(JSON.stringify(m.error))):resolve(m.result);}};
function call(method,params={}){return new Promise((resolve,reject)=>{const id=++serial;const timer=setTimeout(()=>{pending.delete(id);reject(Error('CDP timeout: '+method));},20000);pending.set(id,{resolve,reject,timer});ws.send(JSON.stringify({id,method,params}));});}
async function evaluate(expression){const r=await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result?.value;}
async function change(selector,value){return evaluate(`(()=>{const e=document.querySelector(${JSON.stringify(selector)});e[${JSON.stringify(typeof value==='boolean'?'checked':'value')}]=${JSON.stringify(value)};e.dispatchEvent(new Event('input',{bubbles:true}));return true})()`);}
const text=selector=>evaluate(`document.querySelector(${JSON.stringify(selector)}).innerText`);
const click=selector=>evaluate(`document.querySelector(${JSON.stringify(selector)}).click()`);
async function tab(id){await evaluate(`history.replaceState(null,'','#${id}');navigate('${id}',{scroll:false})`);assert.equal(await evaluate(`document.querySelectorAll('.panel:not([hidden])').length`),1);}
async function load(path,ready){const [file,hash]=path.split('#');const url=pathToFileURL(join(root,file));if(hash)url.hash=hash;await call('Page.navigate',{url:url.href});for(let i=0;i<60;i++){if(await evaluate(ready))return;await new Promise(r=>setTimeout(r,50));}throw Error('Page did not become ready: '+path);}
const screenshots='/tmp/retrieval-intuition-qa';mkdirSync(screenshots,{recursive:true});
async function screenshot(name){await evaluate('window.scrollTo(0,0)');await new Promise(r=>setTimeout(r,300));const r=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});writeFileSync(join(screenshots,name+'.png'),Buffer.from(r.data,'base64'));}
await call('Runtime.enable');await call('Page.enable');await call('Network.enable');
await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1120,deviceScaleFactor:1,mobile:false});
try{
 await load('retrieval-methods/index.html','Boolean(window.RETRIEVAL_READY)');
 assert.equal(await evaluate(`document.querySelectorAll('[role=tab]').length`),17);
 assert.equal(await evaluate(`document.querySelectorAll('details.method').length`),52);
 assert.equal(await evaluate(`document.querySelectorAll('.lab').length`),14);
 assert.equal(await evaluate(`document.querySelectorAll('.idea-diagram').length`),14);
 assert.equal(await evaluate(`document.querySelectorAll('details.method .technical-note').length`),52);
 assert.equal(await evaluate(`document.querySelectorAll('details.method .technical-note[open]').length`),0);
 assert.equal(await evaluate(`document.querySelectorAll('.paper').length`),47);
 assert.equal(await evaluate(`(()=>{let ids=[...document.querySelectorAll('[id]')].map(e=>e.id);return ids.length===new Set(ids).size})()`),true);
 assert.equal(await evaluate(`document.querySelectorAll('script[src],link[rel=stylesheet],img[src^=http]').length`),0);

 const referenceActual=await evaluate(`(()=>{const A=window.RetrievalAtlas;return ${JSON.stringify(referenceCases)}.map(c=>{let rows;switch(c.kind){case 'bm25':rows=A.bm25(...c.args);break;case 'lexical':rows=A.lexical(...c.args);break;case 'likelihood':rows=A.queryLikelihood(...c.args);break;case 'fusion':rows=A.fusionResults(...c.args).ranked;break;case 'mmr':rows=A.mmrSelect(A.fusionResults(c.args[0],60,.5).ranked,c.args[1]);return {ids:rows.map(x=>x.d.id),values:rows.map(x=>x.mmr)};case 'ivf':{let r=A.ivfResults(...c.args);return {ids:r.approx.map(x=>x.id),values:[r.recall]};}case 'metrics':{let r=A.calcMetrics(...c.args);return {values:[r.precision,r.recall,r.rr,r.ndcg,r.ap,r.dcg,r.idcg]};}case 'geometry':return {values:[A.dot(...c.args),A.cosine(...c.args)]};}return {ids:rows.map(x=>x.d.id),values:rows.map(x=>x.score)};});})()`);
 referenceCases.forEach((expected,i)=>{const actual=referenceActual[i],label=expected.kind+' '+JSON.stringify(expected.args);if(expected.ids)assert.deepEqual(actual.ids,expected.ids,label+' order');expected.values.forEach((v,j)=>assert.ok(Math.abs(actual.values[j]-v)<=2e-11*Math.max(1,Math.abs(v)),label+' value '+j+': '+actual.values[j]+' vs '+v));});
 console.log('Passed '+referenceCases.length+' independent Python-reference calculation cases.');
 for(const id of await evaluate('TABLIST.map(t=>t[0])'))await tab(id);
 await tab('boolean');assert.match(await text('#boolean-result'),/2 documents satisfy/);
 await change('#bool-query','(solar OR battery) AND NOT storage');assert.match(await text('#boolean-result'),/2 documents satisfy/);
 await change('#bool-query','storage AND NOT battery');assert.match(await text('#boolean-result'),/3 documents satisfy/);
 await change('#bool-filter',true);assert.match(await text('#boolean-result'),/1 documents satisfy/);
 await change('#bool-filter',false);await change('#bool-query','"energy storage');assert.match(await text('#boolean-result'),/unclosed quote/);
 await change('#bool-query','battery-storage');assert.match(await text('#boolean-result'),/multiple indexed tokens/);await change('#bool-query','solar battery');assert.match(await text('#boolean-result'),/explicit AND or OR/);
 await change('#bool-query','"battery storage"');assert.match(await text('#boolean-result'),/2 documents satisfy/);

 await change('#bool-query','battery');assert.match(await text('#boolean-result'),/3 documents satisfy/);
 assert.equal(await evaluate(`document.querySelector('[data-document-id="D1"] .token-counts').textContent`),'Body occurrences: battery ×2');
 assert.equal(await evaluate(`document.querySelectorAll('[data-document-id="D1"] mark').length`),2);
 await change('#bool-query','batteries');assert.match(await text('#boolean-result'),/0 documents satisfy/);
 assert.equal(await evaluate(`document.querySelectorAll('#word-form-result .status:not(.bad)').length`),1);
 await change('#form-map',true);assert.equal(await evaluate(`document.querySelectorAll('#word-form-result .status:not(.bad)').length`),2);
 assert.match(await text('#boolean-result'),/0 documents satisfy/); // Mapping is confined to the separate fixture.
 await change('#form-map',false);await change('#form-query','batteries');assert.equal(await evaluate(`document.querySelector('[data-fixture="S1"] .status').textContent`),'NO');
 await change('#form-query','battery');
 await change('#bool-query','solar AND (battery OR storage)');
 await tab('lexical');let lex=await text('#lexical-result');assert.match(lex,/D1/);await change('#lex-mode','dot');assert.notEqual(await text('#lexical-result'),lex);await change('#lex-query','unseenword');assert.match(await text('#lexical-result'),/No matches/);await change('#lex-query','solar battery storage');await change('#lex-mode','cosine');
 const binary=await evaluate(`RetrievalAtlas.bm25('solar battery storage',0,.75).find(x=>x.d.id==='D1').score`);
 assert.ok(Math.abs(binary-(2*Math.log(9/3.5)+Math.log(9/5.5)))<1e-10);
 await tab('probabilistic');await change('#bm-mode','lm');assert.match(await text('#probabilistic-result'),/geometric mean/);await change('#bm-query','aquerynotincollection');assert.match(await text('#probabilistic-result'),/zero probability/);await change('#bm-query','solar battery storage');await change('#bm-mode','bm25');
 await tab('expansion');assert.match(await text('#expansion-result'),/vocabulary gap/);await change('#exp-mode','synonym');assert.match(await text('#expansion-result'),/D2/);await change('#exp-weight',0);assert.match(await text('#expansion-result'),/vocabulary gap/);await change('#exp-weight',.6);await change('#exp-mode','hyde');assert.match(await text('#expansion-result'),/D1/);
 await tab('dense');let cos=await evaluate(`[...document.querySelectorAll('#dense-result .rank-value')].map(e=>e.textContent)`);await change('#dense-scale',true);assert.deepEqual(await evaluate(`[...document.querySelectorAll('#dense-result .rank-value')].map(e=>e.textContent)`),cos);await change('#dense-metric','dot');assert.match(await text('#dense-result .rank-row'),/B · electric car/);await change('#dense-scale',false);await change('#dense-metric','cosine');
 await tab('sparse');await change('#sparse-expansion',0);assert.match(await text('#sparse-result'),/2 nonzero word clues/);await change('#sparse-expansion',1);await change('#sparse-threshold',1);assert.match(await text('#sparse-result'),/2 nonzero word clues/);await change('#sparse-threshold',.2);await change('#sparse-expansion',.8);
 await tab('late');assert.match(await text('#late-result'),/MaxSim = 1.70/);await change('#late-doc','duplicate');assert.match(await text('#late-result'),/MaxSim = 1.70/);await change('#late-storage',false);assert.match(await text('#late-result'),/MaxSim = 0.90/);await change('#late-storage',true);await change('#late-doc','one');assert.match(await text('#late-result'),/MaxSim = 1.16/);await change('#late-doc','balanced');
 await tab('indexes');assert.equal(await evaluate('RetrievalAtlas.ivfResults(1,.5).recall'),.5);await change('#ivf-probe',3);assert.match(await text('#indexes-result'),/100%/);await change('#ivf-probe',1);
 await tab('ranking');assert.match(await text('#ranking-result'),/OUT/);await change('#rerank-depth',8);assert.match(await text('#ranking-result'),/7 positive word matches/);assert.match(await text('#ranking-result'),/OUT/);await change('#rerank-source','hybrid');assert.match(await text('#ranking-result .rank-row'),/D2/);await change('#rerank-source','lexical');await change('#rerank-depth',3);
 await tab('fusion');const fused=await evaluate(`RetrievalAtlas.fusionResults(4,60,.5).ranked[0]`);assert.equal(fused.d.id,'D1');assert.ok(Math.abs(fused.score-(.5/61+.5/62))<1e-12);await change('#fusion-alpha',0);assert.match(await text('#fusion-result tbody tr'),/D2/);await change('#fusion-alpha',.5);await change('#fusion-duplicate',true);assert.match(await text('#fusion-result'),/second copy/);await change('#fusion-duplicate',false);await change('#fusion-mode','score');await change('#fusion-depth',1);assert.ok(!(await text('#fusion-result')).includes('NaN'));await change('#fusion-depth',4);await change('#fusion-mode','mmr');assert.match(await text('#fusion-result'),/MMR at selection/);await change('#fusion-mode','rrf');
 await tab('structured');await change('#graph-mode','two');assert.match(await text('#structured-result'),/sodium/);await change('#graph-edge',false);assert.match(await text('#structured-result'),/No supported material answer/);await change('#graph-mode','summary');assert.match(await text('#structured-result'),/do not assert sodium/);await change('#graph-edge',true);
 await tab('multimodal');await change('#visual-query','chart');await change('#visual-mode','layout');assert.match(await text('#multimodal-result'),/loses a clue/);await change('#visual-mode','visual');assert.match(await text('#multimodal-result'),/needed relationship is retained/);
 await tab('frontier');await change('#agent-budget',3);assert.match(await text('#frontier-result'),/100%/);await change('#agent-diverse',false);assert.match(await text('#frontier-result'),/33%/);await change('#agent-diverse',true);
 await tab('evaluation');await change('#eval-preset','ideal');const ideal=await evaluate(`calcMetrics(evalOrder,5)`);for(const key of ['precision','recall','rr','ndcg','ap'])assert.equal(ideal[key],1,key);await change('#eval-k',1);await change('#eval-preset','reverse');assert.match(await text('#evaluation-result .metric-grid'),/0.000/);await click('#evaluation-result [data-move="0"][data-dir="1"]');await change('#eval-k',5);await change('#eval-preset','bm25');
 await click('[data-quiz="right"]');assert.match(await text('#quiz-answer'),/Correct/);
 await tab('sources');await change('#paper-search','Sparse Lexical and Expansion Model');assert.match(await text('#paper-count'),/1 of 47/);await change('#paper-search','unfindablepaper');assert.match(await text('#paper-list'),/No sources match/);await change('#paper-search','');
 await tab('timeline');await click('[data-era="recent"]');assert.ok(await evaluate(`[...document.querySelectorAll('.timeline-event time')].every(e=>parseInt(e.textContent)>=2021)`));await click('[data-milestone="22"]');assert.match(await text('#timeline-detail'),/complementary evidence/i);await click('[data-era="all"]');
 await tab('overview');await change('#global-search','reciprocal rank');await click('[data-result-cat="fusion"]');assert.equal(await evaluate('activeTab'),'fusion');assert.equal(await evaluate(`document.querySelector('#method-fusion-1').open`),true);
 await click('[data-expand="fusion"]');assert.equal(await evaluate(`document.querySelectorAll('#panel-fusion details.method:not([open])').length`),0);await click('[data-expand="fusion"]');
 await tab('overview');await screenshot('unit-desktop');
 await tab('fusion');await screenshot('fusion-desktop');
 const layouts=[];
 for(const width of [1440,1024,768,390,360]){await call('Emulation.setDeviceMetricsOverride',{width,height:1024,deviceScaleFactor:1,mobile:width<641});for(const id of await evaluate('TABLIST.map(t=>t[0])')){await tab(id);const dims=await evaluate(`({w:innerWidth,scroll:document.documentElement.scrollWidth})`);assert.ok(dims.scroll<=dims.w+1,`${id} overflows ${width}: ${dims.scroll}`);}layouts.push(width);}
 await tab('overview');await screenshot('unit-mobile');await click('#menu-toggle');assert.equal(await evaluate(`document.querySelector('#menu-toggle').getAttribute('aria-expanded')`),'true');await click('#tab-timeline');await new Promise(r=>setTimeout(r,50));assert.equal(await evaluate('activeTab'),'timeline');assert.equal(await evaluate(`document.querySelector('#menu-toggle').getAttribute('aria-expanded')`),'false');
 await tab('fusion');await screenshot('fusion-mobile');
 await load('retrieval-methods/index.html#late','Boolean(window.RETRIEVAL_READY)');assert.equal(await evaluate('activeTab'),'late');

 await evaluate("document.querySelector('#tab-late').dispatchEvent(new KeyboardEvent('keydown',{key:'End',bubbles:true}))");assert.equal(await evaluate('activeTab'),'sources');
 await evaluate("document.querySelector('#tab-sources').dispatchEvent(new KeyboardEvent('keydown',{key:'Home',bubbles:true}))");assert.equal(await evaluate('activeTab'),'overview');
 await change('#paper-search','SPLADE');await click('[data-era="recent"]');
 await evaluate("window.dispatchEvent(new Event('beforeprint'))");
 assert.equal(await evaluate("document.querySelectorAll('details:not([open])').length"),0);
 assert.equal(await evaluate("document.querySelectorAll('.paper').length"),47);
 await call('Emulation.setEmulatedMedia',{media:'print'});
 assert.equal(await evaluate("[...document.querySelectorAll('.panel')].filter(e=>getComputedStyle(e).display!=='none').length"),17);
 const printed=await call('Page.printToPDF',{printBackground:true,preferCSSPageSize:true});
 assert.ok(printed.data.length>10000);writeFileSync(join(screenshots,'print-guide.pdf'),Buffer.from(printed.data,'base64'));
 await evaluate("window.dispatchEvent(new Event('afterprint'))");
 assert.equal(await evaluate("document.querySelector('#paper-search').value"),'SPLADE');assert.equal(await evaluate('eraFilter'),'recent');
 await call('Emulation.setEmulatedMedia',{media:''});
 await load('index.html',`Boolean(document.querySelector('#retrieval-unit'))`);
 await change('#unit-search','random no match');assert.equal(await evaluate(`document.querySelector('#retrieval-unit').hidden`),true);await click('#reset-search');assert.equal(await evaluate(`document.querySelector('#retrieval-unit').hidden`),false);await change('#unit-search','rank fusion');assert.equal(await evaluate(`document.querySelector('#retrieval-unit').hidden`),false);await change('#unit-search','');
 for(const width of [1440,1024,768,390,360]){await call('Emulation.setDeviceMetricsOverride',{width,height:1120,deviceScaleFactor:1,mobile:width<641});assert.ok(await evaluate('document.documentElement.scrollWidth<=innerWidth+1'),`home overflows ${width}`);if(width===1440)await screenshot('home-desktop');if(width===390)await screenshot('home-mobile');}
 await click('a[href="retrieval-methods/index.html"]');for(let i=0;i<50&&!await evaluate('Boolean(window.RETRIEVAL_READY)');i++)await new Promise(r=>setTimeout(r,30));assert.equal(await evaluate('Boolean(window.RETRIEVAL_READY)'),true);
 assert.deepEqual(errors,[],'No browser exceptions');
 const external=network.filter(u=>/^https?:/.test(u));assert.deepEqual(external,[],'Reading the guide makes no external network requests');
 console.log(JSON.stringify({ok:true,tabs:17,methodNotes:52,labs:14,references:47,viewports:layouts,independentMathCases:referenceCases.length,checks:'intuition sections, exact word-form behavior, score traces, reference equations, navigation, mobile, complete printing, offline file loading',screenshots},null,2));
}finally{ws.close();}
