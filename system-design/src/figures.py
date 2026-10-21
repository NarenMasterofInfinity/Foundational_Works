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
    add(1,1,'The application and storage work together',[
      ('u',25,88,140,64,'Person','creates a task','external'),('a',270,88,205,64,'To-do application','owns task behavior','flow'),('d',590,88,180,64,'Persistent store','survives restart','control')],
      [('u','a','submit title','flow'),('a','d','commit task','flow')],
      'The application needs storage to keep a task after restart. We include both inside the boundary when discussing that requirement.',
      'Include the parts needed to explain the behaviour you are studying.',boundaries=[(235,32,550,190,'APPLICATION AND ITS STORAGE')])
    add(1,2,'Creating a task changes the stored state',[
      ('s',20,80,190,74,'State S₀','tasks = {}','external'),('c',300,80,200,74,'create(7, “Read”)','validate; insert','flow'),('t',590,80,190,74,'State S₁','7 → Read, open','healthy')],
      [('s','c','command','flow'),('c','t','new state + result','flow')],
      'Before creation, the collection is empty. After create(7, “Read”), it contains task 7, marked incomplete. The function returns the task details.',
      'Read the state before and after the operation to see exactly what changed.')
    add(1,3,'Save before reporting success',[
      ('a',20,40,220,65,'A · memory only','add → “saved”','flow'),('b',290,40,220,65,'B · process exits','task disappears','failure'),('c',560,40,220,65,'C · commit first','then report success','healthy'),('d',560,170,220,60,'Recovery reads store','task still exists','healthy')],
      [('a','b','restart','failure'),('b','c','change the event order','control'),('c','d','restart','flow')],
      'Memory-only tasks disappear after restart. In the revised version, the application commits the task before reporting success. The task remains after a process restart if committed storage is intact.',
      'Compare the two versions by restarting the process.',height=270)
    add(1,4,'Two levels of detail in one design',[
      ('h',30,45,290,70,'High-level view','process → database','flow'),('l',480,45,290,70,'Low-level view','service → repository interface','control'),('q',30,180,290,60,'What if storage fails?','database unavailable','failure'),('r',480,180,290,60,'Which title is valid?','reject empty title','healthy')],
      [('h','l','zoom into responsibility','control','dependency'),('h','q','ask about failures','failure'),('l','r','ask about rules','healthy')],
      'The high-level view shows the application and database. The low-level view shows the service, repository interface, and rules inside the application.',
      'Check that both views agree about saving a task before reporting success.',height=290)
    add(2,1,'Shared storage details make changes spread',[
      ('a',25,35,210,65,'HTTP handler','validates and formats','flow'),('b',295,35,210,65,'Task rules','also knows SQL columns','caution'),('c',565,35,210,65,'CSV exporter','also changes task state','caution'),('d',295,185,210,65,'Shared task dictionary','everybody can mutate','failure')],
      [('a','b','calls','control','dependency'),('b','c','calls','control','dependency'),('a','d','mutates','failure'),('b','d','mutates','failure'),('c','d','mutates','failure')],
      'Several parts read or change the same task data directly. A change to a field or rule may therefore require edits in several places.',
      'Follow the arrows to find which parts know about the shared data.',height=290)
    add(2,2,'Separate responsibilities inside one process',[
      ('a',25,92,190,70,'Input adapter','parse HTTP / CLI','flow'),('b',305,92,190,70,'Task service','validate and coordinate','healthy'),('c',585,92,190,70,'Task repository','read and commit tasks','control')],
      [('a','b','create command','flow'),('b','c','insert(title)','flow')],
      'The adapter reads input, the service checks task rules, and the repository saves and reads tasks. These parts all run inside one application process.',
      'Each kind of work has a clear place in the code.',boundaries=[(10,30,780,185,'ONE APPLICATION PROCESS')])
    add(2,3,'The service uses a repository contract',[
      ('s',25,50,210,72,'Task service','uses repository contract','healthy'),('p',300,50,200,72,'Repository interface','insert(title) → Task','control'),('a',575,50,200,72,'SQLite adapter','implements protocol','external'),('r',170,190,460,62,'Startup code creates and connects the objects','TaskService(SQLiteTasks(path))','control')],
      [('s','p','requires','control','dependency'),('a','p','implements','control','dependency')],
      'The service uses the repository interface. The SQLite adapter implements that interface. Startup code creates the adapter and passes it to the service; during execution, the service calls it.',
      'The dashed arrows show code dependencies. These objects can run in the same process.',height=290)
    add(2,4,'Each layer works at a different level of detail',[
      ('u',240,15,320,50,'User intent','remember “Read”','flow'),('s',240,95,320,50,'Application rule','nonempty title; assign identity','healthy'),('r',240,175,320,50,'Storage operation','insert task atomically','control'),('o',240,255,320,50,'Operating environment','files, device and power assumptions','external')],
      [('u','s','interpret','flow'),('s','r','persist','flow'),('r','o','request I/O','flow')],
      'The user asks to remember a task. The application applies task rules and requests a storage write. Storage uses files and the underlying device to carry out the write.',
      'Follow one request through the layers to connect the user’s action to the work below it.',height=340)
    add(3,1,'Turn “safe” into a checkable requirement',[
      ('a',20,90,210,76,'“Tasks must be safe”','what does “safe” mean?','caution'),('b',295,90,210,76,'Process restarts','after successful create','flow'),('c',570,90,210,76,'Task is still listed','check that the task remains','healthy')],
      [('a','b','name the failure','control'),('b','c','check the result','flow')],
      'Create a task successfully, restart the process, and check that the task remains. This requirement concerns a process restart with committed storage intact.',
      'A specific requirement tells us which test to run.')
    add(3,2,'Choose, record, and review a design',[
      ('a',20,30,215,65,'Requirements + constraints','what must be true?','flow'),('b',295,30,210,65,'Compare alternatives','state assumptions and costs','control'),('c',570,30,210,65,'Record the choice','decision + consequences','healthy'),('d',295,180,210,65,'Measure and revisit','did the trigger change?','caution')],
      [('a','b','evaluate','flow'),('b','c','select','control'),('c','d','validate','flow'),('d','a','revise evidence','control','dependency')],
      'Write down the requirements, compare choices, and record the decision. Later, use measurements and changed requirements to decide whether the design still fits.',
      'Keep the reasons for a decision alongside the decision itself.',height=290)
    add(3,3,'Check requirements before scoring preferences',[
      ('a',25,80,210,74,'Candidate design','memory-only storage','external'),('b',295,80,210,74,'Restart requirement','must preserve saved tasks','control'),('c',565,80,210,74,'Reject candidate','fails the restart requirement','failure')],
      [('a','b','check feasibility','control'),('b','c','fails mandatory test','failure')],
      'Memory-only storage loses tasks after restart, so we reject it for this application. We compare preference scores only for choices that meet the required behaviour.',
      'An easy-to-run choice is useful only if it meets the requirements.')
    add(3,4,'Availability and durability answer different questions',[
      ('a',25,35,330,70,'Serves every request','but loses acknowledged tasks','failure'),('b',445,35,330,70,'Preserves every committed task','but temporarily rejects requests','caution'),('c',25,180,330,60,'Availability evidence','valid requests get useful responses','flow'),('d',445,180,330,60,'Durability evidence','committed state survives stated failures','control')],
      [('a','c','measure serving behavior','flow'),('b','d','test recovery behavior','control')],
      'A service may reply to requests yet lose tasks after restart. Another may keep every committed task but stop accepting requests while it recovers.',
      'Check both whether requests succeed and whether saved data survives the stated failure.',height=280)
    add(4,1,'C4: zoom from the system into its code',[
      ('a',20,85,160,70,'1 · Context','people + systems','external'),('b',220,85,160,70,'2 · Containers','apps + data stores','flow'),('c',420,85,160,70,'3 · Components','inside an application','control'),('d',620,85,160,70,'4 · Code','selected implementation','healthy')],
      [('a','b','zoom','control','dependency'),('b','c','zoom','control','dependency'),('c','d','zoom','control','dependency')],
      'Each step shows more internal detail. The dashed arrows mean “zoom in.” In C4, a container is an application or data store; it need not be a Docker container.',
      'Select the level that helps your reader answer a particular question.')
    add(4,2,'The application and database share one machine',[
      ('a',30,100,180,70,'Browser','untrusted client','external'),('b',310,100,180,70,'HTTPS application','one server process','flow'),('c',580,100,180,70,'Local SQLite file','same machine / disk','control')],
      [('a','b','HTTPS request','flow'),('b','c','local file I/O','flow')],
      'The browser sends requests to an application on one machine. The database file is on that same machine. If the machine fails, the application and access to the file are both affected.',
      'Show physical placement when asking what can fail together.',height=280,boundaries=[(275,35,505,205,'ONE HOST · ONE FAILURE DOMAIN')])
    add(4,3,'The task is saved, but the reply is lost',[
      ('a',20,30,210,65,'1 · client sends create','request received','flow'),('b',295,30,210,65,'2 · database commits','task 7 exists','healthy'),('c',570,30,210,65,'3 · response lost','client times out','failure'),('d',295,180,210,65,'4 · client retries','new task 8 without dedup','caution')],
      [('a','b','execute','flow'),('b','c','success response','flow'),('c','d','retry original intent','caution')],
      'Task 7 is committed before its reply is lost. The client cannot tell what happened. A fresh create request may add task 8 unless the application recognises it as a retry.',
      'Trace the events in order to see why the client can be unsure even when a task exists.',height=290)
    add(4,4,'Each design change answers a new need',[
      ('a',20,70,165,90,'A · one script','single run; memory','external'),('b',220,70,165,90,'B · local application','modules + durable file','healthy'),('c',420,70,165,90,'C · shared service','API + identity + store','flow'),('d',620,70,165,90,'D · redundant service','requires later analysis','control')],
      [('a','b','restart','control'),('b','c','sharing','control'),('c','d','failure / load','control')],
      'Add storage when tasks must survive restart. Add a remote interface when people need shared access. Extra machines require further decisions about data, failures, and load.',
      'State the requirement that makes each change necessary.')
    return f
