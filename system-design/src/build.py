#!/usr/bin/env python3
"""Build the complete, self-contained System Design Atlas; standard library only."""
from pathlib import Path
from html import escape as e
from html.parser import HTMLParser
from collections import Counter
import json,re
from edition import prepare
from figures import FIGURES
from expanded_chapters import concept_body,case_body,paragraphs,slug
from essential_plates import plates
from workbenches import labs
from expanded_workbenches import BENCHES,BUCKET
from teaching.foundations import LESSONS
from teaching.cases import CASES
from teaching.patterns import PATTERN_LESSONS
from teaching.sources import SOURCES
from teaching.summaries import SUMMARIES,PATTERN_SUMMARIES
from teaching.guides import GUIDES
from resources import GLOSSARY,FORMULAS,PATTERNS

HERE=Path(__file__).resolve().parent;OUT=HERE.parent
B,F,ASSESSMENTS=prepare()
CHAPTERS=[c for u in B['units'] for c in u['chapters']]
TITLES={u['id']:u['title'] for u in B['units']}|{c['id']:c['number']+' · '+c['title'] for c in CHAPTERS}
SOURCE_URLS=list(dict.fromkeys(r for c in CHAPTERS for r in c['references']))
LEGEND='<div class="visual-legend" aria-label="Diagram legend"><span><i class="flow"></i>Blue: normal flow</span><span><i class="healthy"></i>Green: healthy</span><span><i class="caution"></i>Amber: caution</span><span><i class="failure"></i>Red: failure</span><span><i class="control"></i>Purple: control / shared infrastructure</span><span><i class="external"></i>Gray: external / inactive</span><span>Solid arrow: labeled action · dashed: dependency or boundary · dotted: acknowledgment where labeled. Snapshot cards compare stated observations; they do not imply network calls.</span></div>'
INTRO_LEGEND='<div class="visual-legend" aria-label="Diagram legend">Read the labels and caption with each figure. Boxes show parts or states; arrows show how they are connected.</div>'

def link(target,label=None,cls=''):return f'<a href="#{e(target)}" class="{cls}">{e(label or TITLES.get(target,target))}</a>'
def badge():return '<span class="badge available">READ NOW</span>'
def heading(kicker,title,description=''):
    return f'<header class="page-heading"><span class="eyebrow">{e(kicker)}</span><h1>{e(title)}</h1>'+('<p class="lead">'+e(description)+'</p>' if description else '')+'</header>'
def panel(ident,body,kind='',part='reference',printing=True):
    return f'<section class="panel {kind}" id="{ident}" data-print="{str(printing).lower()}" data-part="{part}" aria-label="{e(TITLES.get(ident,ident))}">{body}</section>'
def refs(urls):
    result='<section class="reading-room"><h2>Sources & further reading</h2><p>Start with the introductory guidance, then inspect original specifications, research, or implementation details. Access and stated use checked 21 October 2026. Author-created examples and assumed numbers are separate from source guarantees.</p><ol>'
    for url in urls:
        title,kind,use=SOURCES[url]
        result+=f'<li><a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(title)} ↗</a><p>{e(kind)}. {e(use)}.</p><small>Access reviewed · 21 October 2026</small></li>'
    return result+'</ol></section>'
def card(c):
    return f'<a class="chapter-card" href="#{c["id"]}"><span class="chapter-number">{c["number"]}</span><div><h3>{e(c["title"])}</h3><p>{"Complete 22-section design review" if c["id"].startswith("ch-22-") else str(len(c["topics"]))+" assigned concepts · worked mechanisms and original figures"}</p></div>{badge()}<span aria-hidden="true">↗</span></a>'

def render_chapter(u,c,j):
    n=u['n']
    if n==1:
        body=(HERE/f'chapter-{j}.html').read_text()
        for k in range(1,5):body=body.replace('{{fig-'+str(k)+'}}',F[f'{j}-{k}'])
        body=body.replace('{{lab}}',labs(j))
    elif n==22:
        body=case_body(c)+(BUCKET if j==2 else '')
    else:body=concept_body(u,c,BENCHES.get(n,''))
    c['illustrations']=[f for f in FIGURES if f['chapter']==c['id']]
    assert len(c['illustrations'])>=4,c['id']
    c['rendered_words']=len(re.sub('<[^>]+>',' ',body).split())
    c['review']=dict(source_links='checked for stated use',numbers='assumptions labeled; executable models verified separately',code='bounded executable examples or explicitly labeled pseudocode',illustrations='original labeled figures; compare caption to surrounding explanation')
    index=CHAPTERS.index(c)
    previous=link(CHAPTERS[index-1]['id'],'← Previous chapter') if index else link('unit-1','← Unit overview')
    nxt=link(CHAPTERS[index+1]['id'],'Next chapter →','primary') if index<len(CHAPTERS)-1 else link('questions-unit-22','Work through the final assessment →','primary')
    prereq=', '.join(link(p) for p in c['prerequisites']) or 'Basic programming'
    meta=f'<div class="chapter-meta"><span>Prerequisites: {prereq}</span><span>{len(c["illustrations"])} original figures</span><button class="read-toggle quiet" data-read="{c["id"]}" aria-pressed="false" type="button">Mark as read ○</button></div>'
    end='<p>'+link(f'questions-unit-{n}',f'Unit {n} exercises →')+' · '+link(f'answers-unit-{n}',f'Unit {n} explained solutions →')+'</p>'
    legend=LEGEND if n!=1 else '<div class="visual-legend" aria-label="Diagram legend"><span>Reading the figures: boxes name parts or states; arrow labels explain how they relate. Dashed arrows show a code dependency or a change in the level of detail. Each caption explains the example.</span></div>'
    if n in (3,4):legend=INTRO_LEGEND
    reading=refs(c['references'])
    if n==1:
        reading=reading.replace('Start with the introductory guidance, then inspect original specifications, research, or implementation details. Access and stated use checked 21 October 2026. Author-created examples and assumed numbers are separate from source guarantees.','These sources explain the ideas and mechanisms used in this chapter. The to-do application is our own teaching example. Links were reviewed on 21 October 2026.')
    else:
        reading=reading.replace('Start with the introductory guidance, then inspect original specifications, research, or implementation details. Access and stated use checked 21 October 2026. Author-created examples and assumed numbers are separate from source guarantees.','These sources explain the mechanisms used in this chapter. The worked designs and numerical assumptions are our own teaching examples. Links were reviewed on 21 October 2026.')
    return heading(f'PART {u["part"]+1} / UNIT {n:02} / CHAPTER {c["number"]}',c['title'])+meta+legend+body+end+reading+f'<div class="chapter-end">{previous}{nxt}</div>'

def render_unit(u):
    n=u['n'];html=heading(f'PART {u["part"]+1} / UNIT {n:02}',u['title'])
    html+='<div class="edition-note">'+badge()+f'<p>{len(u["chapters"])} produced chapters, with original figures, worked mechanisms, and a complete eleven-question assessment with separate explained solutions.</p></div>'
    html+='<p class="prereq"><strong>Before this unit:</strong> '+(', '.join(link(f'unit-{p}',f'Unit {p}') for p in u['prerequisites']) or 'Basic programming')+'</p>'
    if n==1:
        html+='<p class="lead">How do we turn a small program into an application people can rely on? We will build a to-do application, one decision at a time.</p><p>Begin with a task kept in memory. Save it between runs, organise the code into modules, and work out what the application must do. Then draw the design and trace a request through it.</p>'
    elif n<22:
        html+='<p class="lead">'+e(GUIDES[n][0][0].split('\n\n')[0])+'</p>'
    else:
        html+='<p class="lead">We can now bring the earlier ideas together. Each design starts with a concrete workload, follows its main operation, and examines what happens when part of the system fails.</p>'
    html+='<div class="chapter-list">'+''.join(card(c) for c in u['chapters'])+'</div><h2>The running example</h2>'+paragraphs(u['example'])
    html+='<p>'+link(f'questions-unit-{n}',f'Unit {n} assessment →','primary')+' '+link(f'answers-unit-{n}','Explained solutions →','text-link')+'</p>'
    if n<22:
        html+='<h2>Concept coverage</h2><div class="syllabus">'
        for c in u['chapters']:
            html+='<details><summary>'+e(c['number']+' · '+c['title'])+'</summary><ul>'+''.join('<li>'+link(f'topic-{n}-{i}',t)+'</li>' if n>1 else '<li>'+link(c['id'],t)+'</li>' for i,t in zip(c['topic_numbers'],c['topics']))+'</ul></details>'
        html+='</div>'
        if n>1:
            visual,coverage=plates(u);u['essential_visual_coverage']=coverage
            html+='<h2>Unit plates · the required visual vocabulary</h2><p>Figure numbers with .0 denote unit-level reference plates. Chapter figures retain their chapter numbers.</p>'+(INTRO_LEGEND if n in (3,4) else LEGEND)+visual
        else:u['essential_visual_coverage']=[dict(required=t,figure=f,status='available') for t,f in zip(u['illustrations'],['fig-1-1-4','fig-1-2-4','fig-1-3-2','fig-1-4-1'])]
    else:
        html+='<h2>The complete review protocol</h2><ol class="two-column">'+''.join('<li>'+e(t)+'</li>' for t in B['case_review'])+'</ol><p>Each of the twelve designs above contains every section, including the implementation challenge. Optional next subjects: '+e(' · '.join(B['optional_cases']))+'.</p>'
    return html+refs(u['references'])

def prerequisites_closure(units):
    seen=set(units)
    while True:
        expanded=seen|{p for n in seen for p in B['units'][n-1]['prerequisites']}
        if expanded==seen:return sorted(seen)
        seen=expanded

def question_id(n,ident,prefix):return prefix+'-'+('' if n==1 else str(n)+'-')+ident

def reference_pages():
    pages=[]
    html=heading('THE COMPLETE EDITION','Contents, from objects to systems','All 22 units and 99 chapters are available. Follow prerequisites or use a focused reading path.')
    for p,part in enumerate(B['parts']):
        html+='<h2>Part '+str(p+1)+' · '+e(part)+'</h2>'
        for u in B['units']:
            if u['part']!=p:continue
            html+='<div class="toc-unit"><h3>'+link(u['id'],f'{u["n"]:02} · '+u['title'])+'</h3>'+badge()+'<ol>'+''.join('<li>'+link(c['id'],c['number']+' · '+c['title'])+'</li>' for c in u['chapters'])+'</ol></div>'
    pages.append(panel('contents',html))
    html=heading('HOW THE IDEAS CONNECT','A map of the territory','The simplified concept spine connects modules, networks, data, distribution, and production engineering.')+(HERE/'concept-map.html').read_text()+'<p class="map-key">Solid arrow = conceptual prerequisite · dashed line = cross-cutting constraint. Exact prerequisites are in Reading paths. Author-created illustration.</p>'
    pages.append(panel('concept-map',html))
    html=heading('DEPENDENCY-AWARE ROUTES','Reading paths','Every route below includes the prerequisite closure of its selected units; open any unit for its direct chapter dependencies.')
    for name,targets in [('First complete pass',[1,2,3,4,5,6,7,8,9,10]),('Data and scale',[9,10,11,12,13]),('Distributed correctness',[14,15,16,17]),('Production engineering',[18,19,20,21])]:
        ns=prerequisites_closure(targets);html+='<article class="path-card"><h2>'+name+'</h2><p>'+' → '.join(link(f'unit-{n}',f'{n:02}') for n in ns)+'</p></article>'
    html+='<h2>Direct prerequisites</h2><div class="table-wrap"><table><thead><tr><th>Unit</th><th>Before this unit</th></tr></thead><tbody>'
    for u in B['units']:html+='<tr><td>'+link(u['id'],str(u['n'])+' · '+u['title'])+'</td><td>'+(', '.join(link(f'unit-{p}',str(p)) for p in u['prerequisites']) or 'Basic programming')+'</td></tr>'
    html+='</tbody></table></div><h2>The case-study progression</h2><p>The URL shortener connects estimation, cache freshness, and scaling. Payments connect object boundaries, API identity, transactions, outbox, provider failures, and ledger reconciliation. Tickets connect local concurrency to expiry and external payment. Documents connect immutable input, lineage, durable stages, human review, and publication.</p>'
    for c in B['units'][-1]['chapters']:html+='<p>'+link(c['id'])+' — '+', '.join(link(p) for p in c['prerequisites'])+'</p>'
    pages.append(panel('reading-path',html))
    html=heading('ALL 22 UNITS / 242 QUESTIONS','Exercises','Five conceptual questions, three scenarios, one design challenge, one implementation exercise, and one advanced thought experiment per unit.')
    html+='<div class="reference-jumps">'+' · '.join(link(f'questions-unit-{u["n"]}',f'{u["n"]:02}') for u in B['units'])+'</div>'
    solutions=heading('ALL 22 UNITS / EXPLAINED ANSWERS','Solutions & reasoning','Each explanation connects the outcome to assumptions, mechanism, and failure. A later or linked chapter provides the full surrounding context.')
    solutions+='<div class="reference-jumps">'+' · '.join(link(f'answers-unit-{u["n"]}',f'{u["n"]:02}') for u in B['units'])+'</div>'
    for u in B['units']:
        n=u['n'];html+=f'<div class="assessment-unit" id="questions-unit-{n}" data-unit="{n}"><h2>Unit {n} · {e(u["title"])}</h2>'
        solutions+=f'<div class="assessment-unit" id="answers-unit-{n}" data-unit="{n}"><h2>Unit {n} · {e(u["title"])}</h2>'
        for kind,ident,q,a in ASSESSMENTS[n]:
            qid=question_id(n,ident,'exercise');aid=question_id(n,ident,'solution')
            html+=f'<article class="exercise" id="{qid}"><span class="eyebrow">{e(kind.replace("_"," "))} / {ident}</span><h3>{e(q)}</h3>{link(aid,"Read the explanation →")}</article>'
            solutions+=f'<article class="solution" id="{aid}"><span class="eyebrow">UNIT {n:02} / {ident}</span><h3>{e(q)}</h3>'+paragraphs(a)+link(qid,'← Return to question')+'</article>'
        html+='</div>';solutions+='</div>'
    pages.extend([panel('exercises',html),panel('solutions',solutions)])
    glossary={term:(meaning,target) for term,meaning,target in GLOSSARY}
    for u in B['units']:
        n=u['n']
        if 1<n<22:
            assert len(SUMMARIES[n])==len(u['topics']),n
            for i,title in enumerate(u['topics'],1):
                term=title.rstrip('.?');glossary.setdefault(term,(SUMMARIES[n][i-1],f'topic-{n}-{i}'))
    for group in PATTERN_LESSONS.values():
        for name,prose,_,_ in group:glossary[name]=(PATTERN_SUMMARIES[name],'pattern-'+slug(name))
    html=heading('THE REFERENCE DESK','A searchable glossary','Definitions and concept summaries link directly to their complete treatment, including individual patterns.')+'<label class="filter-label">Find a term<input type="search" id="glossary-search" placeholder="e.g. fencing, isolation, factory"></label><p id="glossary-count" aria-live="polite"></p><dl class="glossary">'
    for term,(meaning,target) in sorted(glossary.items(),key=lambda row:row[0].casefold()):html+=f'<div data-term="{e((term+" "+meaning).lower())}"><dt>{e(term)}</dt><dd>{e(meaning)} {link(target,"Read the lesson →")}</dd></div>'
    pages.append(panel('glossary',html+'</dl><p id="glossary-empty" hidden>No terms match that search.</p>'))
    B['glossary_entries']=len(glossary)
    html=heading('THE VISUAL INDEX','Every diagram has a job',f'{len(FIGURES)} original figures: chapter mechanisms, full-design views, and the required unit plates. The separate master map is Figure M.1.')+'<div class="figure-list">'
    for f in FIGURES:html+=f'<a href="#{f["id"]}"><span class="eyebrow">FIG. {f["number"]}</span><h3>{e(f["title"])}</h3><p>{e(f["why"])}</p></a>'
    pages.append(panel('figure-index',html+'</div>'))
    formulas=[(name,formula,caveat,target) for name,formula,caveat,target,_ in FORMULAS]+[
      ('Ideal M/M/1 mean residence','W = S / (1 − rho)','S is mean service time and rho is utilization, below one. This single-server model assumes Poisson arrivals and independent exponential service times. W includes waiting and service; it is a mean, so it cannot predict p99.','fig-2-0-2'),
      ('Fan-out slow probability','P(any slow) = 1 − (1 − p)^N','Requires independent equal-probability call outcomes in this model. Shared failures can correlate tails.','topic-2-13'),
      ('Retry amplification','maximum attempts = a^L','a allowed attempts at each of L nested independently retrying layers; actual execution can terminate earlier.','topic-17-7'),
      ('Busy-capacity worksheet','instances = ceil(peak RPS / (assumed capacity × utilization target))','Capacity is an explicit hypothetical or tested input; other bottlenecks and surviving failure capacity remain separate.','topic-2-9'),
      ('Error-budget burn','burn = observed bad fraction / allowed bad fraction','Use the same eligible-event denominator and a positive allowance.','topic-19-8'),
      ('Cache service-time average','E[T] = h × T_hit + (1 − h) × T_miss','A simple service-time mixture, excluding queue effects, dependence, and tail inference.','topic-11-1'),
      ('Backlog growth','growth/s = arrival/s − completion/s','Sustained positive growth requires rejection, reduction, or more useful capacity; a bigger queue only changes waiting.','topic-12-18'),
      ('Raw daily storage','bytes/day = records/s × bytes/record × 86400','Add indexes, history, metadata, replication, retention, compression and migration separately.','topic-2-9')]
    html=heading('THE FORMULA REFERENCE','Symbols with assumptions','Every indexed model is introduced in the lessons. Inputs and guarantee boundaries accompany the notation.')
    for name,formula,caveat,target in formulas:html+='<article class="formula"><h2>'+e(name)+'</h2><code>'+e(formula)+'</code><p>'+e(caveat)+'</p>'+link(target,'Derivation and worked example →')+'</article>'
    pages.append(panel('formulas',html))
    html=heading('THE PATTERN INDEX','Start with the problem, then the pattern','Individual LLD patterns include their intent, collaborators, miniature implementation, costs, and alternatives.')
    for target,names in PATTERNS.items():
        html+='<article class="pattern-group"><h2>'+link(target)+'</h2><div class="pattern-tags">'
        for name in names:html+=link('pattern-'+slug(name) if any(name==row[0] for rows in PATTERN_LESSONS.values() for row in rows) else target,name,'tag')
        html+='</div></article>'
    pages.append(panel('patterns',html))
    html=heading('THE READING ROOM','Source bibliography','Original research and specifications are distinguished from university teaching, implementation documentation, and engineering guidance.')+'<p>Access and the stated use were reviewed on 21 October 2026. Versioned documentation is pinned where practical. A checked link does not prove a production system correct; worked workloads, costs, and architectures are original illustrative models. Recheck security guidance and implementation versions when applying them.</p><label class="filter-label">Filter sources<input type="search" id="source-search" placeholder="e.g. Raft, RFC, database"></label><p id="source-count" aria-live="polite"></p><div id="source-list">'
    for url in SOURCE_URLS:
        title,kind,use=SOURCES[url];html+=f'<article class="source" data-source="{e((title+" "+kind+" "+use+" "+url).lower())}"><span class="eyebrow">{e(kind)}</span><h3><a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(title)} ↗</a></h3><p>{e(use)}</p><small>Access reviewed · 21 October 2026</small></article>'
    pages.append(panel('sources',html+'</div><p id="source-empty" hidden>No sources match that search.</p>'))
    html=heading('PRODUCTION AND EVIDENCE','Completion manifest','All units are produced. Coverage, technical review, executable tests, and browser verification are separate kinds of evidence.')+'<div class="edition-note"><span class="eyebrow">COMPLETE FIRST EDITION</span><p>22 units · 99 chapters · 390 exact syllabus items · 12 full case studies · 242 questions with separate explained solutions.</p></div><div class="manifest-actions"><a href="completion-manifest.json" download>Download manifest ↓</a><a href="BLUEPRINT.md">Complete book blueprint ↗</a><a href="SOURCE_REVIEW.md">Source and technical review ↗</a><a href="QA.md">Verification record ↗</a></div><div class="table-wrap"><table><thead><tr><th>Unit</th><th>Chapters produced</th><th>Concept / case coverage</th><th>Questions / answers</th></tr></thead><tbody>'
    for u in B['units']:html+='<tr><td>'+link(u['id'],str(u['n'])+' · '+u['title'])+f'</td><td>{len(u["chapters"])} / {len(u["chapters"])}</td><td>'+str(len(u['topics']) if u['n']<22 else '12 × 22 sections')+'</td><td>11 / 11</td></tr>'
    html+='</tbody></table></div><h2>What the evidence means</h2><p>Content checks establish presence, exact syllabus allocation, figures, references, and assessment. Executable examples test bounded arithmetic and local invariants. Browser checks test reading, interactions, layouts, offline behavior, and print assembly. The book does not report illustrative objectives as measured production achievements or toy protocols as reviewed production consensus, security, or financial integrations.</p><p>The original request is retained in <a href="BRIEF.txt">BRIEF.txt</a>. Additional optional case subjects are suggestions beyond the twelve mandatory worked designs, not omitted required chapters.</p>'
    pages.append(panel('manifest',html))
    return pages,glossary


def build():
    bodies={}
    # Produce chapter artifacts before computing their summaries and indexes.
    for u in B['units']:
        for j,c in enumerate(u['chapters'],1):bodies[c['id']]=render_chapter(u,c,j)
    unit_bodies={u['id']:render_unit(u) for u in B['units']}
    references,glossary=reference_pages()
    count=len(FIGURES)
    hero=(HERE/'overview.html').read_text().replace('{{chapter-count}}',str(len(CHAPTERS))).replace('{{figure-count}}',str(count))
    partcards=''
    for i,title in enumerate(B['parts']):
        units=[u for u in B['units'] if u['part']==i];chapters=sum(len(u['chapters']) for u in units)
        partcards+=f'<a class="part-card" href="#unit-{units[0]["n"]}"><span class="eyebrow">PART {i+1:02}</span><h3>{e(title)}</h3><p>{chapters} chapters · {len(units)} units · '+('twelve complete design reviews' if i==5 else 'worked mechanisms, failures and alternatives')+'</p><span class="card-foot">Ready to read ↗</span></a>'
    hero=hero.replace('{{part-cards}}',partcards)
    sections=[panel('overview',hero,part='reference')]
    for u in B['units']:
        sections.append(panel(u['id'],unit_bodies[u['id']],'unit-page',u['part']+1))
        sections.extend(panel(c['id'],bodies[c['id']],'chapter case-study' if u['n']==22 else 'chapter',u['part']+1) for c in u['chapters'])
    sections+=references
    nav='<a href="#overview" class="nav-home">The atlas <span>↗</span></a><a href="#contents">Complete contents</a><a href="#concept-map">The concept map</a><a href="#reading-path">Reading paths</a><div class="nav-label">THE SIX PARTS</div>'
    for i,part in enumerate(B['parts']):
        nav+=f'<details class="nav-part" {"open" if i==0 else ""}><summary><span>{i+1:02}</span>{e(part)}</summary>'
        for u in B['units']:
            if u['part']!=i:continue
            nav+=f'<a href="#{u["id"]}" class="nav-unit"><small>{u["n"]:02}</small>{e(u["title"])}<i aria-label="available">●</i></a>'
            nav+=''.join(f'<a href="#{c["id"]}" class="nav-chapter"><small>{c["number"]}</small>{e(c["title"])}</a>' for c in u['chapters'])
        nav+='</details>'
    nav+='<div class="nav-label">THE REFERENCE DESK</div>'+''.join(link(k,v) for k,v in [('exercises','Exercises'),('solutions','Solutions'),('glossary','Searchable glossary'),('figure-index','Diagram index'),('formulas','Formula reference'),('patterns','Pattern index'),('sources','Source bibliography'),('manifest','Completion manifest')])
    search=[]
    for u in B['units']:
        search.append(dict(id=u['id'],title=f'Unit {u["n"]} · '+u['title'],text=' '.join(u['topics']),status='available'))
        for c in u['chapters']:
            search.append(dict(id=c['id'],title=c['number']+' · '+c['title'],text=' '.join(c['topics']+c.get('sections',[])),status='available'))
        if 1<u['n']<22:
            for i,title in enumerate(u['topics'],1):
                row=LESSONS[u['n']][i-1]
                prose=re.sub(r'\*\*|`','',row['prose']) if u['n'] in (3,4) else row['prose']
                search.append(dict(id=f'topic-{u["n"]}-{i}',title=row.get('heading',title),text=prose,status='available'))
    for term,(meaning,target) in glossary.items():search.append(dict(id=target,title=term,text=meaning,status='available'))
    for target,title in [('exercises','Exercises'),('solutions','Solutions'),('glossary','Glossary'),('figure-index','Diagrams'),('formulas','Formulas'),('patterns','Patterns'),('sources','Bibliography'),('manifest','Completion manifest')]:search.append(dict(id=target,title=title,text=title,status='available'))
    data=dict(search=search,figures=FIGURES,chapters=[c['id'] for c in CHAPTERS],date=B['date'],counts=dict(chapters=99,figures=count,questions=242,cases=12))
    html=(HERE/'template.html').read_text().replace('/*__CSS__*/',(HERE/'style.css').read_text()).replace('<!--__NAV__-->',nav).replace('<!--__PANELS__-->','\n'.join(sections)).replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/')).replace('/*__JS__*/',(HERE/'app.js').read_text()+'\n'+(HERE/'expanded.js').read_text())
    html=html.replace('<div class="figure-drawing">','<div class="figure-drawing" tabindex="0" role="region" aria-label="Scrollable technical diagram">')
    assert not re.search(r'\{\{[^}]+\}\}|__PANELS__|__DATA__',html),'Unexpanded template token'
    (OUT/'index.html').write_text(html)
    B['figures']=FIGURES;B['sources']=[dict(url=url,title=SOURCES[url][0],kind=SOURCES[url][1],use=SOURCES[url][2],link_status='reviewed',checked_on=B['date']) for url in SOURCE_URLS]
    words=sum(len(row['prose'].split()) for rows in LESSONS.values() for row in rows)+sum(len(s.split()) for case in CASES.values() for s in case['sections'])+sum(len(row[1].split()) for rows in PATTERN_LESSONS.values() for row in rows)+sum(len(re.sub('<[^>]+>',' ',(HERE/f'chapter-{j}.html').read_text()).split()) for j in range(1,5))
    B['counts']=dict(units=22,chapters_total=99,chapters_produced=99,chapters_remaining=0,syllabus_topics=390,figures_produced=count,mandatory_case_studies=12,case_studies_produced=12,case_review_sections=264,exercises_produced=242,solutions_produced=242,authored_lesson_words=words)
    B['review']=dict(stage_1='complete: exact syllabus and prerequisite allocation',stage_2='complete: all 99 chapters and 12 mandatory designs produced',stage_3='editorial/source review and bounded executable verification; see SOURCE_REVIEW.md and QA.md for scope',stage_4='complete digital edition; full PDF export generated by the documented browser workflow')
    (OUT/'completion-manifest.json').write_text(json.dumps(B,ensure_ascii=False,indent=2)+'\n')
    md=['# The System Design Atlas — complete book blueprint','',B['stage'],'',B['scope'],'']
    for u in B['units']:
        md+=[f'## Unit {u["n"]}: {u["title"]}',f'\nStatus: available. Direct prerequisites: {u["prerequisites"]}.',f'\nWorked example: {u["example"]}']
        for c in u['chapters']:
            md+=[f'\n### {c["number"]} {c["title"]} — available','\nContent source: '+c['content_file']]
            md+=['\n- '+s for s in c.get('sections',c['topics'])]
            md+=['\nFigures: '+'; '.join(f['number']+' '+f['title'] for f in c['illustrations']),'\nReferences: '+' · '.join(c['references'])]
        md+=['\nAssessment: all eleven questions and separate explained solutions produced.']
    (OUT/'BLUEPRINT.md').write_text('\n'.join(md)+'\n')
    validate(html)
    print(f'Built complete atlas: 22 units, 99 chapters, {count} original figures, 12 × 22 case sections, 242 questions + 242 solutions, {words:,} authored lesson words, {len(SOURCE_URLS)} production sources, {len(html):,} HTML characters.')


def validate(html):
    class Inspector(HTMLParser):
        def __init__(self):super().__init__();self.ids=[];self.targets=[];self.local=[]
        def handle_starttag(self,tag,attrs):
            attrs=dict(attrs)
            if attrs.get('id'):self.ids.append(attrs['id'])
            if tag=='a' and attrs.get('href','').startswith('#'):self.targets.append(attrs['href'][1:])
    parsed=Inspector();parsed.feed(html);duplicates=[i for i,n in Counter(parsed.ids).items() if n>1]
    assert not duplicates,duplicates
    assert set(parsed.targets)<=set(parsed.ids),set(parsed.targets)-set(parsed.ids)
    for u in B['units']:
        if u['n']<22:assert Counter(i for c in u['chapters'] for i in c['topic_numbers'])==Counter(range(1,len(u['topics'])+1)),u['n']
        assert all(p<u['n'] for p in u['prerequisites'])
        assert all(c['status']=='available' and len(c['illustrations'])>=4 and c['rendered_words']>=300 for c in u['chapters']),u['n']
        assert Counter(row[0] for row in ASSESSMENTS[u['n']])==Counter(conceptual=5,scenario=3,design=1,implementation=1,thought_experiment=1)
        assert all(item['produced']==item['required'] for item in u['assessment'].values())
    for url in SOURCE_URLS:assert url in SOURCES,url
    assert len(CASES)==12 and all(len(c['sections'])==22 for c in CASES.values())
    assert 'class="panel planned-chapter' not in html
    print('Validated actual lesson/figure/assessment artifacts, exact coverage, all anchors, unique IDs, prerequisite DAG, and all case sections.')

if __name__=='__main__':build()
