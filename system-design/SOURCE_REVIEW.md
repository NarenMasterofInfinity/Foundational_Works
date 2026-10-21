# Complete-edition source and technical review

Editorial snapshot: **21 October 2026**. The complete edition contains all 22 units and 12 mandatory designs. This record distinguishes source support, original examples, and bounded verification from production guarantees.

## Reference policy and access

The 61 selected production references are recorded with titles, type, stated use, and access date in `completion-manifest.json`. They are attached to every chapter, with primary specifications or original papers for the relevant guarantees. Original supplied starting URLs remain in the original brief and the manifest's `starting_references`; production references can use more precise versioned or redirected destinations.

Original research includes Little's queueing formula, Parnas on modularization, Lamport on clocks and Paxos, Gilbert/Lynch on CAP, Raft, Dynamo, conflict-free replicated JSON, and The Tail at Scale. The text's examples, architectures, numerical inputs, and SVGs are author-created. The capstones do not claim to reproduce any named company's internal architecture.

University sources include OSTEP, CMU databases, and MIT distributed systems. Official specifications include HTTP semantics/caching, QUIC, TLS 1.3, WebSocket, OAuth security, and OpenID Connect. RFC 2697 and RFC 8216 are correctly identified as Informational protocol descriptions, not Standards Track RFCs. Implementation-sensitive database behavior cites PostgreSQL 18; Kafka behavior cites the 4.1 design documentation. Other evolving documentation is dated and should be rechecked when applied.

A source's access record is scoped: a publisher record or abstract is not described as reading an inaccessible full proof. The CAP PDF's text extraction is imperfect, so the original rendered page was inspected. Some source sites display access banners while also exposing article text. No inaccessible paper is used to invent benchmarks, exact company details, or verbatim content.

## Critical distinctions checked in the lessons

| Area | Correctness boundary and supporting source |
| --- | --- |
| Local durable success | Commit precedes success under explicitly intact storage assumptions; SQLite atomic-commit documentation and process-loss fixture. |
| HTTP and financial result | RFC 9110 semantics do not make provider approval or cross-service commit atomic. |
| Modularity and DI | Parnas/Fowler support responsibility and construction reasoning; injection and inversion are distinct. |
| Concurrency | Language memory models govern visibility; async syntax does not guarantee nonblocking execution or CPU parallelism. Go is one specified example, not a universal language guarantee. |
| Transactions | PostgreSQL 18 isolation behavior is distinguished from generic SQL labels; MVCC does not by itself prevent write skew or prove serializability. |
| Caching | HTTP caching, engine eviction, and application cache-aside races are different contracts. TTL alone is not a source-age or immediate-revocation proof. |
| Quorums | R + W > N is a fixed-set intersection condition, not a complete linearizability proof. |
| CAP and ordering | CAP's formal partition assumptions, linearizability, serializability, causal/session guarantees, and liveness/safety are separate. |
| Consensus | Raft includes persistent vote/log rules, eligible elections, current-term commit reasoning, and membership transition constraints. Paxos remains a conceptual introduction, not toy production code. |
| Leases | An expired local lease cannot stop a paused worker. Fencing must be enforced where relevant effects are accepted. |
| Delivery | Acknowledgment placement trades loss against replay. Idempotency and broker-scoped exactly-once guarantees do not automatically include arbitrary external effects. |
| Workflows | Outbox publication can repeat. Compensation can fail or differ from a perfect inverse. Durable reconciliation handles uncertain outcomes. |
| Security | OAuth authorization and OIDC identity differ. Tenant ownership is enforced across API, storage, cache, jobs, exports, and capability paths. Password guidance cites current OWASP guidance without inventing universal parameters. |
| Operations | Error-budget math uses explicit denominators. Traces distinguish wait from execution. Safe rollback requires compatible state, and restored serving does not resolve every uncertain business outcome. |
| Collaborative editing | OT and CRDT are algorithm families with specific semantics. Convergence is not all intent, rich-text, authorization, or recovery correctness. |

## Calculations and implementation evidence

- The social workload uses 10 million assumed DAU, 50 API requests/day, and peak multiplier five: 5787.04 average and 28935.19 peak API requests/s. Hypothetical per-instance capacity 600 RPS at target utilization 0.6 gives 81 nominal instances and 82 for one-instance loss. This does not validate a deployment or size the database and CDN.
- Raw byte estimates use decimal units. Replicas, indexes, metadata, compaction, retention, history, and migration overlap remain explicit extra costs.
- Little's Law uses stable averages within one boundary; the M/M/1 curve is explicitly a stable Markovian single-server mean model, not a p99 prediction.
- Amdahl's 80%-parallel/four-worker example gives 2.5x ideal speedup. Fifty independent 1%-slow fan-out calls give about 39.5% chance of at least one slow call. Independence and idealized execution are stated assumptions.
- Token refill and debit preserve capacity and reject invalid costs in the local model; shared and distributed admission require additional atomic ownership.
- The cost worksheet totals 371, 551, and 1402 **fictional monthly units**. It does not claim measured p99, availability, capacity, or current commercial pricing for those candidates.
- The architecture comparison uses three explicitly constructed 100-observation latency traces, nearest-rank p99, and a separate independent-component availability model. A partitioned operation requires all three data owners in that example; its formula does not apply to a request needing only one shard. Shared outages, overload, failover delay, and repair are excluded. Operational complexity is a reasoned qualitative judgment, not a measured scalar.
- The 1,000-upload comparison separates ideal I/O concurrency bounds from CPU service demand. Its 100-second sequential and 2-second concurrent waiting examples assume 100 ms per upload and 50 independent waits; actual overhead, bandwidth, and provider limits must be measured. Durable queuing adds recovery obligations rather than creating compute capacity.
- The executable suite verifies conditional seat claims, balanced per-currency postings and operation identity, local inbox/effect atomicity, outbox duplicate delivery, workflow epoch/input/deletion checks, vector relationships, rendezvous remapping, eviction, and keyset continuation.
- Code examples distinguish executable Python from language-neutral pseudocode. Pseudocode showing transaction ownership does not claim that remote providers participate in that local transaction. The collaborative-edit example locks current document state before applying and recording an operation, avoiding a stale read/overwrite miniature.

## Visual and editorial review

Every chapter has at least four numbered SVG figures with explicit labels, captions, teaching relevance, and original-illustration attribution. The unit plates explicitly implement the brief's essential diagram list. Numbered observation cards do not imply causal messages; directed paths are described as actions, dependency relationships, state transitions, or protocol stages. The separate master map is simplified and is supplemented by exact prerequisite tables and dependency-closed routes.

The complete manifest records 390 exact topic allocations, 26 individual LLD pattern treatments, 264 case-review sections, and eleven questions plus explained solutions for every unit. Coverage checks are not a substitute for independent subject-matter review or formal protocol verification. The local browser and executable evidence is recorded in `QA.md`; no illustrative target is relabeled as a measured production achievement.


## Units 2–22 writing revision

The remaining 95 chapters were revised using the installed `ncert-style-writing` skill and Unit 1 as the editorial reference. The revision replaces every concept explanation, individual pattern explanation, and case-review section, with separate authored chapter introductions, takeaways, application questions, and assessment answers. Glossary entries use concise reference definitions rather than extracted opening sentences. Captions summarise the illustrated idea; workbench instructions explain what to change and observe.

Technical conditions remain next to the claims they qualify. In particular, the revised text distinguishes fixed-set quorum intersection from a complete consistency protocol, MVCC from serializability, ownership epochs from external-effect fencing, and local idempotency from provider outcomes. CAP, Raft, and database isolation wording was checked against the linked primary material. Existing code, numerical assumptions, syllabus coverage, and visual conventions are retained. No new source count, company benchmark, or production guarantee is claimed. The four Unit 1 chapter sections compare identically with the preceding edition.
