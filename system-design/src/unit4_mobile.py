"""Compact, mechanism-specific compositions of the seventeen Unit 4 figures.

These preserve the desktop figure's claim while arranging it for a narrow page.
Coordinates are in a 360-unit viewBox; labels remain readable without panning.
"""
from html import escape
from math import atan2, cos, sin

BLUE = '#3978a8'
GREEN = '#26836b'
RED = '#b94b48'
AMBER = '#a96e21'


def text(x, y, value, size=16, anchor='middle', color='#203439'):
    lines = value.split('\n')
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}">' + ''.join(
        f'<tspan x="{x}" dy="{0 if i == 0 else 22}">{escape(line)}</tspan>'
        for i, line in enumerate(lines)) + '</text>'


def box(x, y, w, h, value, fill='#e8f3ed', stroke=GREEN):
    lines = value.count('\n') + 1
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}"/>'
            + text(x + w/2, y + h/2 + 5 - (lines-1)*11, value))


def arrow(x1, y1, x2, y2, color=BLUE, dashed=False):
    angle = atan2(y2-y1, x2-x1)
    points = [(x2, y2)] + [(x2-9*cos(angle+d), y2-9*sin(angle+d)) for d in (-.5,.5)]
    dash = ' stroke-dasharray="5 4"' if dashed else ''
    return (f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="2"{dash}/>'
            + f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in points)}" fill="{color}"/>')


def processes():
    s = box(70, 12, 220, 48, 'upload.py on disk', '#e8eef7', BLUE)
    s += arrow(180, 60, 180, 97) + text(210, 84, 'start twice', 15, 'start')
    s += box(12, 101, 336, 165, '', '#edf5f3')
    s += text(180, 128, 'PROCESS A · own address space')
    s += box(32, 145, 296, 42, 'Shared heap: document A')
    s += box(32, 202, 138, 48, 'Thread 1\nstack 1', '#e8eef7', BLUE)
    s += box(190, 202, 138, 48, 'Thread 2\nstack 2', '#e8eef7', BLUE)
    s += box(12, 288, 336, 142, '', '#fff2df', AMBER)
    s += text(180, 315, 'PROCESS B · own address space')
    s += box(32, 331, 296, 40, 'Own heap: document B', '#fff2df', AMBER)
    s += box(90, 385, 180, 32, 'Thread 3 · stack 3', '#e8eef7', BLUE)
    return s, 445


def memory():
    s = text(180, 28, 'ONE PROCESS ADDRESS SPACE')
    s += box(15, 48, 155, 113, 'Thread A stack\nhandle_upload()\nread_file()', '#e8eef7', BLUE)
    s += box(190, 48, 155, 113, 'Thread B stack\nconvert(file)\nread_buffer()', '#e8eef7', BLUE)
    s += arrow(92, 161, 135, 221, GREEN) + arrow(268, 161, 225, 221, GREEN)
    s += box(55, 225, 250, 78, 'SHARED HEAP\nUpload buffer: 12 KB')
    s += text(180, 338, 'Both threads reach the same object.')
    return s, 358


def scheduling():
    s = text(180, 27, 'ONE CORE · time flows down')
    s += arrow(29, 50, 29, 338)
    s += box(65, 50, 265, 62, 'A executes\nrequests storage read', '#e8eef7', BLUE)
    s += arrow(198, 112, 198, 155, AMBER) + text(215, 140, 'switch', 15, 'start')
    s += box(65, 160, 265, 62, 'B executes\nA is blocked on I/O')
    s += arrow(198, 222, 198, 265, AMBER) + text(215, 250, 'I/O ready', 15, 'start')
    s += box(65, 270, 265, 62, 'A resumes\nB no longer owns the core', '#e8eef7', BLUE)
    return s, 350


def cpu_wait():
    s = text(180, 28, 'ILLUSTRATIVE ELAPSED TIME')
    for y, title, cpu in [(72, 'Compress a file', 250), (186, 'Upload a file', 48)]:
        s += text(20, y, title, anchor='start')
        s += f'<rect x="20" y="{y+15}" width="320" height="44" fill="#fff2df"/>'
        s += f'<rect x="20" y="{y+15}" width="{cpu}" height="44" fill="#d9e4f4"/>'
        s += text(20, y+85, '0%', 15, 'start') + text(340, y+85, '100%', 15, 'end')
    s += text(180, 310, 'Blue = computing · amber = waiting')
    s += text(180, 343, 'The lengths are assumptions,\nnot measured performance.')
    return s, 385


def sync_async():
    s = text(180, 28, 'TIME FLOWS DOWN')
    for y, title in [(62, 'SYNCHRONOUS'), (245, 'ASYNCHRONOUS')]:
        s += text(180, y, title)
        s += text(70, y+30, 'Caller') + text(282, y+30, 'Storage')
        s += arrow(70, y+50, 282, y+50)
        s += arrow(282, y+124, 70, y+124, GREEN)
        s += text(180, y+153, 'reply' if y == 62 else 'later completion')
    s += box(18, 127, 222, 42, 'Caller waits', '#fff2df', AMBER)
    s += box(18, 310, 252, 42, 'Other ready work can run')
    return s, 420


def blocking():
    s = text(180, 28, 'READ WHEN NO BYTES ARE READY')
    s += box(20, 50, 320, 70, 'Blocking read\nthread stays inside the call', '#fff2df', AMBER)
    s += arrow(180, 120, 180, 162) + text(199, 148, 'bytes arrive', 15, 'start')
    s += box(20, 167, 320, 48, 'Call returns bytes')
    s += box(20, 250, 320, 70, 'Nonblocking read\nreturns “not ready”', '#e8eef7', BLUE)
    s += arrow(180, 320, 180, 362) + text(199, 348, 'readiness', 15, 'start')
    s += box(20, 367, 320, 70, 'Try the read again\nother work can run between tries')
    return s, 455


def concurrency():
    s = text(180, 28, 'TIME → · SAME TWO TASKS')
    s += text(20, 65, 'One core: interleaved execution', anchor='start')
    for i, v in enumerate(['A', 'B', 'A', 'B']):
        s += box(20+i*80, 85, 76, 58, v, '#e8eef7' if v=='A' else '#e8f3ed', BLUE if v=='A' else GREEN)
    s += text(20, 200, 'Two cores: execution overlaps', anchor='start')
    s += text(20, 240, 'Core 0', anchor='start') + box(100, 216, 240, 42, 'A', '#e8eef7', BLUE)
    s += text(20, 300, 'Core 1', anchor='start') + box(100, 276, 240, 42, 'B')
    return s, 342


def event_loop():
    s = text(180, 28, 'ONE EVENT-LOOP THREAD')
    s += box(50, 50, 260, 48, 'Ready tasks: A, B')
    s += arrow(180, 98, 180, 132)
    s += box(50, 137, 260, 62, 'Run A\nsubmit read; suspend A', '#e8eef7', BLUE)
    s += arrow(180, 199, 180, 233)
    s += box(50, 238, 260, 48, 'Run another ready task')
    s += arrow(180, 286, 180, 320)
    s += box(50, 325, 260, 62, 'I/O completion\nA becomes ready again', '#fff2df', AMBER)
    s += arrow(310, 354, 338, 354, GREEN) + arrow(338, 354, 338, 74, GREEN) + arrow(338, 74, 310, 74, GREEN)
    s += text(180, 423, 'A long callback delays all ready work.')
    return s, 445


def pool():
    s = text(180, 28, 'TWO WORKERS · THREE WAITING SLOTS')
    s += box(20, 55, 150, 62, 'Worker 1\nruns J1') + box(190, 55, 150, 62, 'Worker 2\nruns J2')
    s += text(180, 153, 'Waiting queue · full')
    for i, v in enumerate(['J3', 'J4', 'J5']):s += box(30+i*102, 175, 96, 48, v, '#e8eef7', BLUE)
    s += arrow(180, 223, 180, 265, RED)
    s += box(25, 270, 310, 76, 'J6 arrives\nreject or apply backpressure', '#fae2dc', RED)
    s += text(180, 384, '2 running + 3 waiting = 5 admitted')
    return s, 405


def messages():
    s = text(180, 28, 'SHARED MEMORY · ONE PROCESS')
    s += box(20, 50, 145, 48, 'Thread A', '#e8eef7', BLUE) + box(195, 50, 145, 48, 'Thread B', '#e8eef7', BLUE)
    s += arrow(92, 98, 145, 148) + arrow(268, 98, 215, 148)
    s += box(65, 153, 230, 48, 'Shared count = 0', '#fff2df', AMBER)
    s += text(180, 249, 'MESSAGE PASSING · ONE OWNER')
    s += box(20, 271, 145, 48, 'Worker A', '#e8eef7', BLUE) + box(195, 271, 145, 48, 'Worker B', '#e8eef7', BLUE)
    s += arrow(92, 319, 145, 384) + arrow(268, 319, 215, 384)
    s += text(180, 351, 'each sends “+1”')
    s += box(45, 389, 270, 70, 'Counter owner\nhandles messages one at a time')
    return s, 480


def lost_update():
    s = text(180, 28, 'TIME ↓ · initial count = 0')
    s += text(96, 65, 'Thread A') + text(264, 65, 'Thread B')
    for x, y, label, color in [(20,90,'reads 0',BLUE),(190,150,'reads 0',GREEN),(20,210,'computes 1',BLUE),(190,270,'computes 1',GREEN),(20,330,'stores 1',BLUE),(190,390,'stores 1',GREEN)]:
        s += box(x,y,150,44,label,'#e8eef7' if color==BLUE else '#e8f3ed',color)
    s += arrow(12, 80, 12, 445)
    s += box(40, 465, 280, 65, 'Final count = 1\ntwo increments should give 2', '#fae2dc', RED)
    return s, 550


def coordination():
    s = text(180, 28, 'CHOOSE THE REQUIRED GUARANTEE')
    for y, value, fill, stroke in [
        (52,'MUTEX · one owner\nA owns the lock; B waits','#e8eef7',BLUE),
        (153,'SEMAPHORE · two permits\ntwo tasks enter; the third waits','#e8f3ed',GREEN),
        (254,'ATOMIC UPDATE\nfetch_add(count, 1) is indivisible','#fff2df',AMBER),
        (355,'CONDITION VARIABLE\nwait; notify; recheck predicate','#f1ecf7','#7b65a8')]:
        s += box(15,y,330,77,value,fill,stroke)
    return s, 452


def deadlock():
    s = text(180, 28, 'OWNERSHIP + WAITING = A CYCLE')
    s += box(15, 55, 145, 55, 'Thread A', '#e8eef7', BLUE)
    s += box(200, 55, 145, 55, 'Lock X\nfile', '#fff2df', AMBER)
    s += box(15, 242, 145, 55, 'Lock Y\ncounter', '#fff2df', AMBER)
    s += box(200, 242, 145, 55, 'Thread B', '#e8eef7', BLUE)
    s += arrow(200,82,160,82,GREEN) + text(180,65,'held by',15)
    s += arrow(160,269,200,269,GREEN) + text(180,252,'held by',15)
    s += arrow(87,110,87,242,RED,True) + text(92,172,'waits for',15,'start',RED)
    s += arrow(272,242,272,110,RED,True) + text(265,205,'waits for',15,'end',RED)
    s += text(180,340,'A → Y → B → X → A',color=RED)
    s += text(180,375,'Neither thread releases its first lock.')
    return s, 397


def visibility():
    s = text(180, 28, 'TIME ↓ · SAME SYNCHRONIZATION OBJECT')
    s += box(20, 52, 320, 63, 'Writer\nwrite result = “done”', '#e8eef7', BLUE)
    s += arrow(180,115,180,149)
    s += box(20,154,320,52,'Writer releases mutex')
    s += arrow(180,206,180,272,GREEN) + text(194,245,'synchronizes',15,'start',GREEN)
    s += box(20,277,320,52,'Reader acquires same mutex')
    s += arrow(180,329,180,363)
    s += box(20,368,320,63,'Reader\nobserve result = “done”','#e8eef7',BLUE)
    s += text(180,466,'Write happens before the protected read.')
    return s, 487


def immutable():
    s = text(180,28,'IMMUTABLE, SAFELY PUBLISHED RESULT')
    s += box(50,52,260,50,'pages = (1, 2, 3)')
    s += arrow(130,102,92,151,GREEN) + arrow(230,102,268,151,GREEN)
    s += box(20,156,145,45,'Reader A') + box(195,156,145,45,'Reader B')
    s += text(180,250,'MUTABLE SHARED COUNTER')
    s += box(50,274,260,50,'count = 0','#fff2df',AMBER)
    s += arrow(180,324,180,363,AMBER)
    s += box(20,368,320,70,'Guard every access with a protocol:\nmutex or suitable atomic operations','#fae2dc',RED)
    return s,458


def backpressure():
    s = text(180,28,'ARRIVE 150/s · FINISH 100/s')
    s += text(180,57,'Without a limit: +50 waiting jobs/s')
    s += arrow(45,265,45,85) + arrow(45,265,330,265)
    s += text(22,84,'jobs',15,'start') + text(330,290,'seconds',15,'end')
    for x,v in [(45,'0'),(112,'0.5'),(180,'1'),(247,'1.5'),(315,'2')]:s += text(x,286,v,15)
    for y,v in [(265,'0'),(224,'25'),(183,'50'),(141,'75'),(100,'100')]:s += text(32,y+5,v,15,'end')
    s += '<path d="M45 265L315 100" fill="none" stroke="#a96e21" stroke-width="3"/>'
    s += '<path d="M45 100H330" stroke="#b94b48" stroke-width="2" stroke-dasharray="5 4"/>'
    s += text(195,93,'capacity = 100',15,color=RED)
    s += box(20,320,320,83,'At capacity: reject or defer input\na bound limits waiting memory;\nit does not speed up the workers','#fff2df',AMBER)
    return s,423


def cancellation():
    s = box(70,15,220,55,'Parent upload request','#e8eef7',BLUE)
    s += text(180,104,'cancel request ↓',color=RED)
    for y,label,fill,stroke in [(138,'Metadata: cancel + cleanup','#e8f3ed',GREEN),(222,'Preview: cancel + cleanup','#e8f3ed',GREEN),(306,'Upload: effect may exist','#fff2df',AMBER)]:
        s += arrow(26,70,26,y+26,RED,True) + arrow(26,y+26,55,y+26,RED,True)
        s += box(55,y,290,55,label,fill,stroke)
    s += text(180,403,'Scope waits for children to finish cleanup.')
    s += box(15,430,330,60,'Stopping a task does not undo\nan already committed external effect.','#fae2dc',RED)
    return s,510


DRAWINGS = {
    1: (processes, memory, scheduling, cpu_wait, sync_async),
    2: (blocking, concurrency, event_loop, pool),
    3: (messages, lost_update, coordination, deadlock),
    4: (visibility, immutable, backpressure, cancellation),
}


def drawing(chapter, index):
    return DRAWINGS[chapter][index]()
