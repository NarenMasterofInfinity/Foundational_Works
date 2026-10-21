"""Original complete-edition SVGs: snapshots plus subject-specific teaching views."""
from html import escape as e
from textwrap import wrap
from math import sin,cos,pi
from figures import FIGURES

C={'flow':'#3978a8','healthy':'#26836b','caution':'#a96e21','failure':'#b94b48','control':'#7b65a8','external':'#738087'}

def text(x,y,value,width=90,size=15,anchor='middle',color='#203439'):
    lines=wrap(str(value),width=width,break_long_words=False) or ['']
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" font-family="sans-serif" font-size="{size}">'+''.join(f'<tspan x="{x}" dy="{0 if i==0 else size*1.45}">{e(s)}</tspan>' for i,s in enumerate(lines))+'</text>'

def box(x,y,w,h,label,kind='flow',sub=None):
    color=C[kind]
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="#fffefa" stroke="{color}" stroke-width="1.5"/><rect x="{x}" y="{y+9}" width="3" height="{h-18}" fill="{color}"/>'+text(x+w/2,y+29,label,max(12,int(w/8)),14)+(text(x+w/2,y+h-16,sub,max(12,int(w/7)),11,color='#61746b') if sub else '')

def shell(n,j,k,title,body,caption,why,height=260,width=900):
    ident=f'fig-{n}-{j}-{k}';number=f'{n}.{j}.{k}'
    svg=f'<svg viewBox="0 0 {width} {height}" role="img" aria-labelledby="{ident}-title {ident}-desc"><title id="{ident}-title">Figure {number}: {e(title)}</title><desc id="{ident}-desc">{e(caption)}</desc>{body}</svg>'
    FIGURES.append(dict(id=ident,number=number,chapter=f'ch-{n}-{j}',title=title,caption=caption,why=why,status='available'))
    return f'<figure class="figure" id="{ident}"><div class="figure-drawing">{svg}</div><figcaption><span>FIG. {number}</span><strong>{e(title)}</strong><p>{e(caption)}</p><p class="figure-why"><em>Author-created illustration. Numbers are illustrative unless stated otherwise.</em></p></figcaption></figure>'

def snapshots(n,j,k,title,items,caption,why='Inspect the concrete state, values, and assumptions rather than infer a guarantee from a component name.'):
    body=''
    for i,item in enumerate(items[:6]):
        col=i%2;row=i//2;x=28+col*445;y=25+row*108
        kind='failure' if any(w in item.lower() for w in ['lost','rejected','fails','broken','forbidden']) else 'caution' if any(w in item.lower() for w in ['stale','uncertain','wait','lag','expiry']) else 'flow'
        body+=box(x,y,400,90,item,kind)
        body+=text(x+18,y+75,str(i+1).zfill(2),size=10,anchor='start',color=C[kind])
    return shell(n,j,k,title,body,caption,why,height=45+108*((len(items[:6])+1)//2))

def flow(n,j,k,title,items,caption,dependency=False):
    count=len(items);w=900;node=(w-60-(count-1)*35)/count;body=''
    for i,item in enumerate(items):
        x=30+i*(node+35);body+=box(x,55,node,105,item,'control' if dependency else 'flow')
        if i<count-1:
            sx=x+node;ex=sx+35;dash=' stroke-dasharray="5 4"' if dependency else ''
            body+=f'<path d="M{sx} 108H{ex-7}" fill="none" stroke="{C["control" if dependency else "flow"]}" stroke-width="1.7"{dash}/><path d="M{ex-7} 103L{ex} 108L{ex-7} 113" fill="none" stroke="{C["control" if dependency else "flow"]}" stroke-width="1.7"/>'
    body+=text(450,203,'Dashed arrows: source dependency' if dependency else 'Arrows: ordered stages of this worked mechanism',size=11,color='#61746b')
    return shell(n,j,k,title,body,caption,'Follow the stated ordering and identify which step owns the relevant outcome.',height=230)

def bars(n,j,k,title,rows,caption,unit='illustrative units'):
    maximum=max(v for _,v in rows) or 1;body=''
    for i,(label,value) in enumerate(rows):
        y=35+i*55;body+=text(205,y+19,label,28,13,'end')
        body+=f'<rect x="225" y="{y}" width="540" height="28" rx="3" fill="#e2e9df"/><rect x="225" y="{y}" width="{540*value/maximum}" height="28" rx="3" fill="{list(C.values())[i%len(C)]}"/>'
        body+=text(780,y+19,f'{value:g}',20,13,'start')
    body+=text(450,55+len(rows)*55,unit,size=11,color='#61746b')
    return shell(n,j,k,title,body,caption,'Compare calculated magnitudes under the same explicit model; bar length is not a benchmark.',height=85+len(rows)*55)

def waterfall(n,j,k,title,rows,caption):
    total=sum(v for _,v in rows);body='';running=0
    for i,(label,value) in enumerate(rows):
        y=28+i*52;start=235+running/total*560;length=value/total*560
        body+=text(215,y+18,label,28,13,'end')+f'<rect x="{start}" y="{y}" width="{max(2,length)}" height="26" fill="{list(C.values())[i%len(C)]}"/>'
        body+=text(start+length+6,y+18,str(value)+' ms',20,11,'start');running+=value
    body+=text(450,50+len(rows)*52,f'Total sequential budget: {total} ms; actual overlap or queueing can differ.',size=12)
    return shell(n,j,k,title,body,caption,'Separate stage waits and execution rather than attach one unexplained number to the entire request.',height=82+len(rows)*52,width=980)

# Topic-specific views replace generic snapshots at the corresponding exact
# syllabus position. The surrounding prose states the formal/implementation limits.
SPECIAL={
(4,1):('memory','Threads share a heap but have execution-local stacks',None,'One process contains three thread contexts and a shared heap/resource region. Source-module boundaries do not isolate their failures.'),
(4,13):('deadlock','A circular wait prevents both participants progressing',None,'A holds inventory and waits for payment; B holds payment and waits for inventory. Consistent resource ordering or redesigned ownership can remove this cycle.'),
(6,7):('matrix','Scope identities make lifetime semantics visible',[['Resolution','Request scope 1','Request scope 2'],['Scoped: first / second','A / A','B / B'],['Transient: first / second','C / D','E / F'],['Singleton in this process','S / S','S / S']],'These are identity observations in one application. Framework registration and disposal rules must still be checked.'),
(7,8):('flow','Context boundaries protect different business meanings',['Catalog: Product description','Explicit model translation','Fulfillment: Item location'],'The source-dependency boundary is not automatically a network deployment. Translation prevents one universal schema from erasing meaningful domain differences.',True),
(9,14):('er','An order schema preserves relationships and history',None,'Customer has many Orders, Order has many Lines, and each Line references a Product identity while retaining purchase-time values.'),
(11,7):('matrix','A stale cache is a separate state copy',[['Location','Version and value','Authority'],['Database','v2: price 12','current authoritative value'],['App cache A','v1: price 10','stale representation'],['Checkout','revalidates database','does not trust display cache']],'Invalidation and propagation policy decide when copies agree. The critical checkout operation uses the required authoritative contract.'),
(13,2):('flow','The upload pipeline separates bytes from control',['Authorized upload intent','Direct resumable byte upload','Verify size and checksum','Commit ready job metadata'],'Incomplete uploads never enter processing as verified input. Metadata failure leaves cleanup/reconciliation work rather than a fictitious cross-service transaction.'),
(14,17):('partition','A partition can leave two live but disconnected sides',None,'Region A remains running while B and C form another reachable side. Correct authority and fencing determine who may make which writes; a missing heartbeat cannot stop A.'),
(15,10):('matrix','Presence in a log is not the same as commitment',[['Participant','Durable log suffix','Meaning'],['Leader term 5','8:t4, 9:t5','current-term entry 9'],['Follower A','8:t4, 9:t5','required durable replica'],['Follower B','8:t4','lagging replica']],'Within the stated fixed-membership Raft protocol, majority replication of the current-term entry can advance commit and protect the prefix. This table is not a generic quorum proof.'),
(16,16):('flow','A failed shipment starts tracked compensation',['Inventory reserved','Payment authorized','Shipment creation fails','Refund/release workflow tracked'],'Each step is a local outcome. Compensation can fail or remain uncertain and must have durable progress and reconciliation.'),
(18,16):('trust','Tenant identity must survive every trust boundary',None,'An authenticated tenant context scopes storage queries, jobs, object capabilities, and search. Client-provided tenant labels are not independent authority.'),
(20,2):('matrix','VMs and containers isolate at different layers',[['Layer','Virtual machine','Container'],['Operating environment','Guest OS per VM','Shared host kernel'],['Process resources','Guest-managed processes','Runtime constraints'],['Persistent state','Explicit attached owner','Not ephemeral writable layer']],'These are common architecture distinctions, not a claim that one option universally provides sufficient security or reliability.'),
(2,5):('bars','A small mean can hide one slow request',[('99 requests each',10),('1 slow request',1000),('Mean across 100',19.9)],'The mean is (99×10+1000)/100 = 19.9 ms. This is a synthetic distribution, not a percentile convention.','milliseconds'),
(2,9):('bars','Different workload dimensions have different magnitudes',[('Post storage GB/day',20),('Image delivery GB/day',20000)],'Ten million assumed users each write one 2 kB post and view ten 200 kB images. Storage and delivered traffic are separate workloads.','decimal GB/day; separate storage and network dimensions'),
(3,8):('waterfall','A cold request spends time before server work',[('DNS',20),('TCP setup',40),('TLS setup',40),('Request and work',55)],'A sequential illustrative cold path totals 155 ms. Reuse, protocol, overlap, and actual distance change the result.'),
(8,9):('flow','A payment retry follows durable operation identity',['Actor + key + fingerprint','Atomic intent reservation','Execute or reconcile effect','Persist and replay result'],'The same key and payload return the established operation; a different payload conflicts. Local identity does not encompass arbitrary provider effects.'),
(10,3):('tree','B+tree lookup narrows an ordered key range',None,'Illustrative keys and leaves demonstrate lookup and range locality. Exact database page layout is implementation-specific.'),
(10,10):('versions','Two snapshots can legitimately see different versions',None,'A reader whose snapshot precedes version two can keep seeing version one while a later reader sees version two. MVCC alone does not imply serializability.'),
(11,8):('matrix','LRU and FIFO disagree after the same accesses',[['Policy','After A,B,C,A','Insert D: evicted'],['Ideal LRU','Order B,C,A','B'],['FIFO','Insertion A,B,C','A']],'Capacity is three. Both policies saw the same requests; policy metadata changes the decision.'),
(12,10):('ring','A new owner takes only part of the hash space',None,'With clockwise-successor ownership, key 190 belongs to C at 240. Adding D at 210 moves it to D; the affected interval is (120,210]. Hash coordinates are illustrative.'),
(12,12):('bars','Averages hide a hot partition',[('Partition A',70),('Partition B',10),('Partition C',10),('Partition D',10)],'Seventy percent of writes go to A. Adding cold capacity does not split one hot ownership key.','percent of writes'),
(13,6):('matrix','An inverted index is a term-to-document map',[['Source / term','Representation','Meaning'],['D1','blue car','document text'],['D2','blue bike','document text'],['blue','D1, D2','posting list'],['car','D1','posting list']],'Token analysis creates the lookup representation. Source versions and permissions remain separately owned.'),
(14,7):('matrix','Vector comparison exposes concurrent events',[['Event or merge step','Vector','Relation'],['A only','[1,0]','not before B'],['B only','[0,1]','not before A'],['Merge before increment','[1,1]','dominates both']],'The componentwise maximum combines known progress. A receive event then advances the receiver’s own entry; neither step chooses a business merge.'),
(14,16):('matrix','Intersecting quorums still need a protocol',[['Set','Members','Intersection'],['Write W=2','A, B','B'],['Read R=2','B, C','B'],['Fixed N=3','R + W = 4 > 3','one shared member']],'Intersection preserves a possible witness. Version, membership, persistence, and concurrency rules determine how that witness is used.'),
(15,8):('raft','Raft election changes authority under protocol rules',None,'Election timeout can make a follower a candidate; a valid majority can elect an eligible leader. Observing a higher term returns a participant to follower. This is the role state machine, not the complete protocol.'),
(16,15):('flow','The outbox closes a local publication gap',['Order + outbox in one commit','Relay reads pending intent','Publish event with stable ID','Mark sent; duplicate still possible'],'The relay can crash after publish but before marking. A consumer must handle the repeated event; the database transaction does not include the entire network.'),
(17,8):('breaker','A circuit breaker bounds futile calls',None,'Closed permits calls, an observed failure policy opens the breaker, and bounded half-open probes test recovery. The breaker does not fabricate a successful business result.'),
(17,15):('timeline','Recovery time and recoverable data are different',None,'Last recoverable data at 11:55, incident at 12:00, service restored at 12:20: five minutes of data exposure and twenty minutes of recovery in this example.'),
(19,4):('waterfall','This slow request is dominated by waiting',[('Ingress and other',300),('Pool acquisition',4600),('Query execution',100)],'The synthetic five-second path spends 92% in pool acquisition. More CPU is not an evidence-based first fix for this execution.'),
(20,12):('bars','Canary exposure expands only after verification',[('Initial cohort',5),('Next cohort',25),('Broader cohort',50),('Full exposure',100)],'Percentages are an illustrative rollout plan, not an automatic safety rule. Each increase depends on meaningful representative checks and stop conditions.','percent of selected traffic'),
(21,9):('bars','Architecture costs are not capacity guarantees',[('Single deployment',371),('Replicated application',551),('Partitioned design',1402)],'The complete cost worksheet uses fictional monthly units. Each candidate still needs independent checks for correctness, performance, and failure requirements.','fictional monthly cost units'),
}

def matrix_body(rows):
    widths=[240,300,300];body=''
    for ri,row in enumerate(rows):
        x=25;y=20+ri*60
        for ci,value in enumerate(row):
            w=widths[ci];body+=f'<rect x="{x}" y="{y}" width="{w}" height="60" fill="{"#e5eee9" if ri==0 else "#fffefa"}" stroke="#d4ddd3"/>'+text(x+w/2,y+24,value,int(w/8),13)
            x+=w
    return body,50+len(rows)*60

def special(n,j,k,topic):
    spec=SPECIAL.get((n,topic))
    if not spec:return None
    # All graph edges below are labeled actions or explicitly stated membership.
    kind,title,data,caption,*rest=spec
    if kind=='bars':return bars(n,j,k,title,data,caption,rest[0] if rest else 'units')
    if kind=='waterfall':return waterfall(n,j,k,title,data,caption)
    if kind=='flow':return flow(n,j,k,title,data,caption,rest[0] if rest else False)
    if kind=='matrix':body,height=matrix_body(data)
    elif kind=='memory':
        body='<rect x="25" y="20" width="850" height="275" rx="9" fill="#edf1e9" stroke="#7b65a8" stroke-dasharray="5 4"/>'+text(450,45,'ONE PROCESS ADDRESS SPACE',size=12,color=C['control'])
        for i in range(3):body+=box(55+i*280,75,230,80,f'Thread {i+1}: stack','flow','call-local execution state')
        body+=box(120,195,660,70,'Shared heap, handles, and process resources','control');height=320
    elif kind=='deadlock':
        body=box(60,55,300,90,'A holds inventory','caution')+box(540,55,300,90,'B holds payment','caution')
        body+='<path d="M360 82H540M540 125H360" stroke="#b94b48" stroke-width="2"/>'+text(450,67,'A waits for payment',size=12,color=C['failure'])+text(450,154,'B waits for inventory',size=12,color=C['failure'])
        body+=text(450,215,'Two opposing wait dependencies form a cycle; neither holder can proceed.',size=13);height=245
    elif kind=='er':
        body=box(35,35,240,70,'Customer','control')+box(330,35,240,70,'Order','flow')+box(330,180,240,70,'Order line','healthy')+box(625,180,240,70,'Product','control')
        body+='<path d="M275 70H330M450 105V180M570 215H625" stroke="#3978a8" stroke-width="2"/>'+text(300,58,'1 : N',size=12)+text(490,150,'1 : N',size=12)+text(598,204,'N : 1',size=12)
        body+=text(450,290,'Order line retains purchase-time amount and address-related facts as required.',size=12);height=320
    elif kind=='partition':
        body=box(65,75,280,95,'Old authority A is alive','caution')+box(540,30,280,75,'Replica B','flow')+box(540,180,280,75,'Replica C','flow')
        body+='<path d="M445 20V270" stroke="#b94b48" stroke-width="3" stroke-dasharray="7 6"/><path d="M680 105V180" stroke="#3978a8"/>'+text(445,300,'Partition blocks communication across the red boundary',size=13,color=C['failure']);height=330
    elif kind=='trust':
        body=box(35,75,190,95,'Untrusted client','external')+box(320,75,220,95,'Authenticated API','flow')+box(640,30,220,75,'Scoped storage','control')+box(640,190,220,75,'Scoped worker','healthy')
        body+='<path d="M270 20V275" stroke="#a96e21" stroke-dasharray="6 4"/><path d="M225 120H320M540 110L640 67M540 135L640 225" stroke="#3978a8" fill="none"/>'
        body+=text(270,300,'Trust boundary: validate identity and permitted resource action',size=12,color=C['caution']);height=330
    elif kind=='tree':
        body=box(330,20,240,65,'Root separators: 20 | 40','control')
        for x,label in [(45,'Leaf: 5, 10, 15'),(330,'Leaf: 20, 25, 30'),(615,'Leaf: 40, 45, 50')]:
            body+=box(x,150,240,75,label)+f'<path d="M450 85L{x+120} 150" fill="none" stroke="#3978a8"/>'
        body+=text(450,125,'Choose [20,40) for key 25',size=13)+text(450,258,'Leaves keep ordered keys; ranges can continue across leaf boundaries.',size=12);height=290
    elif kind=='versions':
        body=box(45,40,330,75,'Version 1: value 10','external','committed at logical time 10')+box(525,40,330,75,'Version 2: value 12','healthy','committed at logical time 20')
        body+=box(45,170,330,75,'Reader snapshot at 15','flow','sees version 1')+box(525,170,330,75,'Reader snapshot at 25','flow','sees version 2')
        body+='<path d="M210 170V115M690 170V115" stroke="#3978a8" stroke-dasharray="4 4"/>';height=280
    elif kind=='ring':
        body='<circle cx="450" cy="155" r="110" fill="none" stroke="#b8cbbd" stroke-width="2"/>'
        for angle,label,color in [(0,'A · 0',C['control']),(120,'B · 120',C['control']),(240,'C · 240',C['control']),(210,'D · 210',C['healthy']),(190,'key 190',C['caution'])]:
            a=(angle-90)*pi/180;x=450+110*cos(a);y=155+110*sin(a)
            body+=f'<circle cx="{x}" cy="{y}" r="7" fill="{color}"/>'
            lx=450+175*cos(a);ly=max(22,155+150*sin(a));body+=text(lx,ly,label,size=13,color=color)
        body+=text(450,330,'Clockwise successor: key 190 moves from C to new owner D.',size=13);height=360
    elif kind in ('raft','breaker'):
        labels=['Follower','Candidate','Leader'] if kind=='raft' else ['Closed','Open','Half-open']
        subs=['timeout → candidate','majority → leader','higher term → follower'] if kind=='raft' else ['failure policy → open','recovery timer → probe','probe result → closed/open']
        body=''
        for i,label in enumerate(labels):body+=box(35+i*295,65,240,100,label,['flow','caution','healthy'][i],subs[i])
        body+='<path d="M275 110H330M570 110H625" stroke="#3978a8" stroke-width="1.7"/>'
        body+=text(450,215,'Transitions depend on the labeled protocol conditions; arrows are state transitions.',size=12);height=245
    elif kind=='timeline':
        body='<path d="M90 130H810" stroke="#3978a8" stroke-width="2"/>'
        for x,label,sub in [(100,'11:55','last recoverable point'),(300,'12:00','incident begins'),(790,'12:20','service restored')]:
            body+=f'<circle cx="{x}" cy="130" r="6" fill="#3978a8"/>'+text(x,105,label,size=15)+text(x,164,sub,24,12)
        body+=text(200,215,'5 min data exposure',size=13,color=C['caution'])+text(550,215,'20 min recovery',size=13,color=C['healthy']);height=250
    else:return None
    return shell(n,j,k,title,body,caption,'Make the internal structure or state relation visible before claiming its behavior.',height=height)
