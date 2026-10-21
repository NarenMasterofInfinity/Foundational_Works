"use strict";
document.body.classList.add('js');
const AtlasData=JSON.parse(document.getElementById('atlas-data').textContent);
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let activePanel='overview';
function navigate(hash,{focus=false}={}){
 const id=decodeURIComponent((hash||'#overview').replace(/^#/,''));
 const target=document.getElementById(id),panel=target?.classList.contains('panel')?target:target?.closest('.panel');
 const chosen=panel||$('#overview');activePanel=chosen.id;
 $$('.panel').forEach(p=>{p.hidden=p!==chosen;});
 $$('#book-nav a').forEach(a=>{if(a.getAttribute('href')==='#'+chosen.id)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
 const nav=$(`#book-nav a[href="#${chosen.id}"]`);if(nav?.closest('details'))nav.closest('details').open=true;
 $('.sidebar').classList.remove('is-open');$('#menu-toggle').setAttribute('aria-expanded','false');
 document.title=(chosen.id==='overview'?'The System Design Atlas':(chosen.querySelector('h1')?.textContent||'System Design Atlas')+' — The System Design Atlas');
 if(focus)$('#main').focus({preventScroll:true});
 if(target&&target!==chosen){target.scrollIntoView({block:'start',behavior:'instant'});target.classList.add('highlight-anchor');setTimeout(()=>target.classList.remove('highlight-anchor'),1800);}
 else window.scrollTo({top:0,behavior:'instant'});
}
document.addEventListener('click',event=>{
 const a=event.target.closest('a[href^="#"]');if(!a)return;
 const href=a.getAttribute('href');if(href==='#')return;
 event.preventDefault();$('#search-results').hidden=true;
 if(a.closest('#search-results'))$('#atlas-search').value='';
 if(location.hash===href)navigate(href,{focus:true});else location.hash=href;
});
window.addEventListener('hashchange',()=>navigate(location.hash,{focus:true}));
$('#menu-toggle').addEventListener('click',()=>{const open=$('.sidebar').classList.toggle('is-open');$('#menu-toggle').setAttribute('aria-expanded',String(open));});
$('#atlas-search').addEventListener('input',()=>{
 const q=$('#atlas-search').value.toLowerCase().trim(),box=$('#search-results');
 if(!q){box.hidden=true;box.innerHTML='';return;}
 const terms=q.split(/\s+/),hits=AtlasData.search.filter(r=>terms.every(t=>(r.title+' '+r.text).toLowerCase().includes(t)));
 box.hidden=false;box.innerHTML=`<p>${hits.length} matches${hits.length>25?' · showing first 25':''}</p>`+hits.slice(0,25).map(r=>`<a class="search-hit" href="#${r.id}">${escapeHTML(r.title)}<small>${r.status==='available'?'Produced lesson / resource':'Planned treatment'}</small></a>`).join('')+(hits.length?'':'<p>No matching concept. Try a shorter term.</p>');
});
$('#atlas-search').addEventListener('keydown',e=>{if(e.key==='Escape'){$('#atlas-search').value='';$('#search-results').hidden=true;}if(e.key==='Enter')$('#search-results a')?.click();});

let readChapters=[];
try{const saved=JSON.parse(localStorage.getItem('system-design-atlas-reading')||'[]');if(Array.isArray(saved))readChapters=saved.filter(x=>AtlasData.chapters.includes(x));}catch{}
function refreshReading(){
 $$('.read-toggle').forEach(b=>{const yes=readChapters.includes(b.dataset.read);b.textContent=yes?'Marked read ✓':'Mark as read ○';b.setAttribute('aria-pressed',String(yes));});
 $('#reading-progress').textContent=`${readChapters.length} of 4 chapters marked read`;
}
$$('.read-toggle').forEach(b=>b.addEventListener('click',()=>{const id=b.dataset.read;readChapters=readChapters.includes(id)?readChapters.filter(x=>x!==id):[...readChapters,id];try{localStorage.setItem('system-design-atlas-reading',JSON.stringify(readChapters));}catch{}refreshReading();}));refreshReading();

const crashEvents={memory:['receive','mutate','ack'],early:['receive','mutate','ack','commit'],durable:['receive','mutate','commit','ack']};
function freshCrash(policy){return {policy,step:0,memory:false,stored:false,ack:false,restarted:false,trace:[]};}
let crash=freshCrash('durable');
function advanceCrash(s){
 if(s.restarted||s.step>=crashEvents[s.policy].length)return s;
 const next={...s,trace:[...s.trace]},event=crashEvents[s.policy][s.step];next.step++;
 if(event==='receive')next.trace.push('1 · Request received: create “Read”.');
 if(event==='mutate'){next.memory=true;next.trace.push('2 · Task added to volatile application memory.');}
 if(event==='commit'){next.stored=true;next.trace.push(next.step+' · Atomic storage commit completed.');}
 if(event==='ack'){next.ack=true;next.trace.push(next.step+' · Caller received “saved” acknowledgment.');}
 return next;
}
function restartCrash(s){return {...s,memory:s.stored,restarted:true,trace:[...s.trace,'Restart · volatile state discarded; committed state reloaded.']};}
function renderCrash(){
 const s=crash,finished=s.step===crashEvents[s.policy].length,violation=s.restarted&&s.ack&&!s.stored;
 const title=violation?'Promise broken: an acknowledged task was lost.':s.restarted&&s.stored?'Task recovered from committed storage.':s.restarted?'No committed task recovered.':s.ack?'The caller has received success.':'The caller has not received success.';
 $('#crash-state').innerHTML=`<p>Policy: ${escapeHTML($('#crash-policy').selectedOptions[0].textContent)} · ${s.step} events executed${s.restarted?' · restarted':''}</p><strong class="${violation?'bad':'good'}">${title}</strong><div class="state-grid"><div><small>APPLICATION MEMORY</small>${s.memory?'Task 7: Read':'Empty'}</div><div><small>COMMITTED STORE</small>${s.stored?'Task 7: Read':'Empty'}</div><div><small>CALLER’S KNOWLEDGE</small>${s.ack?'Received “saved”':'No success received'}</div></div><p style="margin:10px 0 0">${s.restarted&&!s.ack?'No successful response was received; the caller cannot infer whether a commit happened.':violation?'The early success message promised more than the recovered state can support.':s.stored&&!s.ack?'A commit exists before the caller knows the result. A timeout here would leave an uncertain outcome.':'Step the request, or restart to test the current state.'}</p>`;
 $('#crash-next').disabled=s.restarted||finished;$('#crash-restart').disabled=s.restarted;
 $('#crash-trace').innerHTML=s.trace.map(t=>'<li>'+escapeHTML(t)+'</li>').join('');
}
function resetCrash(){crash=freshCrash($('#crash-policy').value);renderCrash();}
$('#crash-policy').addEventListener('change',resetCrash);$('#crash-next').addEventListener('click',()=>{crash=advanceCrash(crash);renderCrash();});$('#crash-restart').addEventListener('click',()=>{crash=restartCrash(crash);renderCrash();});$('#crash-reset').addEventListener('click',resetCrash);renderCrash();

const changeImpact={
 format:{tangled:['Handler','Task logic','Storage access embedded in handler'],separated:['Input adapter'],reason:'Change the transport parser. The application command and persistent representation remain the same.'},
 rule:{tangled:['HTTP validation copy','CLI validation copy','Storage constraint, if present'],separated:['Task service','Storage constraint, if present'],reason:'The service owns the authoritative rule. A storage guard must remain compatible; this is intentional invariant protection.'},
 schema:{tangled:['HTTP handler SQL','Task logic SQL','Exporter SQL'],separated:['Storage adapter','Migration'],reason:'Hide the representation behind the repository. Still test the migration against existing data.'},
 retry:{tangled:['Handler','Task state','Persistence','Caller protocol'],separated:['Input contract','Task service','Repository contract','Caller protocol'],reason:'This changes observable semantics. Good boundaries expose the required agreement; they do not make a cross-boundary behavior local.'}
};
 function renderChange(){const d=changeImpact[$('#change-scenario').value];$('#change-result').innerHTML=`<div class="lab-output"><p><strong>Scenario:</strong> ${escapeHTML($('#change-scenario').selectedOptions[0].textContent)}</p><p><strong>Tangled design:</strong> ${d.tangled.map(escapeHTML).join(' · ')}</p><p><strong>Separated design:</strong> ${d.separated.map(escapeHTML).join(' · ')}</p><p style="margin:0">${escapeHTML(d.reason)}</p></div>`;}
$('#change-scenario').addEventListener('change',renderChange);renderChange();

function decisionScores(weights){
 const total=weights.reduce((a,b)=>a+b,0);if(total===0)return null;
 return {embedded:weights.reduce((s,w,i)=>s+w*[5,2,1][i],0)/total,separate:weights.reduce((s,w,i)=>s+w*[2,4,4][i],0)/total};
}
function renderDecision(){
 const ids=['simple','growth','independent'],weights=ids.map(id=>Number($('#weight-'+id).value));ids.forEach((id,i)=>$('#out-'+id).textContent=weights[i]);const scores=decisionScores(weights);
 if(!scores){$('#decision-result').innerHTML='<div class="lab-output">All weights are zero. Choose a positive preference weight to compare candidates. Memory-only remains infeasible.</div>';return;}
 const row=(name,v,cls='')=>`<div class="bar-row"><span>${name}</span><span class="bar-track ${cls}"><i style="width:${v/5*100}%"></i></span><strong>${v.toFixed(2)}</strong></div>`;
 const tie=Math.abs(scores.embedded-scores.separate)<1e-10;
 $('#decision-result').innerHTML=`<div class="lab-output"><p>Weights (simplicity, growth, host independence): ${weights.join(', ')}.</p>`+row('Embedded store',scores.embedded)+row('Separate database',scores.separate,'purple')+`<p>${tie?'The candidates tie under these judgments.':(scores.embedded>scores.separate?'Embedded store':'Separate database')+' ranks higher under the selected preferences.'} The scores do not establish throughput or availability.</p><p class="bad" style="margin:0">Memory only: rejected by mandatory restart persistence.</p></div>`;
}
['simple','growth','independent'].forEach(id=>$('#weight-'+id).addEventListener('input',renderDecision));renderDecision();

const views={
 context:{question:'Who uses the system?',boxes:['Team member','→ uses →','Task system'],reason:'The system boundary includes responsibility for task behavior. Internal deployment is intentionally hidden.'},
 container:{question:'Which applications and data stores cooperate?',boxes:['Browser client','→ HTTPS →','Server application','→ local I/O →','Task store'],reason:'The application and store are C4 containers. The store can be a local file; this is not a claim that it is a separate server.'},
 component:{question:'Which responsibilities collaborate inside the server?',boxes:['Input adapter','→ create command →','Task service','→ save →','Storage adapter'],reason:'These are modules within the same application process. All share the process and host failure domain.'},
 code:{question:'Which interfaces and types implement the task operation?',boxes:['TaskService.create(title)','→ calls →','TaskRepository.insert(title)','→ returns →','Task(id, title, done)'],reason:'The service owns validation; the repository contract owns commit-before-return. The runtime adapter is supplied at composition.'}
};
function renderView(view='context'){
 const d=views[view];$$('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));
 $('#view-result').innerHTML=`<div class="lab-output"><strong>${escapeHTML(d.question)}</strong><div class="view-boxes">${d.boxes.map(t=>'<span>'+escapeHTML(t)+'</span>').join('')}</div><p style="margin:0">${escapeHTML(d.reason)}</p></div>`;
}
$$('[data-view]').forEach(b=>b.addEventListener('click',()=>renderView(b.dataset.view)));renderView();

function filterRows(inputSelector,rowSelector,countSelector,emptySelector,attribute){
 const input=$(inputSelector),rows=$$(rowSelector),terms=input.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
 let count=0;rows.forEach(row=>{const show=terms.every(t=>row.dataset[attribute].includes(t));row.hidden=!show;if(show)count++;});
 $(countSelector).textContent=`${count} of ${rows.length} ${attribute==='term'?'terms':'sources'}`;$(emptySelector).hidden=count>0;
}
const filterGlossary=()=>filterRows('#glossary-search','.glossary>[data-term]','#glossary-count','#glossary-empty','term');
const filterSources=()=>filterRows('#source-search','#source-list [data-source]','#source-count','#source-empty','source');
$('#glossary-search').addEventListener('input',filterGlossary);$('#source-search').addEventListener('input',filterSources);filterGlossary();filterSources();
let printState=null;
window.addEventListener('beforeprint',()=>{
 if(printState)return;
 printState={closed:$$('details:not([open])'),glossary:$('#glossary-search').value,sources:$('#source-search').value,title:document.title};
 document.title='The System Design Atlas — Foundations Edition';
 printState.closed.forEach(d=>d.open=true);$('#glossary-search').value='';$('#source-search').value='';filterGlossary();filterSources();document.body.classList.add('printing');
});
window.addEventListener('afterprint',()=>{
 if(!printState)return;printState.closed.forEach(d=>d.open=false);$('#glossary-search').value=printState.glossary;$('#source-search').value=printState.sources;document.title=printState.title;filterGlossary();filterSources();document.body.classList.remove('printing');printState=null;
});
$('#print-atlas').addEventListener('click',()=>window.print());
window.SystemAtlas={decisionScores,freshCrash,advanceCrash,restartCrash,crashEvents,changeImpact,navigate,get activePanel(){return activePanel;}};
navigate(location.hash);
window.SYSTEM_ATLAS_READY=true;
