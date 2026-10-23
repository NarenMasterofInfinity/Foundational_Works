"""Original teaching additions and purpose-specific plates for 3.4."""
from html import escape as e
from atlas_figures import shell
INTRO="The library works on one machine. Now place the browser on a mobile network and the service in a cloud region: names change, addresses are translated, caches can be stale, and every call can be delayed or lost."
LESSONS=[{"title":"A guarded entrance and a translated address","text":"A home router may translate several private addresses onto a public-facing address using NAT. A firewall decides which traffic is permitted under configured rules. Ingress describes traffic entering a selected boundary; egress describes traffic leaving it. Trace a response back through the same mapping rather than assuming the private machine is directly reachable from the internet. NAT is not a substitute for application authorization.","visual":"swimlane"},{"title":"Find a service even when its machines change","text":"If a worker is replaced, its IP address may change. Service discovery maps a stable name or logical service identity to eligible endpoints. Suppose checkout workers register as healthy but one becomes slow: discovery and load balancing need health policy and removal latency, not just a static list. The resolver's answer can lag behind reality, so clients need reasonable timeouts and retries.","visual":"topology"},{"title":"Keep popular pages near the reader","text":"A content delivery network caches eligible content at distributed edge locations. A library logo or public cover image may be cached near students, reducing trips to the origin. Personal borrowing details must not be placed into a shared public cache by accident. The diagram distinguishes cache hit, cache miss, and origin fetch; it is not a claim that every edge location stores every object.","visual":"comparison"},{"title":"Silence after a timeout does not tell the whole story","text":"A request may be lost before reaching the server, or the server may commit the change and lose only its response. Both appear as a timeout to the caller. Blindly retrying a payment or checkout could repeat an effect. Add a stable operation ID and an appropriate idempotency contract where repeated effects matter. A network partition can leave both sides alive but unable to communicate; heartbeat failure alone cannot prove a remote process is dead.","visual":"timeline"},{"title":"Reuse expensive connections responsibly","text":"A connection pool keeps a bounded set of reusable database or HTTP connections. Borrowing one avoids repeated setup but a pool with ten slots cannot run fifty simultaneous blocking queries; the others wait or fail according to policy. Draw the borrowing queue and return path. A leaked connection eventually empties the pool, while unbounded opening may overwhelm the server. Always release resources on success, error and cancellation.","visual":"matrix"}]


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
