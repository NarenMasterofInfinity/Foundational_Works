#!/usr/bin/env python3
"""Build the static, offline atlas and an auditable editorial manifest."""
from pathlib import Path
from html import escape as esc
from html.parser import HTMLParser
from urllib.parse import urlparse
import json
import re
from collections import Counter
from blueprint import build_blueprint, DATE, PARTS
from figures import get_figures, FIGURES
from resources import EXERCISES, GLOSSARY, FORMULAS, PATTERNS, CHAPTER_REFS, VERIFIED, STARTING_TITLES

HERE=Path(__file__).resolve().parent
OUT=HERE.parent
B=build_blueprint()
F=get_figures()
CHAPTERS=[c for u in B['units'] for c in u['chapters']]
LOOKUP={c['id']:c for c in CHAPTERS}
TITLES={u['id']:u['title'] for u in B['units']}|{c['id']:c['number']+' · '+c['title'] for c in CHAPTERS}
SOURCE_URLS=list(dict.fromkeys([r for u in B['units'] for r in u['references']]+[r for rs in CHAPTER_REFS.values() for r in rs]))

def link(target,label=None,cls=''):
    return f'<a href="#{esc(target)}" class="{cls}">{esc(label or TITLES.get(target,target))}</a>'

def badge(status):
    return f'<span class="badge {status}">{"READ NOW" if status=="available" else "PLANNED"}</span>'

def source(url):
    return VERIFIED.get(url,(STARTING_TITLES.get(url,urlparse(url).netloc+' · '+urlparse(url).path.strip('/')),'Supplied starting reference','Verification pending before chapter production'))

def references(urls,planned=False):
    items=[]
    for url in urls:
        title,kind,use=source(url)
        state='Link checked · '+DATE if url in VERIFIED else 'Link review pending'
        items.append(f'<li><a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(title)} ↗</a><p>{esc(kind)}. {esc(use)}.</p><small>{state}</small></li>')
    intro='Selected starting references. Technical claims and version-specific guarantees will be checked during production.' if planned else 'Read from introductory guidance to the primary or implementation detail relevant to this chapter. Links checked 21 October 2026.'
    return '<section class="reading-room"><h2>Sources & further reading</h2><p>'+intro+'</p><ol>'+''.join(items)+'</ol></section>'

def heading(kicker,title,description=''):
    return f'<header class="page-heading"><span class="eyebrow">{kicker}</span><h1>{esc(title)}</h1>'+ (f'<p class="lead">{description}</p>' if description else '')+'</header>'

def panel(ident,html,printing=False,kind=''):
    return f'<section class="panel {kind}" id="{ident}" data-print="{str(printing).lower()}" aria-label="{esc(TITLES.get(ident,ident))}">{html}</section>'

def chapter_card(c):
    return f'<a class="chapter-card" href="#{c["id"]}"><span class="chapter-number">{c["number"]}</span><div><h3>{esc(c["title"])}</h3><p>{len(c["topics"])} syllabus topics · {"Full lesson + original figures" if c["status"]=="available" else "Editorial outline"}</p></div>{badge(c["status"])}<span aria-hidden="true">↗</span></a>'

def labs(n):
    common='<span class="eyebrow">THE WORKBENCH · AUTHOR-CREATED MODEL</span>'
    if n==1:
        return '<section class="lab" id="crash-lab">'+common+'''<h3>When is “saved” actually safe?</h3><p>Choose the acknowledgment policy, then step through one request. Restart at any point and compare the promise with the recovered state.</p><label>Policy <select id="crash-policy"><option value="memory">A · memory only</option><option value="early">B · acknowledge before commit</option><option value="durable" selected>C · commit before acknowledgment</option></select></label><div class="lab-actions"><button id="crash-next" type="button">Next event →</button><button id="crash-restart" type="button">Restart process</button><button id="crash-reset" class="quiet" type="button">Reset</button></div><div class="lab-state" id="crash-state" aria-live="polite"></div><ol id="crash-trace" class="event-trace"></ol><p class="assumption">Assumptions: one request, atomic commit, intact storage. A teaching state machine; no real files are written.</p><noscript><p>Without JavaScript: memory-only loses the task on restart; early acknowledgment can lose an acknowledged task; commit-before-ack preserves it under this model.</p></noscript></section>'''
    if n==2:
        return '<section class="lab" id="change-lab">'+common+'''<h3>Follow the knowledge that must change</h3><label>Change scenario <select id="change-scenario"><option value="format">Replace JSON input with a form</option><option value="rule">Change the task title limit</option><option value="schema">Rename a storage column</option><option value="retry">Add a deduplicated-create contract</option></select></label><div id="change-result" aria-live="polite"></div><p class="assumption">This is a dependency model of the worked example, not a prediction of engineering hours.</p><noscript><p>Formatting belongs to the adapter; title policy to the service; schema layout to the repository. Deduplication changes the contract across all three.</p></noscript></section>'''
    if n==3:
        return '<section class="lab" id="decision-lab">'+common+'''<h3>Change the priorities, inspect the decision</h3><div class="lab-controls"><label>Simplicity weight <input type="range" id="weight-simple" min="0" max="5" value="5"><output for="weight-simple" id="out-simple">5</output></label><label>Growth weight <input type="range" id="weight-growth" min="0" max="5" value="1"><output for="weight-growth" id="out-growth">1</output></label><label>Host independence weight <input type="range" id="weight-independent" min="0" max="5" value="1"><output for="weight-independent" id="out-independent">1</output></label></div><div id="decision-result" aria-live="polite"></div><p class="assumption">Illustrative fit scores from Table 1.3.2. Restart persistence is mandatory. Preference weights never override feasibility.</p><noscript><p>At the initial weights, the embedded-store score is 4.00 and the separate-database score is 2.57. Memory-only fails the mandatory restart requirement.</p></noscript></section>'''
    return '<section class="lab" id="view-lab">'+common+'''<h3>Ask the same application four questions</h3><div class="view-buttons" role="group" aria-label="Architecture view"><button type="button" data-view="context" aria-pressed="true">Context</button><button type="button" data-view="container" aria-pressed="false">Containers</button><button type="button" data-view="component" aria-pressed="false">Components</button><button type="button" data-view="code" aria-pressed="false">Code</button></div><div id="view-result" aria-live="polite"></div><p class="assumption">Four views of the same teaching system. A zoom relationship is not a network call. Figure 1.4.1 and Table 1.4.1 provide the complete static version.</p></section>'''

def chapter(c,n):
    body=(HERE/f'chapter-{n}.html').read_text()
    for k in range(1,5):body=body.replace('{{fig-'+str(k)+'}}',F[f'{n}-{k}'])
    body=body.replace('{{lab}}',labs(n))
    prev=link('unit-1','← Unit overview') if n==1 else link(f'ch-1-{n-1}','← Previous chapter')
    nxt=link('exercises','Unit 1 exercises →','primary') if n==4 else link(f'ch-1-{n+1}','Next chapter →','primary')
    prereqs='Basic programming' if n==1 else f'Chapter 1.{n-1}'
    legend='<div class="visual-legend" aria-label="Diagram legend"><span><i class="flow"></i>Blue: normal flow</span><span><i class="healthy"></i>Green: healthy</span><span><i class="caution"></i>Amber: caution</span><span><i class="failure"></i>Red: failure</span><span><i class="control"></i>Purple: control / infrastructure</span><span><i class="external"></i>Gray: external / inactive</span><span>Solid arrow: action / data · dashed: dependency or zoom · dotted: acknowledgment</span></div>'
    return heading(f'PART I / UNIT 01 / CHAPTER {c["number"]}',c['title'])+f'<div class="chapter-meta"><span>Prerequisite: {prereqs}</span><span>4 original figures · 1 workbench</span><button class="read-toggle quiet" data-read="{c["id"]}" aria-pressed="false" type="button">Mark as read ○</button></div>'+legend+body+references(CHAPTER_REFS[c['id']])+f'<div class="chapter-end">{prev}{nxt}</div>'

def unit_page(u):
    available=u['status']=='available';n=u['n']
    note='Four complete chapters: start with behavior, build boundaries, make a decision, and reconcile the architecture views.' if available else 'This unit is mapped for chapter production. The material below is the complete assigned syllabus and illustration plan; the lessons, worked examples, assessments, and solutions are still to be produced.'
    html=heading(f'PART {u["part"]+1} / UNIT {n:02}',u['title'])+f'<div class="edition-note">{badge(u["status"])}<p>{note}</p></div>'
    html+='<p class="prereq"><strong>Before this unit:</strong> '+(', '.join(link(f'unit-{i}',f'Unit {i}') for i in u['prerequisites']) or 'Basic programming; no prior systems background required.')+'</p>'
    html+='<div class="chapter-list">'+''.join(chapter_card(c) for c in u['chapters'])+'</div>'
    html+='<h2>The running example</h2><p>'+esc(u['example'])+'</p>'
    if n==22:
        html+='<h2>A common design-review protocol</h2><p>Each of the twelve designs has these 22 mandatory sections. None is counted as produced yet.</p><ol class="two-column">'+''.join('<li>'+esc(t)+'</li>' for t in B['case_review'])+'</ol><h3>Optional extensions</h3><p>'+esc(' · '.join(B['optional_cases']))+'</p>'
    else:
        html+='<h2>Complete syllabus allocation</h2><div class="syllabus">'
        for c in u['chapters']:
            html+='<details'+(' open' if available else '')+'><summary>'+esc(c['number']+' · '+c['title'])+'</summary><ul>'+''.join('<li>'+esc(t)+'</li>' for t in c['topics'])+'</ul></details>'
        html+='</div><h2>Required visual coverage</h2><p>'+esc('; '.join(u['illustrations']))+'.</p>'
    html+='<h2>Assessment plan</h2><p>Five conceptual questions · three scenarios · one design/debugging challenge · one implementation exercise · one advanced thought experiment. Explanations belong in the separate solutions section.</p>'
    html+=link('exercises','Work through Unit 1’s assessment →','primary') if available else '<p class="status-note">Assessment and solutions: planned. No completion credit is assigned for an outline.</p>'
    return html+references(u['references'],not available)

def planned_page(c,u):
    html=heading(f'EDITORIAL BLUEPRINT / CHAPTER {c["number"]}',c['title'])+'<div class="edition-note">'+badge('planned')+'<p>This is a production brief. The complete teaching chapter has not been written or technically reviewed.</p></div>'
    html+='<p><strong>Prerequisites:</strong> '+', '.join(link(p) for p in c['prerequisites'])+'</p>'
    if 'focus' in c:html+='<h2>Case-study focus</h2><p>'+esc(c['focus'])+'</p>'
    html+='<h2>Subchapters & required concepts</h2><ol>'+''.join(f'<li><strong>{c["number"]}.{i}</strong> · {esc(t)}</li>' for i,t in enumerate(c.get('sections',c['topics']),1))+'</ol>'
    html+='<h2>Illustration commission</h2><ol>'+''.join('<li>'+esc(f['title'])+': '+esc(c['title'])+'</li>' for f in c['illustrations'])+'</ol>'
    html+='<p>Include the unit’s essential diagrams: '+esc('; '.join(u['illustrations']) or 'architecture evolution; sequence and failure paths; data model; capacity and cost comparison')+'.</p>'
    html+='<h2>Production & review requirements</h2><p>Begin with the actual problem; build the simplest working solution; break it; introduce and implement the mechanism; compare alternatives; trace failure; connect to production; end with misconceptions and reasoning questions. Cite exact guarantees, mark assumed numbers, validate code and formulas, and keep state copies and arrow meanings explicit.</p>'
    return html+references(c['references'],True)+link(u['id'],'← Back to the unit blueprint')

def build():
    sections=[]
    hero=(HERE/'overview.html').read_text().replace('{{chapter-count}}',str(len(CHAPTERS)))
    hero=hero.replace('{{part-cards}}',''.join(f'<a class="part-card" href="#unit-{[1,5,9,14,18,22][i]}"><span class="eyebrow">PART {i+1:02}</span><h3>{esc(p)}</h3><p>{["Learn to see the system before scaling it.","Organize behavior, dependencies and change.","Make access patterns and capacity visible.","Reason about uncertainty and partial failure.","Operate, protect and validate the design.","Twelve systems, examined from end to end."][i]}</p><span class="card-foot">{["4 chapters ready", "Blueprint", "Blueprint", "Blueprint", "Blueprint", "12 case studies planned"][i]} ↗</span></a>' for i,p in enumerate(PARTS)))
    sections.append(panel('overview',hero,True))
    for u in B['units']:
        sections.append(panel(u['id'],unit_page(u),False,'unit-page'))
        for j,c in enumerate(u['chapters'],1):
            if u['n']==1:
                c['references']=CHAPTER_REFS[c['id']]
                c['illustrations']=[fig for fig in FIGURES if fig['chapter']==c['id']]
                sections.append(panel(c['id'],chapter(c,j),True,'chapter'))
            else:sections.append(panel(c['id'],planned_page(c,u),False,'planned-chapter'))
    sections.extend(reference_panels())
    sidebar='<a href="#overview" class="nav-home">The atlas <span>↗</span></a><a href="#contents">Complete contents</a><a href="#concept-map">The concept map</a><a href="#reading-path">Reading paths</a><div class="nav-label">THE SIX PARTS</div>'
    for i,p in enumerate(PARTS):
        sidebar+=f'<details class="nav-part" {"open" if i==0 else ""}><summary><span>{i+1:02}</span>{esc(p)}</summary>'
        for u in B['units']:
            if u['part']==i:
                sidebar+=f'<a href="#{u["id"]}" class="nav-unit"><small>{u["n"]:02}</small>{esc(u["title"])}<i aria-label="{u["status"]}">{"●" if u["status"]=="available" else "○"}</i></a>'
                if u['n']==1:
                    sidebar+=''.join(f'<a href="#{c["id"]}" class="nav-chapter"><small>{c["number"]}</small>{esc(c["title"])}</a>' for c in u['chapters'])
        sidebar+='</details>'
    sidebar+='<div class="nav-label">THE REFERENCE DESK</div>'+''.join(link(k,v) for k,v in [('exercises','Exercises'),('solutions','Solutions'),('glossary','Searchable glossary'),('figure-index','Diagram index'),('formulas','Formula reference'),('patterns','Pattern index'),('sources','Source bibliography'),('manifest','Completion manifest')])
    search=[]
    for u in B['units']:
        search.append(dict(id=u['id'],title=f'Unit {u["n"]} · {u["title"]}',text=' '.join(u['topics']),status=u['status']))
        for c in u['chapters']:search.append(dict(id=c['id'],title=f'{c["number"]} · {c["title"]}',text=' '.join(c['topics']+c.get('sections',[])),status=c['status']))
    for term,meaning,target in GLOSSARY:search.append(dict(id=target,title=term,text=meaning,status='available' if target.startswith('ch-1-') else 'planned'))
    for target,title in [('exercises','Exercises'),('solutions','Solutions'),('glossary','Glossary'),('figure-index','Diagrams'),('formulas','Formulas'),('patterns','Patterns'),('sources','Bibliography'),('manifest','Completion manifest')]:search.append(dict(id=target,title=title,text=title,status='available'))
    data=dict(search=search,figures=FIGURES,chapters=[c['id'] for c in CHAPTERS if c['status']=='available'],date=DATE)
    template=(HERE/'template.html').read_text()
    html=template.replace('/*__CSS__*/',(HERE/'style.css').read_text()).replace('<!--__NAV__-->',sidebar).replace('<!--__PANELS__-->','\n'.join(sections)).replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/')).replace('/*__JS__*/',(HERE/'app.js').read_text())
    assert not re.search(r'\{\{[^}]+\}\}|__PANELS__|__DATA__',html),'Unexpanded template token'
    (OUT/'index.html').write_text(html)
    # Separate planned editorial coverage from produced teaching artifacts.
    B['sources']=[dict(url=url,title=source(url)[0],kind=source(url)[1],link_status='checked' if url in VERIFIED else 'pending',checked_on=DATE if url in VERIFIED else None,technical_review='Reviewed for the stated use only' if url in VERIFIED else 'Pending chapter production') for url in SOURCE_URLS]
    B['figures']=FIGURES
    B['review']=dict(stage_1='complete',stage_2='Unit 1 produced; 21 units pending',stage_3='Unit 1 editorial and technical review recorded in SOURCE_REVIEW.md; automated verification recorded in QA.md',stage_4='Partial digital edition assembled; complete-book assembly pending')
    B['counts']=dict(units=22,chapters_planned=len(CHAPTERS),chapters_produced=4,syllabus_topics=sum(len(u['topics']) for u in B['units']),figures_produced=len(FIGURES),mandatory_case_studies=12,case_studies_produced=0,exercises_produced=len(EXERCISES),solutions_produced=len(EXERCISES))
    (OUT/'completion-manifest.json').write_text(json.dumps(B,indent=2,ensure_ascii=False)+'\n')
    md=['# The System Design Atlas — book blueprint','',B['scope'],'',f'Editorial snapshot: {DATE}. {len(CHAPTERS)} chapters across 22 units.','']
    for u in B['units']:
        md.extend([f'## Unit {u["n"]}: {u["title"]}',f'\nStatus: {u["status"]}. Prerequisites: {u["prerequisites"]}.',f'\nWorked example: {u["example"]}'])
        for c in u['chapters']:
            md.extend([f'\n### {c["number"]} {c["title"]} — {c["status"]}','\nPrerequisites: '+', '.join(c['prerequisites'])])
            md.extend('\n- '+t for t in c.get('sections',c['topics']))
            md.append('\nIllustrations: '+ '; '.join(f['title'] for f in c['illustrations']))
            md.append('\nStarting references: '+ ' · '.join(c['references']))
        md.append('\nEssential unit diagrams: '+'; '.join(u['illustrations']))
        md.append('\nAssessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. '+u['assessment']['conceptual']['status']+'.')
    (OUT/'BLUEPRINT.md').write_text('\n'.join(md)+'\n')
    validate()
    print(f'Built System Design Atlas: {len(CHAPTERS)} mapped chapters; 4 produced; {len(FIGURES)} original figures; {len(EXERCISES)} exercises and explained solutions; {len(SOURCE_URLS)} starting sources.')

def reference_panels():
    pages=[]
    html=heading('THE COMPLETE BOOK BLUEPRINT','Contents, from objects to systems','Every unit and subchapter is mapped. Filled marks denote produced lessons; open marks denote planned work.')
    for p,part in enumerate(PARTS):
        html+=f'<h2>Part {p+1} · {esc(part)}</h2>'
        for u in B['units']:
            if u['part']!=p:continue
            label=str(u['n']).zfill(2)+' · '+u['title']
            html+=f'<div class="toc-unit"><h3>{link(u["id"],label)}</h3>{badge(u["status"])}<ol>'+''.join(f'<li>{link(c["id"],c["number"]+" · "+c["title"])}</li>' for c in u['chapters'])+'</ol></div>'
    pages.append(panel('contents',html))
    html=heading('HOW THE IDEAS CONNECT','A map of the territory','Read the arrows as prerequisite relationships. Security and operations also constrain designs throughout the map.')+(HERE/'concept-map.html').read_text()
    html+='<div class="map-key">Solid arrow = prerequisite · dashed line = a cross-cutting constraint · author-created illustration</div><h2>Why these connections matter</h2><p>Interfaces make ownership explicit. Data models determine which invariants transactions must protect. Concurrency makes execution order observable. Networks introduce partial failure. Replication combines those concerns; reliability, security, deployment, and observability determine whether the resulting system can be operated.</p>'
    pages.append(panel('concept-map',html,True))
    html=heading('BEGIN WHERE YOU ARE','Dependency-aware reading paths','Routes select a goal; chapter prerequisites still apply. Planned units are included as an editorial path, not as available lessons.')
    routes=[('First pass · from program to service',[1,2,3,4,5,6,7,8,9,10]),('Data and scale',[1,2,3,4,8,9,10,11,12,13]),('Distributed correctness',[1,3,4,9,10,14,15,16,17]),('Production engineering',[1,2,3,4,5,6,7,8,9,10,11,12,14,15,16,17,18,19,20,21])]
    for name,ns in routes:html+='<article class="path-card"><h2>'+name+'</h2><p>'+ ' → '.join(link(f'unit-{n}',f'{n:02}') for n in ns)+'</p></article>'
    html+='<h2>The complete prerequisite graph</h2><div class="table-wrap"><table><thead><tr><th>Unit</th><th>Direct prerequisites</th><th>Reason to read next</th></tr></thead><tbody>'
    for u in B['units']:html+=f'<tr><td>{link(u["id"],str(u["n"])+" · "+u["title"])}</td><td>'+(', '.join(link(f'unit-{p}',str(p)) for p in u['prerequisites']) or 'Basic programming')+'</td><td>'+esc(u['chapters'][0]['title'])+'</td></tr>'
    html+='</tbody></table></div><h2>Recurring systems & case-study progression</h2><p>The to-do application establishes boundaries and commit timing in Unit 1. Payments connect refactoring (5), API retries (8), workflow compensation (16), provider outages (17), and the final ledger design (22.9). Ticket booking connects transaction races (10) to reservations and expiry (22.8). Document processing connects ingestion and lineage (13) to durable orchestration and human review (22.12). URL shortening connects measured scaling (12) to complete design review (22.1).</p>'
    pages.append(panel('reading-path',html,True))
    html=heading('UNIT 01 / ASSESSMENT','Reason about the design','Write an answer before opening the separate solutions. These questions test assumptions and failure histories.')
    for kind,ident,q,a in EXERCISES:html+=f'<article class="exercise" id="exercise-{ident}"><span class="eyebrow">{esc(kind.replace("_"," "))} / {ident}</span><h3>{esc(q)}</h3>{link("solution-"+ident,"Read the explanation →")}</article>'
    pages.append(panel('exercises',html,True))
    html=heading('UNIT 01 / EXPLAINED ANSWERS','Solutions & reasoning','Each explanation identifies the relevant assumption and why a tempting alternative fails.')
    for kind,ident,q,a in EXERCISES:html+=f'<article class="solution" id="solution-{ident}"><span class="eyebrow">{ident}</span><h2>{esc(q)}</h2><p>{esc(a)}</p>{link("exercise-"+ident,"← Return to question")}</article>'
    html+='<p>'+link('unit-2','Next production stage · Requirements, estimation, and trade-offs →','primary')+'</p>'
    pages.append(panel('solutions',html,True))
    html=heading('THE REFERENCE DESK','A searchable glossary','Compact definitions support reading; a link to a planned unit identifies where the full treatment belongs.')+'<label class="filter-label">Find a term <input type="search" id="glossary-search" placeholder="e.g. invariant, quorum, durability"></label><p id="glossary-count" aria-live="polite"></p><dl class="glossary">'
    for term,meaning,target in sorted(GLOSSARY):html+=f'<div data-term="{esc((term+" "+meaning).lower())}"><dt>{esc(term)}</dt><dd>{esc(meaning)} {link(target,"Read the lesson →" if target.startswith("ch-1-") else "Planned treatment →")}</dd></div>'
    html+='</dl><p id="glossary-empty" hidden>No terms match that search.</p>'
    pages.append(panel('glossary',html,True))
    html=heading('THE VISUAL INDEX','Every diagram has a job','Sixteen original figures accompany the four produced chapters. Further figures remain commissions in the chapter blueprint.')+'<div class="figure-list">'
    for f in FIGURES:html+=f'<a href="#{f["id"]}"><span class="eyebrow">FIG. {f["number"]}</span><h3>{esc(f["title"])}</h3><p>{esc(f["why"])}</p></a>'
    pages.append(panel('figure-index',html+'</div>',True))
    html=heading('THE FORMULA REFERENCE','Symbols with assumptions','Two models are introduced in Unit 1. Later formulas are indexed with their conditions and planned teaching destination.')
    for name,formula,caveat,target,status in FORMULAS:html+=f'<article class="formula"><span class="eyebrow">{status}</span><h2>{esc(name)}</h2><code>{esc(formula)}</code><p>{esc(caveat)}</p>{link(target,"Lesson →" if status=="introduced" else "Planned derivation →")}</article>'
    pages.append(panel('formulas',html,True))
    html=heading('THE PATTERN INDEX','Start with the problem, then the pattern','This is a destination index. The full pattern lessons are planned; names alone do not constitute coverage.')
    for target,names in PATTERNS.items():html+='<article class="pattern-group"><h2>'+link(target)+'</h2><div class="pattern-tags">'+''.join(link(target,name,'tag') for name in names)+'</div><p class="status-note">Planned · mechanism, miniature implementation, failure behavior, and alternatives required.</p></article>'
    pages.append(panel('patterns',html,True))
    html=heading('THE READING ROOM','Sources, close to the claim','The book distinguishes original research, formal specifications, official documentation, and engineering guidance. No company architecture or benchmark is invented here.')+'<p>“Link checked” means that the source was opened and inspected for the stated use on 21 October 2026. It does not mean all future chapters have been verified. Supplied references not yet checked remain explicitly pending. Version-sensitive documentation must be rechecked during chapter production.</p><label class="filter-label">Filter sources <input type="search" id="source-search" placeholder="e.g. Raft, C4, database"></label><p id="source-count" aria-live="polite"></p><div id="source-list">'
    for url in SOURCE_URLS:
        title,kind,use=source(url);state='Link checked · '+DATE if url in VERIFIED else 'Link verification pending'
        html+=f'<article class="source" data-source="{esc((title+" "+kind+" "+use+" "+url).lower())}"><span class="eyebrow">{esc(kind)}</span><h3><a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(title)} ↗</a></h3><p>{esc(use)}</p><small>{state}</small></article>'
    pages.append(panel('sources',html+'</div><p id="source-empty" hidden>No sources match that search.</p>',True))
    html=heading('AN HONEST COMPLETION MANIFEST','Mapped is different from produced','A visible record of scope prevents a syllabus, diagram plan, or source list from being mistaken for a finished textbook.')+f'<div class="edition-note"><span class="eyebrow">CURRENT INSTALLMENT</span><p>{esc(B["stage"])}. The complete atlas is still in production.</p></div><div class="manifest-actions"><a href="completion-manifest.json" download>Download completion manifest ↓</a><a href="BLUEPRINT.md">Read the full blueprint ↗</a><a href="SOURCE_REVIEW.md">Technical source review ↗</a></div><div class="table-wrap"><table><thead><tr><th>Unit</th><th>Topics mapped</th><th>Chapters produced</th><th>Exercises / solutions</th></tr></thead><tbody>'
    for u in B['units']:html+=f'<tr><td>{link(u["id"],str(u["n"])+" · "+u["title"])}</td><td>{len(u["topics"]) if u["n"]!=22 else "12 cases × 22 review sections"}</td><td>{len(u["chapters"]) if u["n"]==1 else 0} / {len(u["chapters"])}</td><td>{"11 / 11" if u["n"]==1 else "0 / 0 · planned"}</td></tr>'
    html+='</tbody></table></div><h2>The production contract</h2><ol><li>Blueprint: allocate every topic, prerequisite, essential illustration, source, and case-study requirement.</li><li>Production: write a coherent chapter with worked execution, original visuals, failure behavior, and alternatives.</li><li>Review: check primary references, code, formulas, diagrams, cross-references, and assumptions.</li><li>Assembly: maintain indexes and a navigable reading edition; print only produced lessons and clearly identified reference material.</li></ol><p>Four Unit 1 chapters, 16 figures, four interactive workbenches, and 11 questions with separate explanations are produced. Unit 1 implementation is downloadable. Units 2–22 and all mandatory case studies remain planned. This status is also embedded in the machine-readable manifest.</p>'
    pages.append(panel('manifest',html,True))
    return pages

def validate():
    for u in B['units']:
        if u['n']<22:
            assigned=[i for c in u['chapters'] for i in c['topic_numbers']]
            assert Counter(assigned)==Counter(range(1,len(u['topics'])+1)),f'Topic allocation incorrect in Unit {u["n"]}: {assigned}'
        assert all(p<u['n'] for p in u['prerequisites']), 'Cyclic unit prerequisite'
    html=(OUT/'index.html').read_text()
    class Inspector(HTMLParser):
        def __init__(self):
            super().__init__();self.ids=[];self.targets=[]
        def handle_starttag(self,tag,attrs):
            attrs=dict(attrs)
            if 'id' in attrs:self.ids.append(attrs['id'])
            if tag=='a' and attrs.get('href','').startswith('#'):self.targets.append(attrs['href'][1:])
    parsed=Inspector();parsed.feed(html);ids=parsed.ids
    dup=[i for i,n in Counter(ids).items() if n>1]
    assert not dup,f'Duplicate HTML ids: {dup}'
    for target in parsed.targets:assert target in ids,f'Broken internal link: {target}'
    for c in B['units'][0]['chapters']:assert len(c['illustrations'])>=4
    assert len(EXERCISES)==11 and Counter(q[0] for q in EXERCISES)==Counter(conceptual=5,scenario=3,design=1,implementation=1,thought_experiment=1)
    assert len(B['units'][-1]['chapters'])==12
    assert all(len(c['sections'])==22 for c in B['units'][-1]['chapters'])
    print('Validated: exact syllabus allocation, acyclic prerequisites, unique IDs, all internal links, 12 × 22 case requirements, assessment counts.')

if __name__=='__main__':build()
