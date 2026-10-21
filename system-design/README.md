# The System Design Atlas

**From Objects to Planet-Scale Systems** — the complete first edition in the Learn · Research · Visualise design language.

Open [the digital edition](index.html) or download [the complete PDF](System-Design-Atlas-Complete.pdf) (1,012 tagged A4 pages, approximately 13 MB). The earlier [foundations PDF](System-Design-Atlas-Foundations.pdf) is retained as a separately scoped historical installment.

## What is included

- All **22 units and 99 chapters**, covering all **390 exact supplied syllabus items**.
- **50,392 words of authored lesson, pattern, and case-study prose**, excluding the separate solutions and much of the reader/reference material.
- **575 original SVG figures**, including at least four per chapter and all 94 required unit illustration assignments. Four Unit 1 assignments refer to its existing chapter figures; 90 additional unit plates cover the other required visual vocabulary. The master concept map is separately numbered M.1.
- All **12 mandatory end-to-end designs**, each with all **22 required review sections**, explicit assumptions, APIs, logical schemas, LLD, HLD, flows, calculations, failures, security, deployment, observability, costs, alternatives, evolution, review, and an implementation challenge.
- **242 questions and 242 separate explained answers**: five conceptual, three scenarios, one design/debugging challenge, one implementation exercise, and one advanced thought experiment for every unit.
- **26 individual LLD pattern treatments**, including miniature pseudocode, intent, collaborator roles, use, cost, and distinctions from related patterns.
- **13 browser-local workbenches**: acknowledgment/crash ordering, change propagation, weighted design preferences, C4 views, capacity, bounded queues, last-seat claims, LRU, rendezvous assignment, pipeline fencing, quorum intersection, token bucket, and cost per useful outcome.
- A **441-entry glossary and concept reference**, complete contents, dependency-closed reading paths, formula reference, pattern destinations, diagram index, and **61 selected production sources**.

Unit 1 has been revised to introduce each idea through the to-do application before naming it. The four chapters use shorter paragraphs, worked sequences, and optional sections for extra detail; their figures, workbenches, questions, and answers use the same approach. Units 2–22 retain their existing text.

The content-driven [manifest](completion-manifest.json) records actual produced artifacts and review boundaries. The [book blueprint](BLUEPRINT.md) retains stable chapter IDs and exact topic allocation. The original request remains in [BRIEF.txt](BRIEF.txt).

## Reading and visual design

Warm paper, serif display typography, teal navigation, semantic diagram colors, and generous spacing continue the Retrieval Atlas design language. Diagrams distinguish numbered snapshots, ordered actions, dependencies, boundaries, and acknowledgments where applicable; a snapshot card does not imply an independent process or a network call.

The HTML embeds its CSS, JavaScript, text, search index, and vectors. It works through `file://`, a local server, or GitHub Pages under a repository subpath without installation, external fonts, or runtime network calls. JavaScript adds navigation, search, interactive models, and optional browser-local read marks. All chapters remain readable without JavaScript.

Workloads, latency budgets, capacity inputs, and cost rates are **illustrative assumptions**, not company benchmarks or claims about real infrastructure. Local executable models demonstrate specific mechanisms and failure boundaries; they are not production consensus, authentication, accounting, or payment-provider integrations. See [SOURCE_REVIEW.md](SOURCE_REVIEW.md) for the technical distinctions and [QA.md](QA.md) for verification evidence.

## Build

Python's standard library is sufficient:

```bash
python3 system-design/src/build.py
python3 system-design/src/verify_example.py
python3 system-design/src/verify_mechanisms.py
```

The builder produces `index.html`, `BLUEPRINT.md`, and `completion-manifest.json`, validating actual content, exact topic allocation, chapter figures, all case sections, assessment counts, unique IDs, anchors, and prerequisite order. Production status follows authored lessons and figures through `src/edition.py`; it is not inferred from a topic checklist alone.

The teaching content lives in `src/teaching/`, separated into foundations, LLD, data, distributed systems, production, cases, patterns, assessment, sources, and miniature implementations. Existing Unit 1 HTML and workbench controls retain stable links. Required unit plates are implemented in `src/essential_plates.py` and subject-specific graphics in `src/atlas_figures.py`.

## Browser verification and PDF

Use Node 22+ and a dedicated local Chrome debugging profile; no npm packages are required:

```bash
google-chrome --headless=new --no-sandbox --disable-gpu \
  --disable-dev-shm-usage --disable-background-networking \
  --no-first-run --no-default-browser-check \
  --remote-debugging-port=0 \
  --user-data-dir=/tmp/system-design-atlas-chrome about:blank

node system-design/src/verify_complete.mjs \
  "$PWD" /tmp/system-design-atlas-chrome/DevToolsActivePort
```

The browser test checks all 133 views, five widths, actual chapter/case/assessment counts, model arithmetic and failures, deep links, source/glossary filters, saved reading progress, JavaScript-disabled reading, offline loading, SVG text bounds, and print visibility. `verify_browser.mjs` is a compatibility entry point for the same complete-edition test.

Regenerate the full export after a successful build:

```bash
node system-design/src/verify_complete.mjs \
  "$PWD" /tmp/system-design-atlas-chrome/DevToolsActivePort --pdf-only
```

This writes `System-Design-Atlas-Complete.pdf`, including every produced chapter, unit reference plates, and reference desks. The browser's Print command uses the same print styling. The retained foundations PDF is not silently overwritten by the complete export.

For representative figure screenshots, use `--figures-only`. QA artifacts are written to `/tmp/system-design-complete-qa`; they are not runtime dependencies. Local socket access may need the environment's standard approval.

No deployment or git push is performed by the builder or verification scripts.
