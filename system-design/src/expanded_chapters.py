"""Render authored concept chapters and full case-study reviews."""
from html import escape as e
import re
from atlas_figures import snapshots,flow,special
from figures import FIGURES
from teaching.foundations import LESSONS
from teaching.cases import CASES,FAILURE_TRACES,EVOLUTION
from teaching.patterns import PATTERN_LESSONS
from teaching.worked import CODE,CASE_FOR_UNIT
from teaching.assessment import THOUGHT,TASKS


def paragraphs(value):return ''.join('<p>'+e(p)+'</p>' for p in value.split('\n\n'))

def slug(value):return re.sub(r'[^a-z0-9]+','-',value.lower()).strip('-')


def concept_body(unit,chapter,bench=''):
    n=unit['n'];j=int(chapter['number'].split('.')[1]);rows=[(i,LESSONS[n][i-1]) for i in chapter['topic_numbers']]
    html='<div class="chapter-intro"><p class="lead">'+e(unit['example'])+'</p><p>This chapter examines '+e(chapter['title'].lower())+' through concrete mechanisms, state snapshots, failure cases, and alternatives.</p></div>'
    fig_no=0
    for sub,(i,row) in enumerate(rows,1):
        title=unit['topics'][i-1].rstrip('.')
        html+=f'<section class="concept-lesson" id="topic-{n}-{i}" data-syllabus-topic="{n}:{i}"><h2>{chapter["number"]}.{sub} · {e(title)}</h2>'+paragraphs(row['prose'])
        fig_no+=1
        visual=special(n,j,fig_no,i)
        if visual is None:visual=snapshots(n,j,fig_no,title.rstrip('?')+' · worked snapshots',row['trace'],' · '.join(row['trace'])+'. These labeled observations explain the mechanism discussed above; cards do not imply independent processes or network calls.')
        html+=visual+'</section>'
    if n==6 and j in PATTERN_LESSONS:
        for name,prose,trace,code in PATTERN_LESSONS[j]:
            html+=f'<section class="pattern-lesson" id="pattern-{slug(name)}"><span class="eyebrow">PATTERN / MECHANISM, USE, AND COST</span><h2>{e(name)}</h2>'+paragraphs(prose)
            fig_no+=1;html+=flow(n,j,fig_no,name+' · collaborator roles',trace,' · '.join(trace)+'. This is the pattern’s original miniature example, not a claim that every role must be a separate class or deployed service.',True)
            html+='<pre><code>'+e(code)+'</code></pre></section>'
    # Short chapters receive additional meaningful views of the unit's worked
    # system, not empty commissions or duplicated hidden figures.
    case=CASES[CASE_FOR_UNIT[n]]
    while fig_no<4:
        fig_no+=1
        if fig_no%2:
            html+=flow(n,j,fig_no,'The running system · ordered responsibility',case['flow'],case['sections'][8])
        else:
            html+=snapshots(n,j,fig_no,'The running system · invariant and recovery review',[case['entities'][0],case['entities'][1],case['flow'][-1],case['entities'][-1]],case['sections'][20])
    if j==len(unit['chapters']):
        kind,code,outcome=CODE[n]
        html+='<h2>Worked implementation · connect the unit</h2><p class="eyebrow">'+e(kind)+'</p><pre><code>'+e(code)+'</code></pre>'+paragraphs(outcome)
        html+='<p><a href="examples/mechanisms.py">Download the executable mechanism collection ↓</a> · <a href="#ch-22-'+str(CASE_FOR_UNIT[n])+'">Follow the connected complete design →</a></p>'
        html+=bench
    if n==4 and j==4:
        html+='''<h2>1,000 uploads · compare the resource that dominates</h2><p>Assume each independent upload needs exactly 100 ms of waiting for storage and no meaningful CPU work. Ignore startup, connection limits, bandwidth, queue overhead, and variance. Sequential execution then needs 100 seconds; allowing 50 independent waits at once has an ideal lower bound of 2 seconds. These are constructed lower bounds, not measurements.</p><div class="table-wrap"><table><caption>Same I/O workload, different execution and recovery boundaries</caption><thead><tr><th>Execution model</th><th>Ideal elapsed time</th><th>What must be bounded</th><th>Crash recovery</th></tr></thead><tbody><tr><td>Sequential</td><td>100 s</td><td>One active upload; backlog elsewhere</td><td>Requires a durable record</td></tr><tr><td>50 threads with blocking I/O</td><td>2 s</td><td>Threads, stacks, connections</td><td>Memory alone loses accepted work</td></tr><tr><td>Async I/O with 50 in flight</td><td>2 s</td><td>Tasks, buffers, sockets</td><td>Memory alone loses accepted work</td></tr><tr><td>Durable queue, 50 workers</td><td>At least 2 s, plus queue overhead</td><td>Admission, queue age, worker count</td><td>Durable intent plus retry and idempotent completion</td></tr></tbody></table></div><p>Change the workload: each upload instead requires 20 ms of CPU and negligible I/O. The batch needs 20 CPU-seconds. One executing core therefore needs at least 20 seconds; eight truly parallel cores have an ideal lower bound of 2.5 seconds. An event loop creates no extra cores. Runtime restrictions can also prevent CPU-heavy threads from running in parallel. Measure overhead and contention before choosing threads or processes. A durable queue changes acknowledgment and recovery behavior; it does not erase service demand.</p>'''
    if n==21 and j==2:
        html+='''<h2>A complete cost worksheet with fictional inputs</h2><p>Monthly rates below are invented teaching inputs, not provider quotations. Capacity, p99, and availability are evaluation dimensions whose results must be measured; this cost table cannot establish them.</p><div class="table-wrap"><table><caption>Fictional monthly cost units; compare only after checking requirements</caption><thead><tr><th>Architecture</th><th>Compute</th><th>Data</th><th>Cache</th><th>Storage</th><th>Transfer</th><th>Telemetry</th><th>Total</th></tr></thead><tbody><tr><td>Single deployment</td><td>40</td><td>300</td><td>0</td><td>1</td><td>20</td><td>10</td><td>371</td></tr><tr><td>Replicated application</td><td>160</td><td>300</td><td>50</td><td>1</td><td>20</td><td>20</td><td>551</td></tr><tr><td>Partitioned design</td><td>320</td><td>900</td><td>100</td><td>2</td><td>40</td><td>40</td><td>1402</td></tr></tbody></table></div>'''
        html+='''<h2>Compare latency, availability, and operating work under stated assumptions</h2><p>Construct a 100-request trace for each option: single deployment has 98 observations at 190 ms, one at 900 ms, and one at 1,400 ms; replicated application has 98 at 140 ms, one at 450 ms, and one at 800 ms; partitioned design has 98 at 110 ms, one at 600 ms, and one at 1,600 ms. Nearest-rank p99 is observation 99 after sorting. These synthetic traces deliberately show that lower common-case latency can coexist with worse tail latency. They predict no real deployment.</p><p>For a separate steady-state availability model, assume independent app-instance availability of 0.99 and data-owner availability of 0.999. An interchangeable pool of k apps is available with probability 1 − 0.01^k. The single and replicated options require one data owner. The partitioned operation in this example requires all three independent owners, so multiply by 0.999³. Shared outages, overload, failover time, repair, and correlated failures are omitted; these probabilities are not SLO commitments.</p><div class="table-wrap"><table><caption>Illustrative comparison; latency traces, availability probabilities, and operating judgments are assumptions</caption><thead><tr><th>Architecture</th><th>Monthly cost units</th><th>Constructed p99</th><th>Modeled availability</th><th>Operational complexity judgment</th></tr></thead><tbody><tr><td>Single: 1 app, 1 data owner</td><td>371</td><td>900 ms</td><td>98.901%</td><td>Lower: one app release and one data owner</td></tr><tr><td>Replicated: 4 apps, 1 data owner</td><td>551</td><td>450 ms</td><td>99.899999%</td><td>Medium: rolling releases, shared cache, pool capacity and failover</td></tr><tr><td>Partitioned: 8 apps, 3 required data owners</td><td>1,402</td><td>600 ms</td><td>99.700300%</td><td>Higher: routing, rebalancing, multiple owners and partial recovery</td></tr></tbody></table></div><p>For a per-key request touching only one shard, the all-three-owners availability expression does not apply. Replication with an actual quorum or failover protocol also needs a different model. The calculation is executable as architecture_comparison() in the mechanism collection. Choose a candidate against the workload and targets, then test tail latency, degraded capacity, restoration, and operating burden. Cost arithmetic alone cannot establish those properties.</p>'''
    if n==2 and j==3:
        html+='''<div class="callout theory"><span class="eyebrow">INFRASTRUCTURE WORKSHEET · ASSUMED CAPACITY</span><p>At 28,935.19 peak requests/s, a hypothetical tested instance capacity of 600 requests/s and a 60% utilization target imply ceil(28,935.19 / 360) = 81 active instances. Reserving capacity for one lost instance gives 82. This does not size the database, image delivery path, or failure domains. Validate each separately; the 600 figure is an assumed input, not a reported benchmark.</p></div>'''
    html+='<details class="deep-dive"><summary>Architecture review · '+e(THOUGHT[n])+'</summary>'+paragraphs(TASKS[n][1])+paragraphs('Use the failure histories and assumptions above to defend an answer. Distinguish the local mechanism demonstrated here from the full system boundary in the linked complete design.')+'</details>'
    html+='<div class="callout misconception"><span class="eyebrow">CHECK THE BOUNDARY</span><p>'+e(rows[-1][1]['prose'].split('. ')[-2]+'.' if len(rows[-1][1]['prose'].split('. '))>1 else rows[-1][1]['prose'])+'</p></div>'
    html+='<p class="mental-model"><strong>Carry forward:</strong> '+e(' · '.join(rows[-1][1]['trace']))+'.</p>'
    return html


def case_body(chapter):
    j=int(chapter['number'].split('.')[1]);case=CASES[j]
    html='<div class="chapter-intro"><p class="lead">'+e(case['sections'][0])+'</p><p class="assumption">Original teaching design. All workload, latency, capacity, and price figures are illustrative assumptions, not company architecture claims or measured benchmarks.</p></div>'
    fig=0
    for i,(title,prose) in enumerate(zip(chapter['sections'],case['sections']),1):
        html+=f'<section class="case-section" data-case-section="{i}" id="case-{j}-section-{i}"><h2>{chapter["number"]}.{i} · {e(title)}</h2>'+paragraphs(prose)
        if i==6:
            fig+=1;html+=snapshots(22,j,fig,'Data ownership and relationships',case['entities'],prose,'Identify identities, authoritative relationships, derived records, and the invariant that must remain true.')
        if i==8:
            fig+=1;html+=flow(22,j,fig,'The high-level path and responsibility boundaries',case['flow'],prose)
        if i==12:
            fig+=1;html+=snapshots(22,j,fig,'Naive path, failure, improved path, review',FAILURE_TRACES[j],prose,'Read this failure history alongside the naive design and the protocol; the surrounding text names the ambiguity and correction.')
        if i==20:
            fig+=1;html+=flow(22,j,fig,'Evolution follows demonstrated requirements',EVOLUTION[j],prose)
        html+='</section>'
    html+='<h2>Miniature implementation of the core boundary</h2><p class="eyebrow">LANGUAGE-NEUTRAL PSEUDOCODE · NOT A COMPLETE PRODUCTION SERVICE</p><pre><code>'+e(case['code'])+'</code></pre><p>Use the final challenge to exercise the invariant and failure window. Runnable local models for conditional claims, deduplication, ledger balance, and workflow fencing are in <a href="examples/mechanisms.py">the mechanism collection</a>.</p>'
    return html
