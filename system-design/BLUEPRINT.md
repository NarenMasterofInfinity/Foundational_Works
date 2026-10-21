# The System Design Atlas — complete book blueprint

Complete first edition: all 22 units and all 12 mandatory case studies produced

A complete illustrated reference edition. Workload, latency, capacity and price examples are explicitly assumed models; code examples demonstrate bounded mechanisms rather than production infrastructure.

## Unit 1: Introduction to System Design

Status: available. Direct prerequisites: [].

Worked example: Design a basic to-do application. Begin with a single program and progressively identify modules, persistent storage, a web API, and deployment boundaries.

### 1.1 From a program to a system — available

Content source: src/chapter-1.html

- What is a software system?

- What does it mean to design a system?

- HLD vs LLD vs software architecture.

- Components, boundaries, interfaces, and contracts.

- State, data, computation, and communication.

Figures: 1.1.1 The application and storage work together; 1.1.2 Creating a task changes the stored state; 1.1.3 Save before reporting success; 1.1.4 Two levels of detail in one design

References: https://www.sqlite.org/atomiccommit.html · https://www.rfc-editor.org/rfc/rfc9110.html

### 1.2 Organising code into modules — available

Content source: src/chapter-2.html

- Coupling, cohesion, modularity, separation of concerns.

- Abstraction layers.

Figures: 1.2.1 Shared storage details make changes spread; 1.2.2 Separate responsibilities inside one process; 1.2.3 The service uses a repository contract; 1.2.4 Each layer works at a different level of detail

References: https://doi.org/10.1145/361598.361623 · https://martinfowler.com/articles/injection.html

### 1.3 From requirements to design choices — available

Content source: src/chapter-3.html

- Functional and nonfunctional requirements.

- Constraints, assumptions, risks, and trade-offs.

- Architectural characteristics and quality attributes.

- Architecture Decision Records (ADRs).

- Why the simplest sufficient design is often preferable.

Figures: 1.3.1 Turn “safe” into a checkable requirement; 1.3.2 Choose, record, and review a design; 1.3.3 Check requirements before scoring preferences; 1.3.4 Availability and durability answer different questions

References: https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions · https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html

### 1.4 Drawing the system at different levels — available

Content source: src/chapter-4.html

- Architecture diagrams: C4 model, context, container, component, deployment, sequence.

Figures: 1.4.1 C4: zoom from the system into its code; 1.4.2 The application and database share one machine; 1.4.3 The task is saved, but the reply is lost; 1.4.4 Each design change answers a new need

References: https://c4model.com/diagrams · https://c4model.com/abstractions/container · https://www.rfc-editor.org/rfc/rfc9110.html

Assessment: all eleven questions and separate explained solutions produced.
## Unit 2: Requirements, Estimation, and Engineering Trade-offs

Status: available. Direct prerequisites: [1].

Worked example: A social platform has 10 million daily active users. Estimate requests per second, traffic at peak, storage growth, image bandwidth, and approximate infrastructure requirements.

### 2.1 Turn user journeys into workloads — available

Content source: src/teaching/foundations.py

- Gathering and prioritizing requirements.

- User journeys and workload characteristics.

- Read-heavy vs write-heavy systems.

Figures: 2.1.1 Gathering and prioritizing requirements · worked snapshots; 2.1.2 User journeys and workload characteristics · worked snapshots; 2.1.3 Read-heavy vs write-heavy systems · worked snapshots; 2.1.4 The running system · invariant and recovery review

References: https://sre.google/workbook/implementing-slos/ · https://doi.org/10.1287/opre.9.3.383 · https://research.google/pubs/the-tail-at-scale/

### 2.2 Measure the experience — available

Content source: src/teaching/foundations.py

- Latency, throughput, QPS, RPS, TPS.

- Average vs median vs p95/p99 latency.

- Availability, reliability, durability, consistency.

- SLI, SLO, SLA, and error budgets.

Figures: 2.2.1 Latency, throughput, QPS, RPS, TPS · worked snapshots; 2.2.2 A small mean can hide one slow request; 2.2.3 Availability, reliability, durability, consistency · worked snapshots; 2.2.4 SLI, SLO, SLA, and error budgets · worked snapshots

References: https://sre.google/workbook/implementing-slos/ · https://doi.org/10.1287/opre.9.3.383 · https://research.google/pubs/the-tail-at-scale/

### 2.3 Estimate the resources — available

Content source: src/teaching/foundations.py

- Capacity and growth planning.

- Storage, memory, bandwidth, and CPU estimates.

- Peak vs average load.

Figures: 2.3.1 Capacity and growth planning · worked snapshots; 2.3.2 Different workload dimensions have different magnitudes; 2.3.3 Peak vs average load · worked snapshots; 2.3.4 The running system · invariant and recovery review

References: https://sre.google/workbook/implementing-slos/ · https://doi.org/10.1287/opre.9.3.383 · https://research.google/pubs/the-tail-at-scale/

### 2.4 Queues, bottlenecks & defensible decisions — available

Content source: src/teaching/foundations.py

- Little's Law and queueing intuition.

- Amdahl's Law and bottlenecks.

- Tail latency and latency budgets.

- Cost, security, operational complexity, and maintainability as constraints.

- Decision matrices and trade-off analysis.

Figures: 2.4.1 Little's Law and queueing intuition · worked snapshots; 2.4.2 Amdahl's Law and bottlenecks · worked snapshots; 2.4.3 Tail latency and latency budgets · worked snapshots; 2.4.4 Cost, security, operational complexity, and maintainability as constraints · worked snapshots; 2.4.5 Decision matrices and trade-off analysis · worked snapshots

References: https://sre.google/workbook/implementing-slos/ · https://doi.org/10.1287/opre.9.3.383 · https://research.google/pubs/the-tail-at-scale/

Assessment: all eleven questions and separate explained solutions produced.
## Unit 3: Networking Foundations for System Design

Status: available. Direct prerequisites: [1].

Worked example: Trace what happens when someone enters a website URL, from DNS lookup through server execution to browser rendering.

### 3.1 Addresses, sockets & transports — available

Content source: src/teaching/foundations.py

- How the internet works from the application perspective.

- IP addresses, ports, sockets, routing.

- TCP vs UDP vs QUIC.

Figures: 3.1.1 How the internet works from the application perspective · worked snapshots; 3.1.2 IP addresses, ports, sockets, routing · worked snapshots; 3.1.3 TCP vs UDP vs QUIC · worked snapshots; 3.1.4 The running system · invariant and recovery review

References: https://www.rfc-editor.org/rfc/rfc9110.html · https://www.rfc-editor.org/rfc/rfc9000.html · https://www.rfc-editor.org/rfc/rfc8446.html

### 3.2 A secure request, one round trip at a time — available

Content source: src/teaching/foundations.py

- DNS resolution and DNS caching.

- TLS and HTTPS.

- HTTP/1.1, HTTP/2, HTTP/3.

- Connection establishment and connection reuse.

- Latency caused by network round trips.

Figures: 3.2.1 DNS resolution and DNS caching · worked snapshots; 3.2.2 TLS and HTTPS · worked snapshots; 3.2.3 HTTP/1.1, HTTP/2, HTTP/3 · worked snapshots; 3.2.4 Connection establishment and connection reuse · worked snapshots; 3.2.5 A cold request spends time before server work

References: https://www.rfc-editor.org/rfc/rfc9110.html · https://www.rfc-editor.org/rfc/rfc9000.html · https://www.rfc-editor.org/rfc/rfc8446.html

### 3.3 Intermediaries & persistent connections — available

Content source: src/teaching/foundations.py

- Reverse proxies vs forward proxies.

- Load balancers vs API gateways.

- L4 vs L7 load balancing.

- WebSockets, Server-Sent Events, and polling.

Figures: 3.3.1 Reverse proxies vs forward proxies · worked snapshots; 3.3.2 Load balancers vs API gateways · worked snapshots; 3.3.3 L4 vs L7 load balancing · worked snapshots; 3.3.4 WebSockets, Server-Sent Events, and polling · worked snapshots

References: https://www.rfc-editor.org/rfc/rfc9110.html · https://www.rfc-editor.org/rfc/rfc9000.html · https://www.rfc-editor.org/rfc/rfc8446.html

### 3.4 Discover, route & survive the network — available

Content source: src/teaching/foundations.py

- NAT, firewalls, ingress, egress.

- Service discovery.

- CDN and edge networking.

- Network partitions, timeouts, packet loss.

- Connection pooling and keepalive.

Figures: 3.4.1 NAT, firewalls, ingress, egress · worked snapshots; 3.4.2 Service discovery · worked snapshots; 3.4.3 CDN and edge networking · worked snapshots; 3.4.4 Network partitions, timeouts, packet loss · worked snapshots; 3.4.5 Connection pooling and keepalive · worked snapshots

References: https://www.rfc-editor.org/rfc/rfc9110.html · https://www.rfc-editor.org/rfc/rfc9000.html · https://www.rfc-editor.org/rfc/rfc8446.html

Assessment: all eleven questions and separate explained solutions produced.
## Unit 4: Runtime, Processes, Threads, and Concurrency

Status: available. Direct prerequisites: [1].

Worked example: Build a service that processes 1,000 file uploads. Compare sequential execution, threads, asynchronous I/O, and worker queues. Identify which architecture helps under which workload.

### 4.1 The runtime owns your resources — available

Content source: src/teaching/foundations.py

- Program vs process vs thread.

- Memory, stack, heap, and object lifetimes.

- Scheduling and context switching.

- CPU-bound vs I/O-bound workloads.

- Synchronous vs asynchronous execution.

Figures: 4.1.1 Threads share a heap but have execution-local stacks; 4.1.2 Memory, stack, heap, and object lifetimes · worked snapshots; 4.1.3 Scheduling and context switching · worked snapshots; 4.1.4 CPU-bound vs I/O-bound workloads · worked snapshots; 4.1.5 Synchronous vs asynchronous execution · worked snapshots

References: https://pages.cs.wisc.edu/~remzi/OSTEP/ · https://go.dev/ref/mem

### 4.2 Tasks, threads & event loops — available

Content source: src/teaching/foundations.py

- Blocking vs nonblocking I/O.

- Concurrency vs parallelism.

- Event loops, tasks, futures, promises.

- Thread pools and worker pools.

Figures: 4.2.1 Blocking vs nonblocking I/O · worked snapshots; 4.2.2 Concurrency vs parallelism · worked snapshots; 4.2.3 Event loops, tasks, futures, promises · worked snapshots; 4.2.4 Thread pools and worker pools · worked snapshots

References: https://pages.cs.wisc.edu/~remzi/OSTEP/ · https://go.dev/ref/mem

### 4.3 Shared memory & coordination — available

Content source: src/teaching/foundations.py

- Shared memory vs message passing.

- Race conditions and critical sections.

- Mutexes, semaphores, atomics, condition variables.

- Deadlocks, starvation, livelocks.

Figures: 4.3.1 Shared memory vs message passing · worked snapshots; 4.3.2 Race conditions and critical sections · worked snapshots; 4.3.3 Mutexes, semaphores, atomics, condition variables · worked snapshots; 4.3.4 A circular wait prevents both participants progressing

References: https://pages.cs.wisc.edu/~remzi/OSTEP/ · https://go.dev/ref/mem

### 4.4 Visibility, cancellation & overload — available

Content source: src/teaching/foundations.py

- Memory visibility and happens-before relationships.

- Thread safety and immutability.

- Resource exhaustion and backpressure.

- Cancellation and structured concurrency.

Figures: 4.4.1 Memory visibility and happens-before relationships · worked snapshots; 4.4.2 Thread safety and immutability · worked snapshots; 4.4.3 Resource exhaustion and backpressure · worked snapshots; 4.4.4 Cancellation and structured concurrency · worked snapshots

References: https://pages.cs.wisc.edu/~remzi/OSTEP/ · https://go.dev/ref/mem

Assessment: all eleven questions and separate explained solutions produced.
## Unit 5: Object-Oriented and Modular Software Design

Status: available. Direct prerequisites: [1].

Worked example: Start with a poorly designed payment-processing class. Refactor it into appropriate components, showing which problems each design improvement solves.

### 5.1 Model behavior with objects and values — available

Content source: src/teaching/lld.py

- Abstraction, encapsulation, polymorphism, inheritance.

- Composition vs inheritance.

- Interfaces and contracts.

- High cohesion and low coupling.

- SOLID principles, including their limitations.

Figures: 5.1.1 Abstraction, encapsulation, polymorphism, inheritance · worked snapshots; 5.1.2 Composition vs inheritance · worked snapshots; 5.1.3 Interfaces and contracts · worked snapshots; 5.1.4 High cohesion and low coupling · worked snapshots; 5.1.5 SOLID principles, including their limitations · worked snapshots

References: https://doi.org/10.1145/361598.361623 · https://refactoring.guru/design-patterns/catalog

### 5.2 Principles under pressure — available

Content source: src/teaching/lld.py

- DRY, KISS, YAGNI.

- Law of Demeter.

- Tell, Don't Ask.

- Command-query separation.

Figures: 5.2.1 DRY, KISS, YAGNI · worked snapshots; 5.2.2 Law of Demeter · worked snapshots; 5.2.3 Tell, Don't Ask · worked snapshots; 5.2.4 Command-query separation · worked snapshots

References: https://doi.org/10.1145/361598.361623 · https://refactoring.guru/design-patterns/catalog

### 5.3 Side effects, domain models & collaboration — available

Content source: src/teaching/lld.py

- Immutability and side-effect management.

- Domain models, entities, value objects.

- Object collaboration.

- Testability and design for change.

Figures: 5.3.1 Immutability and side-effect management · worked snapshots; 5.3.2 Domain models, entities, value objects · worked snapshots; 5.3.3 Object collaboration · worked snapshots; 5.3.4 Testability and design for change · worked snapshots

References: https://doi.org/10.1145/361598.361623 · https://refactoring.guru/design-patterns/catalog

### 5.4 Design for change, testing & functions — available

Content source: src/teaching/lld.py

- Refactoring and recognizing code smells.

- Functional programming alternatives to object-centric design.

Figures: 5.4.1 Refactoring and recognizing code smells · worked snapshots; 5.4.2 Functional programming alternatives to object-centric design · worked snapshots; 5.4.3 The running system · ordered responsibility; 5.4.4 The running system · invariant and recovery review

References: https://doi.org/10.1145/361598.361623 · https://refactoring.guru/design-patterns/catalog

Assessment: all eleven questions and separate explained solutions produced.
## Unit 6: Design Patterns, Dependency Injection, and Object Lifecycles

Status: available. Direct prerequisites: [5].

Worked example: Create a notification platform supporting email, SMS, and push notifications. Evolve it from hardcoded classes to DI, Strategy, Factory, and Decorator patterns.

### 6.1 Dependencies, inversion & composition — available

Content source: src/teaching/lld.py

- Dependency, dependency direction, and inversion.

- Inversion of Control (IoC).

- Dependency Injection (DI).

- Constructor, property/setter, and method injection.

- Dependency inversion principle vs DI.

- Composition roots and DI containers.

Figures: 6.1.1 Dependency, dependency direction, and inversion · worked snapshots; 6.1.2 Inversion of Control (IoC) · worked snapshots; 6.1.3 Dependency Injection (DI) · worked snapshots; 6.1.4 Constructor, property/setter, and method injection · worked snapshots; 6.1.5 Dependency inversion principle vs DI · worked snapshots; 6.1.6 Composition roots and DI containers · worked snapshots

References: https://martinfowler.com/articles/injection.html · https://refactoring.guru/design-patterns/catalog

### 6.2 Lifetimes, ownership & cleanup — available

Content source: src/teaching/lld.py

- Transient, scoped, singleton, and framework-specific lifetimes.

- Request scopes, session scopes, and custom scopes.

- Object creation vs object ownership.

- Disposal, cleanup, and resource lifecycles.

- Lazy initialization.

- Dependency cycles and captive dependencies.

Figures: 6.2.1 Scope identities make lifetime semantics visible; 6.2.2 Request scopes, session scopes, and custom scopes · worked snapshots; 6.2.3 Object creation vs object ownership · worked snapshots; 6.2.4 Disposal, cleanup, and resource lifecycles · worked snapshots; 6.2.5 Lazy initialization · worked snapshots; 6.2.6 Dependency cycles and captive dependencies · worked snapshots

References: https://martinfowler.com/articles/injection.html · https://refactoring.guru/design-patterns/catalog

### 6.3 Injection, locators & factories — available

Content source: src/teaching/lld.py

- DI vs service locator.

- DI vs factory pattern.

Figures: 6.3.1 DI vs service locator · worked snapshots; 6.3.2 DI vs factory pattern · worked snapshots; 6.3.3 The running system · ordered responsibility; 6.3.4 The running system · invariant and recovery review

References: https://martinfowler.com/articles/injection.html · https://refactoring.guru/design-patterns/catalog

### 6.4 Creational patterns — available

Content source: src/teaching/lld.py

- Factory Method, Abstract Factory, Builder, Prototype, Singleton.

Figures: 6.4.1 Factory Method, Abstract Factory, Builder, Prototype, Singleton · worked snapshots; 6.4.2 Factory Method · collaborator roles; 6.4.3 Abstract Factory · collaborator roles; 6.4.4 Builder · collaborator roles; 6.4.5 Prototype · collaborator roles; 6.4.6 Singleton · collaborator roles

References: https://martinfowler.com/articles/injection.html · https://refactoring.guru/design-patterns/catalog

### 6.5 Structural patterns — available

Content source: src/teaching/lld.py

- Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy.

Figures: 6.5.1 Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy · worked snapshots; 6.5.2 Adapter · collaborator roles; 6.5.3 Bridge · collaborator roles; 6.5.4 Composite · collaborator roles; 6.5.5 Decorator · collaborator roles; 6.5.6 Facade · collaborator roles; 6.5.7 Flyweight · collaborator roles; 6.5.8 Proxy · collaborator roles

References: https://martinfowler.com/articles/injection.html · https://refactoring.guru/design-patterns/catalog

### 6.6 Behavioral patterns — available

Content source: src/teaching/lld.py

- Strategy, Observer, Command, State, Chain of Responsibility, Template Method, Iterator, Mediator, Memento, Visitor.

Figures: 6.6.1 Strategy, Observer, Command, State, Chain of Responsibility, Template Method, Iterator, Mediator, Memento, Visitor · worked snapshots; 6.6.2 Strategy · collaborator roles; 6.6.3 Observer · collaborator roles; 6.6.4 Command · collaborator roles; 6.6.5 State · collaborator roles; 6.6.6 Chain of Responsibility · collaborator roles; 6.6.7 Template Method · collaborator roles; 6.6.8 Iterator · collaborator roles; 6.6.9 Mediator · collaborator roles; 6.6.10 Memento · collaborator roles; 6.6.11 Visitor · collaborator roles

References: https://martinfowler.com/articles/injection.html · https://refactoring.guru/design-patterns/catalog

### 6.7 Enterprise patterns & boundaries — available

Content source: src/teaching/lld.py

- Repository, Unit of Work, Specification, CQRS, and dependency boundaries.

Figures: 6.7.1 Repository, Unit of Work, Specification, CQRS, and dependency boundaries · worked snapshots; 6.7.2 Repository · collaborator roles; 6.7.3 Unit of Work · collaborator roles; 6.7.4 Specification · collaborator roles; 6.7.5 CQRS · collaborator roles

References: https://martinfowler.com/articles/injection.html · https://refactoring.guru/design-patterns/catalog

Assessment: all eleven questions and separate explained solutions produced.
## Unit 7: Application Architecture and Domain-Driven Design

Status: available. Direct prerequisites: [5, 6].

Worked example: Design an online shopping application first as a modular monolith, then examine the conditions under which selected domains should become independent services.

### 7.1 Layers, monoliths & ports — available

Content source: src/teaching/lld.py

- Layered/N-tier architecture.

- Modular monoliths.

- Monolith vs microservices.

- Clean Architecture.

- Hexagonal/Ports and Adapters.

- Onion Architecture.

Figures: 7.1.1 Layered/N-tier architecture · worked snapshots; 7.1.2 Modular monoliths · worked snapshots; 7.1.3 Monolith vs microservices · worked snapshots; 7.1.4 Clean Architecture · worked snapshots; 7.1.5 Hexagonal/Ports and Adapters · worked snapshots; 7.1.6 Onion Architecture · worked snapshots

References: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/ · https://martinfowler.com/bliki/BoundedContext.html · https://martinfowler.com/articles/microservices.html

### 7.2 Model a bounded context — available

Content source: src/teaching/lld.py

- Domain-Driven Design (DDD).

- Bounded contexts and ubiquitous language.

- Aggregates, entities, value objects, domain services.

- Domain events.

Figures: 7.2.1 Domain-Driven Design (DDD) · worked snapshots; 7.2.2 Context boundaries protect different business meanings; 7.2.3 Aggregates, entities, value objects, domain services · worked snapshots; 7.2.4 Domain events · worked snapshots

References: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/ · https://martinfowler.com/bliki/BoundedContext.html · https://martinfowler.com/articles/microservices.html

### 7.3 Keep business policy inside — available

Content source: src/teaching/lld.py

- Dependency rules and module boundaries.

- Business logic vs orchestration vs infrastructure.

- Controllers, services, repositories, adapters.

- Anti-corruption layers.

- Event-driven architecture.

Figures: 7.3.1 Dependency rules and module boundaries · worked snapshots; 7.3.2 Business logic vs orchestration vs infrastructure · worked snapshots; 7.3.3 Controllers, services, repositories, adapters · worked snapshots; 7.3.4 Anti-corruption layers · worked snapshots; 7.3.5 Event-driven architecture · worked snapshots

References: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/ · https://martinfowler.com/bliki/BoundedContext.html · https://martinfowler.com/articles/microservices.html

### 7.4 Evolution without a distributed monolith — available

Content source: src/teaching/lld.py

- Serverless and function-oriented architectures.

- Evolutionary architecture.

- Technical vs business boundaries.

- Distributed monolith antipattern.

- When not to use microservices.

Figures: 7.4.1 Serverless and function-oriented architectures · worked snapshots; 7.4.2 Evolutionary architecture · worked snapshots; 7.4.3 Technical vs business boundaries · worked snapshots; 7.4.4 Distributed monolith antipattern · worked snapshots; 7.4.5 When not to use microservices · worked snapshots

References: https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/ · https://martinfowler.com/bliki/BoundedContext.html · https://martinfowler.com/articles/microservices.html

Assessment: all eleven questions and separate explained solutions produced.
## Unit 8: API Design and Communication Contracts

Status: available. Direct prerequisites: [1, 3].

Worked example: Design a payment API with create-payment, payment-status, refunds, idempotency protection, duplicate requests, and failed network responses.

### 8.1 Model resources and messages — available

Content source: src/teaching/lld.py

- API fundamentals and interface contracts.

- REST, GraphQL, gRPC, RPC.

- Resource modeling.

- Request/response schemas.

- Status codes and error models.

- Pagination, filtering, sorting.

Figures: 8.1.1 API fundamentals and interface contracts · worked snapshots; 8.1.2 REST, GraphQL, gRPC, RPC · worked snapshots; 8.1.3 Resource modeling · worked snapshots; 8.1.4 Request/response schemas · worked snapshots; 8.1.5 Status codes and error models · worked snapshots; 8.1.6 Pagination, filtering, sorting · worked snapshots

References: https://www.rfc-editor.org/rfc/rfc9110.html · https://api-security.owasp.org/editions/2023/en/0x11-t10/ · https://www.rfc-editor.org/rfc/rfc9700.html

### 8.2 Compatibility & idempotency — available

Content source: src/teaching/lld.py

- Cursor vs offset pagination.

- API versioning and compatibility.

- Idempotency and idempotency keys.

Figures: 8.2.1 Cursor vs offset pagination · worked snapshots; 8.2.2 API versioning and compatibility · worked snapshots; 8.2.3 A payment retry follows durable operation identity; 8.2.4 The running system · invariant and recovery review

References: https://www.rfc-editor.org/rfc/rfc9110.html · https://api-security.owasp.org/editions/2023/en/0x11-t10/ · https://www.rfc-editor.org/rfc/rfc9700.html

### 8.3 Control access, load & long operations — available

Content source: src/teaching/lld.py

- Authentication vs authorization at API boundaries.

- Rate limits and quotas.

- Retries and timeouts.

- Streaming APIs and long-running operations.

- Webhooks and delivery acknowledgments.

Figures: 8.3.1 Authentication vs authorization at API boundaries · worked snapshots; 8.3.2 Rate limits and quotas · worked snapshots; 8.3.3 Retries and timeouts · worked snapshots; 8.3.4 Streaming APIs and long-running operations · worked snapshots; 8.3.5 Webhooks and delivery acknowledgments · worked snapshots

References: https://www.rfc-editor.org/rfc/rfc9110.html · https://api-security.owasp.org/editions/2023/en/0x11-t10/ · https://www.rfc-editor.org/rfc/rfc9700.html

### 8.4 Evolve a public contract — available

Content source: src/teaching/lld.py

- Schema evolution.

- Consumer-driven contracts.

- API gateways and BFF.

- Public vs internal APIs.

- API documentation and discoverability.

Figures: 8.4.1 Schema evolution · worked snapshots; 8.4.2 Consumer-driven contracts · worked snapshots; 8.4.3 API gateways and BFF · worked snapshots; 8.4.4 Public vs internal APIs · worked snapshots; 8.4.5 API documentation and discoverability · worked snapshots

References: https://www.rfc-editor.org/rfc/rfc9110.html · https://api-security.owasp.org/editions/2023/en/0x11-t10/ · https://www.rfc-editor.org/rfc/rfc9700.html

Assessment: all eleven questions and separate explained solutions produced.
## Unit 9: Data Models and Storage Technologies

Status: available. Direct prerequisites: [1].

Worked example: Choose storage technologies for user profiles, financial transactions, chat messages, event logs, and uploaded PDFs. Justify each decision.

### 9.1 Storage promises & database families — available

Content source: src/teaching/data.py

- What data storage must guarantee.

- Relational databases and SQL.

- Document databases.

- Key-value databases.

- Wide-column stores.

- Graph databases.

- Time-series databases.

- Search indexes.

- Vector indexes: introductory architecture only.

Figures: 9.1.1 What data storage must guarantee · worked snapshots; 9.1.2 Relational databases and SQL · worked snapshots; 9.1.3 Document databases · worked snapshots; 9.1.4 Key-value databases · worked snapshots; 9.1.5 Wide-column stores · worked snapshots; 9.1.6 Graph databases · worked snapshots; 9.1.7 Time-series databases · worked snapshots; 9.1.8 Search indexes · worked snapshots; 9.1.9 Vector indexes: introductory architecture only · worked snapshots

References: https://db.cs.cmu.edu/courses/ · https://www.postgresql.org/docs/18/indexes-types.html

### 9.2 Files, objects & analytical layouts — available

Content source: src/teaching/data.py

- Object storage vs block vs file storage.

- OLTP vs OLAP.

- Row-oriented vs column-oriented storage.

- Normalization vs denormalization.

Figures: 9.2.1 Object storage vs block vs file storage · worked snapshots; 9.2.2 OLTP vs OLAP · worked snapshots; 9.2.3 Row-oriented vs column-oriented storage · worked snapshots; 9.2.4 Normalization vs denormalization · worked snapshots

References: https://db.cs.cmu.edu/courses/ · https://www.postgresql.org/docs/18/indexes-types.html

### 9.3 Model relationships and ownership — available

Content source: src/teaching/data.py

- ER diagrams and relational modeling.

- Referential integrity.

- Data ownership.

- Choosing storage based on access patterns.

Figures: 9.3.1 An order schema preserves relationships and history; 9.3.2 Referential integrity · worked snapshots; 9.3.3 Data ownership · worked snapshots; 9.3.4 Choosing storage based on access patterns · worked snapshots

References: https://db.cs.cmu.edu/courses/ · https://www.postgresql.org/docs/18/indexes-types.html

### 9.4 Access patterns, retention & operational cost — available

Content source: src/teaching/data.py

- Data retention and lifecycle.

- Polyglot persistence and its operational costs.

Figures: 9.4.1 Data retention and lifecycle · worked snapshots; 9.4.2 Polyglot persistence and its operational costs · worked snapshots; 9.4.3 The running system · ordered responsibility; 9.4.4 The running system · invariant and recovery review

References: https://db.cs.cmu.edu/courses/ · https://www.postgresql.org/docs/18/indexes-types.html

Assessment: all eleven questions and separate explained solutions produced.
## Unit 10: Database Internals, Transactions, and Concurrency Control

Status: available. Direct prerequisites: [4, 9].

Worked example: Two users attempt to purchase the last available ticket. Demonstrate the lost-update race, show why naive reads fail, and implement valid alternatives using transactions and concurrency control.

### 10.1 Pages, indexes & query plans — available

Content source: src/teaching/data.py

- How databases store and retrieve records.

- Pages, records, indexes, and buffer pools.

- B-tree/B+tree and hash indexing.

- LSM trees and write amplification.

- Query planning and EXPLAIN.

- Index selection and query optimization.

Figures: 10.1.1 How databases store and retrieve records · worked snapshots; 10.1.2 Pages, records, indexes, and buffer pools · worked snapshots; 10.1.3 B+tree lookup narrows an ordered key range; 10.1.4 LSM trees and write amplification · worked snapshots; 10.1.5 Query planning and EXPLAIN · worked snapshots; 10.1.6 Index selection and query optimization · worked snapshots

References: https://www.postgresql.org/docs/18/transaction-iso.html · https://www.postgresql.org/docs/18/indexes-types.html · https://www.postgresql.org/docs/18/wal-intro.html · https://github.com/facebook/rocksdb/wiki/RocksDB-Overview

### 10.2 Commit, logging & versions — available

Content source: src/teaching/data.py

- ACID properties.

- Transaction commit and rollback.

- Write-ahead logging.

- MVCC.

Figures: 10.2.1 ACID properties · worked snapshots; 10.2.2 Transaction commit and rollback · worked snapshots; 10.2.3 Write-ahead logging · worked snapshots; 10.2.4 Two snapshots can legitimately see different versions

References: https://www.postgresql.org/docs/18/transaction-iso.html · https://www.postgresql.org/docs/18/indexes-types.html · https://www.postgresql.org/docs/18/wal-intro.html · https://github.com/facebook/rocksdb/wiki/RocksDB-Overview

### 10.3 Races, anomalies & isolation — available

Content source: src/teaching/data.py

- Locking and optimistic concurrency control.

- Dirty reads, nonrepeatable reads, phantom reads.

- Lost updates, write skew, serialization anomalies.

- Isolation levels and implementation differences.

- Serializable execution and serializability.

Figures: 10.3.1 Locking and optimistic concurrency control · worked snapshots; 10.3.2 Dirty reads, nonrepeatable reads, phantom reads · worked snapshots; 10.3.3 Lost updates, write skew, serialization anomalies · worked snapshots; 10.3.4 Isolation levels and implementation differences · worked snapshots; 10.3.5 Serializable execution and serializability · worked snapshots

References: https://www.postgresql.org/docs/18/transaction-iso.html · https://www.postgresql.org/docs/18/indexes-types.html · https://www.postgresql.org/docs/18/wal-intro.html · https://github.com/facebook/rocksdb/wiki/RocksDB-Overview

### 10.4 Pools, recovery & ticket correctness — available

Content source: src/teaching/data.py

- Database connection pooling.

- Transactions across multiple operations.

- Backup, recovery, and durability.

Figures: 10.4.1 Database connection pooling · worked snapshots; 10.4.2 Transactions across multiple operations · worked snapshots; 10.4.3 Backup, recovery, and durability · worked snapshots; 10.4.4 The running system · invariant and recovery review

References: https://www.postgresql.org/docs/18/transaction-iso.html · https://www.postgresql.org/docs/18/indexes-types.html · https://www.postgresql.org/docs/18/wal-intro.html · https://github.com/facebook/rocksdb/wiki/RocksDB-Overview

Assessment: all eleven questions and separate explained solutions produced.
## Unit 11: Caching and Content Delivery

Status: available. Direct prerequisites: [3, 9].

Worked example: A popular product page receives enormous traffic. Introduce caching gradually and examine stale prices, thundering herds, inventory correctness, and failure behavior.

### 11.1 Locality and cache placement — available

Content source: src/teaching/data.py

- Why caching works.

- Cache locality and the working set.

- In-process vs distributed caches.

- Browser, CDN, application, and database caches.

Figures: 11.1.1 Why caching works · worked snapshots; 11.1.2 Cache locality and the working set · worked snapshots; 11.1.3 In-process vs distributed caches · worked snapshots; 11.1.4 Browser, CDN, application, and database caches · worked snapshots

References: https://www.rfc-editor.org/rfc/rfc9111.html · https://redis.io/docs/latest/develop/reference/eviction/ · https://www.cloudflare.com/learning/cdn/what-is-a-cdn/

### 11.2 Copies, freshness & eviction — available

Content source: src/teaching/data.py

- Cache-aside, read-through, write-through, write-behind.

- TTL and cache expiration.

- Cache consistency and invalidation.

- Eviction: LRU, LFU, FIFO, and alternatives.

Figures: 11.2.1 Cache-aside, read-through, write-through, write-behind · worked snapshots; 11.2.2 TTL and cache expiration · worked snapshots; 11.2.3 A stale cache is a separate state copy; 11.2.4 LRU and FIFO disagree after the same accesses

References: https://www.rfc-editor.org/rfc/rfc9111.html · https://redis.io/docs/latest/develop/reference/eviction/ · https://www.cloudflare.com/learning/cdn/what-is-a-cdn/

### 11.3 Hot keys, stampedes & negative results — available

Content source: src/teaching/data.py

- Hot keys.

- Cache stampedes, penetration, and avalanche.

- Negative caching.

- Stale-while-revalidate.

- Cache warming and prefetching.

Figures: 11.3.1 Hot keys · worked snapshots; 11.3.2 Cache stampedes, penetration, and avalanche · worked snapshots; 11.3.3 Negative caching · worked snapshots; 11.3.4 Stale-while-revalidate · worked snapshots; 11.3.5 Cache warming and prefetching · worked snapshots

References: https://www.rfc-editor.org/rfc/rfc9111.html · https://redis.io/docs/latest/develop/reference/eviction/ · https://www.cloudflare.com/learning/cdn/what-is-a-cdn/

### 11.4 Edges, partitions & the price of a cache — available

Content source: src/teaching/data.py

- Redis-like data structures.

- CDN architecture and origin shielding.

- Cache partitioning and replication.

- When caching is harmful.

Figures: 11.4.1 Redis-like data structures · worked snapshots; 11.4.2 CDN architecture and origin shielding · worked snapshots; 11.4.3 Cache partitioning and replication · worked snapshots; 11.4.4 When caching is harmful · worked snapshots

References: https://www.rfc-editor.org/rfc/rfc9111.html · https://redis.io/docs/latest/develop/reference/eviction/ · https://www.cloudflare.com/learning/cdn/what-is-a-cdn/

Assessment: all eleven questions and separate explained solutions produced.
## Unit 12: Scalability, Load Balancing, and Data Distribution

Status: available. Direct prerequisites: [2, 3, 9, 10, 11].

Worked example: Scale a URL shortener from 100 requests per second to 100,000. Introduce new components only when justified by a demonstrated bottleneck.

### 12.1 Scale compute & route requests — available

Content source: src/teaching/data.py

- Vertical vs horizontal scaling.

- Stateless vs stateful services.

- Load distribution algorithms.

- Health checks and failover.

- Sticky sessions.

- Autoscaling metrics.

Figures: 12.1.1 Vertical vs horizontal scaling · worked snapshots; 12.1.2 Stateless vs stateful services · worked snapshots; 12.1.3 Load distribution algorithms · worked snapshots; 12.1.4 Health checks and failover · worked snapshots; 12.1.5 Sticky sessions · worked snapshots; 12.1.6 Autoscaling metrics · worked snapshots

References: https://learn.microsoft.com/en-us/azure/architecture/best-practices/index-best-practices · https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store

### 12.2 Replicate and partition data — available

Content source: src/teaching/data.py

- Replication.

- Partitioning and sharding.

- Range partitioning vs hash partitioning.

- Consistent hashing and rendezvous hashing.

- Rebalancing.

- Hot partitions and skew.

Figures: 12.2.1 Replication · worked snapshots; 12.2.2 Partitioning and sharding · worked snapshots; 12.2.3 Range partitioning vs hash partitioning · worked snapshots; 12.2.4 A new owner takes only part of the hash space; 12.2.5 Rebalancing · worked snapshots; 12.2.6 Averages hide a hot partition

References: https://learn.microsoft.com/en-us/azure/architecture/best-practices/index-best-practices · https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store

### 12.3 Lag, proxies & saturated pools — available

Content source: src/teaching/data.py

- Read replicas and read/write splitting.

- Replication lag.

- Database proxying.

- Connection pool saturation.

- Bottleneck identification.

Figures: 12.3.1 Read replicas and read/write splitting · worked snapshots; 12.3.2 Replication lag · worked snapshots; 12.3.3 Database proxying · worked snapshots; 12.3.4 Connection pool saturation · worked snapshots; 12.3.5 Bottleneck identification · worked snapshots

References: https://learn.microsoft.com/en-us/azure/architecture/best-practices/index-best-practices · https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store

### 12.4 Regions, write paths & scale economics — available

Content source: src/teaching/data.py

- Queueing and overload.

- Single points of failure.

- Multi-region strategies.

- Scaling writes vs scaling reads.

- Scale-out economics.

Figures: 12.4.1 Queueing and overload · worked snapshots; 12.4.2 Single points of failure · worked snapshots; 12.4.3 Multi-region strategies · worked snapshots; 12.4.4 Scaling writes vs scaling reads · worked snapshots; 12.4.5 Scale-out economics · worked snapshots

References: https://learn.microsoft.com/en-us/azure/architecture/best-practices/index-best-practices · https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store

Assessment: all eleven questions and separate explained solutions produced.
## Unit 13: File Systems, Search Infrastructure, and Data Pipelines

Status: available. Direct prerequisites: [8, 9, 10].

Worked example: Design a document-processing system accepting millions of files, tracking processing state, extracting metadata, maintaining provenance, and exposing searchable results.

### 13.1 Upload bytes without losing identity — available

Content source: src/teaching/data.py

- Binary/object storage.

- Large-file upload architecture.

- Multipart and resumable uploads.

- Checksums and content addressing.

- Metadata vs binary data.

Figures: 13.1.1 Binary/object storage · worked snapshots; 13.1.2 The upload pipeline separates bytes from control; 13.1.3 Multipart and resumable uploads · worked snapshots; 13.1.4 Checksums and content addressing · worked snapshots; 13.1.5 Metadata vs binary data · worked snapshots

References: https://openlineage.io/docs/ · https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex · https://kafka.apache.org/41/design/design/

### 13.2 Build and rebuild a search index — available

Content source: src/teaching/data.py

- Search engines and inverted indexes.

- Indexing pipelines.

- Search ingestion and reindexing.

Figures: 13.2.1 An inverted index is a term-to-document map; 13.2.2 Indexing pipelines · worked snapshots; 13.2.3 Search ingestion and reindexing · worked snapshots; 13.2.4 The running system · invariant and recovery review

References: https://openlineage.io/docs/ · https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex · https://kafka.apache.org/41/design/design/

### 13.3 Move data through batch and streams — available

Content source: src/teaching/data.py

- Batch vs streaming pipelines.

- ETL vs ELT.

- Change Data Capture (CDC).

- Data lakes and warehouses.

- Stream processing fundamentals.

Figures: 13.3.1 Batch vs streaming pipelines · worked snapshots; 13.3.2 ETL vs ELT · worked snapshots; 13.3.3 Change Data Capture (CDC) · worked snapshots; 13.3.4 Data lakes and warehouses · worked snapshots; 13.3.5 Stream processing fundamentals · worked snapshots

References: https://openlineage.io/docs/ · https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex · https://kafka.apache.org/41/design/design/

### 13.4 Quality, provenance & replay — available

Content source: src/teaching/data.py

- Data provenance and lineage.

- Data quality, schema validation, and replay.

- Lifecycle policies and retention.

- Designing data-intensive applications.

Figures: 13.4.1 Data provenance and lineage · worked snapshots; 13.4.2 Data quality, schema validation, and replay · worked snapshots; 13.4.3 Lifecycle policies and retention · worked snapshots; 13.4.4 Designing data-intensive applications · worked snapshots

References: https://openlineage.io/docs/ · https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex · https://kafka.apache.org/41/design/design/

Assessment: all eleven questions and separate explained solutions produced.
## Unit 14: Distributed Systems Fundamentals

Status: available. Direct prerequisites: [3, 4, 10].

Worked example: A social application writes a new post in one region while a friend reads it from another. Examine different consistency contracts and their user-visible effects.

### 14.1 Partial failure & the meaning of time — available

Content source: src/teaching/distributed.py

- What makes a distributed system difficult?

- Partial failures.

- Network uncertainty.

- Fault models.

- Time, clocks, and event ordering.

- Physical vs logical clocks.

- Lamport clocks and vector clocks.

Figures: 14.1.1 What makes a distributed system difficult · worked snapshots; 14.1.2 Partial failures · worked snapshots; 14.1.3 Network uncertainty · worked snapshots; 14.1.4 Fault models · worked snapshots; 14.1.5 Time, clocks, and event ordering · worked snapshots; 14.1.6 Physical vs logical clocks · worked snapshots; 14.1.7 Vector comparison exposes concurrent events

References: https://jepsen.io/consistency · https://lamport.azurewebsites.net/pubs/time-clocks.pdf · https://users.ece.cmu.edu/~adrian/731-sp04/readings/GL-cap.pdf

### 14.2 Consistency as a reader-visible contract — available

Content source: src/teaching/distributed.py

- Consistency models.

- Strong consistency and eventual consistency.

- Linearizability.

- Serializability vs linearizability.

- Sequential and causal consistency.

- Read-your-writes and monotonic reads.

Figures: 14.2.1 Consistency models · worked snapshots; 14.2.2 Strong consistency and eventual consistency · worked snapshots; 14.2.3 Linearizability · worked snapshots; 14.2.4 Serializability vs linearizability · worked snapshots; 14.2.5 Sequential and causal consistency · worked snapshots; 14.2.6 Read-your-writes and monotonic reads · worked snapshots

References: https://jepsen.io/consistency · https://lamport.azurewebsites.net/pubs/time-clocks.pdf · https://users.ece.cmu.edu/~adrian/731-sp04/readings/GL-cap.pdf

### 14.3 Partitions, CAP, PACELC & quorums — available

Content source: src/teaching/distributed.py

- CAP theorem, with its actual assumptions.

- PACELC as a useful extension.

- Quorums and read/write trade-offs.

- Split-brain situations.

Figures: 14.3.1 CAP theorem, with its actual assumptions · worked snapshots; 14.3.2 PACELC as a useful extension · worked snapshots; 14.3.3 Intersecting quorums still need a protocol; 14.3.4 A partition can leave two live but disconnected sides

References: https://jepsen.io/consistency · https://lamport.azurewebsites.net/pubs/time-clocks.pdf · https://users.ece.cmu.edu/~adrian/731-sp04/readings/GL-cap.pdf

### 14.4 Coordination, safety & liveness — available

Content source: src/teaching/distributed.py

- Distributed coordination.

- The fallacies of distributed computing.

- Safety vs liveness.

Figures: 14.4.1 Distributed coordination · worked snapshots; 14.4.2 The fallacies of distributed computing · worked snapshots; 14.4.3 Safety vs liveness · worked snapshots; 14.4.4 The running system · invariant and recovery review

References: https://jepsen.io/consistency · https://lamport.azurewebsites.net/pubs/time-clocks.pdf · https://users.ece.cmu.edu/~adrian/731-sp04/readings/GL-cap.pdf

Assessment: all eleven questions and separate explained solutions produced.
## Unit 15: Replication, Leader Election, and Consensus

Status: available. Direct prerequisites: [14].

Worked example: Three database replicas, one leader, and a network partition. Walk through elections, writes, acknowledgement rules, recovery, and potential data loss.

### 15.1 Choose a replication model — available

Content source: src/teaching/distributed.py

- Primary/replica architectures.

- Leader/follower replication.

- Multi-leader replication.

- Leaderless replication.

- Synchronous vs asynchronous replication.

- Quorum-based systems.

Figures: 15.1.1 Primary/replica architectures · worked snapshots; 15.1.2 Leader/follower replication · worked snapshots; 15.1.3 Multi-leader replication · worked snapshots; 15.1.4 Leaderless replication · worked snapshots; 15.1.5 Synchronous vs asynchronous replication · worked snapshots; 15.1.6 Quorum-based systems · worked snapshots

References: https://pdos.csail.mit.edu/6.5840/ · https://raft.github.io/raft.pdf · https://lamport.azurewebsites.net/pubs/paxos-simple.pdf · https://arxiv.org/abs/1608.03960

### 15.2 Raft and replicated state machines — available

Content source: src/teaching/distributed.py

- Consensus and replicated state machines.

- Raft: terms, elections, log replication, commit.

- Paxos: conceptual foundations.

- Log ordering and durability.

- Membership changes.

Figures: 15.2.1 Consensus and replicated state machines · worked snapshots; 15.2.2 Raft election changes authority under protocol rules; 15.2.3 Paxos: conceptual foundations · worked snapshots; 15.2.4 Presence in a log is not the same as commitment; 15.2.5 Membership changes · worked snapshots

References: https://pdos.csail.mit.edu/6.5840/ · https://raft.github.io/raft.pdf · https://lamport.azurewebsites.net/pubs/paxos-simple.pdf · https://arxiv.org/abs/1608.03960

### 15.3 Fences, leases & failure detection — available

Content source: src/teaching/distributed.py

- Split-brain prevention and fencing tokens.

- Failure detection.

- Strongly consistent metadata services.

- Distributed locks and leases.

Figures: 15.3.1 Split-brain prevention and fencing tokens · worked snapshots; 15.3.2 Failure detection · worked snapshots; 15.3.3 Strongly consistent metadata services · worked snapshots; 15.3.4 Distributed locks and leases · worked snapshots

References: https://pdos.csail.mit.edu/6.5840/ · https://raft.github.io/raft.pdf · https://lamport.azurewebsites.net/pubs/paxos-simple.pdf · https://arxiv.org/abs/1608.03960

### 15.4 Conflicts, CRDTs & regional trade-offs — available

Content source: src/teaching/distributed.py

- Conflict resolution and CRDT introduction.

- Multi-region replication trade-offs.

Figures: 15.4.1 Conflict resolution and CRDT introduction · worked snapshots; 15.4.2 Multi-region replication trade-offs · worked snapshots; 15.4.3 The running system · ordered responsibility; 15.4.4 The running system · invariant and recovery review

References: https://pdos.csail.mit.edu/6.5840/ · https://raft.github.io/raft.pdf · https://lamport.azurewebsites.net/pubs/paxos-simple.pdf · https://arxiv.org/abs/1608.03960

Assessment: all eleven questions and separate explained solutions produced.
## Unit 16: Message Queues, Events, and Distributed Workflows

Status: available. Direct prerequisites: [8, 10, 14, 15].

Worked example: Design an e-commerce checkout that coordinates payment, inventory reservation, shipment creation, and refund compensation.

### 16.1 Queues, logs & delivery boundaries — available

Content source: src/teaching/distributed.py

- Synchronous vs asynchronous communication.

- Queues vs logs vs pub/sub.

- Producers, consumers, brokers.

- Partitions, consumer groups, offsets.

- Delivery guarantees.

- At-most-once and at-least-once processing.

- Exactly-once processing within defined boundaries.

- Ordering guarantees.

- Consumer acknowledgements.

Figures: 16.1.1 Synchronous vs asynchronous communication · worked snapshots; 16.1.2 Queues vs logs vs pub/sub · worked snapshots; 16.1.3 Producers, consumers, brokers · worked snapshots; 16.1.4 Partitions, consumer groups, offsets · worked snapshots; 16.1.5 Delivery guarantees · worked snapshots; 16.1.6 At-most-once and at-least-once processing · worked snapshots; 16.1.7 Exactly-once processing within defined boundaries · worked snapshots; 16.1.8 Ordering guarantees · worked snapshots; 16.1.9 Consumer acknowledgements · worked snapshots

References: https://learn.microsoft.com/en-us/azure/architecture/patterns/saga · https://microservices.io/patterns/data/transactional-outbox.html · https://kafka.apache.org/41/design/design/

### 16.2 Retries, poison messages & idempotence — available

Content source: src/teaching/distributed.py

- Retries and dead-letter queues.

- Poison messages.

- Idempotent consumers.

- Event sourcing.

Figures: 16.2.1 Retries and dead-letter queues · worked snapshots; 16.2.2 Poison messages · worked snapshots; 16.2.3 Idempotent consumers · worked snapshots; 16.2.4 Event sourcing · worked snapshots

References: https://learn.microsoft.com/en-us/azure/architecture/patterns/saga · https://microservices.io/patterns/data/transactional-outbox.html · https://kafka.apache.org/41/design/design/

### 16.3 Event sourcing, CQRS & the outbox — available

Content source: src/teaching/distributed.py

- CQRS.

- Transactional outbox.

- Sagas and compensating transactions.

Figures: 16.3.1 CQRS · worked snapshots; 16.3.2 The outbox closes a local publication gap; 16.3.3 A failed shipment starts tracked compensation; 16.3.4 The running system · invariant and recovery review

References: https://learn.microsoft.com/en-us/azure/architecture/patterns/saga · https://microservices.io/patterns/data/transactional-outbox.html · https://kafka.apache.org/41/design/design/

### 16.4 Sagas, durable work & reconciliation — available

Content source: src/teaching/distributed.py

- Choreography vs orchestration.

- Workflow engines.

- Durable job execution.

- Scheduling, leases, and worker coordination.

- Backpressure and replay.

- Reconciliation after partial failure.

Figures: 16.4.1 Choreography vs orchestration · worked snapshots; 16.4.2 Workflow engines · worked snapshots; 16.4.3 Durable job execution · worked snapshots; 16.4.4 Scheduling, leases, and worker coordination · worked snapshots; 16.4.5 Backpressure and replay · worked snapshots; 16.4.6 Reconciliation after partial failure · worked snapshots

References: https://learn.microsoft.com/en-us/azure/architecture/patterns/saga · https://microservices.io/patterns/data/transactional-outbox.html · https://kafka.apache.org/41/design/design/

Assessment: all eleven questions and separate explained solutions produced.
## Unit 17: Reliability, Fault Tolerance, and Disaster Recovery

Status: available. Direct prerequisites: [2, 12, 15, 16].

Worked example: A downstream payment provider becomes unavailable during peak traffic. Demonstrate the failure cascade and progressively introduce resilience mechanisms.

### 17.1 Failure domains & redundancy — available

Content source: src/teaching/distributed.py

- Failure domains and fault isolation.

- Availability vs durability.

- Redundancy.

- Active-active vs active-passive.

Figures: 17.1.1 Failure domains and fault isolation · worked snapshots; 17.1.2 Availability vs durability · worked snapshots; 17.1.3 Redundancy · worked snapshots; 17.1.4 Active-active vs active-passive · worked snapshots

References: https://sre.google/sre-book/handling-overload/ · https://docs.cloud.google.com/architecture/dr-scenarios-planning-guide · https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html

### 17.2 Retries, circuit breakers & isolation — available

Content source: src/teaching/distributed.py

- Timeouts.

- Retries, exponential backoff, jitter.

- Retry storms.

- Circuit breakers.

- Bulkheads.

- Rate limiting.

Figures: 17.2.1 Timeouts · worked snapshots; 17.2.2 Retries, exponential backoff, jitter · worked snapshots; 17.2.3 Retry storms · worked snapshots; 17.2.4 A circuit breaker bounds futile calls; 17.2.5 Bulkheads · worked snapshots; 17.2.6 Rate limiting · worked snapshots

References: https://sre.google/sre-book/handling-overload/ · https://docs.cloud.google.com/architecture/dr-scenarios-planning-guide · https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html

### 17.3 Shed load and degrade deliberately — available

Content source: src/teaching/distributed.py

- Load shedding.

- Graceful degradation.

- Fallbacks.

- Health checking.

Figures: 17.3.1 Load shedding · worked snapshots; 17.3.2 Graceful degradation · worked snapshots; 17.3.3 Fallbacks · worked snapshots; 17.3.4 Health checking · worked snapshots

References: https://sre.google/sre-book/handling-overload/ · https://docs.cloud.google.com/architecture/dr-scenarios-planning-guide · https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html

### 17.4 Recover, test & learn from failure — available

Content source: src/teaching/distributed.py

- RTO and RPO.

- Backups and restore testing.

- Failover and failback.

- Multi-zone and multi-region deployments.

- Chaos engineering.

- SLO-based reliability decisions.

- Cascading failures.

- Incident analysis and prevention.

Figures: 17.4.1 Recovery time and recoverable data are different; 17.4.2 Backups and restore testing · worked snapshots; 17.4.3 Failover and failback · worked snapshots; 17.4.4 Multi-zone and multi-region deployments · worked snapshots; 17.4.5 Chaos engineering · worked snapshots; 17.4.6 SLO-based reliability decisions · worked snapshots; 17.4.7 Cascading failures · worked snapshots; 17.4.8 Incident analysis and prevention · worked snapshots

References: https://sre.google/sre-book/handling-overload/ · https://docs.cloud.google.com/architecture/dr-scenarios-planning-guide · https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html

Assessment: all eleven questions and separate explained solutions produced.
## Unit 18: Security Architecture and Privacy

Status: available. Direct prerequisites: [3, 7, 8, 9].

Worked example: Design a multi-tenant SaaS application where an administrator must never gain access to another organization's data.

### 18.1 Threats, identity & authorization — available

Content source: src/teaching/production.py

- Threat modeling.

- Trust boundaries.

- Authentication vs authorization.

- Sessions, cookies, tokens.

- OAuth 2.0 and OpenID Connect.

- Role-based and attribute-based access control.

- Least privilege.

Figures: 18.1.1 Threat modeling · worked snapshots; 18.1.2 Trust boundaries · worked snapshots; 18.1.3 Authentication vs authorization · worked snapshots; 18.1.4 Sessions, cookies, tokens · worked snapshots; 18.1.5 OAuth 2.0 and OpenID Connect · worked snapshots; 18.1.6 Role-based and attribute-based access control · worked snapshots; 18.1.7 Least privilege · worked snapshots

References: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html · https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html · https://www.rfc-editor.org/rfc/rfc9700.html · https://openid.net/specs/openid-connect-core-1_0.html

### 18.2 Secrets, encryption & trust boundaries — available

Content source: src/teaching/production.py

- Defense in depth.

- Secrets management.

- Encryption in transit and at rest.

- Password hashing.

- Key management and rotation.

- Network segmentation.

- Zero-trust principles.

Figures: 18.2.1 Defense in depth · worked snapshots; 18.2.2 Secrets management · worked snapshots; 18.2.3 Encryption in transit and at rest · worked snapshots; 18.2.4 Password hashing · worked snapshots; 18.2.5 Key management and rotation · worked snapshots; 18.2.6 Network segmentation · worked snapshots; 18.2.7 Zero-trust principles · worked snapshots

References: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html · https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html · https://www.rfc-editor.org/rfc/rfc9700.html · https://openid.net/specs/openid-connect-core-1_0.html

### 18.3 Tenant isolation, audit & deletion — available

Content source: src/teaching/production.py

- API security and common vulnerabilities.

- Multi-tenant isolation.

- Data minimization.

- Audit trails.

- Privacy, retention, and deletion.

Figures: 18.3.1 API security and common vulnerabilities · worked snapshots; 18.3.2 Tenant identity must survive every trust boundary; 18.3.3 Data minimization · worked snapshots; 18.3.4 Audit trails · worked snapshots; 18.3.5 Privacy, retention, and deletion · worked snapshots

References: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html · https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html · https://www.rfc-editor.org/rfc/rfc9700.html · https://openid.net/specs/openid-connect-core-1_0.html

### 18.4 Supply chains and security reviews — available

Content source: src/teaching/production.py

- Supply-chain security.

- Security vs usability trade-offs.

- Secure-by-design reviews.

Figures: 18.4.1 Supply-chain security · worked snapshots; 18.4.2 Security vs usability trade-offs · worked snapshots; 18.4.3 Secure-by-design reviews · worked snapshots; 18.4.4 The running system · invariant and recovery review

References: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html · https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html · https://www.rfc-editor.org/rfc/rfc9700.html · https://openid.net/specs/openid-connect-core-1_0.html

Assessment: all eleven questions and separate explained solutions produced.
## Unit 19: Observability, Monitoring, and Incident Engineering

Status: available. Direct prerequisites: [2, 3, 4, 10].

Worked example: An API's p99 latency increases from 200 ms to 5 seconds. Use traces, metrics, logs, and database analysis to localize the bottleneck.

### 19.1 Observe behavior with three signals — available

Content source: src/teaching/production.py

- Monitoring vs observability.

- Logs, metrics, and traces.

- Structured logging.

- Distributed tracing.

- Trace IDs, span IDs, context propagation.

- Golden signals.

Figures: 19.1.1 Monitoring vs observability · worked snapshots; 19.1.2 Logs, metrics, and traces · worked snapshots; 19.1.3 Structured logging · worked snapshots; 19.1.4 This slow request is dominated by waiting; 19.1.5 Trace IDs, span IDs, context propagation · worked snapshots; 19.1.6 Golden signals · worked snapshots

References: https://opentelemetry.io/docs/concepts/signals/ · https://opentelemetry.io/docs/concepts/context-propagation/ · https://sre.google/workbook/alerting-on-slos/

### 19.2 Choose indicators, budgets & alerts — available

Content source: src/teaching/production.py

- RED and USE methods.

- SLIs, SLOs, error budgets.

- Alert design and alert fatigue.

- Sampling and telemetry cost.

- Dashboards.

Figures: 19.2.1 RED and USE methods · worked snapshots; 19.2.2 SLIs, SLOs, error budgets · worked snapshots; 19.2.3 Alert design and alert fatigue · worked snapshots; 19.2.4 Sampling and telemetry cost · worked snapshots; 19.2.5 Dashboards · worked snapshots

References: https://opentelemetry.io/docs/concepts/signals/ · https://opentelemetry.io/docs/concepts/context-propagation/ · https://sre.google/workbook/alerting-on-slos/

### 19.3 Profile and investigate production — available

Content source: src/teaching/production.py

- Profiling.

- Query and application performance diagnosis.

- Incident response.

- On-call and runbooks.

- Root-cause investigation.

Figures: 19.3.1 Profiling · worked snapshots; 19.3.2 Query and application performance diagnosis · worked snapshots; 19.3.3 Incident response · worked snapshots; 19.3.4 On-call and runbooks · worked snapshots; 19.3.5 Root-cause investigation · worked snapshots

References: https://opentelemetry.io/docs/concepts/signals/ · https://opentelemetry.io/docs/concepts/context-propagation/ · https://sre.google/workbook/alerting-on-slos/

### 19.4 Learn from incidents and trace async work — available

Content source: src/teaching/production.py

- Blameless postmortems.

- Capacity monitoring.

- Observability across asynchronous workflows.

Figures: 19.4.1 Blameless postmortems · worked snapshots; 19.4.2 Capacity monitoring · worked snapshots; 19.4.3 Observability across asynchronous workflows · worked snapshots; 19.4.4 The running system · invariant and recovery review

References: https://opentelemetry.io/docs/concepts/signals/ · https://opentelemetry.io/docs/concepts/context-propagation/ · https://sre.google/workbook/alerting-on-slos/

Assessment: all eleven questions and separate explained solutions produced.
## Unit 20: Deployment, Cloud Infrastructure, and Platform Architecture

Status: available. Direct prerequisites: [3, 7, 17, 18, 19].

Worked example: Take a single-process application and deploy it into a reliable, observable, multi-instance production environment with safe releases.

### 20.1 Environments, VMs & containers — available

Content source: src/teaching/production.py

- Development vs staging vs production.

- Virtual machines vs containers.

- Container fundamentals.

- Kubernetes fundamentals.

Figures: 20.1.1 Development vs staging vs production · worked snapshots; 20.1.2 VMs and containers isolate at different layers; 20.1.3 Container fundamentals · worked snapshots; 20.1.4 Kubernetes fundamentals · worked snapshots

References: https://12factor.net/ · https://kubernetes.io/docs/concepts/overview/components/ · https://sre.google/workbook/canarying-releases/

### 20.2 Control planes, scheduling & configuration — available

Content source: src/teaching/production.py

- Control plane vs data plane.

- Scheduling and service discovery.

- Autoscaling.

- Configuration and secret delivery.

- Immutable infrastructure.

Figures: 20.2.1 Control plane vs data plane · worked snapshots; 20.2.2 Scheduling and service discovery · worked snapshots; 20.2.3 Autoscaling · worked snapshots; 20.2.4 Configuration and secret delivery · worked snapshots; 20.2.5 Immutable infrastructure · worked snapshots

References: https://12factor.net/ · https://kubernetes.io/docs/concepts/overview/components/ · https://sre.google/workbook/canarying-releases/

### 20.3 Releases, flags & schema migrations — available

Content source: src/teaching/production.py

- Infrastructure as Code.

- CI/CD.

- Rolling, blue-green, and canary deployments.

- Feature flags.

- Rollbacks and database migrations.

- Multi-environment configuration.

Figures: 20.3.1 Infrastructure as Code · worked snapshots; 20.3.2 CI/CD · worked snapshots; 20.3.3 Canary exposure expands only after verification; 20.3.4 Feature flags · worked snapshots; 20.3.5 Rollbacks and database migrations · worked snapshots; 20.3.6 Multi-environment configuration · worked snapshots

References: https://12factor.net/ · https://kubernetes.io/docs/concepts/overview/components/ · https://sre.google/workbook/canarying-releases/

### 20.4 Platforms, serverless & ownership — available

Content source: src/teaching/production.py

- Twelve-Factor App principles.

- Serverless compute.

- Cloud vs on-premises trade-offs.

- Infrastructure ownership and managed services.

- Deployment topologies and networking.

- Platform engineering basics.

Figures: 20.4.1 Twelve-Factor App principles · worked snapshots; 20.4.2 Serverless compute · worked snapshots; 20.4.3 Cloud vs on-premises trade-offs · worked snapshots; 20.4.4 Infrastructure ownership and managed services · worked snapshots; 20.4.5 Deployment topologies and networking · worked snapshots; 20.4.6 Platform engineering basics · worked snapshots

References: https://12factor.net/ · https://kubernetes.io/docs/concepts/overview/components/ · https://sre.google/workbook/canarying-releases/

Assessment: all eleven questions and separate explained solutions produced.
## Unit 21: Performance, Cost Optimization, and System Validation

Status: available. Direct prerequisites: [2, 4, 10, 12, 17, 19, 20].

Worked example: Compare three production architectures for a service with variable traffic. Model monthly costs, p99 latency, availability, and operational complexity under explicit assumptions.

### 21.1 Budgets, bottlenecks & honest benchmarks — available

Content source: src/teaching/production.py

- Performance budgets.

- CPU, memory, disk, network, and database bottlenecks.

- Profiling and benchmarking.

- Load, stress, spike, and soak testing.

- Benchmark methodology and statistical pitfalls.

- Tail latency analysis.

Figures: 21.1.1 Performance budgets · worked snapshots; 21.1.2 CPU, memory, disk, network, and database bottlenecks · worked snapshots; 21.1.3 Profiling and benchmarking · worked snapshots; 21.1.4 Load, stress, spike, and soak testing · worked snapshots; 21.1.5 Benchmark methodology and statistical pitfalls · worked snapshots; 21.1.6 Tail latency analysis · worked snapshots

References: https://martinfowler.com/articles/practical-test-pyramid.html · https://sre.google/sre-book/handling-overload/ · https://research.google/pubs/the-tail-at-scale/

### 21.2 Capacity, architecture & cost per outcome — available

Content source: src/teaching/production.py

- Queue saturation and throughput ceilings.

- Performance tuning vs architecture changes.

- Horizontal scaling economics.

- Compute, storage, networking, and telemetry costs.

- Cost per request or transaction.

- Capacity reservation vs elastic capacity.

Figures: 21.2.1 Queue saturation and throughput ceilings · worked snapshots; 21.2.2 Performance tuning vs architecture changes · worked snapshots; 21.2.3 Architecture costs are not capacity guarantees; 21.2.4 Compute, storage, networking, and telemetry costs · worked snapshots; 21.2.5 Cost per request or transaction · worked snapshots; 21.2.6 Capacity reservation vs elastic capacity · worked snapshots

References: https://martinfowler.com/articles/practical-test-pyramid.html · https://sre.google/sre-book/handling-overload/ · https://research.google/pubs/the-tail-at-scale/

### 21.3 Efficiency and a useful test portfolio — available

Content source: src/teaching/production.py

- Cost-performance optimization.

- Sustainability and resource efficiency.

- Unit, integration, contract, end-to-end, and performance tests.

- Fault-injection tests.

Figures: 21.3.1 Cost-performance optimization · worked snapshots; 21.3.2 Sustainability and resource efficiency · worked snapshots; 21.3.3 Unit, integration, contract, end-to-end, and performance tests · worked snapshots; 21.3.4 Fault-injection tests · worked snapshots

References: https://martinfowler.com/articles/practical-test-pyramid.html · https://sre.google/sre-book/handling-overload/ · https://research.google/pubs/the-tail-at-scale/

### 21.4 Fitness functions and design validation — available

Content source: src/teaching/production.py

- Data consistency validation.

- Architecture fitness functions.

- Regression testing.

- Evaluating a design against its original requirements.

Figures: 21.4.1 Data consistency validation · worked snapshots; 21.4.2 Architecture fitness functions · worked snapshots; 21.4.3 Regression testing · worked snapshots; 21.4.4 Evaluating a design against its original requirements · worked snapshots

References: https://martinfowler.com/articles/practical-test-pyramid.html · https://sre.google/sre-book/handling-overload/ · https://research.google/pubs/the-tail-at-scale/

Assessment: all eleven questions and separate explained solutions produced.
## Unit 22: End-to-End Design, Architecture Reviews, and Evolution

Status: available. Direct prerequisites: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21].

Worked example: Twelve complete architectural designs with a common 22-point review protocol.

### 22.1 URL Shortener — available

Content source: src/teaching/cases.py

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

Figures: 22.1.1 Data ownership and relationships; 22.1.2 The high-level path and responsibility boundaries; 22.1.3 Naive path, failure, improved path, review; 22.1.4 Evolution follows demonstrated requirements

References: https://www.rfc-editor.org/rfc/rfc9110.html · https://www.rfc-editor.org/rfc/rfc9111.html · https://learn.microsoft.com/en-us/azure/architecture/best-practices/index-best-practices

### 22.2 Rate Limiter — available

Content source: src/teaching/cases.py

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

Figures: 22.2.1 Data ownership and relationships; 22.2.2 The high-level path and responsibility boundaries; 22.2.3 Naive path, failure, improved path, review; 22.2.4 Evolution follows demonstrated requirements

References: https://www.rfc-editor.org/rfc/rfc2697.html · https://sre.google/sre-book/handling-overload/

### 22.3 Chat Application — available

Content source: src/teaching/cases.py

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

Figures: 22.3.1 Data ownership and relationships; 22.3.2 The high-level path and responsibility boundaries; 22.3.3 Naive path, failure, improved path, review; 22.3.4 Evolution follows demonstrated requirements

References: https://www.rfc-editor.org/rfc/rfc6455.html · https://kafka.apache.org/41/design/design/ · https://www.postgresql.org/docs/18/transaction-iso.html

### 22.4 Notification Platform — available

Content source: src/teaching/cases.py

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

Figures: 22.4.1 Data ownership and relationships; 22.4.2 The high-level path and responsibility boundaries; 22.4.3 Naive path, failure, improved path, review; 22.4.4 Evolution follows demonstrated requirements

References: https://martinfowler.com/articles/injection.html · https://microservices.io/patterns/data/transactional-outbox.html · https://kafka.apache.org/41/design/design/

### 22.5 Social Media Feed — available

Content source: src/teaching/cases.py

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

Figures: 22.5.1 Data ownership and relationships; 22.5.2 The high-level path and responsibility boundaries; 22.5.3 Naive path, failure, improved path, review; 22.5.4 Evolution follows demonstrated requirements

References: https://www.rfc-editor.org/rfc/rfc9111.html · https://learn.microsoft.com/en-us/azure/architecture/best-practices/index-best-practices · https://kafka.apache.org/41/design/design/

### 22.6 Video Streaming Platform — available

Content source: src/teaching/cases.py

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

Figures: 22.6.1 Data ownership and relationships; 22.6.2 The high-level path and responsibility boundaries; 22.6.3 Naive path, failure, improved path, review; 22.6.4 Evolution follows demonstrated requirements

References: https://www.rfc-editor.org/rfc/rfc8216.html · https://www.rfc-editor.org/rfc/rfc9111.html · https://openlineage.io/docs/

### 22.7 Ride-Hailing System — available

Content source: src/teaching/cases.py

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

Figures: 22.7.1 Data ownership and relationships; 22.7.2 The high-level path and responsibility boundaries; 22.7.3 Naive path, failure, improved path, review; 22.7.4 Evolution follows demonstrated requirements

References: https://postgis.net/docs/ST_DWithin.html · https://www.postgresql.org/docs/18/transaction-iso.html · https://learn.microsoft.com/en-us/azure/architecture/patterns/saga

### 22.8 Online Ticket Booking — available

Content source: src/teaching/cases.py

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

Figures: 22.8.1 Data ownership and relationships; 22.8.2 The high-level path and responsibility boundaries; 22.8.3 Naive path, failure, improved path, review; 22.8.4 Evolution follows demonstrated requirements

References: https://www.postgresql.org/docs/18/transaction-iso.html · https://learn.microsoft.com/en-us/azure/architecture/patterns/saga · https://www.rfc-editor.org/rfc/rfc9110.html

### 22.9 Payment System — available

Content source: src/teaching/cases.py

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

Figures: 22.9.1 Data ownership and relationships; 22.9.2 The high-level path and responsibility boundaries; 22.9.3 Naive path, failure, improved path, review; 22.9.4 Evolution follows demonstrated requirements

References: https://www.postgresql.org/docs/18/transaction-iso.html · https://microservices.io/patterns/data/transactional-outbox.html · https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html

### 22.10 Distributed Job Scheduler — available

Content source: src/teaching/cases.py

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

Figures: 22.10.1 Data ownership and relationships; 22.10.2 The high-level path and responsibility boundaries; 22.10.3 Naive path, failure, improved path, review; 22.10.4 Evolution follows demonstrated requirements

References: https://sre.google/sre-book/distributed-periodic-scheduling/ · https://raft.github.io/raft.pdf · https://kafka.apache.org/41/design/design/

### 22.11 Collaborative Document Editor — available

Content source: src/teaching/cases.py

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

Figures: 22.11.1 Data ownership and relationships; 22.11.2 The high-level path and responsibility boundaries; 22.11.3 Naive path, failure, improved path, review; 22.11.4 Evolution follows demonstrated requirements

References: https://arxiv.org/abs/1608.03960 · https://www.rfc-editor.org/rfc/rfc6455.html · https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html

### 22.12 Large-Scale Document Processing Platform — available

Content source: src/teaching/cases.py

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

Figures: 22.12.1 Data ownership and relationships; 22.12.2 The high-level path and responsibility boundaries; 22.12.3 Naive path, failure, improved path, review; 22.12.4 Evolution follows demonstrated requirements

References: https://openlineage.io/docs/ · https://kafka.apache.org/41/design/design/ · https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html · https://microservices.io/patterns/data/transactional-outbox.html

Assessment: all eleven questions and separate explained solutions produced.
