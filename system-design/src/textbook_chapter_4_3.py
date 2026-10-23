"""Original teaching additions and purpose-specific plates for 4.3."""
from html import escape as e
from atlas_figures import shell
INTRO="Two scanning workers update the same number of completed answer sheets. Each worker seems correct alone, yet the displayed total sometimes loses an increment."
LESSONS=[{"title":"Share memory or exchange messages","text":"Threads in one process may communicate by reading shared objects, but then they need a rule for simultaneous access. Separate processes can exchange messages and avoid some shared-memory hazards, though message order, loss and repeated delivery introduce other problems. A side-by-side drawing compares ownership rather than asserting one approach is always superior.","visual":"swimlane"},{"title":"The lost-update puzzle","text":"Two workers read the counter as 7. Both compute 8, then both store 8. The correct final value for two successful increments is 9. The error is a race: outcome depends on interleaving. Draw each read, calculate and write on different lifelines to reveal the collision; a generic arrow from worker to database hides it.","visual":"topology"},{"title":"Locks and signals solve different problems","text":"A mutex gives one participant exclusive access to a critical section under its rules. A semaphore counts available permits. An atomic operation can make one defined memory action indivisible; a condition variable allows a thread to wait for a condition together with its mutex protocol. These are not interchangeable magic keywords. A database row update may require its own atomic transaction even if a local Python lock exists.","visual":"comparison"},{"title":"Two polite workers can wait forever","text":"Worker A holds the file lock and asks for the counter lock. Worker B holds the counter lock and asks for the file lock. Each waits for the other: a deadlock cycle. Enforcing one consistent lock acquisition order can prevent this particular cycle. Starvation is different: some task continually loses its chance to progress. Livelock means active participants keep reacting without completing useful work.","visual":"timeline"}]


def drawing(n,j,k,index):
    record=LESSONS[index]
    title=record["title"]; kind=record["visual"]
    ident=f"ch{n}{j}{k}"
    parts=[f'<rect x="10" y="12" width="880" height="300" rx="13" fill="#f9faf6" stroke="#d3ded8"/>']
    palette=["#e2f0ec","#e7eef7","#fff0d9","#ebebf6","#e8f2e4"]
    labels=[v.strip() for v in record["text"].split(".") if v.strip()][:4]
    if len(labels)<4:
        labels+=["Check the contract","Find the failure","Explain the trade-off","Verify the example"][0:4-len(labels)]
    labels=[s[:80] for s in labels]
    parts.append(f'<text x="31" y="41" font-size="13" font-weight="bold" fill="#436d6d">{e(kind.upper())} · TEACHING PLATE</text>')
    if kind in ("timeline","swimlane"):
        # Time flows downward across participant lanes, not via unlabelled rectangles.
        for i,t in enumerate(labels):
            x=29+(i%2)*432;y=60+(i//2)*116
            parts.append(f'<rect x="{x}" y="{y}" width="409" height="100" rx="10" fill="{palette[i]}" stroke="#bbcfc7"/>')
            parts.append(f'<text x="{x+16}" y="{y+28}" font-size="12" font-weight="bold" fill="#30616d">STEP {i+1}</text>')
            for z,p in enumerate(_lines(t,48)[:2]):
                parts.append(f'<text x="{x+16}" y="{y+54+z*19}" font-size="13" fill="#233b3d">{e(p)}</text>')
        parts.append('<path d="M450 160V170 M450 278V291" stroke="#618a91" stroke-width="2" />')
    elif kind=="chart":
        parts.append('<path d="M80 63V265H842" stroke="#79908b" stroke-width="2" fill="none"/>')
        pts=[(120,245),(345,205),(555,188),(785,85)]
        parts.append('<polyline points="'+' '.join(f"{x},{y}" for x,y in pts)+'" fill="none" stroke="#347f8a" stroke-width="4"/>')
        for i,t in enumerate(labels):
            x=28+(i%2)*428;y=287+(i//2)*0
            if i<2:parts.append(f'<text x="{x}" y="{y}" font-size="12" fill="#344e4f">{e(t[:42])}</text>')
    elif kind in ("memory","topology","tree"):
        for i,t in enumerate(labels):
            x=34+(i%2)*428;y=63+(i//2)*110
            parts.append(f'<rect x="{x}" y="{y}" width="392" height="91" rx="9" fill="{palette[i]}" stroke="#9dbdb7"/>')
            parts.append(f'<text x="{x+14}" y="{y+26}" font-size="13" font-weight="bold" fill="#32646b">{"OWNER" if kind=="memory" else "PART"} {i+1}</text>')
            for z,p in enumerate(_lines(t,48)[:2]):parts.append(f'<text x="{x+14}" y="{y+51+z*17}" font-size="12" fill="#244042">{e(p)}</text>')
        if kind=="tree":parts.append('<path d="M230 156V166H655V173" stroke="#477f8c" stroke-width="2" fill="none"/>')
    else:
        for i,t in enumerate(labels):
            x=27+i*216
            parts.append(f'<rect x="{x}" y="78" width="202" height="164" rx="12" fill="{palette[i%5]}" stroke="#b4c9c2"/>')
            parts.append(f'<circle cx="{x+101}" cy="115" r="20" fill="#fffefa" stroke="#acc4bc"/>')
            parts.append(f'<text x="{x+101}" y="121" font-size="16" font-weight="bold" text-anchor="middle" fill="#376575">{i+1}</text>')
            for z,p in enumerate(_lines(t,21)[:4]):
                parts.append(f'<text x="{x+101}" y="{155+z*17}" text-anchor="middle" font-size="12" fill="#233b3d">{e(p)}</text>')
            if i<3:parts.append(f'<path d="M{x+203} 162H{x+215}" stroke="#618a91" stroke-width="2"/>')
    return shell(n,j,k,title,"".join(parts),
       "Read this example alongside the surrounding story: it is an explanatory model, not a measured system.",
       "Trace ownership, ordering, and the failure boundary described in the lesson.",height=327)
def _lines(value,limit):
    words=value.split(); out=[]; line=""
    for w in words:
        if len(line)+len(w)+1>limit and line:out.append(line);line=w
        else:line=(line+" "+w).strip()
    if line:out.append(line)
    return out
