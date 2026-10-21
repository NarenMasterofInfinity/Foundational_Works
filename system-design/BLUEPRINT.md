# The System Design Atlas — book blueprint

This is a staged first installment, not the finished textbook. Planned pages are editorial outlines, not lessons.

Editorial snapshot: 2026-10-21. 99 chapters across 22 units.

## Unit 1: Introduction to System Design

Status: available. Prerequisites: [].

Worked example: Design a basic to-do application. Begin with a single program and progressively identify modules, persistent storage, a web API, and deployment boundaries.

### 1.1 A system is a promise — available

Prerequisites: 

- What is a software system?

- What does it mean to design a system?

- HLD vs LLD vs software architecture.

- Components, boundaries, interfaces, and contracts.

- State, data, computation, and communication.

Illustrations: The boundary follows the promise; Data becomes state through a transition; HLD and LLD ask connected questions; From a working demo to a recoverable write

Starting references: https://www.sqlite.org/atomiccommit.html · https://www.rfc-editor.org/rfc/rfc9110.html

### 1.2 Boundaries that make change local — available

Prerequisites: ch-1-1

- Coupling, cohesion, modularity, separation of concerns.

- Abstraction layers.

Illustrations: An innocent feature crosses every responsibility; Separate responsibilities inside one process; Dependency direction differs from execution direction; Abstraction narrows the question at each layer

Starting references: https://doi.org/10.1145/361598.361623 · https://martinfowler.com/articles/injection.html

### 1.3 Requirements become decisions — available

Prerequisites: ch-1-2

- Functional and nonfunctional requirements.

- Constraints, assumptions, risks, and trade-offs.

- Architectural characteristics and quality attributes.

- Architecture Decision Records (ADRs).

- Why the simplest sufficient design is often preferable.

Illustrations: Make a vague quality measurable; A decision is a testable hypothesis; A hard constraint comes before a preference score; Healthy traffic does not prove durable data

Starting references: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions · https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html

### 1.4 One application, many architectural views — available

Prerequisites: ch-1-3

- Architecture diagrams: C4 model, context, container, component, deployment, sequence.

Illustrations: C4 changes the level of detail; A deployment view locates the single points of failure; A lost response makes the outcome uncertain; Architecture evolves when an assumption fails

Starting references: https://c4model.com/diagrams · https://c4model.com/abstractions/container · https://www.rfc-editor.org/rfc/rfc9110.html

Essential unit diagrams: HLD vs LLD comparison; abstraction layers; architecture decision workflow; C4 diagram hierarchy

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. available.
## Unit 2: Requirements, Estimation, and Engineering Trade-offs

Status: planned. Prerequisites: [1].

Worked example: A social platform has 10 million daily active users. Estimate requests per second, traffic at peak, storage growth, image bandwidth, and approximate infrastructure requirements.

### 2.1 Turn user journeys into workloads — planned

Prerequisites: unit-1

- Gathering and prioritizing requirements.

- User journeys and workload characteristics.

- Read-heavy vs write-heavy systems.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://sre.google/workbook/table-of-contents/ · https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html

### 2.2 Measure the experience — planned

Prerequisites: ch-2-1

- Latency, throughput, QPS, RPS, TPS.

- Average vs median vs p95/p99 latency.

- Availability, reliability, durability, consistency.

- SLI, SLO, SLA, and error budgets.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://sre.google/workbook/table-of-contents/ · https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html

### 2.3 Estimate the resources — planned

Prerequisites: ch-2-2

- Capacity and growth planning.

- Storage, memory, bandwidth, and CPU estimates.

- Peak vs average load.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://sre.google/workbook/table-of-contents/ · https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html

### 2.4 Queues, bottlenecks & defensible decisions — planned

Prerequisites: ch-2-3

- Little's Law and queueing intuition.

- Amdahl's Law and bottlenecks.

- Tail latency and latency budgets.

- Cost, security, operational complexity, and maintainability as constraints.

- Decision matrices and trade-off analysis.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://sre.google/workbook/table-of-contents/ · https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html

Essential unit diagrams: Request-volume timeline; throughput-latency curve; latency waterfall; capacity planning worksheet

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 3: Networking Foundations for System Design

Status: planned. Prerequisites: [1].

Worked example: Trace what happens when someone enters a website URL, from DNS lookup through server execution to browser rendering.

### 3.1 Addresses, sockets & transports — planned

Prerequisites: unit-1

- How the internet works from the application perspective.

- IP addresses, ports, sockets, routing.

- TCP vs UDP vs QUIC.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview · https://www.cloudflare.com/learning/cdn/what-is-a-cdn/ · https://github.com/ByteByteGoHq/system-design-101 · https://www.rfc-editor.org/rfc/rfc9110.html

### 3.2 A secure request, one round trip at a time — planned

Prerequisites: ch-3-1

- DNS resolution and DNS caching.

- TLS and HTTPS.

- HTTP/1.1, HTTP/2, HTTP/3.

- Connection establishment and connection reuse.

- Latency caused by network round trips.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview · https://www.cloudflare.com/learning/cdn/what-is-a-cdn/ · https://github.com/ByteByteGoHq/system-design-101 · https://www.rfc-editor.org/rfc/rfc9110.html

### 3.3 Intermediaries & persistent connections — planned

Prerequisites: ch-3-2

- Reverse proxies vs forward proxies.

- Load balancers vs API gateways.

- L4 vs L7 load balancing.

- WebSockets, Server-Sent Events, and polling.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview · https://www.cloudflare.com/learning/cdn/what-is-a-cdn/ · https://github.com/ByteByteGoHq/system-design-101 · https://www.rfc-editor.org/rfc/rfc9110.html

### 3.4 Discover, route & survive the network — planned

Prerequisites: ch-3-3

- NAT, firewalls, ingress, egress.

- Service discovery.

- CDN and edge networking.

- Network partitions, timeouts, packet loss.

- Connection pooling and keepalive.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview · https://www.cloudflare.com/learning/cdn/what-is-a-cdn/ · https://github.com/ByteByteGoHq/system-design-101 · https://www.rfc-editor.org/rfc/rfc9110.html

Essential unit diagrams: Complete HTTP request timeline; TCP/TLS interaction; load-balancing topology; WebSocket vs polling communication

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 4: Runtime, Processes, Threads, and Concurrency

Status: planned. Prerequisites: [1].

Worked example: Build a service that processes 1,000 file uploads. Compare sequential execution, threads, asynchronous I/O, and worker queues. Identify which architecture helps under which workload.

### 4.1 The runtime owns your resources — planned

Prerequisites: unit-1

- Program vs process vs thread.

- Memory, stack, heap, and object lifetimes.

- Scheduling and context switching.

- CPU-bound vs I/O-bound workloads.

- Synchronous vs asynchronous execution.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://pages.cs.wisc.edu/~remzi/OSTEP/ · https://go.dev/ref/mem

### 4.2 Tasks, threads & event loops — planned

Prerequisites: ch-4-1

- Blocking vs nonblocking I/O.

- Concurrency vs parallelism.

- Event loops, tasks, futures, promises.

- Thread pools and worker pools.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://pages.cs.wisc.edu/~remzi/OSTEP/ · https://go.dev/ref/mem

### 4.3 Shared memory & coordination — planned

Prerequisites: ch-4-2

- Shared memory vs message passing.

- Race conditions and critical sections.

- Mutexes, semaphores, atomics, condition variables.

- Deadlocks, starvation, livelocks.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://pages.cs.wisc.edu/~remzi/OSTEP/ · https://go.dev/ref/mem

### 4.4 Visibility, cancellation & overload — planned

Prerequisites: ch-4-3

- Memory visibility and happens-before relationships.

- Thread safety and immutability.

- Resource exhaustion and backpressure.

- Cancellation and structured concurrency.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://pages.cs.wisc.edu/~remzi/OSTEP/ · https://go.dev/ref/mem

Essential unit diagrams: Process/thread memory model; scheduling timeline; race-condition interleaving; deadlock wait graph; event-loop flow

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 5: Object-Oriented and Modular Software Design

Status: planned. Prerequisites: [1].

Worked example: Start with a poorly designed payment-processing class. Refactor it into appropriate components, showing which problems each design improvement solves.

### 5.1 Model behavior with objects and values — planned

Prerequisites: unit-1

- Abstraction, encapsulation, polymorphism, inheritance.

- Composition vs inheritance.

- Interfaces and contracts.

- High cohesion and low coupling.

- SOLID principles, including their limitations.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://refactoring.guru/design-patterns · https://martinfowler.com/bliki/BoundedContext.html

### 5.2 Principles under pressure — planned

Prerequisites: ch-5-1

- DRY, KISS, YAGNI.

- Law of Demeter.

- Tell, Don't Ask.

- Command-query separation.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://refactoring.guru/design-patterns · https://martinfowler.com/bliki/BoundedContext.html

### 5.3 Side effects, domain models & collaboration — planned

Prerequisites: ch-5-2

- Immutability and side-effect management.

- Domain models, entities, value objects.

- Object collaboration.

- Testability and design for change.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://refactoring.guru/design-patterns · https://martinfowler.com/bliki/BoundedContext.html

### 5.4 Design for change, testing & functions — planned

Prerequisites: ch-5-3

- Refactoring and recognizing code smells.

- Functional programming alternatives to object-centric design.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://refactoring.guru/design-patterns · https://martinfowler.com/bliki/BoundedContext.html

Essential unit diagrams: Before/after class diagrams; dependency graph; inheritance vs composition; cohesion/coupling illustrations

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 6: Design Patterns, Dependency Injection, and Object Lifecycles

Status: planned. Prerequisites: [5].

Worked example: Create a notification platform supporting email, SMS, and push notifications. Evolve it from hardcoded classes to DI, Strategy, Factory, and Decorator patterns.

### 6.1 Dependencies, inversion & composition — planned

Prerequisites: unit-5

- Dependency, dependency direction, and inversion.

- Inversion of Control (IoC).

- Dependency Injection (DI).

- Constructor, property/setter, and method injection.

- Dependency inversion principle vs DI.

- Composition roots and DI containers.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://martinfowler.com/articles/injection.html · https://refactoring.guru/design-patterns · https://refactoring.guru/design-patterns/catalog

### 6.2 Lifetimes, ownership & cleanup — planned

Prerequisites: ch-6-1

- Transient, scoped, singleton, and framework-specific lifetimes.

- Request scopes, session scopes, and custom scopes.

- Object creation vs object ownership.

- Disposal, cleanup, and resource lifecycles.

- Lazy initialization.

- Dependency cycles and captive dependencies.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://martinfowler.com/articles/injection.html · https://refactoring.guru/design-patterns · https://refactoring.guru/design-patterns/catalog

### 6.3 Injection, locators & factories — planned

Prerequisites: ch-6-2

- DI vs service locator.

- DI vs factory pattern.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://martinfowler.com/articles/injection.html · https://refactoring.guru/design-patterns · https://refactoring.guru/design-patterns/catalog

### 6.4 Creational patterns — planned

Prerequisites: ch-6-3

- Factory Method, Abstract Factory, Builder, Prototype, Singleton.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://martinfowler.com/articles/injection.html · https://refactoring.guru/design-patterns · https://refactoring.guru/design-patterns/catalog

### 6.5 Structural patterns — planned

Prerequisites: ch-6-4

- Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://martinfowler.com/articles/injection.html · https://refactoring.guru/design-patterns · https://refactoring.guru/design-patterns/catalog

### 6.6 Behavioral patterns — planned

Prerequisites: ch-6-5

- Strategy, Observer, Command, State, Chain of Responsibility, Template Method, Iterator, Mediator, Memento, Visitor.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://martinfowler.com/articles/injection.html · https://refactoring.guru/design-patterns · https://refactoring.guru/design-patterns/catalog

### 6.7 Enterprise patterns & boundaries — planned

Prerequisites: ch-6-6

- Repository, Unit of Work, Specification, CQRS, and dependency boundaries.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://martinfowler.com/articles/injection.html · https://refactoring.guru/design-patterns · https://refactoring.guru/design-patterns/catalog

Essential unit diagrams: Object creation timelines; singleton/scoped/transient identity illustration; UML class relationships; dependency inversion before/after; pattern comparisons

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 7: Application Architecture and Domain-Driven Design

Status: planned. Prerequisites: [5, 6].

Worked example: Design an online shopping application first as a modular monolith, then examine the conditions under which selected domains should become independent services.

### 7.1 Layers, monoliths & ports — planned

Prerequisites: unit-5, unit-6

- Layered/N-tier architecture.

- Modular monoliths.

- Monolith vs microservices.

- Clean Architecture.

- Hexagonal/Ports and Adapters.

- Onion Architecture.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://learn.microsoft.com/azure/architecture/guide/architecture-styles · https://martinfowler.com/bliki/BoundedContext.html · https://www.martinfowler.com/articles/microservices.html

### 7.2 Model a bounded context — planned

Prerequisites: ch-7-1

- Domain-Driven Design (DDD).

- Bounded contexts and ubiquitous language.

- Aggregates, entities, value objects, domain services.

- Domain events.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://learn.microsoft.com/azure/architecture/guide/architecture-styles · https://martinfowler.com/bliki/BoundedContext.html · https://www.martinfowler.com/articles/microservices.html

### 7.3 Keep business policy inside — planned

Prerequisites: ch-7-2

- Dependency rules and module boundaries.

- Business logic vs orchestration vs infrastructure.

- Controllers, services, repositories, adapters.

- Anti-corruption layers.

- Event-driven architecture.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://learn.microsoft.com/azure/architecture/guide/architecture-styles · https://martinfowler.com/bliki/BoundedContext.html · https://www.martinfowler.com/articles/microservices.html

### 7.4 Evolution without a distributed monolith — planned

Prerequisites: ch-7-3

- Serverless and function-oriented architectures.

- Evolutionary architecture.

- Technical vs business boundaries.

- Distributed monolith antipattern.

- When not to use microservices.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://learn.microsoft.com/azure/architecture/guide/architecture-styles · https://martinfowler.com/bliki/BoundedContext.html · https://www.martinfowler.com/articles/microservices.html

Essential unit diagrams: Layered vs Hexagonal; modular monolith vs microservices; dependency arrows; bounded context map

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 8: API Design and Communication Contracts

Status: planned. Prerequisites: [1, 3].

Worked example: Design a payment API with create-payment, payment-status, refunds, idempotency protection, duplicate requests, and failed network responses.

### 8.1 Model resources and messages — planned

Prerequisites: unit-1, unit-3

- API fundamentals and interface contracts.

- REST, GraphQL, gRPC, RPC.

- Resource modeling.

- Request/response schemas.

- Status codes and error models.

- Pagination, filtering, sorting.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://developer.mozilla.org/en-US/docs/Web/HTTP · https://learn.microsoft.com/en-us/azure/architecture/best-practices/index-best-practices · https://api-security.owasp.org/editions/2023/en/0x11-t10/

### 8.2 Compatibility & idempotency — planned

Prerequisites: ch-8-1

- Cursor vs offset pagination.

- API versioning and compatibility.

- Idempotency and idempotency keys.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://developer.mozilla.org/en-US/docs/Web/HTTP · https://learn.microsoft.com/en-us/azure/architecture/best-practices/index-best-practices · https://api-security.owasp.org/editions/2023/en/0x11-t10/

### 8.3 Control access, load & long operations — planned

Prerequisites: ch-8-2

- Authentication vs authorization at API boundaries.

- Rate limits and quotas.

- Retries and timeouts.

- Streaming APIs and long-running operations.

- Webhooks and delivery acknowledgments.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://developer.mozilla.org/en-US/docs/Web/HTTP · https://learn.microsoft.com/en-us/azure/architecture/best-practices/index-best-practices · https://api-security.owasp.org/editions/2023/en/0x11-t10/

### 8.4 Evolve a public contract — planned

Prerequisites: ch-8-3

- Schema evolution.

- Consumer-driven contracts.

- API gateways and BFF.

- Public vs internal APIs.

- API documentation and discoverability.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://developer.mozilla.org/en-US/docs/Web/HTTP · https://learn.microsoft.com/en-us/azure/architecture/best-practices/index-best-practices · https://api-security.owasp.org/editions/2023/en/0x11-t10/

Essential unit diagrams: REST request flow; API gateway topology; synchronous vs asynchronous API; payment state-machine diagram

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 9: Data Models and Storage Technologies

Status: planned. Prerequisites: [1].

Worked example: Choose storage technologies for user profiles, financial transactions, chat messages, event logs, and uploaded PDFs. Justify each decision.

### 9.1 Storage promises & database families — planned

Prerequisites: unit-1

- What data storage must guarantee.

- Relational databases and SQL.

- Document databases.

- Key-value databases.

- Wide-column stores.

- Graph databases.

- Time-series databases.

- Search indexes.

- Vector indexes: introductory architecture only.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://db.cs.cmu.edu/courses/ · https://learn.microsoft.com/en-us/azure/architecture/guide/

### 9.2 Files, objects & analytical layouts — planned

Prerequisites: ch-9-1

- Object storage vs block vs file storage.

- OLTP vs OLAP.

- Row-oriented vs column-oriented storage.

- Normalization vs denormalization.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://db.cs.cmu.edu/courses/ · https://learn.microsoft.com/en-us/azure/architecture/guide/

### 9.3 Model relationships and ownership — planned

Prerequisites: ch-9-2

- ER diagrams and relational modeling.

- Referential integrity.

- Data ownership.

- Choosing storage based on access patterns.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://db.cs.cmu.edu/courses/ · https://learn.microsoft.com/en-us/azure/architecture/guide/

### 9.4 Access patterns, retention & operational cost — planned

Prerequisites: ch-9-3

- Data retention and lifecycle.

- Polyglot persistence and its operational costs.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://db.cs.cmu.edu/courses/ · https://learn.microsoft.com/en-us/azure/architecture/guide/

Essential unit diagrams: Database taxonomy; physical storage representations; normalized vs denormalized schema; entity-relationship diagrams

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 10: Database Internals, Transactions, and Concurrency Control

Status: planned. Prerequisites: [4, 9].

Worked example: Two users attempt to purchase the last available ticket. Demonstrate the lost-update race, show why naive reads fail, and implement valid alternatives using transactions and concurrency control.

### 10.1 Pages, indexes & query plans — planned

Prerequisites: unit-4, unit-9

- How databases store and retrieve records.

- Pages, records, indexes, and buffer pools.

- B-tree/B+tree and hash indexing.

- LSM trees and write amplification.

- Query planning and EXPLAIN.

- Index selection and query optimization.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://15445.courses.cs.cmu.edu/ · https://www.postgresql.org/docs/current/transaction-iso.html

### 10.2 Commit, logging & versions — planned

Prerequisites: ch-10-1

- ACID properties.

- Transaction commit and rollback.

- Write-ahead logging.

- MVCC.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://15445.courses.cs.cmu.edu/ · https://www.postgresql.org/docs/current/transaction-iso.html

### 10.3 Races, anomalies & isolation — planned

Prerequisites: ch-10-2

- Locking and optimistic concurrency control.

- Dirty reads, nonrepeatable reads, phantom reads.

- Lost updates, write skew, serialization anomalies.

- Isolation levels and implementation differences.

- Serializable execution and serializability.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://15445.courses.cs.cmu.edu/ · https://www.postgresql.org/docs/current/transaction-iso.html

### 10.4 Pools, recovery & ticket correctness — planned

Prerequisites: ch-10-3

- Database connection pooling.

- Transactions across multiple operations.

- Backup, recovery, and durability.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://15445.courses.cs.cmu.edu/ · https://www.postgresql.org/docs/current/transaction-iso.html

Essential unit diagrams: B+tree traversal; MVCC version timeline; concurrent transaction interleavings; lock wait graph; WAL and recovery

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 11: Caching and Content Delivery

Status: planned. Prerequisites: [3, 9].

Worked example: A popular product page receives enormous traffic. Introduce caching gradually and examine stale prices, thundering herds, inventory correctness, and failure behavior.

### 11.1 Locality and cache placement — planned

Prerequisites: unit-3, unit-9

- Why caching works.

- Cache locality and the working set.

- In-process vs distributed caches.

- Browser, CDN, application, and database caches.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://redis.io/docs/latest/develop/use/patterns/ · https://www.cloudflare.com/learning/cdn/what-is-a-cdn/ · https://learn.microsoft.com/en-us/azure/architecture/patterns

### 11.2 Copies, freshness & eviction — planned

Prerequisites: ch-11-1

- Cache-aside, read-through, write-through, write-behind.

- TTL and cache expiration.

- Cache consistency and invalidation.

- Eviction: LRU, LFU, FIFO, and alternatives.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://redis.io/docs/latest/develop/use/patterns/ · https://www.cloudflare.com/learning/cdn/what-is-a-cdn/ · https://learn.microsoft.com/en-us/azure/architecture/patterns

### 11.3 Hot keys, stampedes & negative results — planned

Prerequisites: ch-11-2

- Hot keys.

- Cache stampedes, penetration, and avalanche.

- Negative caching.

- Stale-while-revalidate.

- Cache warming and prefetching.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://redis.io/docs/latest/develop/use/patterns/ · https://www.cloudflare.com/learning/cdn/what-is-a-cdn/ · https://learn.microsoft.com/en-us/azure/architecture/patterns

### 11.4 Edges, partitions & the price of a cache — planned

Prerequisites: ch-11-3

- Redis-like data structures.

- CDN architecture and origin shielding.

- Cache partitioning and replication.

- When caching is harmful.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://redis.io/docs/latest/develop/use/patterns/ · https://www.cloudflare.com/learning/cdn/what-is-a-cdn/ · https://learn.microsoft.com/en-us/azure/architecture/patterns

Essential unit diagrams: Cache hit/miss sequence; cache hierarchy; eviction simulation; stampede timeline; geographic CDN delivery

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 12: Scalability, Load Balancing, and Data Distribution

Status: planned. Prerequisites: [2, 3, 9, 10, 11].

Worked example: Scale a URL shortener from 100 requests per second to 100,000. Introduce new components only when justified by a demonstrated bottleneck.

### 12.1 Scale compute & route requests — planned

Prerequisites: unit-2, unit-3, unit-9, unit-10, unit-11

- Vertical vs horizontal scaling.

- Stateless vs stateful services.

- Load distribution algorithms.

- Health checks and failover.

- Sticky sessions.

- Autoscaling metrics.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://learn.microsoft.com/en-us/azure/architecture/best-practices/index-best-practices

### 12.2 Replicate and partition data — planned

Prerequisites: ch-12-1

- Replication.

- Partitioning and sharding.

- Range partitioning vs hash partitioning.

- Consistent hashing and rendezvous hashing.

- Rebalancing.

- Hot partitions and skew.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://learn.microsoft.com/en-us/azure/architecture/best-practices/index-best-practices

### 12.3 Lag, proxies & saturated pools — planned

Prerequisites: ch-12-2

- Read replicas and read/write splitting.

- Replication lag.

- Database proxying.

- Connection pool saturation.

- Bottleneck identification.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://learn.microsoft.com/en-us/azure/architecture/best-practices/index-best-practices

### 12.4 Regions, write paths & scale economics — planned

Prerequisites: ch-12-3

- Queueing and overload.

- Single points of failure.

- Multi-region strategies.

- Scaling writes vs scaling reads.

- Scale-out economics.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://learn.microsoft.com/en-us/azure/architecture/best-practices/index-best-practices

Essential unit diagrams: Architecture evolution across four load levels; consistent-hashing ring; sharding heatmap; load-balancer failover

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 13: File Systems, Search Infrastructure, and Data Pipelines

Status: planned. Prerequisites: [8, 9, 10].

Worked example: Design a document-processing system accepting millions of files, tracking processing state, extracting metadata, maintaining provenance, and exposing searchable results.

### 13.1 Upload bytes without losing identity — planned

Prerequisites: unit-8, unit-9, unit-10

- Binary/object storage.

- Large-file upload architecture.

- Multipart and resumable uploads.

- Checksums and content addressing.

- Metadata vs binary data.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://15445.courses.cs.cmu.edu/ · https://learn.microsoft.com/en-us/azure/architecture/ · https://kafka.apache.org/documentation/

### 13.2 Build and rebuild a search index — planned

Prerequisites: ch-13-1

- Search engines and inverted indexes.

- Indexing pipelines.

- Search ingestion and reindexing.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://15445.courses.cs.cmu.edu/ · https://learn.microsoft.com/en-us/azure/architecture/ · https://kafka.apache.org/documentation/

### 13.3 Move data through batch and streams — planned

Prerequisites: ch-13-2

- Batch vs streaming pipelines.

- ETL vs ELT.

- Change Data Capture (CDC).

- Data lakes and warehouses.

- Stream processing fundamentals.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://15445.courses.cs.cmu.edu/ · https://learn.microsoft.com/en-us/azure/architecture/ · https://kafka.apache.org/documentation/

### 13.4 Quality, provenance & replay — planned

Prerequisites: ch-13-3

- Data provenance and lineage.

- Data quality, schema validation, and replay.

- Lifecycle policies and retention.

- Designing data-intensive applications.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://15445.courses.cs.cmu.edu/ · https://learn.microsoft.com/en-us/azure/architecture/ · https://kafka.apache.org/documentation/

Essential unit diagrams: Upload pipeline; inverted index; ingestion DAG; batch vs stream timeline; lineage graph

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 14: Distributed Systems Fundamentals

Status: planned. Prerequisites: [3, 4, 10].

Worked example: A social application writes a new post in one region while a friend reads it from another. Examine different consistency contracts and their user-visible effects.

### 14.1 Partial failure & the meaning of time — planned

Prerequisites: unit-3, unit-4, unit-10

- What makes a distributed system difficult?

- Partial failures.

- Network uncertainty.

- Fault models.

- Time, clocks, and event ordering.

- Physical vs logical clocks.

- Lamport clocks and vector clocks.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://pdos.csail.mit.edu/6.5840/ · https://learn.microsoft.com/en-us/azure/architecture/patterns · https://lamport.azurewebsites.net/pubs/time-clocks.pdf

### 14.2 Consistency as a reader-visible contract — planned

Prerequisites: ch-14-1

- Consistency models.

- Strong consistency and eventual consistency.

- Linearizability.

- Serializability vs linearizability.

- Sequential and causal consistency.

- Read-your-writes and monotonic reads.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://pdos.csail.mit.edu/6.5840/ · https://learn.microsoft.com/en-us/azure/architecture/patterns · https://lamport.azurewebsites.net/pubs/time-clocks.pdf

### 14.3 Partitions, CAP, PACELC & quorums — planned

Prerequisites: ch-14-2

- CAP theorem, with its actual assumptions.

- PACELC as a useful extension.

- Quorums and read/write trade-offs.

- Split-brain situations.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://pdos.csail.mit.edu/6.5840/ · https://learn.microsoft.com/en-us/azure/architecture/patterns · https://lamport.azurewebsites.net/pubs/time-clocks.pdf

### 14.4 Coordination, safety & liveness — planned

Prerequisites: ch-14-3

- Distributed coordination.

- The fallacies of distributed computing.

- Safety vs liveness.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://pdos.csail.mit.edu/6.5840/ · https://learn.microsoft.com/en-us/azure/architecture/patterns · https://lamport.azurewebsites.net/pubs/time-clocks.pdf

Essential unit diagrams: Network partition; causality timeline; consistency model comparisons; read/write quorum visualizations

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 15: Replication, Leader Election, and Consensus

Status: planned. Prerequisites: [14].

Worked example: Three database replicas, one leader, and a network partition. Walk through elections, writes, acknowledgement rules, recovery, and potential data loss.

### 15.1 Choose a replication model — planned

Prerequisites: unit-14

- Primary/replica architectures.

- Leader/follower replication.

- Multi-leader replication.

- Leaderless replication.

- Synchronous vs asynchronous replication.

- Quorum-based systems.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://pdos.csail.mit.edu/6.5840/ · https://redis.io/docs/latest/develop/use/patterns/ · https://raft.github.io/raft.pdf

### 15.2 Raft and replicated state machines — planned

Prerequisites: ch-15-1

- Consensus and replicated state machines.

- Raft: terms, elections, log replication, commit.

- Paxos: conceptual foundations.

- Log ordering and durability.

- Membership changes.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://pdos.csail.mit.edu/6.5840/ · https://redis.io/docs/latest/develop/use/patterns/ · https://raft.github.io/raft.pdf

### 15.3 Fences, leases & failure detection — planned

Prerequisites: ch-15-2

- Split-brain prevention and fencing tokens.

- Failure detection.

- Strongly consistent metadata services.

- Distributed locks and leases.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://pdos.csail.mit.edu/6.5840/ · https://redis.io/docs/latest/develop/use/patterns/ · https://raft.github.io/raft.pdf

### 15.4 Conflicts, CRDTs & regional trade-offs — planned

Prerequisites: ch-15-3

- Conflict resolution and CRDT introduction.

- Multi-region replication trade-offs.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://pdos.csail.mit.edu/6.5840/ · https://redis.io/docs/latest/develop/use/patterns/ · https://raft.github.io/raft.pdf

Essential unit diagrams: Raft state transitions; election timeline; replicated log; quorum intersection; network partition recovery

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 16: Message Queues, Events, and Distributed Workflows

Status: planned. Prerequisites: [8, 10, 14, 15].

Worked example: Design an e-commerce checkout that coordinates payment, inventory reservation, shipment creation, and refund compensation.

### 16.1 Queues, logs & delivery boundaries — planned

Prerequisites: unit-8, unit-10, unit-14, unit-15

- Synchronous vs asynchronous communication.

- Queues vs logs vs pub/sub.

- Producers, consumers, brokers.

- Partitions, consumer groups, offsets.

- Delivery guarantees.

- At-most-once and at-least-once processing.

- Exactly-once processing within defined boundaries.

- Ordering guarantees.

- Consumer acknowledgements.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://kafka.apache.org/documentation/ · https://microservices.io/patterns/data/transactional-outbox · https://learn.microsoft.com/en-us/azure/architecture/patterns · https://microservices.io/patterns/data/transactional-outbox.html

### 16.2 Retries, poison messages & idempotence — planned

Prerequisites: ch-16-1

- Retries and dead-letter queues.

- Poison messages.

- Idempotent consumers.

- Event sourcing.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://kafka.apache.org/documentation/ · https://microservices.io/patterns/data/transactional-outbox · https://learn.microsoft.com/en-us/azure/architecture/patterns · https://microservices.io/patterns/data/transactional-outbox.html

### 16.3 Event sourcing, CQRS & the outbox — planned

Prerequisites: ch-16-2

- CQRS.

- Transactional outbox.

- Sagas and compensating transactions.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://kafka.apache.org/documentation/ · https://microservices.io/patterns/data/transactional-outbox · https://learn.microsoft.com/en-us/azure/architecture/patterns · https://microservices.io/patterns/data/transactional-outbox.html

### 16.4 Sagas, durable work & reconciliation — planned

Prerequisites: ch-16-3

- Choreography vs orchestration.

- Workflow engines.

- Durable job execution.

- Scheduling, leases, and worker coordination.

- Backpressure and replay.

- Reconciliation after partial failure.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://kafka.apache.org/documentation/ · https://microservices.io/patterns/data/transactional-outbox · https://learn.microsoft.com/en-us/azure/architecture/patterns · https://microservices.io/patterns/data/transactional-outbox.html

Essential unit diagrams: Queue lifecycle; consumer partition assignment; Saga happy/failure paths; outbox transaction; event replay

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 17: Reliability, Fault Tolerance, and Disaster Recovery

Status: planned. Prerequisites: [2, 12, 15, 16].

Worked example: A downstream payment provider becomes unavailable during peak traffic. Demonstrate the failure cascade and progressively introduce resilience mechanisms.

### 17.1 Failure domains & redundancy — planned

Prerequisites: unit-2, unit-12, unit-15, unit-16

- Failure domains and fault isolation.

- Availability vs durability.

- Redundancy.

- Active-active vs active-passive.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/reliability.html · https://docs.cloud.google.com/architecture/disaster-recovery · https://sre.google/workbook/table-of-contents/

### 17.2 Retries, circuit breakers & isolation — planned

Prerequisites: ch-17-1

- Timeouts.

- Retries, exponential backoff, jitter.

- Retry storms.

- Circuit breakers.

- Bulkheads.

- Rate limiting.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/reliability.html · https://docs.cloud.google.com/architecture/disaster-recovery · https://sre.google/workbook/table-of-contents/

### 17.3 Shed load and degrade deliberately — planned

Prerequisites: ch-17-2

- Load shedding.

- Graceful degradation.

- Fallbacks.

- Health checking.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/reliability.html · https://docs.cloud.google.com/architecture/disaster-recovery · https://sre.google/workbook/table-of-contents/

### 17.4 Recover, test & learn from failure — planned

Prerequisites: ch-17-3

- RTO and RPO.

- Backups and restore testing.

- Failover and failback.

- Multi-zone and multi-region deployments.

- Chaos engineering.

- SLO-based reliability decisions.

- Cascading failures.

- Incident analysis and prevention.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/reliability.html · https://docs.cloud.google.com/architecture/disaster-recovery · https://sre.google/workbook/table-of-contents/

Essential unit diagrams: Retry amplification timeline; circuit breaker state machine; bulkhead isolation; failure-domain map; RTO/RPO timeline

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 18: Security Architecture and Privacy

Status: planned. Prerequisites: [3, 7, 8, 9].

Worked example: Design a multi-tenant SaaS application where an administrator must never gain access to another organization's data.

### 18.1 Threats, identity & authorization — planned

Prerequisites: unit-3, unit-7, unit-8, unit-9

- Threat modeling.

- Trust boundaries.

- Authentication vs authorization.

- Sessions, cookies, tokens.

- OAuth 2.0 and OpenID Connect.

- Role-based and attribute-based access control.

- Least privilege.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://api-security.owasp.org/editions/2023/en/0x11-t10/ · https://sre.google/books/

### 18.2 Secrets, encryption & trust boundaries — planned

Prerequisites: ch-18-1

- Defense in depth.

- Secrets management.

- Encryption in transit and at rest.

- Password hashing.

- Key management and rotation.

- Network segmentation.

- Zero-trust principles.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://api-security.owasp.org/editions/2023/en/0x11-t10/ · https://sre.google/books/

### 18.3 Tenant isolation, audit & deletion — planned

Prerequisites: ch-18-2

- API security and common vulnerabilities.

- Multi-tenant isolation.

- Data minimization.

- Audit trails.

- Privacy, retention, and deletion.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://api-security.owasp.org/editions/2023/en/0x11-t10/ · https://sre.google/books/

### 18.4 Supply chains and security reviews — planned

Prerequisites: ch-18-3

- Supply-chain security.

- Security vs usability trade-offs.

- Secure-by-design reviews.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://api-security.owasp.org/editions/2023/en/0x11-t10/ · https://sre.google/books/

Essential unit diagrams: Trust-boundary map; authentication sequence; authorization decision flow; tenant-isolation architecture

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 19: Observability, Monitoring, and Incident Engineering

Status: planned. Prerequisites: [2, 3, 4, 10].

Worked example: An API's p99 latency increases from 200 ms to 5 seconds. Use traces, metrics, logs, and database analysis to localize the bottleneck.

### 19.1 Observe behavior with three signals — planned

Prerequisites: unit-2, unit-3, unit-4, unit-10

- Monitoring vs observability.

- Logs, metrics, and traces.

- Structured logging.

- Distributed tracing.

- Trace IDs, span IDs, context propagation.

- Golden signals.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://opentelemetry.io/docs/concepts/ · https://opentelemetry.io/docs/concepts/observability-primer/ · https://sre.google/workbook/table-of-contents/

### 19.2 Choose indicators, budgets & alerts — planned

Prerequisites: ch-19-1

- RED and USE methods.

- SLIs, SLOs, error budgets.

- Alert design and alert fatigue.

- Sampling and telemetry cost.

- Dashboards.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://opentelemetry.io/docs/concepts/ · https://opentelemetry.io/docs/concepts/observability-primer/ · https://sre.google/workbook/table-of-contents/

### 19.3 Profile and investigate production — planned

Prerequisites: ch-19-2

- Profiling.

- Query and application performance diagnosis.

- Incident response.

- On-call and runbooks.

- Root-cause investigation.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://opentelemetry.io/docs/concepts/ · https://opentelemetry.io/docs/concepts/observability-primer/ · https://sre.google/workbook/table-of-contents/

### 19.4 Learn from incidents and trace async work — planned

Prerequisites: ch-19-3

- Blameless postmortems.

- Capacity monitoring.

- Observability across asynchronous workflows.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://opentelemetry.io/docs/concepts/ · https://opentelemetry.io/docs/concepts/observability-primer/ · https://sre.google/workbook/table-of-contents/

Essential unit diagrams: Distributed trace waterfall; request ID propagation; metrics-to-root-cause workflow; error-budget burn chart

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 20: Deployment, Cloud Infrastructure, and Platform Architecture

Status: planned. Prerequisites: [3, 7, 17, 18, 19].

Worked example: Take a single-process application and deploy it into a reliable, observable, multi-instance production environment with safe releases.

### 20.1 Environments, VMs & containers — planned

Prerequisites: unit-3, unit-7, unit-17, unit-18, unit-19

- Development vs staging vs production.

- Virtual machines vs containers.

- Container fundamentals.

- Kubernetes fundamentals.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://kubernetes.io/docs/concepts/overview/components/ · https://12factor.net/ · https://docs.aws.amazon.com/wellarchitected/

### 20.2 Control planes, scheduling & configuration — planned

Prerequisites: ch-20-1

- Control plane vs data plane.

- Scheduling and service discovery.

- Autoscaling.

- Configuration and secret delivery.

- Immutable infrastructure.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://kubernetes.io/docs/concepts/overview/components/ · https://12factor.net/ · https://docs.aws.amazon.com/wellarchitected/

### 20.3 Releases, flags & schema migrations — planned

Prerequisites: ch-20-2

- Infrastructure as Code.

- CI/CD.

- Rolling, blue-green, and canary deployments.

- Feature flags.

- Rollbacks and database migrations.

- Multi-environment configuration.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://kubernetes.io/docs/concepts/overview/components/ · https://12factor.net/ · https://docs.aws.amazon.com/wellarchitected/

### 20.4 Platforms, serverless & ownership — planned

Prerequisites: ch-20-3

- Twelve-Factor App principles.

- Serverless compute.

- Cloud vs on-premises trade-offs.

- Infrastructure ownership and managed services.

- Deployment topologies and networking.

- Platform engineering basics.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://kubernetes.io/docs/concepts/overview/components/ · https://12factor.net/ · https://docs.aws.amazon.com/wellarchitected/

Essential unit diagrams: VM/container comparison; Kubernetes cluster; CI/CD pipeline; blue-green deployment; canary traffic progression

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 21: Performance, Cost Optimization, and System Validation

Status: planned. Prerequisites: [2, 4, 10, 12, 17, 19, 20].

Worked example: Compare three production architectures for a service with variable traffic. Model monthly costs, p99 latency, availability, and operational complexity under explicit assumptions.

### 21.1 Budgets, bottlenecks & honest benchmarks — planned

Prerequisites: unit-2, unit-4, unit-10, unit-12, unit-17, unit-19, unit-20

- Performance budgets.

- CPU, memory, disk, network, and database bottlenecks.

- Profiling and benchmarking.

- Load, stress, spike, and soak testing.

- Benchmark methodology and statistical pitfalls.

- Tail latency analysis.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://docs.aws.amazon.com/wellarchitected/latest/framework/cost-optimization.html · https://martinfowler.com/articles/practical-test-pyramid.html · https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html

### 21.2 Capacity, architecture & cost per outcome — planned

Prerequisites: ch-21-1

- Queue saturation and throughput ceilings.

- Performance tuning vs architecture changes.

- Horizontal scaling economics.

- Compute, storage, networking, and telemetry costs.

- Cost per request or transaction.

- Capacity reservation vs elastic capacity.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://docs.aws.amazon.com/wellarchitected/latest/framework/cost-optimization.html · https://martinfowler.com/articles/practical-test-pyramid.html · https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html

### 21.3 Efficiency and a useful test portfolio — planned

Prerequisites: ch-21-2

- Cost-performance optimization.

- Sustainability and resource efficiency.

- Unit, integration, contract, end-to-end, and performance tests.

- Fault-injection tests.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://docs.aws.amazon.com/wellarchitected/latest/framework/cost-optimization.html · https://martinfowler.com/articles/practical-test-pyramid.html · https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html

### 21.4 Fitness functions and design validation — planned

Prerequisites: ch-21-3

- Data consistency validation.

- Architecture fitness functions.

- Regression testing.

- Evaluating a design against its original requirements.

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://docs.aws.amazon.com/wellarchitected/latest/framework/cost-optimization.html · https://martinfowler.com/articles/practical-test-pyramid.html · https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html

Essential unit diagrams: Performance bottleneck tree; throughput-latency curve; cost breakdown; test pyramid; design decision matrix

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
## Unit 22: End-to-End Design, Architecture Reviews, and Evolution

Status: planned. Prerequisites: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21].

Worked example: Twelve complete architectural designs with a common 22-point review protocol.

### 22.1 URL Shortener — planned

Prerequisites: unit-8, unit-9, unit-11, unit-12

- Functional requirements

- Nonfunctional requirements

- Explicit assumptions and workload numbers

- Naive initial architecture

- Core API contracts

- Data model and schema

- Low-level component organization

- High-level system architecture

- Data and control flows

- Capacity estimates

- End-to-end latency estimates

- Failure scenarios

- Scalability improvements

- Consistency requirements

- Security model

- Deployment approach

- Observability design

- Infrastructure cost considerations

- Alternative architectures and trade-offs

- Architecture evolution from small scale to large scale

- Design review identifying weaknesses and improvements

- A short implementation exercise

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://github.com/ByteByteGoHq/system-design-101 · https://learn.microsoft.com/en-us/azure/architecture/ · https://pdos.csail.mit.edu/6.5840/

### 22.2 Rate Limiter — planned

Prerequisites: unit-2, unit-4, unit-12, unit-17

- Functional requirements

- Nonfunctional requirements

- Explicit assumptions and workload numbers

- Naive initial architecture

- Core API contracts

- Data model and schema

- Low-level component organization

- High-level system architecture

- Data and control flows

- Capacity estimates

- End-to-end latency estimates

- Failure scenarios

- Scalability improvements

- Consistency requirements

- Security model

- Deployment approach

- Observability design

- Infrastructure cost considerations

- Alternative architectures and trade-offs

- Architecture evolution from small scale to large scale

- Design review identifying weaknesses and improvements

- A short implementation exercise

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://github.com/ByteByteGoHq/system-design-101 · https://learn.microsoft.com/en-us/azure/architecture/ · https://pdos.csail.mit.edu/6.5840/

### 22.3 Chat Application — planned

Prerequisites: unit-3, unit-9, unit-14, unit-16

- Functional requirements

- Nonfunctional requirements

- Explicit assumptions and workload numbers

- Naive initial architecture

- Core API contracts

- Data model and schema

- Low-level component organization

- High-level system architecture

- Data and control flows

- Capacity estimates

- End-to-end latency estimates

- Failure scenarios

- Scalability improvements

- Consistency requirements

- Security model

- Deployment approach

- Observability design

- Infrastructure cost considerations

- Alternative architectures and trade-offs

- Architecture evolution from small scale to large scale

- Design review identifying weaknesses and improvements

- A short implementation exercise

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://github.com/ByteByteGoHq/system-design-101 · https://learn.microsoft.com/en-us/azure/architecture/ · https://pdos.csail.mit.edu/6.5840/

### 22.4 Notification Platform — planned

Prerequisites: unit-6, unit-8, unit-16, unit-17

- Functional requirements

- Nonfunctional requirements

- Explicit assumptions and workload numbers

- Naive initial architecture

- Core API contracts

- Data model and schema

- Low-level component organization

- High-level system architecture

- Data and control flows

- Capacity estimates

- End-to-end latency estimates

- Failure scenarios

- Scalability improvements

- Consistency requirements

- Security model

- Deployment approach

- Observability design

- Infrastructure cost considerations

- Alternative architectures and trade-offs

- Architecture evolution from small scale to large scale

- Design review identifying weaknesses and improvements

- A short implementation exercise

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://github.com/ByteByteGoHq/system-design-101 · https://learn.microsoft.com/en-us/azure/architecture/ · https://pdos.csail.mit.edu/6.5840/

### 22.5 Social Media Feed — planned

Prerequisites: unit-9, unit-11, unit-12, unit-16

- Functional requirements

- Nonfunctional requirements

- Explicit assumptions and workload numbers

- Naive initial architecture

- Core API contracts

- Data model and schema

- Low-level component organization

- High-level system architecture

- Data and control flows

- Capacity estimates

- End-to-end latency estimates

- Failure scenarios

- Scalability improvements

- Consistency requirements

- Security model

- Deployment approach

- Observability design

- Infrastructure cost considerations

- Alternative architectures and trade-offs

- Architecture evolution from small scale to large scale

- Design review identifying weaknesses and improvements

- A short implementation exercise

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://github.com/ByteByteGoHq/system-design-101 · https://learn.microsoft.com/en-us/azure/architecture/ · https://pdos.csail.mit.edu/6.5840/

### 22.6 Video Streaming Platform — planned

Prerequisites: unit-3, unit-11, unit-13, unit-20

- Functional requirements

- Nonfunctional requirements

- Explicit assumptions and workload numbers

- Naive initial architecture

- Core API contracts

- Data model and schema

- Low-level component organization

- High-level system architecture

- Data and control flows

- Capacity estimates

- End-to-end latency estimates

- Failure scenarios

- Scalability improvements

- Consistency requirements

- Security model

- Deployment approach

- Observability design

- Infrastructure cost considerations

- Alternative architectures and trade-offs

- Architecture evolution from small scale to large scale

- Design review identifying weaknesses and improvements

- A short implementation exercise

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://github.com/ByteByteGoHq/system-design-101 · https://learn.microsoft.com/en-us/azure/architecture/ · https://pdos.csail.mit.edu/6.5840/

### 22.7 Ride-Hailing System — planned

Prerequisites: unit-9, unit-12, unit-14, unit-16

- Functional requirements

- Nonfunctional requirements

- Explicit assumptions and workload numbers

- Naive initial architecture

- Core API contracts

- Data model and schema

- Low-level component organization

- High-level system architecture

- Data and control flows

- Capacity estimates

- End-to-end latency estimates

- Failure scenarios

- Scalability improvements

- Consistency requirements

- Security model

- Deployment approach

- Observability design

- Infrastructure cost considerations

- Alternative architectures and trade-offs

- Architecture evolution from small scale to large scale

- Design review identifying weaknesses and improvements

- A short implementation exercise

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://github.com/ByteByteGoHq/system-design-101 · https://learn.microsoft.com/en-us/azure/architecture/ · https://pdos.csail.mit.edu/6.5840/

### 22.8 Online Ticket Booking — planned

Prerequisites: unit-8, unit-10, unit-16, unit-18

- Functional requirements

- Nonfunctional requirements

- Explicit assumptions and workload numbers

- Naive initial architecture

- Core API contracts

- Data model and schema

- Low-level component organization

- High-level system architecture

- Data and control flows

- Capacity estimates

- End-to-end latency estimates

- Failure scenarios

- Scalability improvements

- Consistency requirements

- Security model

- Deployment approach

- Observability design

- Infrastructure cost considerations

- Alternative architectures and trade-offs

- Architecture evolution from small scale to large scale

- Design review identifying weaknesses and improvements

- A short implementation exercise

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://github.com/ByteByteGoHq/system-design-101 · https://learn.microsoft.com/en-us/azure/architecture/ · https://pdos.csail.mit.edu/6.5840/

### 22.9 Payment System — planned

Prerequisites: unit-8, unit-10, unit-16, unit-17, unit-18

- Functional requirements

- Nonfunctional requirements

- Explicit assumptions and workload numbers

- Naive initial architecture

- Core API contracts

- Data model and schema

- Low-level component organization

- High-level system architecture

- Data and control flows

- Capacity estimates

- End-to-end latency estimates

- Failure scenarios

- Scalability improvements

- Consistency requirements

- Security model

- Deployment approach

- Observability design

- Infrastructure cost considerations

- Alternative architectures and trade-offs

- Architecture evolution from small scale to large scale

- Design review identifying weaknesses and improvements

- A short implementation exercise

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://github.com/ByteByteGoHq/system-design-101 · https://learn.microsoft.com/en-us/azure/architecture/ · https://pdos.csail.mit.edu/6.5840/

### 22.10 Distributed Job Scheduler — planned

Prerequisites: unit-4, unit-15, unit-16, unit-17

- Functional requirements

- Nonfunctional requirements

- Explicit assumptions and workload numbers

- Naive initial architecture

- Core API contracts

- Data model and schema

- Low-level component organization

- High-level system architecture

- Data and control flows

- Capacity estimates

- End-to-end latency estimates

- Failure scenarios

- Scalability improvements

- Consistency requirements

- Security model

- Deployment approach

- Observability design

- Infrastructure cost considerations

- Alternative architectures and trade-offs

- Architecture evolution from small scale to large scale

- Design review identifying weaknesses and improvements

- A short implementation exercise

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://github.com/ByteByteGoHq/system-design-101 · https://learn.microsoft.com/en-us/azure/architecture/ · https://pdos.csail.mit.edu/6.5840/

### 22.11 Collaborative Document Editor — planned

Prerequisites: unit-3, unit-14, unit-15, unit-16

- Functional requirements

- Nonfunctional requirements

- Explicit assumptions and workload numbers

- Naive initial architecture

- Core API contracts

- Data model and schema

- Low-level component organization

- High-level system architecture

- Data and control flows

- Capacity estimates

- End-to-end latency estimates

- Failure scenarios

- Scalability improvements

- Consistency requirements

- Security model

- Deployment approach

- Observability design

- Infrastructure cost considerations

- Alternative architectures and trade-offs

- Architecture evolution from small scale to large scale

- Design review identifying weaknesses and improvements

- A short implementation exercise

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://github.com/ByteByteGoHq/system-design-101 · https://learn.microsoft.com/en-us/azure/architecture/ · https://pdos.csail.mit.edu/6.5840/

### 22.12 Large-Scale Document Processing Platform — planned

Prerequisites: unit-13, unit-16, unit-17, unit-18, unit-19, unit-20

- Functional requirements

- Nonfunctional requirements

- Explicit assumptions and workload numbers

- Naive initial architecture

- Core API contracts

- Data model and schema

- Low-level component organization

- High-level system architecture

- Data and control flows

- Capacity estimates

- End-to-end latency estimates

- Failure scenarios

- Scalability improvements

- Consistency requirements

- Security model

- Deployment approach

- Observability design

- Infrastructure cost considerations

- Alternative architectures and trade-offs

- Architecture evolution from small scale to large scale

- Design review identifying weaknesses and improvements

- A short implementation exercise

Illustrations: A — simplest working arrangement; B — failure or limiting assumption; C — revised mechanism and cost; Execution trace and alternatives

Starting references: https://github.com/donnemartin/system-design-primer · https://github.com/ByteByteGoHq/system-design-101 · https://learn.microsoft.com/en-us/azure/architecture/ · https://pdos.csail.mit.edu/6.5840/

Essential unit diagrams: 

Assessment: 5 conceptual + 3 scenario + design + implementation + thought experiment; separate explained solutions. planned.
