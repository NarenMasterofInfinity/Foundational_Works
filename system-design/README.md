# The System Design Atlas

**From Objects to Planet-Scale Systems** — a staged, illustrated textbook in the existing Learn · Research · Visualise design language.

Open [the digital edition](index.html) or [the foundations PDF](System-Design-Atlas-Foundations.pdf).

## Current scope

The entire supplied syllabus is allocated to **22 units and 99 chapters**, with 390 exact topic items, unit/chapter prerequisites, illustration commissions, starting references, and all 12 mandatory case studies. Each case study has the complete 22-section review protocol. The original request is retained in [BRIEF.txt](BRIEF.txt).

**Unit 1 is produced:** four substantive chapters follow one to-do application through state, contracts, module boundaries, requirements, ADRs, C4, request ordering, and deployment. They include 16 original SVG teaching figures, four interactive workbenches, executable Python, five conceptual questions, three scenarios, one design challenge, one implementation exercise, one thought experiment, and separate explained solutions.

**Units 2–22 are planned.** Their pages are explicitly labeled editorial outlines. They are not counted as finished lessons, worked case studies, or completed assessments. See the [hierarchical blueprint](BLUEPRINT.md) and [machine-readable manifest](completion-manifest.json).

## Reader experience

- Warm paper, serif display typography, teal navigation, restrained semantic diagram colors, and original vectors match the Retrieval Atlas.
- The HTML embeds its CSS, JavaScript, content, search index, and illustrations. It reads offline, through `file://`, or under a repository subpath with no installation or external fonts.
- All lesson text remains available without JavaScript. JavaScript adds navigation, global concept search, glossary/source filtering, workbenches, and optional browser-local read marks.
- Workbenches model acknowledgment/crash ordering, change propagation, weighted design preferences, and C4 views. Assumptions and limitations are visible; no invented performance measurements are used.
- Reference desks include a concept map, reading paths, glossary, formula reference, diagram index, pattern destinations, source bibliography, and completion manifest.
- Printing includes the produced chapters, explained assessment, and reference desks. Planned chapter bodies are excluded. The PDF is a **foundations installment**, not the complete future textbook.

## Build and verify

Build with Python’s standard library:

```bash
python3 system-design/src/build.py
python3 system-design/src/verify_example.py
```

The builder regenerates `index.html`, `BLUEPRINT.md`, and `completion-manifest.json`. It validates exact topic allocation, prerequisites, internal links, unique IDs, assessment counts, and case-study requirements. The example verification tests invalid input, storage errors, completion, reopening, and abrupt process termination before/after commit.

Browser verification uses Node 22+ and a dedicated Chrome debugging session; no npm packages are needed:

```bash
google-chrome --headless=new --no-sandbox --disable-gpu \
  --disable-dev-shm-usage --disable-background-networking \
  --no-first-run --no-default-browser-check \
  --remote-debugging-port=0 \
  --user-data-dir=/tmp/system-design-atlas-chrome about:blank

node system-design/src/verify_browser.mjs \
  "$PWD" /tmp/system-design-atlas-chrome/DevToolsActivePort
```

The browser script verifies all 133 views at five widths, tests workbench behavior and edge conditions, checks deep links and saved read marks, verifies JavaScript-disabled reading and no external reading requests, tests library search, and regenerates the foundations PDF. It writes review screenshots to `/tmp/system-design-atlas-qa`. Chrome may require the environment’s normal approval for local socket access.

See [QA.md](QA.md) and [SOURCE_REVIEW.md](SOURCE_REVIEW.md) for verification boundaries and source review.

## Continue production

1. Select the next dependency-ready chapter in the manifest; Unit 2 is the next coherent unit.
2. Produce the full teaching chapter and original figures, not only a summary of its topic list.
3. Verify primary sources and precise implementation versions; update source status without implying that a checked link proves a future claim.
4. Add its assessment and separate reasoning-based solutions.
5. Update the chapter production registry and indexes, rebuild, and rerun checks appropriate to the changes.

The current builder intentionally recognizes only Unit 1 as produced. Future work must extend production data and content before changing those statuses. Do not mark the rest complete by relabeling the existing outlines.
