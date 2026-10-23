"""Original teaching additions and purpose-specific plates for 3.3."""
from html import escape as e
from atlas_figures import shell
INTRO="Imagine the school library website serving ten thousand readers on examination day. The same request may pass through a proxy, a load balancer and an API gateway. They are not interchangeable: each exists to solve a different problem."
LESSONS=[{"title":"Who is the proxy speaking for?","text":"A forward proxy sits on the caller's side: a school network might use one to control which sites its computers reach. A reverse proxy sits at the service's entrance: browsers call the library's public address and it forwards to internal servers. The diagram labels both trust boundaries. Neither position alone tells you whether traffic is encrypted end-to-end; inspect where TLS is terminated. Ask who configured the proxy and whose address the caller sees.","visual":"swimlane"},{"title":"One entrance, many jobs","text":"A load balancer chooses a healthy backend from a pool. An API gateway can additionally check credentials, enforce quotas or route API methods. One product can implement both roles, but the responsibilities remain different. Suppose three servers can handle 100 requests per second each: distributing 250 evenly might work in a simplified healthy case, but a failed instance leaves only 200 requests per second of assumed capacity. The gateway cannot manufacture backend capacity.","visual":"topology"},{"title":"Which layer makes the routing decision?","text":"Layer 4 routing observes transport-level endpoints such as addresses and ports; Layer 7 routing can examine HTTP paths or headers after appropriate protocol processing. A diagram comparing port 443 to route /books makes the distinction visible. L7 features require more protocol work and, for HTTPS content, suitable TLS termination or another permitted inspection arrangement. Do not claim every L4 device is protocol-blind or that L7 always performs user authentication.","visual":"comparison"},{"title":"How does a page learn about new books?","text":"Polling asks the server periodically: 'Any new books?' Server-Sent Events keep an HTTP response open so the server can send one-way updates. WebSockets support two-way messaging over an established connection. Each has a different failure/reconnection story. A book-availability banner usually needs server-to-browser updates, while a multiplayer drawing board needs both directions. Draw the messages on a timeline; choosing a persistent connection does not automatically guarantee delivery after reconnection.","visual":"timeline"}]


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
