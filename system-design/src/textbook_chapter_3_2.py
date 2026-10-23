"""Original textbook rewrite, chapter 3.2."""
TOPICS = {
4: {"heading": "A name is a question asked of DNS", "prose": "A student remembers the name library.example, not its numeric IP address. The browser or operating system may consult a **DNS resolver** to find suitable records. The answer can be cached for some time under DNS caching rules. A cache can save a lookup, but a cached address can also become outdated until refreshed.\n\nTrace the resolver journey: local cache, configured recursive resolver, and the authoritative DNS information reached through the resolver's lookup process. This is a simplified model; not every request visits all levels, and modern resolvers can use additional security and caching behavior. DNS answers are not proof that a website is trustworthy, and DNS by itself does not encrypt the subsequent application exchange.\n\n**Try it:** If the address is validly cached, must the computer traverse the full DNS tree every time? No. The lookup can be answered from cache under the applicable policy."},
5: {"heading": "Why HTTPS needs a protected connection", "prose": "When someone logs in to the library, the password must not be readable by an ordinary network observer. **TLS** protects data in transit and authenticates the peer under its certificate and trust validation rules. HTTPS is HTTP carried over this secure channel (or its HTTP/3/QUIC equivalent).\n\nA simplified TLS handshake allows client and server to agree on cryptographic parameters and establish protected communication, while the client verifies that the server certificate is appropriate for the intended host. An attacker controlling a network path should not be able to substitute arbitrary content unnoticed if validation and the cryptographic assumptions hold.\n\nTLS does not automatically authenticate the human user to the application, decide which library books that user may view, or prevent insecure application code. Encryption in transit and authorization inside the application are separate questions.\n\n**Try it:** Can HTTPS alone stop Alice from viewing Bob's private borrowing record if the server forgets to check authorization? No."},
6: {"heading": "HTTP versions improve how messages travel", "prose": "A browser might need HTML, styles, scripts, and images. **HTTP/1.1** can reuse connections but has limitations around sequential request/response use on one connection. **HTTP/2** multiplexes streams over one TCP connection; independent application exchanges can share it, though packet loss in that TCP connection can still affect its streams. **HTTP/3** uses QUIC's stream abstraction to change loss-related behavior at the transport layer.\n\nThe figure compares the wire-level conversation and concurrent request bars without claiming that a newer version always makes every website faster. Server computation, caches, browser scheduling, connection reuse, geographic distance, and bottlenecks can dominate.\n\nThe semantics of HTTP requests, status codes, and resources are not completely redefined every time the transport changes. A GET remains a request for the representation of a target resource under HTTP semantics.\n\n**Try it:** If database computation takes several seconds, will changing only HTTP/1.1 to HTTP/3 necessarily solve it? No."},
7: {"heading": "A connection can be expensive to establish", "prose": "Imagine introducing yourself every time you ask a librarian another question. Network setup can have similar repeated overhead. A new TCP connection ordinarily uses a three-way handshake to establish the connection state. For HTTPS over TCP, TLS setup follows or can be optimized according to protocol/version and resumption behavior.\n\n**Connection reuse** avoids repeating some setup work for each request. But keeping connections open also consumes file descriptors, memory, pool slots, and server resources. Idle-connection policies and limits therefore matter.\n\nA handshake diagram must use explicit client/server lifelines and named messages: SYN, SYN-ACK, ACK for TCP. Do not confuse these protocol acknowledgments with business-level “the task was saved” messages.\n\n**Try it:** If the TCP connection is already reusable, will each GET require a new TCP three-way handshake? Not ordinarily."},
8: {"heading": "Break an end-to-end delay into its parts", "prose": "A student reports that loading the library page takes 155 milliseconds. That single number hides where the time goes. In an illustrative **cold request**, suppose DNS takes 20 ms, TCP setup 40 ms, TLS setup 40 ms, and request transfer plus server work 55 ms. If these stages are sequential under our simplified assumptions, the total is 20 + 40 + 40 + 55 = **155 ms**.\n\nA **latency waterfall** draws the stages on a common time axis so that a large wait becomes visible. Real requests can overlap activities, reuse connections, access caches, or use QUIC, so you should not mechanically sum timings from overlapping traces. Different protocol versions have different setup behavior.\n\n**Try it:** If a warm connection eliminates the assumed TCP/TLS setup and the other stages are unchanged, which portion might be avoided? Eighty milliseconds in this deliberately simplified example; actual savings must be measured."},
}
FIGURES = {
4: ["tree","A name can be answered from a cache",["Browser cache","Recursive resolver","DNS hierarchy","Authoritative answer"]],
5: ["boundary","TLS protects data crossing an untrusted network",["Client verifies host","TLS channel","Server certificate","Authorization stays in app"]],
6: ["streams","HTTP messages and transport streams",["HTTP/1.1 reuse","HTTP/2 multiplexing","HTTP/3 QUIC streams","Server work remains"]],
7: ["timeline","TCP establishes state before protected HTTP",["Client SYN","Server SYN-ACK","Client ACK","TLS then HTTP"]],
8: ["waterfall","A cold request pays for multiple stages",["DNS: 20 ms","TCP: 40 ms","TLS: 40 ms","Request + work: 55 ms"]],
}
# For chapters with three syllabus topics, the fourth illustration is supplemental.
SUPPLEMENT = None

from html import escape as E
from atlas_figures import shell

def _rect(x,y,w,h,fill,stroke="#bccaca",radius=8):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'
def _txt(x,y,s,size=13,color="#30474a",anchor="start",weight="normal"):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}">{E(str(s))}</text>'
def figure(n,j,k,topic):
    spec=FIGURES.get(topic) or (SUPPLEMENT if topic==0 else None)
    if not spec:return None
    kind,title,items=spec
    svg=_rect(13,16,874,290,"#fafbf8","#d8e2df",14)
    svg+=_txt(33,44,kind.upper().replace("_"," ")+" / LOOK AT THE MECHANISM",11,"#547a77",weight="bold")
    if kind in ("timeline","journey","tree"):
        for i,item in enumerate(items):
            x=42+i*208
            svg+=_rect(x,99,188,112,["#e6f0ef","#e9eef8","#fff1dd","#e5f1e8"][i%4])
            svg+=_txt(x+94,133,f"{i+1:02d}",20,"#648182","middle","bold")
            # line wrapping by a conservative word limit
            words=item.split(); rows=[]; line=""
            for w in words:
                if len(line+" "+w)>22:rows.append(line);line=w
                else:line=(line+" "+w).strip()
            if line:rows.append(line)
            for z,row in enumerate(rows):svg+=_txt(x+94,168+z*17,row,12,"#30474a","middle")
            if i<3:svg+=f'<path d="M{x+188} 155H{x+207}" stroke="#487c91" stroke-width="2"/><path d="M{x+201} 150L{x+207} 155L{x+201} 160" stroke="#487c91" fill="none" stroke-width="2"/>'
        svg+=_txt(449,269,"Read the order; each arrow names an illustrative step, not an instant network hop.",12,"#688078","middle")
    elif kind in ("curve","area","distribution","dots"):
        svg+=f'<path d="M83 70V255H828" stroke="#829995" stroke-width="2" fill="none"/>'
        if kind=="curve": coords=[(110,231),(308,219),(505,202),(786,91)]
        elif kind=="area":coords=[(110,225),(300,222),(420,212),(510,90),(610,200),(790,222)]
        elif kind=="distribution":coords=[(118,241),(118,107),(172,107),(172,241),(680,241),(680,188),(735,188),(735,241)]
        else:coords=[(120,230),(240,211),(400,165),(570,123),(770,104)]
        svg+='<polyline points="'+" ".join(f"{x},{y}" for x,y in coords)+'" fill="none" stroke="#287e8c" stroke-width="4"/>'
        for i,item in enumerate(items):
            x=48+(i%2)*415;y=282+(i//2)*21
            # place compact labels in footer of svg, clipped to figure height if needed
            svg+=_txt(x,275 if i<2 else 300,item,12,"#4d6564")
    elif kind in ("waterfall","progress"):
        for i,item in enumerate(items):
            y=70+i*53
            w=[680,520,360,220,150][i]
            svg+=_rect(45,y,w,29,["#6c9ca5","#7fac9a","#deb178","#94a8c5","#b9c7b6"][i])
            svg+=_txt(60,y+20,item,13,"#142e31",weight="bold")
    elif kind in ("streams","nested","boundary","gate"):
        for i,item in enumerate(items):
            y=70+i*54
            x=65+i*39 if kind=="nested" else 45
            w=780-i*78 if kind=="nested" else 745
            svg+=_rect(x,y,w,45,["#e5eff1","#eaf3e9","#fff0de","#edf0fa"][i])
            svg+=_txt(x+20,y+28,item,15,weight="bold")
        if kind=="boundary":svg+='<path d="M420 58V286" stroke="#c66b59" stroke-width="3" stroke-dasharray="8 5"/>'
    elif kind in ("worksheet","matrix"):
        for i,item in enumerate(items):
            x=37+(i%2)*420;y=68+(i//2)*108
            svg+=_rect(x,y,398,91,["#e8f1ef","#eef0fa","#fff3e3","#eaf1e8"][i%4])
            svg+=_txt(x+20,y+50,item,15,weight="bold")
    else:
        for i,item in enumerate(items):
            x=48+i*206
            svg+=_rect(x,100,186,123,["#e6f0ef","#eef0fa","#fff2df","#e7f2e9"][i%4])
            svg+=_txt(x+93,139,str(i+1),23,"#507b80","middle","bold")
            words=item.split();first=" ".join(words[:3]);second=" ".join(words[3:])
            svg+=_txt(x+93,171,first,12,"#334d50","middle")
            svg+=_txt(x+93,189,second,12,"#334d50","middle")
    return shell(n,j,k,title,svg,
        "An original concept-specific study plate. All numeric examples are fictional teaching assumptions.",
        "Read the labels against the explained mechanism; the drawing is not a measured production topology.",
        height=324)
