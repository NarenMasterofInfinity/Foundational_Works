# Complete-edition verification

Verified locally on **27 October 2026** for the merged-source integration and focused Unit 4 review.

## Scope and editorial evidence

The committed HTML and PDF include the merged chapter companions. Expected companion modules, chapter keys, and lesson/diagram lengths are required by the renderer. The manifest records companion source paths. Figure registration matches actual HTML figures exactly; the integration removed 26 registrations for figures that were generated and then overwritten.

Unit 4’s 17 custom figures are active. Its duplicate chapter introductions and appended lesson/caption repetitions are removed. The uploaded-file example, counters, worker limits, semaphore permits, lock names, and overload rates agree across prose and graphics. Each figure has desktop and narrow-screen compositions; print uses the desktop composition once.

A context-free read of Chapter 4.3 found four clarity gaps, now corrected: workers versus threads, the reason a lost update loses information, the two-account transfer, and the coordinated condition-variable wait. Synchronization and cancellation statements were checked against the [Go memory model](https://go.dev/ref/mem), [Python condition-variable documentation](https://docs.python.org/3.14/library/threading.html#condition-objects), and [Python task-group documentation](https://docs.python.org/3/library/asyncio-task.html#task-groups). Numerical workloads remain illustrative assumptions.

This pass does not certify the teaching quality of every merged companion or every chapter. Other units retain earlier writing revisions and the merged additions; they still need focused editorial and visual review.

## Build, executable, and browser checks

- Python compilation, deterministic HTML rebuild, JavaScript parsing, and `git diff --check` pass.
- Coverage checks pass for 22 units, 99 chapters, 390 syllabus items, 575 rendered figures, 12 designs with 264 sections, and 242 questions with separate answers. Figure IDs in the manifest match the rendered HTML exactly.
- The task example and bounded mechanism suite pass validation, persistence/crash ordering, arithmetic, queueing, caching, pagination, vector order, assignment, seat claims, postings, repeated delivery, fencing, deletion, tenant policy, and assumed costs.
- All 133 views fit 1440, 1024, 768, 390, and 360 px. The 13 workbenches, navigation, filters, deep links, and saved reading progress pass. Offline reading makes no external requests; all chapters remain readable without JavaScript. Print exposes all chapters and restores the interactive state afterward.
- Unit 4’s 17 narrow compositions fit their containers at 360 and 390 px, have no text outside the SVG canvas or overlapping text labels, and have labels of at least 12 rendered CSS pixels. Their captions are not repeated as lesson paragraphs. The deadlock’s four semantic edges match the worked cycle and touch the correct diagram nodes.
- Desktop and phone versions of all 17 figures were captured and visually reviewed. Actual PDF pages 100, 113, and 117 cover memory, deadlock, and backpressure; representative pages were rendered for print inspection.

These checks establish artifact integrity, selected mechanisms, and rendering behavior. They do not measure learning outcomes. The deadlock topology is checked against the worked example rather than inferred from the diagram’s own labels; human inspection remains necessary for other diagram semantics.

## PDF and release integrity

The current export contains **1,153 tagged A4 pages**. `verify_release.py` independently extracts the PDF and checks all 99 chapter titles, 575 figure labels, and 264 case-section headings. It requires the current source identifier inside both HTML and PDF and verifies the hashes of all generated artifacts against [release.json](release.json).

Negative checks on an isolated copy accept the intact release and reject independently changed source, HTML, and PDF files. Attempting to record the previous PDF after a source change also fails. Regenerating HTML alone therefore cannot make the stale export pass the release check.

The larger export includes the previously source-only companion introductions, questions, and code examples. The retained foundations PDF is unchanged. Exact export size and hashes are release data, not manually maintained QA claims.

## Hosting and reproduction

Pages serves committed files from main at the repository root. The blocked custom deployment workflow is retired. The shell-only **Atlas release check** checks out the exact event commit without external actions, verifies regenerated files and release identity, then runs executable and browser checks under the existing local-actions policy. Live publication must be confirmed by comparing served HTML/PDF hashes to the release record after merge.

Commands are in [README.md](README.md#release). Local evidence is under `/tmp/system-design-complete-qa` and `/tmp/atlas-audit`; these are not runtime dependencies. The source identifier covers source files and is not a score for teaching quality.
