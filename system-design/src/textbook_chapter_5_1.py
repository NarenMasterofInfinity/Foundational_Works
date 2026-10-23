"""Original teaching additions and purpose-specific plates for 5.1."""
from html import escape as e
from atlas_figures import shell
INTRO="A small payments class initially validates an amount, calculates fees, calls a gateway, writes a receipt and sends email. It works until each business rule changes at a different pace."
LESSONS=[{"title":"An object should have a clear job","text":"Abstraction exposes the useful behavior while hiding irrelevant detail. Encapsulation protects an object's state through controlled operations. Polymorphism lets distinct implementations honor one contract. Inheritance can share behavior through a subtype relation, but not every reuse need justifies that relationship. Draw each operation against a payment example and show what the caller must know.","visual":"swimlane"},{"title":"Prefer a useful part to a fragile family tree","text":"If a payment service *has a* gateway, composition expresses collaboration: the service receives a gateway interface and calls it. Inheritance says one class *is a* specialized kind of another, which can constrain behavior and couple changes. A refund policy does not naturally have to inherit an entire payment gateway. Side-by-side class diagrams make this distinction visible.","visual":"topology"},{"title":"A function name is not enough","text":"The contract for charge(amount, currency, idempotency_key) must state units, validation, failure modes, and whether a successful result is durable. A caller should not guess whether amount=100 means cents or rupees. Interface contracts support substitution only when implementations honor the same observable expectations. Sketch valid, invalid, and uncertain outcomes.","visual":"comparison"},{"title":"Keep one reason for change together","text":"Cohesion asks whether a module's responsibilities belong together; coupling asks how much one module needs to know about another. A class that queries SQL columns, sends SMS, and computes tax changes for unrelated reasons. Split data access, communication, and business policy along useful seams—without creating one-class-per-line overengineering.","visual":"timeline"},{"title":"Use SOLID as questions, not commandments","text":"Single responsibility asks whether changes have one coherent reason. Open/closed encourages extension without rewriting stable rules; Liskov substitution protects contracts; interface segregation avoids forcing irrelevant operations; dependency inversion points high-level policy toward suitable abstractions. These principles can conflict with simplicity if applied mechanically. Test them against one realistic change: adding a second payment provider without modifying fee policy.","visual":"matrix"}]


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
