"""Original textbook rewrite, chapter 2.4."""
TOPICS = {
11: {"heading": "How much work is inside the system?", "prose": "At a small bakery, customers arrive steadily and each customer spends time waiting and receiving bread. If 500 customers finished their visit every second in a hypothetical super-fast bakery, and each spent an average 40 milliseconds inside, the average number inside would be 500 × 0.04 = **20**. This is **Little's Law**, written L = λW.\n\nL is the average number of items inside a clearly defined boundary; λ is the long-run throughput/arrival rate in a stable system; W is their average time inside that same boundary. Units must agree: seconds with items per second. It does not tell us the maximum queue, p99 latency, or how to make an overloaded service stable.\n\nImagine the average time rises to 0.4 seconds while stable throughput remains 500/s. L becomes 200. More concurrent work may mean more waiting, not more useful processing. The illustration draws work in flight as dots, not as network components. A queue growing forever is not in the stable situation we used for the equation.\n\n**Try it:** At 100 jobs per second and an average 0.5-second residence time, how many jobs are present on average? Fifty."},
12: {"heading": "Why eight workers may not run eight times faster", "prose": "Suppose an image-processing batch needs 100 seconds on one processor. Twenty seconds must run in sequence; eighty seconds can be split perfectly among workers. With four workers, the shared part ideally takes 80/4 = 20 seconds, but the sequential twenty seconds remain. The new time is 40 seconds, only **2.5×** faster.\n\nThis is **Amdahl's Law**. For a fixed job with sequential fraction s and n ideal processors, speedup = 1 / (s + (1-s)/n). Here s=0.2 and n=4. Even infinitely many workers cannot remove the sequential twenty seconds, so the ideal speedup ceiling is 5×. Real overhead can make the outcome worse.\n\nThe figure is a comparison of colored time bars, not a chain of boxes. It marks the immovable sequential work and shrinking parallel work. Before buying more machines, find the part that cannot be divided and any shared storage/coordination bottleneck.\n\n**Try it:** What happens if you double workers from four to eight? The ideal time becomes 20 + 80/8 = 30 seconds, not 20 seconds."},
13: {"heading": "The slowest dependency sets the deadline", "prose": "A checkout request may contact shipping, pricing, inventory, and fraud services. If the calls run in parallel and the reply needs **all** of them, its duration is approximately the slowest completed dependency plus surrounding work, rather than the sum of all durations. But that statement assumes true overlap and no additional shared queueing.\n\nIf a request fans out to fifty services and each one independently has a one-percent chance of being slow, the chance that **at least one** is slow is 1 − 0.99^50, about 39.5 percent. This artificial independence model explains why wide fan-out can worsen end-user tail latency even when most individual calls are quick.\n\nUse a timeline with parallel lifelines to see who blocks the final reply. Set explicit deadlines, cancellation rules, and fallbacks only where business semantics permit them. A payment authorization cannot usually be invented just because its provider timed out.\n\n**Try it:** If three required parallel calls finish in 20, 50, and 200 milliseconds, what dominates completion? The 200-ms dependency, assuming overlapping start times."},
14: {"heading": "A cheap architecture can still be unacceptable", "prose": "A design review offers two options for storing medical notes. The cheaper one accidentally lets one tenant read another tenant's data. It should be rejected even if its latency is excellent. **Requirements are gates before they are preferences.** Security, correctness and legal constraints may be non-negotiable; saving money cannot compensate for violating them.\n\nWrite assumptions and risks explicitly. For example, a cloud service with low unit cost may need extra staffing, monitoring, and operational complexity. A serverless design may be attractive for sporadic work and expensive or awkward under different sustained loads. A decision must compare feasible alternatives for the same workload, not marketing labels.\n\nThe figure uses a decision gate instead of identical architecture boxes. First eliminate an option that violates a mandatory condition, then compare the survivors with evidence. An unknown measurement is not a pass: write how you will test it.\n\n**Try it:** If an option has unverified data isolation, should you award it high security points or mark validation required? Mark validation required."},
15: {"heading": "Make the trade-off visible and revisable", "prose": "After passing mandatory checks, suppose two architectures remain. One is simpler to operate; the other provides faster recovery but costs more. A weighted score may help the team structure discussion, but a score cannot replace correctness or evidence. Declare who chose the weights, which measurements support each score, and how sensitive the result is to changing assumptions.\n\nAn **Architecture Decision Record (ADR)** captures the context, chosen option, rejected alternatives, consequences, and what would cause reconsideration. The goal is not to prove that one architecture is universally best. It is to show why the choice is defensible for today's constraints.\n\nTry the reversible decision first when uncertainty is high: a measured monolith may be preferable to prematurely splitting services. But do not confuse simplicity with a refusal to plan for recovery, security, or data ownership.\n\n**Try it:** If measured peak traffic doubles, which parts of the decision need revisiting? Capacity tests, bottleneck assumptions, cost, and perhaps the selected architecture."},
}
FIGURES = {
11: ["dots","Little's Law counts work in flight",["λ=500 operations/s","W=0.04 s","L=20 average","Steady state only"]],
12: ["waterfall","More workers cannot shrink sequential time",["1 worker: 100 s","4 workers: 40 s","8 workers: 30 s","Limit: 20 s"]],
13: ["timeline","Parallel calls finish when the last required call does",["Pricing: 20 ms","Inventory: 50 ms","Fraud: 200 ms","All required"]],
14: ["gate","Reject infeasible designs before scoring",["Security: must pass","Correctness: must pass","Performance: measure","Cost: compare feasible"]],
15: ["matrix","Keep a decision record, not only a winner",["Decision context","Assumptions","Consequences","Revisit trigger"]],
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
