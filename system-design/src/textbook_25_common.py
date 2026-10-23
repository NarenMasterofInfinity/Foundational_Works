"""Textbook teaching plate renderer: topic-directed forms, no external dependencies."""
from html import escape as E
from atlas_figures import shell

FORMS=("sequence","contrast","state","timeline","boundary","ladder","decision","ledger","lifecycle","tree")
def lines(s,limit=25):
    words=s.split();res=[];part=""
    for word in words:
        if part and len(part)+len(word)+1>limit:res.append(part);part=word
        else:part=(part+" "+word).strip()
    if part:res.append(part)
    return res
def t(x,y,s,sz=13,col="#243f42",anchor="start",weight="normal"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{sz}" font-weight="{weight}" fill="{col}">{E(s)}</text>'
def rect(x,y,w,h,fill,stroke="#adc5bf"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="{stroke}"/>'
def plate(n,j,k,heading,objects,form=None):
    form=form or FORMS[(n*7+j*3+k)%len(FORMS)]
    objects=list(objects)[:4]
    while len(objects)<4:objects.append("Check the assumptions")
    palette=("#e8f3ed","#e8eef7","#fff2df","#f1ecf7")
    svg=rect(12,12,876,298,"#fafbf7","#d6e1db")
    svg+=t(32,43,f"{form.upper()}  /  {heading[:72]}",14,"#386772",weight="bold")
    if form in ("sequence","timeline"):
        # Explicit time axis, individual rows and actor marks.
        svg+='<path d="M65 77V265" stroke="#597f86" stroke-width="2"/>'
        for a,v in enumerate(objects):
            y=76+a*52
            svg+=f'<circle cx="65" cy="{y+19}" r="6" fill="#43848e"/>'
            svg+=rect(94,y,733,41,palette[a])
            svg+=t(113,y+25,f"{a+1}. {v[:86]}",14)
    elif form in ("state","lifecycle"):
        for a,v in enumerate(objects):
            x=30+(a%2)*438;y=73+(a//2)*108
            svg+=rect(x,y,414,89,palette[a])
            svg+=t(x+17,y+25,("STATE " if form=="state" else "STAGE ")+str(a+1),11,"#55777d",weight="bold")
            for z,ln in enumerate(lines(v,43)[:2]):svg+=t(x+17,y+49+18*z,ln,13)
        svg+='<path d="M444 120H458M444 229H458" stroke="#46808c" stroke-width="2"/>'
    elif form=="tree":
        svg+=rect(335,71,230,64,palette[0])+t(450,107,objects[0][:25],14,anchor="middle",weight="bold")
        for a,v in enumerate(objects[1:]):
            x=39+a*286
            svg+=f'<path d="M450 135L{x+126} 200" stroke="#46808c" stroke-width="2"/>'
            svg+=rect(x,200,251,70,palette[a+1])
            for z,ln in enumerate(lines(v,27)[:2]):svg+=t(x+125,230+17*z,ln,12,anchor="middle")
    elif form=="ladder":
        for a,v in enumerate(objects):
            x=45+a*197;y=216-a*40
            svg+=rect(x,y,185,65,palette[a])
            for z,ln in enumerate(lines(v,20)[:2]):svg+=t(x+92,y+28+16*z,ln,12,anchor="middle")
    elif form=="ledger":
        for a,v in enumerate(objects):
            x=43+(a%2)*422;y=78+(a//2)*99
            svg+=rect(x,y,395,82,palette[a])
            svg+=t(x+17,y+24,f"OBSERVATION {a+1}",11,"#53777c",weight="bold")
            for z,ln in enumerate(lines(v,44)[:2]):svg+=t(x+17,y+47+18*z,ln,12)
    else:
        for a,v in enumerate(objects):
            x=32+a*215
            svg+=rect(x,83,197,173,palette[a])
            svg+=t(x+98,119,str(a+1),23,"#497784",anchor="middle",weight="bold")
            for z,ln in enumerate(lines(v,23)[:4]):svg+=t(x+98,156+18*z,ln,12,anchor="middle")
    svg+=t(450,292,"Illustrative teaching model; use the written assumptions and failure contract.",11,"#71837e",anchor="middle")
    return shell(n,j,k,heading,svg,"A teaching illustration of the stated example; values and guarantees are defined in the adjacent text.","Read the diagram's meaning and its limits.",height=324)
