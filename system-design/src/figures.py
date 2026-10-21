"""Original, labeled SVG teaching figures. No remote assets or renderer."""
from html import escape as e

COLORS={'flow':'#3978a8','healthy':'#26836b','caution':'#a96e21','failure':'#b94b48','control':'#7b65a8','external':'#738087'}
FIGURES=[]

def diagram(ch,k,title,nodes,edges,caption,why,width=800,height=260,boundaries=()):
    ident=f'fig-1-{ch}-{k}';number=f'1.{ch}.{k}'
    parts=[f'<svg viewBox="0 0 {width} {height}" role="img" aria-labelledby="{ident}-title {ident}-desc"><title id="{ident}-title">Figure {number}: {e(title)}</title><desc id="{ident}-desc">{e(caption)}</desc><defs>']
    for key,color in COLORS.items():parts.append(f'<marker id="{ident}-{key}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{color}"/></marker>')
    parts.append('</defs>')
    for x,y,w,h,label in boundaries:parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#edf1ea" stroke="#a8b9ae" stroke-dasharray="5 5"/><text x="{x+12}" y="{y+20}" class="boundary-label">{e(label)}</text>')
    lookup={n[0]:n for n in nodes}
    for start,end,label,kind,*style in edges:
        a,b=lookup[start],lookup[end];x1,y1,w1,h1=a[1:5];x2,y2,w2,h2=b[1:5]
        # Rectilinear intersection works for all horizontal/vertical layouts used here.
        if abs((x2+w2/2)-(x1+w1/2))>abs((y2+h2/2)-(y1+h1/2))*1.5:
            sx=x1+w1 if x2>x1 else x1;sy=y1+h1/2;tx=x2 if x2>x1 else x2+w2;ty=y2+h2/2
        else:
            sx=x1+w1/2;sy=y1+h1 if y2>y1 else y1;tx=x2+w2/2;ty=y2 if y2>y1 else y2+h2
        dash=' stroke-dasharray="6 4"' if style and style[0]=='dependency' else ' stroke-dasharray="2 4"' if style and style[0]=='ack' else ''
        color=COLORS[kind]
        path=f'M{sx} {sy}L{tx} {ty}'
        lx=(sx+tx)/2;ly=(sy+ty)/2-9
        # Long horizontal labels need their own channel. Otherwise the text
        # extends into neighboring node labels at ordinary reading size.
        if abs(sy-ty)<1 and abs(tx-sx)>0 and len(label)*6.5>abs(tx-sx)-12:
            channel=min(y1,y2)-22 if min(y1,y2)>=60 else max(y1+h1,y2+h2)+26
            direction=1 if tx>sx else -1
            path=f'M{sx} {sy}L{sx+8*direction} {sy}L{sx+8*direction} {channel}L{tx-8*direction} {channel}L{tx-8*direction} {ty}L{tx} {ty}'
            ly=channel-8
        parts.append(f'<path d="{path}" fill="none" stroke="{color}" stroke-width="1.6"{dash} marker-end="url(#{ident}-{kind})"/>')
        if label:
            parts.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" class="edge-label" stroke="#f8f6f1" stroke-width="6" paint-order="stroke">{e(label)}</text>')
    for _,x,y,w,h,label,sub,kind in nodes:
        color=COLORS[kind];parts.append(f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="#fffefa" stroke="{color}" stroke-width="1.4"/><rect x="{x}" y="{y+9}" width="3" height="{h-18}" fill="{color}"/><text x="{x+w/2}" y="{y+h/2-4 if sub else y+h/2+5}" text-anchor="middle" class="node-label">{e(label)}</text>')
        if sub:parts.append(f'<text x="{x+w/2}" y="{y+h/2+17}" text-anchor="middle" class="node-sub">{e(sub)}</text>')
        parts.append('</g>')
    parts.append('</svg>')
    html=f'<figure id="{ident}" class="figure"><div class="figure-drawing">'+''.join(parts)+f'</div><figcaption><span>FIG. {number}</span> <strong>{e(title)}</strong><p>{e(caption)}</p><p class="figure-why">Why this view: {e(why)} <em>Author-created illustration.</em></p></figcaption></figure>'
    FIGURES.append(dict(id=ident,chapter=f'ch-1-{ch}',number=number,title=title,caption=caption,why=why,status='available'))
    return html

def get_figures():
    FIGURES.clear();f={}
    def add(ch,k,*args,**kw):f[f'{ch}-{k}']=diagram(ch,k,*args,**kw)
    add(1,1,'The boundary follows the promise',[
      ('u',25,88,140,64,'Person','creates a task','external'),('a',270,88,205,64,'To-do application','owns task behavior','flow'),('d',590,88,180,64,'Persistent store','survives restart','control')],
      [('u','a','submit title','flow'),('a','d','commit task','flow')],
      'A user asks the application to remember a task. The store is inside the service responsibility boundary even if a different team operates it.',
      'It separates the user-visible obligation from the process that happens to run the code.',boundaries=[(235,32,550,190,'SERVICE RESPONSIBILITY BOUNDARY')])
    add(1,2,'Data becomes state through a transition',[
      ('s',20,80,190,74,'State S₀','tasks = {}','external'),('c',300,80,200,74,'create(7, “Read”)','validate; insert','flow'),('t',590,80,190,74,'State S₁','7 → Read, open','healthy')],
      [('s','c','command','flow'),('c','t','new state + result','flow')],
      'Given an empty collection and the create command, the state gains task 7 and the caller receives its identifier. Repeating that command is a separate design question.',
      'A concrete transition exposes both the state owner and the effect that a retry could duplicate.')
    add(1,3,'HLD and LLD ask connected questions',[
      ('h',30,45,290,70,'High-level view','process → database','flow'),('l',480,45,290,70,'Low-level view','service → repository interface','control'),('q',30,180,290,60,'Which failure boundary?','database unavailable','failure'),('r',480,180,290,60,'Which local invariant?','reject empty title','healthy')],
      [('h','l','zoom into responsibility','control','dependency'),('h','q','operational question','failure'),('l','r','behavioral question','healthy')],
      'The high-level view places persistent state and communication boundaries. The low-level view explains how application components enforce behavior inside a process.',
      'Both views must agree about who commits state and who reports success.',height=290)
    add(1,4,'From a working demo to a recoverable write',[
      ('a',20,40,220,65,'A · memory only','add → “saved”','flow'),('b',290,40,220,65,'B · process exits','task disappears','failure'),('c',560,40,220,65,'C · commit first','then report success','healthy'),('d',560,170,220,60,'Recovery reads store','task still exists','healthy')],
      [('a','b','restart','failure'),('b','c','change the contract','control'),('c','d','restart','flow')],
      'The naive program works within one run. A restart disproves its persistence promise. Committing before success fixes that failure under the storage assumptions; it does not by itself solve lost replies.',
      'The improvement is tied to a reproducible failure rather than an arbitrary desire for more components.',height=270)
    add(2,1,'An innocent feature crosses every responsibility',[
      ('a',25,35,210,65,'HTTP handler','validates and formats','flow'),('b',295,35,210,65,'Task rules','also knows SQL columns','caution'),('c',565,35,210,65,'CSV exporter','also changes task state','caution'),('d',295,185,210,65,'Shared task dictionary','everybody can mutate','failure')],
      [('a','b','calls','control','dependency'),('b','c','calls','control','dependency'),('a','d','mutates','failure'),('b','d','mutates','failure'),('c','d','mutates','failure')],
      'In the tangled implementation, formatting, business rules, and persistence all know the mutable representation. Changing a field or invariant can break several paths.',
      'Dependency arrows identify the concrete knowledge that makes a change spread.',height=290)
    add(2,2,'Separate responsibilities inside one process',[
      ('a',25,92,190,70,'Input adapter','parse HTTP / CLI','flow'),('b',305,92,190,70,'Task service','validate and coordinate','healthy'),('c',585,92,190,70,'Task repository','read and commit tasks','control')],
      [('a','b','create command','flow'),('b','c','save(task)','flow')],
      'The adapter translates input, the service owns task rules, and the repository owns persistence operations. All three can be ordinary functions in one deployment.',
      'A module boundary can reduce change propagation without adding a network boundary.',boundaries=[(10,30,780,185,'ONE APPLICATION PROCESS')])
    add(2,3,'Dependency direction differs from execution direction',[
      ('s',25,50,210,72,'Task service','depends on save contract','healthy'),('p',300,50,200,72,'Repository protocol','save(task) → result','control'),('a',575,50,200,72,'SQLite adapter','implements protocol','external'),('r',170,190,460,62,'Composition root · construction expression','TaskService(SQLiteTasks(path))','control')],
      [('s','p','requires','control','dependency'),('a','p','implements','control','dependency')],
      'Dashed arrows mean source-level dependencies. At runtime the task service calls the concrete adapter through the agreed contract; there is no extra repository server.',
      'It prevents the common mistake of interpreting every diagram arrow as a network request.',height=290)
    add(2,4,'Abstraction narrows the question at each layer',[
      ('u',240,15,320,50,'User intent','remember “Read”','flow'),('s',240,95,320,50,'Application rule','nonempty title; assign identity','healthy'),('r',240,175,320,50,'Storage operation','insert task atomically','control'),('o',240,255,320,50,'Operating environment','files, device and power assumptions','external')],
      [('u','s','interpret','flow'),('s','r','persist','flow'),('r','o','request I/O','flow')],
      'Each layer hides details but relies on a narrower promise below it. A successful application call cannot offer stronger persistence than its storage and operating assumptions support.',
      'Abstraction reduces what a caller must know; it cannot remove physical dependencies.',height=340)
    add(3,1,'Make a vague quality measurable',[
      ('a',20,90,210,76,'“Tasks must be safe”','ambiguous aspiration','caution'),('b',295,90,210,76,'Process restarts','after successful create','flow'),('c',570,90,210,76,'Task is still listed','executable acceptance check','healthy')],
      [('a','b','choose failure + context','control'),('b','c','define observable result','flow')],
      'The quality scenario names a stimulus, an environment, and a response. This example concerns process restart; it makes no claim about losing the only disk or an entire region.',
      'A precise scope makes a design falsifiable and reveals the assumptions still needing discussion.')
    add(3,2,'A decision is a testable hypothesis',[
      ('a',20,30,215,65,'Requirements + constraints','what must be true?','flow'),('b',295,30,210,65,'Compare alternatives','state assumptions and costs','control'),('c',570,30,210,65,'Record the choice','decision + consequences','healthy'),('d',295,180,210,65,'Measure and revisit','did the trigger change?','caution')],
      [('a','b','evaluate','flow'),('b','c','select','control'),('c','d','validate','flow'),('d','a','revise evidence','control','dependency')],
      'An ADR records why a choice fits current evidence and when to revisit it. The feedback dependency returns changed evidence to requirements analysis.',
      'It keeps a previously sensible choice from becoming an unquestioned permanent rule.',height=290)
    add(3,3,'A hard constraint comes before a preference score',[
      ('a',25,80,210,74,'Candidate design','memory-only storage','external'),('b',295,80,210,74,'Restart requirement','must preserve saved tasks','control'),('c',565,80,210,74,'Reject candidate','cannot buy correctness with points','failure')],
      [('a','b','check feasibility','control'),('b','c','fails mandatory test','failure')],
      'An in-memory design is infeasible for the chosen restart promise, however cheap or quick it is. Weighted scores compare only candidates that pass the hard constraints.',
      'It distinguishes a preference trade-off from violating an invariant.')
    add(3,4,'Healthy traffic does not prove durable data',[
      ('a',25,35,330,70,'Serves every request','but loses acknowledged tasks','failure'),('b',445,35,330,70,'Preserves every committed task','but temporarily rejects requests','caution'),('c',25,180,330,60,'Availability evidence','valid requests get useful responses','flow'),('d',445,180,330,60,'Durability evidence','committed state survives stated failures','control')],
      [('a','c','measure serving behavior','flow'),('b','d','test recovery behavior','control')],
      'Availability and durability require different observations. A fully reachable service can lose data; a temporarily unreachable store can retain all committed data.',
      'Separate evidence prevents an uptime dashboard from being treated as proof of data safety.',height=280)
    add(4,1,'C4 changes the level of detail',[
      ('a',20,85,160,70,'1 · Context','people + systems','external'),('b',220,85,160,70,'2 · Containers','apps + data stores','flow'),('c',420,85,160,70,'3 · Components','inside an application','control'),('d',620,85,160,70,'4 · Code','selected implementation','healthy')],
      [('a','b','zoom','control','dependency'),('b','c','zoom','control','dependency'),('c','d','zoom','control','dependency')],
      'The dashed arrows mean a change in abstraction, not a runtime call. C4 containers are applications or data stores; they are not synonymous with operating-system containers.',
      'Choose the view that answers a real reader question, rather than drawing all four levels automatically.')
    add(4,2,'A deployment view locates the single points of failure',[
      ('a',30,100,180,70,'Browser','untrusted client','external'),('b',310,100,180,70,'HTTPS application','one server process','flow'),('c',580,100,180,70,'Local SQLite file','same machine / disk','control')],
      [('a','b','HTTPS request','flow'),('b','c','local file I/O','flow')],
      'The example has one machine with a local store. Module separation has not created redundancy; host or disk loss can still remove the whole service.',
      'Deployment placement exposes correlated failure that logical component boxes can hide.',height=280,boundaries=[(275,35,505,205,'ONE HOST · ONE FAILURE DOMAIN')])
    add(4,3,'A lost response makes the outcome uncertain',[
      ('a',20,30,210,65,'1 · client sends create','request received','flow'),('b',295,30,210,65,'2 · database commits','task 7 exists','healthy'),('c',570,30,210,65,'3 · response lost','client times out','failure'),('d',295,180,210,65,'4 · client retries','new task 8 without dedup','caution')],
      [('a','b','execute','flow'),('b','c','success response','flow'),('c','d','retry original intent','caution')],
      'Commit precedes the lost response. A timeout cannot distinguish this case from a failure before commit. Retrying a create without a deduplication contract can create another task.',
      'A sequence explains the ambiguity that a static architecture diagram leaves out.',height=290)
    add(4,4,'Architecture evolves when an assumption fails',[
      ('a',20,70,165,90,'A · one script','single run; memory','external'),('b',220,70,165,90,'B · local application','modules + durable file','healthy'),('c',420,70,165,90,'C · shared service','API + identity + store','flow'),('d',620,70,165,90,'D · redundant service','requires later analysis','control')],
      [('a','b','restart','control'),('b','c','sharing','control'),('c','d','failure / load','control')],
      'Persistence addresses restart. An API addresses shared remote access. Redundancy and data distribution require their own failure, correctness, and load analysis; they are not a free final step.',
      'The sequence is a set of justified changes, not a universal maturity ladder.')
    return f
