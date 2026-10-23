"""Original textbook rewrite, chapter 2.3."""
TOPICS = {
8: {"heading": "A growing library needs a bigger shelf", "prose": "Imagine a school library adds ten percent more books every month. It does not add the same number of books each month: growth applies to the new total. One shelf-unit becomes 1.1 units, then 1.21 units, then about 3.14 units after twelve months because 1.1 raised to the twelfth power is approximately 3.14.\n\nDigital systems accumulate data in much the same way, but **storage growth is not automatically traffic growth**. Some data is deleted; some is replicated; new indexes and backups consume space; transient migration copies occupy space only temporarily. The capacity plan needs separate rows for primary data, replicas, retained history, backups, and headroom. A capacity estimate is a scenario to test, not a guarantee.\n\nThe first figure is a rising curve; the second is a resource worksheet. Suppose a database needs two weeks to expand safely. If its fill-date estimate is one week away, the capacity alert came too late. Record what to measure, an intervention threshold, and how much lead time is required. Good capacity planning asks not merely “How big?” but “When will the next expansion be too late?”\n\n**Try it:** If the first month starts at 100 GB and ends at 110 GB, what is the volume after a second ten-percent increase? 121 GB, not 120 GB."},
9: {"heading": "Translate people into bytes and requests", "prose": "Ten million daily active users tells us nothing about the number of servers by itself. We must assume actions per user. Suppose each user makes fifty API requests per day: 10,000,000 × 50 = 500,000,000 requests per day. Divide by 86,400 seconds to get about **5,787 requests per second on average**.\n\nNow make two separate assumptions: each user publishes one 2 kB text post per day and views ten 200 kB images. Posts contribute 10 million × 2,000 bytes = **20 GB per day of raw content**, using decimal units. Images deliver 10 million × 10 × 200,000 bytes = **20 TB per day of transfer**. Storage and transfer are different things: post bytes accumulate while retained, but image-transfer bytes count repeated delivery.\n\nA resource worksheet must avoid turning this bandwidth figure into server count. CPU depends on computation, RAM on active working data and concurrency, storage on retention and copies, and network on actual transfers. An application instance capacity must come from measurement or an expressly fictional planning assumption. Add request headers, indexes, replication, caching, backups, and retry overhead to the resource they really affect.\n\n**Try it:** If image views double without changing post creation, what happens to raw post growth? It stays 20 GB/day in this model; image delivery doubles to 40 TB/day."},
10: {"heading": "The hour everyone arrives together", "prose": "Suppose the school publishes examination results at noon. Daily averages smooth away the rush. If a planning assumption says the peak is five times the calculated average, the traffic estimate is about **28,935 requests per second**. The number five is deliberately assumed, not learned from school measurements.\n\nEven auto-scaling needs time. Imagine demand exceeds the current service rate by 1,000 requests every second for 30 seconds. If nothing is rejected and no new capacity appears, the queue gains 30,000 requests. Users may still be waiting when the spike ends. A **bounded queue** can absorb a limited burst, but it should reject or defer further work once waiting would exceed the service's deadline.\n\nLook at the peak-versus-average area chart. Ask whether the excess is only ten seconds or continues all afternoon. Ask whether each failed attempt triggers a retry, which can amplify the spike. Scale-out plans must include the time instances take to start, load balancers take to route, and downstream databases take to serve extra pressure. Adding API replicas does not enlarge a single saturated database.\n\n**Try it:** If demand is 500 requests/s above capacity for 40 seconds, what is the additional backlog with no rejection? 20,000 requests."},
}
FIGURES = {
8: ["curve","Compound growth is not a straight line",["Month 0: 100 GB","Month 1: 110 GB","Month 2: 121 GB","Month 12: 314 GB"]],
9: ["worksheet","One million actions can stress different resources",["Requests/day: 500 M","Raw posts/day: 20 GB","Images delivered/day: 20 TB","CPU/RAM: measure"]],
10: ["area","An average hides a noon surge",["Daily mean: 5,787 RPS","Assumed peak: 28,935 RPS","5× illustration","Scaling needs lead time"]],
0: ["progress","A short spike leaves a real backlog",["+1,000 jobs/s","30-second overload","30,000 jobs queued","Bound waiting and shed excess"]],
}
# For chapters with three syllabus topics, the fourth illustration is supplemental.
SUPPLEMENT = ["progress","A short spike leaves a real backlog",["+1,000 jobs/s","30-second overload","30,000 jobs queued","Bound waiting and shed excess"]]

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
