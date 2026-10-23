"""Original textbook rewrite, chapter 2.2."""
TOPICS = {
4: {"heading": "The queue that grows while the dashboard looks healthy", "prose": "At a railway ticket counter, two hundred people arrive each minute but the clerk serves only one hundred and eighty. The clerk is busy, yet the line gains twenty people each minute. After ten minutes the queue has grown by two hundred people, if nobody leaves. A web server can behave exactly like this: its completed requests per second may stay steady even as waiting users accumulate.\n\n**Throughput** counts work completed per second. **Arrival rate** counts work offered. **Latency** measures how long one operation takes from a stated start to a stated end, including waiting. A system can report 180 successful requests per second and still be overloaded if 200 arrive each second. **RPS** counts requests, **QPS** queries, and **TPS** transactions; these labels are not interchangeable because one request may run several queries.\n\nTrace the queue in the figure. The backlog grows by arrival rate minus completion rate only under the stated assumptions of a continually busy service, no rejection, and no abandonment. Real systems can time out, shed load, or slow further. Measure arrivals, success, rejection, timeouts, latency, and queue depth together, not throughput alone.\n\n**Try it:** If the clerk is upgraded to serve 210 people per minute while arrivals stay at 200, how does the backlog behave? It can shrink by at most ten people per minute until empty; the clerk cannot serve non-existent requests."},
5: {"heading": "When the average conceals the slowest learner", "prose": "Imagine one hundred students submitting a quiz online. Ninety-nine receive results in 10 milliseconds; the remaining student waits 1,000 milliseconds. The **mean** is (99 × 10 + 1,000) / 100 = 19.9 milliseconds. That sounds small, but it fails to describe the student who waited a second.\n\nSort all one hundred observations. The **median** is the middle result, here 10 milliseconds. Under the **nearest-rank** convention, p95 is observation 95 and p99 is observation 99, both 10 milliseconds. The slow request is observation 100, so even p99 misses it in this tiny sample. Do not claim that p99 guarantees no one waits longer.\n\nThe figure uses a **distribution**, not a sequence of generic boxes. In a real dashboard, preserve histogram buckets or compatible raw observations when calculating an overall percentile. Averaging the p99 values from several machines is generally wrong. Account for timeouts; removing slow failures makes an apparently fast service look better than users experience.\n\n**Try it:** Replace the slowest request with 5,000 milliseconds. Which of mean, median, and nearest-rank p99 changes? Only the mean changes here, to 59.9 milliseconds. We still need the maximum or a more detailed tail view to see the incident."},
6: {"heading": "Four different promises about a service", "prose": "A bank's account page may load promptly but show yesterday's balance. The page was reachable, yet its answer was not fresh enough for a transfer. What went wrong? We have confused separate system properties.\n\n**Availability** asks whether the service can perform the required operation when needed. **Durability** asks whether data already acknowledged as committed survives the failures covered by its storage contract. **Consistency** describes which observations of state are permitted, for example whether a transfer confirmation must be reflected in a subsequent account read. **Reliability** concerns correct operation over time, and needs a specific way to measure correctness.\n\nDraw four independent checkboxes rather than one green badge marked reliable. An API returning a success-shaped error does not satisfy the correct service contract. A service that survives application restarts but loses its only disk is not durable against disk destruction. A cached view may be acceptable for popularity counts and forbidden for the last available ticket.\n\n**Try it:** A newly paid bill is committed, the website is accessible, and the next screen shows the old amount. Which guarantee should you examine first? The read's consistency/freshness contract, not only service availability."},
7: {"heading": "Turn a promise into a measurable reliability budget", "prose": "Suppose a school promises that 99.9 percent of eligible feed requests will succeed over one calendar month. The **SLI** is the measured fraction of good eligible requests. The **SLO** is its chosen target and time window. An **SLA** is a separate agreement that can include obligations and consequences. The three are related but not synonyms.\n\nAssume the school receives one million eligible requests in a month. At a 99.9 percent SLO, at most 0.1 percent are allowed to be bad under that event-based objective. The **error budget** is 1,000,000 × 0.001 = 1,000 bad requests. If 600 have failed, 400 remain. We have chosen a request-count denominator; a time-based availability target would have a different denominator and calculation.\n\nBefore using the number, specify which calls are eligible, what counts as success, which time window is assessed, and how timeouts are treated. Excluding the very requests that fail makes the number meaningless. A budget does not certify that every failure is harmless: a short checkout outage may deserve urgent attention even if the monthly threshold survives.\n\n**Try it:** With two million eligible requests at the same target, how many may be bad? Two thousand. If the error budget is nearly consumed, which new deployment risks should the team reduce?"},
}
FIGURES = {
4: ["timeline","A line grows even when service is busy",["0 min: 0 waiting","5 min: 100 waiting","10 min: 200 waiting","200 arrive/min; 180 complete/min"]],
5: ["distribution","One outlier, three very different summaries",["99 requests: 10 ms","1 request: 1,000 ms","Mean: 19.9 ms","p99: 10 ms"]],
6: ["matrix","Four promises require four tests",["Available?","Durable?","Consistent?","Reliable?"]],
7: ["progress","An error budget is a measured allowance",["1,000 allowed failures","600 observed failures","400 remain","99.9% of 1,000,000"]],
}
# For chapters with three syllabus topics, the fourth illustration is supplemental.
SUPPLEMENT = null

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
