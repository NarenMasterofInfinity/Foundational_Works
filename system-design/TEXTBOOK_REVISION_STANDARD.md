# System Design Atlas — Textbook Rewrite Standard

This is an original, NCERT-inspired engineering textbook revision of the existing
System Design Atlas. It is **not** a reproduction of NCERT or of third-party system
design books. Preserve the existing 22-unit / 99-chapter syllabus and every
existing public chapter/topic link.

## Editorial north star

Explain the *need* before naming the technology. Start with an ordinary person
and a concrete problem; let the learner try the simple design, see exactly why it
fails or becomes inadequate, and only then introduce the formal name.

Every chapter should make the following progression evident:

1. **Observe.** A relatable problem: a school feed, to-do list, library, cafe,
   payments desk, ticket window, document processing job, or another coherent
   real-world scenario.
2. **Attempt.** Begin with the smallest plausible implementation, including
   the assumptions that make it work.
3. **Encounter a problem.** Show a precise failure, growth constraint, race,
   incompatible requirement, or change request. Avoid artificial drama.
4. **Name the concept.** Introduce an accurate definition *after* readers have
   seen what it explains.
5. **Draw the mechanism.** Figure captions describe evidence, step ordering,
   identities, units, and boundaries, not merely repeat the heading.
6. **Make a decision.** When to use the idea, what alternatives exist, what it
   costs, and which assumptions could change the choice.
7. **Verify and transfer.** A small worked example, counterexample, and
   exercise requiring the learner to apply the idea to a different setting.

Teach the everyday analogy first but **explicitly say where it stops matching**
the computer system. Short paragraphs are preferable, but never omit a crucial
intermediate step to make the chapter shorter. Explain notation, acronyms,
prerequisites and units where first needed. Differently sized readers should
have a path from intuitive first pass to precise technical details.

### Technical accuracy is mandatory

- Differentiate *design assumption*, *hypothetical demonstration*, *measured
  benchmark*, and *standard/specification guarantee*.
- Do not conflate API requests, user actions, database writes, storage bytes,
  network bytes, throughput and latency.
- Every diagram must distinguish a synchronous call from an async event,
  source-code dependency from deployment communication, and a possible
  repeated message from a guaranteed exactly-once effect.
- For a concurrency or consistency claim, state the scope and failure model.
  A local transaction does not span an arbitrary remote provider.
- Source links should support specific mechanism or trade-off claims.
- Existing working code, interactive workbenches, questions, navigation,
  anchors, glossary and the complete-edition export must not regress.

## Figure-first production: choose the visual grammar based on the question

Every important figure must earn its place. Four generic component cards do
not count as four independent explanations.

| Learner's question | Prefer | Avoid |
| --- | --- | --- |
| What must the system promise? | Annotated brief → acceptance criteria | Network boxes |
| What happens and when? | Sequence/swimlane/timeline | Unordered cards |
| Who owns which responsibility? | Bounded regions/C4/class dependency map | Unlabeled arrows |
| Where does work multiply? | Fan-out/tree/quantity bracket | Drawing 1000 arrows |
| Which bytes live where? | Memory/page/log/storage cross-section | App-server topology |
| How do two states differ? | Before/after or state machine | Generic linear pipeline |
| Why does a queue build? | Arrival-vs-service graph / backlog curve | Queue logo |
| How do values compare? | Axes, histogram, distribution, waterfall | Decorative bars |
| Why was a design selected? | Constraint gates/trade-off worksheet | Single “best” box |
| Where did a failure occur? | Numbered incident timeline/fault boundary | Generic red node |
| How are data related? | ER relationships/ownership map | Sequence arrows |

Within a unit, plan figures **before** producing their SVG. Each figure
commission specifies: learning question, accurate claim, focal object,
chosen grammar, necessary annotations, edge semantics, caption, mobile
readability, and print behavior.

Visual quality principles:

- Use a consistent *book identity* but varied compositions. Repeat color
  semantics for consistency, **not** diagram geometry.
- Reserve red for actual failures, amber for risks/assumptions, green for
  confirmed successful outcomes. Do not assign meaning by color alone.
- Labels must be readable at a typical mobile viewport and in printed PDF.
- State where time runs, arrow direction, scope, units, and magnitudes.
- Do not use unlabeled arrows between unrelated snapshots.
- For visual density, draw a representative subset plus an explicit quantity
  bracket rather than many tiny glyphs.
- Prefer author-owned, source-controlled SVG and simple browser-native
  interactivity. Avoid runtime network dependencies.
- Captions explain **what can be inferred** and, where helpful, what cannot.

## Chapter-by-chapter release protocol

- Branch: \`atlas/textbook-edition-unit-NN\`, created from a current main
  commit. One PR per unit, no direct pushes to \`main\`.
- PRs may be drafts while a unit is incomplete. Make completion claims only
  when *every* chapter in that unit has been reviewed.
- Retain stable figures and lesson identifiers. Rebuild generated HTML and
  PDF when producing a release, and explain any artifact size changes.
- Review in four passes: conceptual correctness; teaching clarity; figure
  craft; build/browser/PDF/accessibility checks.
- Before marking a unit complete, run:
  \`python3 system-design/src/build.py\`,
  \`python3 system-design/src/verify_example.py\`,
  \`python3 system-design/src/verify_mechanisms.py\`, and the browser suite
  documented in \`system-design/README.md\`.
- Do not claim tests passed unless they actually ran. Browser inspections
  must include smartphone layout, desktop, print, and screen-reader labels.
- Merge units in order; rebase a later unit branch when earlier shared
  renderer files change.

## Unit 2 progress

**Chapter 2.1 rewritten in source** (three topic lessons) with four new,
concept-specific generated SVG plates:

1. Vague brief → measurable promise, an editorial annotated worksheet.
2. One feed opening → many kinds of network work, a time-down swimlane.
3. Fan-out on write vs read, an asymmetric branching comparison.
4. Count at the correct boundary, a measurement ledger.

Chapters **2.2–2.4 are not yet textbook-revised**. The rest of the existing
atlas content is intentionally preserved in this change. Do not use the Unit 2
PR as evidence of unit-level editorial completion until these remaining three
chapters are revised and visual/browser verification is performed.
