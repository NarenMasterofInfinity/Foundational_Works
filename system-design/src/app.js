"use strict";
document.body.classList.add('js');
const AtlasData=JSON.parse(document.getElementById('atlas-data').textContent);
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let activePanel='overview';
function navigate(hash,{focus=false}={}){
 let id;try{id=decodeURIComponent((hash||'#overview').replace(/^#/,''));}catch{id='overview';}
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
 $('#reading-progress').textContent=`${readChapters.length} of ${AtlasData.chapters.length} chapters marked read`;
}
$$('.read-toggle').forEach(b=>b.addEventListener('click',()=>{const id=b.dataset.read;readChapters=readChapters.includes(id)?readChapters.filter(x=>x!==id):[...readChapters,id];try{localStorage.setItem('system-design-atlas-reading',JSON.stringify(readChapters));}catch{}refreshReading();}));refreshReading();

const crashEvents={memory:['receive','mutate','ack'],early:['receive','mutate','ack','commit'],durable:['receive','mutate','commit','ack']};
function freshCrash(policy){return {policy,step:0,memory:false,stored:false,ack:false,restarted:false,trace:[]};}
let crash=freshCrash('durable');
function advanceCrash(s){
 if(s.restarted||s.step>=crashEvents[s.policy].length)return s;
 const next={...s,trace:[...s.trace]},event=crashEvents[s.policy][s.step];next.step++;
 if(event==='receive')next.trace.push('1 · Request received: create “Read”.');
 if(event==='mutate'){next.memory=true;next.trace.push('2 · Task added to the running program’s memory.');}
 if(event==='commit'){next.stored=true;next.trace.push(next.step+' · Database commit completed: the task is saved.');}
 if(event==='ack'){next.ack=true;next.trace.push(next.step+' · Caller received the “Saved” reply.');}
 return next;
}
function restartCrash(s){return {...s,memory:s.stored,restarted:true,trace:[...s.trace,'Restart · memory is cleared; saved tasks are read from storage.']};}
function renderCrash(){
 const s=crash,finished=s.step===crashEvents[s.policy].length,violation=s.restarted&&s.ack&&!s.stored;
 const title=violation?'Promise broken: the user was told “Saved,” but the task was lost.':s.restarted&&s.stored?'Task recovered from storage after restart.':s.restarted?'No saved task found after restart.':s.ack?'The caller has received success.':'The caller has not received success.';
 $('#crash-state').innerHTML=`<p>Choice: ${escapeHTML($('#crash-policy').selectedOptions[0].textContent)} · ${s.step} events completed${s.restarted?' · restarted':''}</p><strong class="${violation?'bad':'good'}">${title}</strong><div class="state-grid"><div><small>APPLICATION MEMORY</small>${s.memory?'Task 7: Read':'Empty'}</div><div><small>SAVED IN STORAGE</small>${s.stored?'Task 7: Read':'Empty'}</div><div><small>WHAT THE CALLER SEES</small>${s.ack?'Received “saved”':'No success received'}</div></div><p style="margin:10px 0 0">${s.restarted&&!s.ack?'The caller received no success reply. It cannot tell from that alone whether the task was saved.':violation?'The application reported success before saving the task. Restart removed the only copy.':s.stored&&!s.ack?'The task is saved, but the caller has not received its reply yet.':'Choose “Next event” to continue, or restart to see what remains.'}</p>`;
 $('#crash-next').disabled=s.restarted||finished;$('#crash-restart').disabled=s.restarted;
 $('#crash-trace').innerHTML=s.trace.map(t=>'<li>'+escapeHTML(t)+'</li>').join('');
}
function resetCrash(){crash=freshCrash($('#crash-policy').value);renderCrash();}
$('#crash-policy').addEventListener('change',resetCrash);$('#crash-next').addEventListener('click',()=>{crash=advanceCrash(crash);renderCrash();});$('#crash-restart').addEventListener('click',()=>{crash=restartCrash(crash);renderCrash();});$('#crash-reset').addEventListener('click',resetCrash);renderCrash();

const changeImpact={
 format:{tangled:['Handler','Task logic','SQL inside the handler'],separated:['Input adapter'],reason:'Update the adapter that reads input. It can pass the same title to the service, which saves it in the same way.'},
 rule:{tangled:['Title check in web adapter','Title check in command-line adapter','Matching database constraint, if present'],separated:['Task service','Matching database constraint, if present'],reason:'Change the shared title rule in the service. If the database also restricts title length, update that restriction to agree with the rule.'},
 schema:{tangled:['HTTP handler SQL','Task logic SQL','Exporter SQL'],separated:['Storage adapter','Database update'],reason:'Change the SQL in the repository and update existing data as needed. Check that previously saved tasks can still be read.'},
 retry:{tangled:['Handler','Task state','Persistence','How the caller identifies retries'],separated:['Input contract','Task service','Repository contract','How the caller identifies retries'],reason:'The caller must identify a retry, and the application must recognise it and return the stored result. This new behaviour needs changes in several parts.'}
};
 function renderChange(){const d=changeImpact[$('#change-scenario').value];$('#change-result').innerHTML=`<div class="lab-output"><p><strong>Scenario:</strong> ${escapeHTML($('#change-scenario').selectedOptions[0].textContent)}</p><p><strong>Tangled design:</strong> ${d.tangled.map(escapeHTML).join(' · ')}</p><p><strong>Separated design:</strong> ${d.separated.map(escapeHTML).join(' · ')}</p><p style="margin:0">${escapeHTML(d.reason)}</p></div>`;}
$('#change-scenario').addEventListener('change',renderChange);renderChange();

function decisionScores(weights){
 const total=weights.reduce((a,b)=>a+b,0);if(total===0)return null;
 return {embedded:weights.reduce((s,w,i)=>s+w*[5,2,1][i],0)/total,separate:weights.reduce((s,w,i)=>s+w*[2,4,4][i],0)/total};
}
function renderDecision(){
 const ids=['simple','growth','independent'],weights=ids.map(id=>Number($('#weight-'+id).value));ids.forEach((id,i)=>$('#out-'+id).textContent=weights[i]);const scores=decisionScores(weights);
 if(!scores){$('#decision-result').innerHTML='<div class="lab-output">All weights are zero. Increase at least one weight to compare the choices. Memory alone still fails the restart requirement.</div>';return;}
 const row=(name,v,cls='')=>`<div class="bar-row"><span>${name}</span><span class="bar-track ${cls}"><i style="width:${v/5*100}%"></i></span><strong>${v.toFixed(2)}</strong></div>`;
 const tie=Math.abs(scores.embedded-scores.separate)<1e-10;
 $('#decision-result').innerHTML=`<div class="lab-output"><p>Weights (simplicity, multiple app machines, separate storage): ${weights.join(', ')}.</p>`+row('Embedded store',scores.embedded)+row('Separate database',scores.separate,'purple')+`<p>${tie?'Both choices have the same score with these weights.':(scores.embedded>scores.separate?'Embedded store':'Separate database')+' has the higher score with these weights.'} These are preference scores; they do not measure speed or availability.</p><p class="bad" style="margin:0">Memory only: rejected because tasks disappear after restart.</p></div>`;
}
['simple','growth','independent'].forEach(id=>$('#weight-'+id).addEventListener('input',renderDecision));renderDecision();

const views={
 context:{question:'Who uses the system?',boxes:['Team member','→ uses →','Task system'],reason:'This view shows who uses the system. It leaves the internal parts for a closer view.'},
 container:{question:'Which applications and data stores cooperate?',boxes:['Browser client','→ HTTPS →','Server application','→ local I/O →','Task store'],reason:'This view opens up the system into applications and data stores. Our task store is a local file used by the server application.'},
 component:{question:'Which responsibilities collaborate inside the server?',boxes:['Input adapter','→ create command →','Task service','→ save →','Storage adapter'],reason:'These modules run inside the same server application. If its process stops, all three stop.'},
 code:{question:'Which interfaces and types implement the task operation?',boxes:['TaskService.create(title)','→ calls →','TaskRepository.insert(title)','→ returns →','Task(id, title, done)'],reason:'The service checks the title and calls the repository. The repository commits the task before returning. Startup code passes the repository to the service.'}
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
 document.title='The System Design Atlas — Complete Edition';
 printState.closed.forEach(d=>d.open=true);$('#glossary-search').value='';$('#source-search').value='';filterGlossary();filterSources();document.body.classList.add('printing');
});
window.addEventListener('afterprint',()=>{
 if(!printState)return;printState.closed.forEach(d=>d.open=false);$('#glossary-search').value=printState.glossary;$('#source-search').value=printState.sources;document.title=printState.title;filterGlossary();filterSources();document.body.classList.remove('printing');printState=null;
});
$('#print-atlas').addEventListener('click',()=>window.print());
window.SystemAtlas={decisionScores,freshCrash,advanceCrash,restartCrash,crashEvents,changeImpact,navigate,get activePanel(){return activePanel;}};
navigate(location.hash);
window.SYSTEM_ATLAS_READY=true;
