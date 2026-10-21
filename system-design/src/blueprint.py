"""Editorial structure. Topic numbers refer to the unchanged supplied syllabus."""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATE = '2026-10-21'
PARTS = ['System design foundations', 'Low-level design & software architecture',
         'Data, storage & scalability', 'Distributed systems & reliability',
         'Security & production engineering', 'Complete system design case studies']
# Each chapter's exact syllabus allocation is explicit, so future editorial work
# cannot accidentally turn a checkmarked unit into a partially covered unit.
OUTLINES = {
1: [('From a program to a system', [1,2,3,5,8]), ('Organising code into modules', [6,7]),
    ('From requirements to design choices', [4,9,11,12,13]), ('Drawing the system at different levels', [10])],
2: [('Turn user journeys into workloads', list(range(1,4))), ('Measure the experience', list(range(4,8))), ('Estimate the resources', list(range(8,11))), ('Queues, bottlenecks & defensible decisions', list(range(11,16)))],
3: [('Addresses, sockets & transports', list(range(1,4))), ('A secure request, one round trip at a time', list(range(4,9))), ('Intermediaries & persistent connections', list(range(9,13))), ('Discover, route & survive the network', list(range(13,18)))],
4: [('The runtime owns your resources', list(range(1,6))), ('Tasks, threads & event loops', list(range(6,10))), ('Shared memory & coordination', list(range(10,14))), ('Visibility, cancellation & overload', list(range(14,18)))],
5: [('Model behavior with objects and values', list(range(1,6))), ('Principles under pressure', list(range(6,10))), ('Side effects, domain models & collaboration', list(range(10,14))), ('Design for change, testing & functions', [14,15])],
6: [('Dependencies, inversion & composition', list(range(1,7))), ('Lifetimes, ownership & cleanup', list(range(7,13))), ('Injection, locators & factories', [13,14]), ('Creational patterns', [15]), ('Structural patterns', [16]), ('Behavioral patterns', [17]), ('Enterprise patterns & boundaries', [18])],
7: [('Layers, monoliths & ports', list(range(1,7))), ('Model a bounded context', list(range(7,11))), ('Keep business policy inside', list(range(11,16))), ('Evolution without a distributed monolith', list(range(16,21)))],
8: [('Model resources and messages', list(range(1,7))), ('Compatibility & idempotency', list(range(7,10))), ('Control access, load & long operations', list(range(10,15))), ('Evolve a public contract', list(range(15,20)))],
9: [('Storage promises & database families', list(range(1,10))), ('Files, objects & analytical layouts', list(range(10,14))), ('Model relationships and ownership', list(range(14,18))), ('Access patterns, retention & operational cost', [18,19])],
10: [('Pages, indexes & query plans', list(range(1,7))), ('Commit, logging & versions', list(range(7,11))), ('Races, anomalies & isolation', list(range(11,16))), ('Pools, recovery & ticket correctness', list(range(16,19)))],
11: [('Locality and cache placement', list(range(1,5))), ('Copies, freshness & eviction', list(range(5,9))), ('Hot keys, stampedes & negative results', list(range(9,14))), ('Edges, partitions & the price of a cache', list(range(14,18)))],
12: [('Scale compute & route requests', list(range(1,7))), ('Replicate and partition data', list(range(7,13))), ('Lag, proxies & saturated pools', list(range(13,18))), ('Regions, write paths & scale economics', list(range(18,23)))],
13: [('Upload bytes without losing identity', list(range(1,6))), ('Build and rebuild a search index', list(range(6,9))), ('Move data through batch and streams', list(range(9,14))), ('Quality, provenance & replay', list(range(14,18)))],
14: [('Partial failure & the meaning of time', list(range(1,8))), ('Consistency as a reader-visible contract', list(range(8,14))), ('Partitions, CAP, PACELC & quorums', list(range(14,18))), ('Coordination, safety & liveness', list(range(18,21)))],
15: [('Choose a replication model', list(range(1,7))), ('Raft and replicated state machines', list(range(7,12))), ('Fences, leases & failure detection', list(range(12,16))), ('Conflicts, CRDTs & regional trade-offs', [16,17])],
16: [('Queues, logs & delivery boundaries', list(range(1,10))), ('Retries, consumers & event history', list(range(10,14))), ('Read models, the outbox & sagas', list(range(14,17))), ('Coordinate durable workflows', list(range(17,23)))],
17: [('Failure domains & redundancy', list(range(1,5))), ('Retries, circuit breakers & isolation', list(range(5,11))), ('Shed load and degrade deliberately', list(range(11,15))), ('Recover, test & learn from failure', list(range(15,23)))],
18: [('Threats, identity & authorization', list(range(1,8))), ('Secrets, encryption & trust boundaries', list(range(8,15))), ('Tenant isolation, audit & deletion', list(range(15,20))), ('Supply chains and security reviews', list(range(20,23)))],
19: [('Observe behavior with three signals', list(range(1,7))), ('Choose indicators, budgets & alerts', list(range(7,12))), ('Profile and investigate production', list(range(12,17))), ('Learn from incidents and trace async work', list(range(17,20)))],
20: [('Environments, VMs & containers', list(range(1,5))), ('Control planes, scheduling & configuration', list(range(5,10))), ('Releases, flags & schema migrations', list(range(10,16))), ('Platforms, serverless & ownership', list(range(16,22)))],
21: [('Budgets, bottlenecks & honest benchmarks', list(range(1,7))), ('Capacity, architecture & cost per outcome', list(range(7,13))), ('Efficiency and a useful test portfolio', list(range(13,17))), ('Fitness functions and design validation', list(range(17,21)))],
}
PREREQS = {1:[],2:[1],3:[1],4:[1],5:[1],6:[5],7:[5,6],8:[1,3],9:[1],10:[4,9],11:[3,9],12:[2,3,9,10,11],13:[8,9,10],14:[3,4,10],15:[14],16:[8,10,14,15],17:[2,12,15,16],18:[3,7,8,9],19:[2,3,4,10],20:[3,7,17,18,19],21:[2,4,10,12,17,19,20],22:list(range(1,22))}
CASE_NAMES = ['URL Shortener','Rate Limiter','Chat Application','Notification Platform','Social Media Feed','Video Streaming Platform','Ride-Hailing System','Online Ticket Booking','Payment System','Distributed Job Scheduler','Collaborative Document Editor','Large-Scale Document Processing Platform']
CASE_PREREQS = [[8,9,11,12],[2,4,12,17],[3,9,14,16],[6,8,16,17],[9,11,12,16],[3,11,13,20],[9,12,14,16],[8,10,16,18],[8,10,16,17,18],[4,15,16,17],[3,14,15,16],[13,16,17,18,19,20]]
CASE_FOCUS = ['ID space, collisions, cache correctness and read scaling','Token bucket arithmetic, atomic updates and regional quotas','Reconnect, offline delivery, ordering and presence expiry','Channel strategies, preferences, retries and delivery receipts','Fan-out choices, celebrity skew and ranking pipelines','Resumable ingestion, encoding ladders and edge delivery','Location freshness, spatial indexes and assignment races','Reservation expiry, isolation, payment and compensation','Ledger invariants, idempotency and reconciliation','Durable time, leases, fencing and duplicate effects','Concurrent edits, causal history, OT and CRDT assumptions','Ingestion, extraction, provenance, human review and recovery']
CASE_REVIEW = ['Functional requirements','Nonfunctional requirements','Explicit assumptions and workload numbers','Naive initial architecture','Core API contracts','Data model and schema','Low-level component organization','High-level system architecture','Data and control flows','Capacity estimates','End-to-end latency estimates','Failure scenarios','Scalability improvements','Consistency requirements','Security model','Deployment approach','Observability design','Infrastructure cost considerations','Alternative architectures and trade-offs','Architecture evolution from small scale to large scale','Design review identifying weaknesses and improvements','A short implementation exercise']

EXTRA_REFS = {
1: ['https://c4model.com/diagrams','https://c4model.com/abstractions/container','https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions','https://www.sqlite.org/atomiccommit.html','https://www.rfc-editor.org/rfc/rfc9110.html'],
3:['https://www.rfc-editor.org/rfc/rfc9110.html'],
14:['https://lamport.azurewebsites.net/pubs/time-clocks.pdf'],
15:['https://raft.github.io/raft.pdf'],
16:['https://microservices.io/patterns/data/transactional-outbox.html']}

def build_blueprint():
    units = json.loads((HERE/'syllabus.json').read_text())
    brief = (HERE.parent/'BRIEF.txt').read_text()
    for u in units:
        n=u['n'];u['id']=f'unit-{n}';u['part']=0 if n<=4 else 1 if n<=8 else 2 if n<=13 else 3 if n<=17 else 4 if n<=21 else 5
        u['prerequisites']=PREREQS[n];u['status']='available' if n==1 else 'planned'
        u['references']=list(dict.fromkeys(u['references']+EXTRA_REFS.get(n,[])))
        outlines=OUTLINES.get(n,[(title,[]) for title in CASE_NAMES])
        u['chapters']=[]
        for j,(title,indices) in enumerate(outlines,1):
            c=dict(id=f'ch-{n}-{j}',number=f'{n}.{j}',title=title,topics=[u['topics'][i-1] for i in indices],topic_numbers=indices,status='available' if n==1 else 'planned',references=u['references'],prerequisites=([f'ch-{n}-{j-1}'] if j>1 else [f'unit-{p}' for p in PREREQS[n]]))
            c['illustrations']=[dict(id=f'fig-{n}-{j}-{k}',title=t,status='planned') for k,t in enumerate(['A — simplest working arrangement','B — failure or limiting assumption','C — revised mechanism and cost','Execution trace and alternatives'],1)]
            if n==22:
                c['focus']=CASE_FOCUS[j-1];c['prerequisites']=[f'unit-{p}' for p in CASE_PREREQS[j-1]];c['sections']=CASE_REVIEW
            u['chapters'].append(c)
        if n==1:
            for c in u['chapters']:
                for fig in c['illustrations']:fig['status']='available'
        u['assessment']={kind:dict(required=count,produced=count if n==1 else 0,status='available' if n==1 else 'planned') for kind,count in [('conceptual',5),('scenario',3),('design',1),('implementation',1),('thought_experiment',1)]}
    optional=re.search(r'Additional optional case studies:\n(.*?)\nEvery case study',brief,re.S).group(1)
    return dict(title='The System Design Atlas',subtitle='From Objects to Planet-Scale Systems',date=DATE,parts=PARTS,units=units,optional_cases=re.findall(r'^- (.+)',optional,re.M),case_review=CASE_REVIEW,stage='Blueprint complete; Unit 1 produced; Units 2–22 planned',scope='This is a staged first installment, not the finished textbook. Planned pages are editorial outlines, not lessons.',visual_language=dict(paper='#f8f6f1',ink='#203439',teal='#087a72',flow='#3978a8',healthy='#26836b',caution='#a96e21',failure='#b94b48',control='#7b65a8',external='#738087'))
