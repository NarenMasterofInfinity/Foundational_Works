"""Unit 2, Chapter 2.1: original, illustrated textbook revision.

Keep syllabus IDs and the book's existing figure registry stable. This module
changes the *teaching*, not the promised scope of the complete edition.
All named people and workload numbers are invented educational examples.
"""
from html import escape

# Each topic is taught as a story first; the figure supplies a different visual
# grammar for the specific concept rather than recycling four-box snapshots.
CHAPTER_2_1 = {
    1: {
        "heading": "Begin with a promise, not a server",
        "prose": """Imagine a school wants a new social app. Mira can post photographs and see what her friends share. The school tells us that ten million people might use it each day. Does that mean we should immediately draw ten servers? No. We still do not know what the servers must do. How often will students post? Who may see private photographs? What does the word *posted* promise? A design made before these questions are answered may solve the wrong problem.

**A requirement is a promise we can check.** “The feed must be fast” is a wish, not a clear test. We could instead propose: “When an authorized student publishes a valid post and receives success, the post remains stored across an application restart, and permitted followers can see it within five seconds during normal operation.” The five-second target is an **assumption for this lesson**, not a universal standard. The product team must agree to it.

Notice that this sentence contains several different promises: an authorized student, valid input, an acknowledged save, survival after restart, permitted readers, and a visibility deadline. Each needs its own test. **Functional requirements** say what users can do, such as publishing or deleting a post. **Quality and constraint requirements** say how correctly, quickly, securely, or dependably it must happen. Some requirements, especially security, span both categories. We should record priorities, exclusions, open questions, and the reason for every important assumption.

**Check your understanding:** If the post appears in one second but disappears when the application restarts, which promise did we break? We kept the visibility target but broke the saved-data promise. These are separate properties; a single adjective like “reliable” hides the distinction.""",
        "trace": ["Vague request: make it fast", "Specify action, outcome and conditions", "Propose measurable promise", "Confirm target and test it"],
    },
    2: {
        "heading": "Walk beside the user",
        "prose": """Mira opens the app, scrolls through her feed, opens a photograph, and taps Like. To her, these are a few simple actions. To the system, they can produce many separate requests and storage operations. A **user journey** follows a person's intention through to the result they expect. A **workload** describes the operations that journeys create, including their frequency, size, and cost.

Assume that opening the feed sends **one API request** for a page of posts, downloads **twenty image objects**, and sends **one optional analytics event**. In this simplified example, that is twenty-two requests associated with one feed opening. The actual number may be smaller: images can be cached, multiple items can be batched, and analytics may be disabled. The point is not to memorize twenty-two. It is to draw the journey, then count real operations at a clearly defined boundary.

Follow the illustrated swimlanes from top to bottom. The feed API looks up post metadata; image transfers can begin afterward and may run concurrently; analytics is independent of showing the feed. Do not add together overlapping durations as though every step runs sequentially. Different operations stress different resources. Sending an image may cost mostly bandwidth, while recommending posts may cost more CPU or database work.

**Try it:** If the browser already has ten of the twenty images in its cache, how many image fetches remain? Ten, assuming no other cache or batch effects. What changes if the analytics event is not sent? One fewer request in this teaching example. Record both assumptions before choosing a capacity estimate.""",
        "trace": ["One feed opening", "One post-list request", "20 assumed image fetches", "One optional analytics event"],
    },
    3: {
        "heading": "Count reads and writes at the right boundary",
        "prose": """Suppose that for every post students publish, they open ten feeds. Looking only at public actions, we could call the app **read-heavy**: ten feed opens for one publish. But watch what happens inside one possible implementation. Publishing writes the post once, then places a post reference into a thousand followers' prepared feed lists. The one publishing action has caused roughly **1,001 storage writes**, before counting indexes, replication, or other side effects.

This spreading of work from one event to many destinations is called **fan-out**. With *fan-out on write*, the system prepares follower feeds while publishing. With *fan-out on read*, the system gathers posts when someone opens a feed. Neither removes all the work; the choice shifts when and where the work happens. A popular author with a million followers is not like an author with ten followers. We need to understand the distribution, not only an average.

There is no contradiction between “the product is read-heavy” and “publishing creates many writes.” They count different things. Always label your boundary: **user actions, API calls, database queries, or storage writes**. Without that label, an impressive read/write ratio can be misleading. A read replica may reduce some read pressure but could temporarily show older information; it does not automatically solve write fan-out.

**Question:** If an author has zero followers, will the system still store the post? In our assumed design, yes: the primary post write remains. If an author has one thousand followers, a prepared-feed design may issue an additional thousand feed updates. Treat these counts as model inputs to test, not evidence about any real social platform.""",
        "trace": ["User actions: 10 reads / 1 publish", "Publish creates 1 primary write", "Prepared feeds: 1000 additional writes", "Count each system boundary separately"],
    },
}


def _svg(label, x, y, size=15, color="#233a3b", anchor=None, weight=None):
    attrs = f' x="{x}" y="{y}" font-size="{size}" fill="{color}"'
    if anchor:
        attrs += f' text-anchor="{anchor}"'
    if weight:
        attrs += f' font-weight="{weight}"'
    return f'<text{attrs}>{escape(label)}</text>'


def _rect(x, y, w, h, fill, stroke="none", radius=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def _path(d, color="#377a88", width=2, dash=None):
    attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{attr}/>'


def unit2_figure(n, chapter, sequence, topic):
    """One original, intentionally different visual grammar per teaching question."""
    if (n, chapter) != (2, 1):
        return None
    from atlas_figures import shell
    if topic == 1:
        # Editorial transformation plate: before/question/after, not a server map.
        body = _rect(26, 60, 220, 194, "#fff0e6", "#d7a279")
        body += _svg("THE BRIEF", 44, 88, 12, "#94562d", weight="bold")
        body += _svg("Make our", 48, 141, 24, "#483528", weight="bold")
        body += _svg("app fast!", 48, 172, 24, "#483528", weight="bold")
        body += _svg("No measurable test", 44, 219, 14, "#94562d")
        body += _path("M257 156 H305", "#a76e37", 3)
        body += _rect(310, 60, 238, 194, "#eef5f6", "#93b9c2")
        body += _svg("ASK THREE QUESTIONS", 326, 88, 12, "#306a76", weight="bold")
        for i, line in enumerate(["1  What action?", "2  What outcome?", "3  Under what conditions?"]):
            body += _svg(line, 326, 132 + i * 39, 16)
        body += _path("M560 156 H603", "#377a88", 3)
        body += _rect(609, 60, 263, 194, "#e8f4e9", "#89b495")
        body += _svg("A TESTABLE PROMISE", 625, 88, 12, "#28784c", weight="bold")
        for i, line in enumerate(["✓  Authorized publisher", "✓  Accepted post survives", "    application restart", "✓  Permitted readers see it", "    within 5 s in normal use"]):
            body += _svg(line, 625, 122 + i * 25, 14)
        body += _svg("5 seconds is an assumption to agree on.", 450, 293, 14, "#687276", "middle")
        title = "A vague request becomes a testable promise"
        caption = "A real design begins by naming the action, outcome, and conditions. The time target is illustrative."
        height = 318
    elif topic == 2:
        # Swimlanes: time moves downward and overlapping image transfers are explicit.
        body = _rect(20, 48, 860, 333, "#f8f9f7", "#d5dfdd")
        cols = [(27, 167, "MIRA / PHONE"), (199, 167, "FEED API"), (371, 167, "POST STORE"), (543, 167, "IMAGE DELIVERY"), (715, 155, "ANALYTICS")]
        for x, w, label in cols:
            body += _rect(x, 58, w, 40, "#e4eeee", radius=5)
            body += _svg(label, x + w / 2, 82, 11, "#325e67", "middle", "bold")
            body += _path(f"M{x+w/2} 103 V365", "#c6d6d5", 1, "4 5")
        body += _svg("time ↓", 29, 120, 12, "#6b7979")
        body += _path("M112 133 H285", "#397f99", 2)
        body += _svg("GET feed", 198, 126, 12, "#397f99", "middle")
        body += _path("M285 163 H457", "#397f99", 2)
        body += _svg("read posts", 371, 156, 12, "#397f99", "middle")
        body += _path("M457 191 H285", "#258068", 2)
        body += _path("M285 220 H112", "#258068", 2)
        body += _svg("list returned", 198, 210, 12, "#258068", "middle")
        body += _rect(549, 239, 158, 72, "#f6ebd6", "#cba560", 9)
        body += _svg("20 image requests", 628, 261, 13, "#80591e", "middle", "bold")
        body += _svg("can overlap", 628, 284, 12, "#80591e", "middle")
        body += _path("M112 255 H550", "#c79548", 2)
        body += _path("M112 338 H790", "#8a86b7", 1.7, "6 4")
        body += _svg("optional event", 424, 331, 12, "#78729a", "middle")
        body += _svg("One user action ≠ one network request", 449, 407, 17, "#30555b", "middle", "bold")
        title = "One feed opening creates several kinds of work"
        caption = "The illustrated one-feed, twenty-image, one-event workload is assumed. Some transfers may overlap or be cached."
        height = 433
    elif topic == 3:
        # Asymmetric fan-out: a single operation becomes many updates.
        body = _rect(20, 43, 548, 282, "#ecf5ed", "#a3c7aa")
        body += _svg("FAN-OUT ON WRITE", 39, 73, 13, "#28784c", weight="bold")
        body += _rect(40, 100, 143, 56, "white", "#56927c")
        body += _svg("1 publish", 112, 132, 17, "#2d5f55", "middle", "bold")
        body += _path("M183 128 H224", "#377a88", 2.5)
        body += _rect(226, 100, 150, 56, "white", "#56927c")
        body += _svg("Store 1 post", 301, 132, 16, "#2d5f55", "middle", "bold")
        body += _path("M301 156 V188 H390 V209", "#b78635", 3)
        body += _rect(205, 210, 337, 91, "#fffbf2", "#d8b778")
        for i in range(30):
            x=223+(i%10)*30; y=226+(i//10)*17
            body += _rect(x,y,19,10, "#a8d0b0", radius=2)
        body += _svg("1,000 follower-feed writes (illustrative)", 375, 291, 12, "#7d5b26", "middle", "bold")
        body += _rect(587, 43, 295, 282, "#f0f1f9", "#babcd8")
        body += _svg("FAN-OUT ON READ", 603, 73, 13, "#615d91", weight="bold")
        body += _rect(606, 111, 111, 58, "white", "#918bb9")
        body += _svg("Open feed", 661, 145, 15, "#625f8c", "middle")
        body += _path("M717 140 H749", "#918bb9", 2.5)
        body += _rect(752, 111, 110, 58, "white", "#918bb9")
        body += _svg("Find posts", 807, 145, 15, "#625f8c", "middle")
        body += _svg("More work when", 604, 231, 16, "#4d4f72")
        body += _svg("someone reads.", 604, 253, 16, "#4d4f72")
        body += _svg("Same feature. Different place to do the work.", 449, 357, 16, "#365256", "middle", "bold")
        title = "One publish can create a thousand storage writes"
        caption = "Precomputed feeds move work to publishing; on-demand feeds move more work to reading. Neither is free."
        height=382
    elif topic == 0 and sequence == 4:
        # Ledger/measurement worksheet; highlights the boundary of every claim.
        body = _svg("THE BOUNDARY CHANGES THE ANSWER", 32, 64, 17, "#37595f", weight="bold")
        headings = ["WHAT WE COUNT", "ILLUSTRATIVE RESULT", "WHAT IT DOES NOT TELL US"]
        widths = [230, 250, 346]; xs = [27, 257, 507]
        for x, w, label in zip(xs, widths, headings):
            body += _rect(x, 85, w, 46, "#dfebeb", "#c3d4d2", 4)
            body += _svg(label, x+10, 112, 12, "#315963", weight="bold")
        entries = [
            ["User actions", "10 feed opens : 1 publish", "Not database read/write ratio"],
            ["One publish", "1 post + 1,000 feed updates", "Not average across all authors"],
            ["20 image objects", "Up to 20 fetches on a cold view", "Not a guarantee: caching matters"],
        ]
        for i, entry in enumerate(entries):
            y=135+i*57
            for x,w,val in zip(xs,widths,entry):
                body += _rect(x,y,w,53, "#fffefa" if i%2==0 else "#f5f8f5", "#d5dfd8", 3)
                body += _svg(val,x+10,y+31,12,"#2d4547")
        body += _svg("Write assumptions down; replace them with observations.", 444, 338, 15, "#47765f", "middle", "bold")
        title="An estimate is meaningful only with its boundary"
        caption="The ledger prevents a public API ratio from being mistaken for storage work and distinguishes assumptions from measurements."
        height=363
    else:
        return None
    return shell(n, chapter, sequence, title, body, caption,
                 "Choose a visual that explains this concept rather than a generic sequence of boxes.",
                 height=height)
