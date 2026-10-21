# Foundations source and technical review

Editorial snapshot: **21 October 2026**. This review covers Unit 1. It does not certify the unwritten chapters.

| Chapter | Claim or mechanism | Source / evidence | Boundary |
| --- | --- | --- | --- |
| 1.1 | Durable commit must precede application success for the chosen restart promise. | [SQLite atomic commit](https://www.sqlite.org/atomiccommit.html); executable process-loss verification. | Process restart with intact committed storage. Not a claim to survive destruction of the only disk. |
| 1.1, 1.4 | HTTP success semantics and application persistence policy are separate. | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html), including the 201 Created definition. | The RFC does not supply the atlas’s application-specific commit or deduplication mechanism. |
| 1.2 | Modularization should be evaluated through the criteria used to divide responsibilities. | [Parnas, 1972, original ACM article record](https://doi.org/10.1145/361598.361623). Metadata and abstract inspected. | The to-do decomposition and change-impact model are original teaching examples, not copied paper diagrams or measured results. |
| 1.2 | Supplying an implementation at composition is dependency injection; a container is optional. | [Martin Fowler, 2004](https://martinfowler.com/articles/injection.html). | Unit 1 introduces the boundary only. Object lifetimes and the complete pattern treatment remain assigned to Unit 6. |
| 1.3 | ADRs record a decision’s context, status, choice, and consequences. | [Michael Nygard, 2011](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions). | ADR 001 is author-created and conditional on the explicit example requirements. |
| 1.3 | Quality frameworks provide review lenses, not proofs. | [AWS Well-Architected pillars](https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html). | The book remains provider-neutral; no requirement to use AWS services is implied. |
| 1.4 | C4 has context, container, component, and code levels; dynamic/deployment diagrams support them. | [C4 diagram documentation](https://c4model.com/diagrams). | Our application drawings are original examples. They are not claims about real company infrastructure. |
| 1.4 | C4 “container” is not synonymous with Docker. | [C4 container definition](https://c4model.com/abstractions/container). | The example’s local store can be a C4 data-store container while sharing a host with the application. |

The bibliography retains the supplied starting collections for later chapters. Its `Link checked` label concerns access and the stated use. Unchecked links remain pending. Links such as PostgreSQL `/current/`, Kafka’s version selector, Kubernetes concepts, and SQLite documentation must be rechecked when version-specific behavior is taught. PostgreSQL’s current isolation documentation resolved to version 18 during this session; no claim about all database implementations follows from it.

## Calculations and code

- Unit 1’s state-transition model is explicitly a simplified behavioral model, not a simulation of an operating system.
- Weighted scores use `sum(weight × score) / sum(weight)` only for a positive weight total. The initial examples independently evaluate to `4` and `18/7`. All-zero weights produce an explanation, not an invalid number. Scores represent stated judgments rather than benchmarks.
- The crash workbench distinguishes volatile state, committed state, and acknowledged success. It can exhibit loss after early acknowledgment and commit without an observed response. It models one atomic commit and process loss only.
- The Python example performs parameterized SQL, validates titles before insertion, commits before returning, propagates storage errors, and closes owned connections in `finally` blocks. Completion sets `done = 1`; repeating it preserves the task-state result.
- Verification launches subprocesses that terminate using `os._exit(0)` without normal cleanup. The uncommitted insert is absent after recovery; the committed insert remains. This is evidence for the tested process-loss behavior, not power-loss testing.
- The example is a single-user local program. Authentication, authorization, idempotency-key storage, backup automation, and a complete HTTP server are deliberately outside that executable’s contract and remain explicit work in the book plan.

## Visual and editorial review

- Each produced chapter has four numbered, original SVG figures with labels, a teaching caption, relevance, and attribution.
- Arrow line styles distinguish actions/data, source dependencies or zoom, and acknowledgments. Color meaning is accompanied by text and a visible legend.
- Diagram 1.4.3 orders commit before response loss and retry. It does not claim that a timeout proves failure.
- Diagram 1.4.2 places application and store in one host failure domain. It does not imply availability from module separation.
- The C4 hierarchy is a zoom relation, not a request path. Diagram M.1 is explicitly a simplified conceptual spine; exact prerequisites are tabulated separately.
- Preference examples reject the memory-only candidate before scoring. Availability and durability are taught separately. Microservice extraction and additional servers require a demonstrated reason.
- Every supplied topic is retained verbatim in `src/syllabus.json` and allocated once in the blueprint. Production status is distinct from allocation status.
- All 11 Unit 1 questions have separate explanations including why tempting alternatives fail. All future assessments remain unproduced in the manifest.

## Assembly boundary

The digital edition and foundations PDF include **four produced chapters**, not 99 completed chapters. Planned chapters retain their syllabus, prerequisites, illustration commissions, and references. Complete-book assembly and the twelve fully worked case studies remain pending.
