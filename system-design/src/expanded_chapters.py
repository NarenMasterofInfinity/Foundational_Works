"""Render authored concept chapters and full case-study reviews."""
from html import escape as e
import re
from atlas_figures import snapshots,flow,special
from figures import FIGURES
from teaching.foundations import LESSONS
from teaching.cases import CASES,FAILURE_TRACES,EVOLUTION
from teaching.patterns import PATTERN_LESSONS
from teaching.worked import CODE,CASE_FOR_UNIT,CODE_CONTEXT
from teaching.assessment import THOUGHT,TASKS,THOUGHT_ANSWERS
from teaching.guides import GUIDES,CASE_OPENINGS,CASE_CAPTIONS
from teaching.summaries import SUMMARIES,PATTERN_SUMMARIES


def paragraphs(value):return ''.join('<p>'+e(p)+'</p>' for p in value.split('\n\n'))


def lesson_paragraphs(value):
    """Allow named terms and code fragments in the two introductory rewrites."""
    result=[]
    for paragraph in value.split('\n\n'):
        safe=e(paragraph)
        safe=re.sub(r'`([^`]+)`',r'<code>\1</code>',safe)
        safe=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',safe)
        result.append('<p>'+safe+'</p>')
    return ''.join(result)

def introduction(value,note=None):
    first,*rest=value.split('\n\n')
    body='<p class="lead">'+e(first)+'</p>'+''.join('<p>'+e(p)+'</p>' for p in rest)
    if note:body+='<p class="assumption">'+e(note)+'</p>'
    return '<div class="chapter-intro">'+body+'</div>'


def slug(value):return re.sub(r'[^a-z0-9]+','-',value.lower()).strip('-')


def concept_body(unit,chapter,bench=''):
    n=unit['n'];j=int(chapter['number'].split('.')[1]);rows=[(i,LESSONS[n][i-1]) for i in chapter['topic_numbers']]
    render_paragraphs=lesson_paragraphs if n in (3,4) else paragraphs
    opening,takeaway,question=GUIDES[n][j-1]
    html=introduction(opening)
    fig_no=0
    for sub,(i,row) in enumerate(rows,1):
        title=unit['topics'][i-1].rstrip('.')
        display_title=row.get('heading',title)
        html+=f'<section class="concept-lesson" id="topic-{n}-{i}" data-syllabus-topic="{n}:{i}"><h2>{chapter["number"]}.{sub} · {e(display_title)}</h2>'+render_paragraphs(row['prose'])
        fig_no+=1
        visual=special(n,j,fig_no,i)
        if visual is None:visual=snapshots(n,j,fig_no,display_title.rstrip('?')+' · the example',row['trace'],SUMMARIES[n][i-1])
        html+=visual+'</section>'
    if n==6 and j in PATTERN_LESSONS:
        for name,prose,trace,code in PATTERN_LESSONS[j]:
            html+=f'<section class="pattern-lesson" id="pattern-{slug(name)}"><span class="eyebrow">PATTERN / MECHANISM, USE, AND COST</span><h2>{e(name)}</h2>'+paragraphs(prose)
            fig_no+=1;html+=flow(n,j,fig_no,name+' · the example',trace,PATTERN_SUMMARIES[name],True)
            html+='<pre><code>'+e(code)+'</code></pre></section>'
    # Short chapters receive additional meaningful views of the unit's worked
    # system, not empty commissions or duplicated hidden figures.
    case=CASES[CASE_FOR_UNIT[n]]
    while fig_no<4:
        fig_no+=1
        if n==3 and j==1:
            html+=flow(n,j,fig_no,'Follow the task-list request',['Browser asks: GET /tasks','Address and port lead to service','Application obtains the task list','Response returns to the browser'],'Addresses and ports bring data to the program. HTTP tells the program what was requested and gives the response its meaning.')
        elif fig_no%2:
            html+=flow(n,j,fig_no,'Follow the related complete design',case['flow'],CASE_CAPTIONS[CASE_FOR_UNIT[n]][1])
        else:
            html+=snapshots(n,j,fig_no,'State and ownership in the related design',[case['entities'][0],case['entities'][1],case['flow'][-1],case['entities'][-1]],CASE_CAPTIONS[CASE_FOR_UNIT[n]][0])
    if j==len(unit['chapters']):
        kind,code,outcome=CODE[n]
        html+='<h2>Try the mechanism in code</h2>'
        if n in CODE_CONTEXT:html+=render_paragraphs(CODE_CONTEXT[n])
        html+='<p class="eyebrow">'+e(kind)+'</p><pre><code>'+e(code)+'</code></pre>'+render_paragraphs(outcome)
        html+='<p><a href="examples/mechanisms.py">Download the executable mechanism collection ↓</a> · <a href="#ch-22-'+str(CASE_FOR_UNIT[n])+'">Follow the connected complete design →</a></p>'
        html+=bench
    if n==4 and j==4:
        html+="""<h2>Compare waiting with calculation</h2>
<p>Assume 1,000 independent files each wait 100 ms for storage and need negligible calculation. One at a time, they take 100 seconds. Fifty waits at once give twenty groups of 100 ms: an ideal two seconds. For this calculation, ignore startup, transfer limits, and other overhead.</p>
<div class="table-wrap"><table><caption>The same assumed I/O work, with different ways to run and retain jobs</caption><thead><tr><th>Arrangement</th><th>Ideal elapsed time</th><th>What needs a limit?</th><th>After process restart</th></tr></thead><tbody>
<tr><td>One upload at a time</td><td>100 s</td><td>One active file; waiting work elsewhere</td><td>A saved job record is needed to resume</td></tr>
<tr><td>50 threads doing blocking I/O</td><td>2 s</td><td>Threads, buffers, connections, and waiting jobs</td><td>Memory-only jobs are lost</td></tr>
<tr><td>Nonblocking I/O, 50 files in progress</td><td>2 s</td><td>Tasks, buffers, connections, and waiting jobs</td><td>Memory-only jobs are lost</td></tr>
<tr><td>Saved job queue and 50 workers</td><td>At least 2 s, plus queue work</td><td>Accepted jobs, waiting jobs, and active workers</td><td>Saved records identify work to resume</td></tr>
</tbody></table></div>
<p>Now change the work: each file needs 20 ms of CPU time and negligible I/O. The total is 1,000 × 0.02 = 20 CPU-seconds. One executing core needs at least 20 seconds. Eight cores sharing the work perfectly need at least 20/8 = 2.5 seconds. An event loop does not supply those extra cores; the runtime must permit actual parallel execution.</p>
<p>A saved queue preserves job records. It does not remove processing time or prevent every repeated effect during recovery. These calculations compare stated assumptions, rather than measured systems.</p>"""
    if n==21 and j==2:
        html+='''<h2>A complete cost worksheet with fictional inputs</h2><p>Monthly rates below are invented teaching inputs, not provider quotations. Capacity, p99, and availability are evaluation dimensions whose results must be measured; this cost table cannot establish them.</p><div class="table-wrap"><table><caption>Fictional monthly cost units; compare only after checking requirements</caption><thead><tr><th>Architecture</th><th>Compute</th><th>Data</th><th>Cache</th><th>Storage</th><th>Transfer</th><th>Telemetry</th><th>Total</th></tr></thead><tbody><tr><td>Single deployment</td><td>40</td><td>300</td><td>0</td><td>1</td><td>20</td><td>10</td><td>371</td></tr><tr><td>Replicated application</td><td>160</td><td>300</td><td>50</td><td>1</td><td>20</td><td>20</td><td>551</td></tr><tr><td>Partitioned design</td><td>320</td><td>900</td><td>100</td><td>2</td><td>40</td><td>40</td><td>1402</td></tr></tbody></table></div>'''
        html+='''<h2>Compare latency, availability, and operating work under stated assumptions</h2><p>Construct a 100-request trace for each option: single deployment has 98 observations at 190 ms, one at 900 ms, and one at 1,400 ms; replicated application has 98 at 140 ms, one at 450 ms, and one at 800 ms; partitioned design has 98 at 110 ms, one at 600 ms, and one at 1,600 ms. Nearest-rank p99 is observation 99 after sorting. These synthetic traces deliberately show that lower common-case latency can coexist with worse tail latency. They predict no real deployment.</p><p>For a separate steady-state availability model, assume independent app-instance availability of 0.99 and data-owner availability of 0.999. An interchangeable pool of k apps is available with probability 1 − 0.01^k. The single and replicated options require one data owner. The partitioned operation in this example requires all three independent owners, so multiply by 0.999³. Shared outages, overload, failover time, repair, and correlated failures are omitted; these probabilities are not SLO commitments.</p><div class="table-wrap"><table><caption>Illustrative comparison; latency traces, availability probabilities, and operating judgments are assumptions</caption><thead><tr><th>Architecture</th><th>Monthly cost units</th><th>Constructed p99</th><th>Modeled availability</th><th>Operational complexity judgment</th></tr></thead><tbody><tr><td>Single: 1 app, 1 data owner</td><td>371</td><td>900 ms</td><td>98.901%</td><td>Lower: one app release and one data owner</td></tr><tr><td>Replicated: 4 apps, 1 data owner</td><td>551</td><td>450 ms</td><td>99.899999%</td><td>Medium: rolling releases, shared cache, pool capacity and failover</td></tr><tr><td>Partitioned: 8 apps, 3 required data owners</td><td>1,402</td><td>600 ms</td><td>99.700300%</td><td>Higher: routing, rebalancing, multiple owners and partial recovery</td></tr></tbody></table></div><p>For a per-key request touching only one shard, the all-three-owners availability expression does not apply. Replication with an actual quorum or failover protocol also needs a different model. The calculation is executable as architecture_comparison() in the mechanism collection. Choose a candidate against the workload and targets, then test tail latency, degraded capacity, restoration, and operating burden. Cost arithmetic alone cannot establish those properties.</p>'''
    if n==2 and j==3:
        html+='''<div class="callout theory"><span class="eyebrow">INFRASTRUCTURE WORKSHEET · ASSUMED CAPACITY</span><p>At 28,935.19 peak requests/s, a hypothetical tested instance capacity of 600 requests/s and a 60% utilization target imply ceil(28,935.19 / 360) = 81 active instances. Reserving capacity for one lost instance gives 82. This does not size the database, image delivery path, or failure domains. Validate each separately; the 600 figure is an assumed input, not a reported benchmark.</p></div>'''
    if n not in (3,4) or j==len(unit['chapters']):
        html+='<details class="deep-dive"><summary>Think further · '+e(THOUGHT[n])+'</summary>'+paragraphs(THOUGHT_ANSWERS[n])+'</details>'
    html+='<p class="mental-model"><strong>Remember:</strong> '+e(takeaway)+'</p>'
    html+='<p class="check-question">Try applying it: '+e(question)+'</p>'
    return html


def case_body(chapter):
    j=int(chapter['number'].split('.')[1]);case=CASES[j]
    html=introduction(CASE_OPENINGS[j],'The workload, timing, and prices in this design are teaching assumptions. They are not measured benchmarks or a description of a particular company.')
    fig=0
    for i,(title,prose) in enumerate(zip(chapter['sections'],case['sections']),1):
        html+=f'<section class="case-section" data-case-section="{i}" id="case-{j}-section-{i}"><h2>{chapter["number"]}.{i} · {e(title)}</h2>'+paragraphs(prose)
        if i==6:
            fig+=1;html+=snapshots(22,j,fig,'Data ownership and relationships',case['entities'],CASE_CAPTIONS[j][0])
        if i==8:
            fig+=1;html+=flow(22,j,fig,'Follow the main operation',case['flow'],CASE_CAPTIONS[j][1])
        if i==12:
            fig+=1;html+=snapshots(22,j,fig,'Follow the failure and its correction',FAILURE_TRACES[j],CASE_CAPTIONS[j][2])
        if i==20:
            fig+=1;html+=flow(22,j,fig,'How the design can grow',EVOLUTION[j],CASE_CAPTIONS[j][3])
        html+='</section>'
    html+='<h2>A small implementation of the key rule</h2><p class="eyebrow">PSEUDOCODE · ONE PART OF THE DESIGN</p><pre><code>'+e(case['code'])+'</code></pre><p>Use the implementation exercise to test the rule and the failure described above. You can also run local examples of seat claims, duplicate handling, ledger balance, and workflow epochs in <a href="examples/mechanisms.py">the mechanism collection</a>.</p>'
    return html
