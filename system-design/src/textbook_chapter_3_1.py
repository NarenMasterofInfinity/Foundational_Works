"""Original textbook rewrite, chapter 3.1."""
TOPICS = {
1: {"heading": "A website visit is a journey through several systems", "prose": "When Arjun types the address of a library website into a browser, it looks like a single action. But his computer first needs to discover where to send network traffic. The browser then establishes a suitable connection, sends an HTTP request, and receives bytes that can be interpreted as a page. Each step has its own owner and possible failure.\n\nThe **internet** is a network of networks that forwards packets using IP addressing and routing. Applications exchange meaningful messages using protocols built on top of that packet delivery. The website name people remember, such as library.example, is not the numerical network address routers primarily use. A name-resolution system helps the browser find an address. Later chapters will examine DNS, encryption, and HTTP in detail.\n\nThe figure is a geographically inspired journey map rather than a row of generic components. The user, resolver, network, server and browser occupy distinguishable roles. We must not mistake a diagram arrow for a guaranteed physical direct wire: packets may traverse many routers and different paths.\n\n**Try it:** If the browser already knows the server address, which discovery step might be avoided? A new DNS lookup may be unnecessary, depending on cache validity."},
2: {"heading": "Find the machine, then the program", "prose": "A building address identifies where to deliver a parcel, but the room number tells the courier whom to visit. An **IP address** identifies a network endpoint under the applicable addressing and routing rules; a **port number** identifies a service endpoint at that host in the relevant transport context. The analogy helps, but ports are numbers in protocol headers, not literal rooms, and hosts may have many addresses.\n\nFor a TCP connection, a **socket** represents an endpoint managed by the operating system. A particular TCP connection is identified by both endpoints' address-and-port pairs (along with its protocol context). This is why a server can accept many browser connections at once even though they connect to the same listening port.\n\n**Routing** decides how packets move toward a destination across networks. A local operating system decides which program should receive the traffic. NAT, firewalls, load balancers, and proxies can alter what a packet's path looks like; we will revisit those. The diagram uses nested address labels, not merely another timeline.\n\n**Try it:** Two browser tabs connect to the same server port. Must they be the same TCP connection? No; distinct client endpoints/connections may exist, and browsers can also reuse a shared connection."},
3: {"heading": "TCP, UDP and QUIC promise different things", "prose": "Suppose the library sends a long document in small pieces. With **TCP**, the receiving application gets an ordered stream of bytes. TCP handles retransmission and ordering as required for the connection, but it does not tell the application where one business message ends. The application needs a framing rule, such as a length field or protocol-defined boundary.\n\n**UDP** sends datagrams. It does not provide TCP-style ordered reliable byte-stream delivery, so an application that needs loss recovery or ordering must implement or use another protocol that provides them. **QUIC** runs over UDP but adds secure connections, reliable streams, and stream-level handling of loss. The fact that QUIC uses UDP does not make its stream semantics identical to bare UDP.\n\nThe figure compares streams and datagrams side by side. No transport magically makes a database operation exactly once. Network delivery guarantees and application side-effect guarantees are different layers.\n\n**Try it:** If a user sends a payment request twice after a timeout, does TCP's ordering prevent a duplicate charge? No. Application-level identity and idempotency protection are needed."},
}
FIGURES = {
1: ["journey","Follow the browser's journey through the internet",["Human enters URL","Find network address","Route packets","Server answers"]],
2: ["nested","An address finds a host, a port finds a service",["Network address","Host IP","Listening port","Connection endpoints"]],
3: ["streams","Three transports, three different delivery contracts",["TCP: ordered bytes","UDP: datagrams","QUIC: secure streams","App handles message meaning"]],
0: ["matrix","Packet delivery is not business success",["Network packet arrived","HTTP request parsed","Operation committed","Response received"]],
}
# For chapters with three syllabus topics, the fourth illustration is supplemental.
SUPPLEMENT = ["matrix","Packet delivery is not business success",["Network packet arrived","HTTP request parsed","Operation committed","Response received"]]

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
