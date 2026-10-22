"""Concise concept-reference explanations, distinct from example-led openings."""
SUMMARIES={}
def add(n,raw):
    SUMMARIES[n]=[line.strip() for line in raw.strip().splitlines() if line.strip()]

add(2, '''Requirements state necessary outcomes and constraints; prioritisation identifies what matters most and what still needs evidence.
A workload describes the operations users cause, their frequency, payloads, and dependent work.
A read/write ratio counts work at a specified boundary; one user action can cause many physical operations.
Latency is elapsed time per operation; throughput is completed work per interval. Define which queries, requests, or transactions are counted.
Means and percentiles describe different features of a timing distribution; combined percentiles require appropriate underlying data.
Availability, durability, reliability, and consistency concern different serving, persistence, correctness, and observation requirements.
An SLI measures behaviour, an SLO targets it over a window, and an SLA states agreement obligations.
Capacity planning connects growth scenarios and resource limits to the time and evidence needed for expansion.
Estimate requests, bytes, memory, CPU, and transfer separately using explicit workload assumptions.
Peak load and its duration can differ substantially from an evenly distributed daily average.
Little's Law relates stable long-run averages: work in progress equals rate times residence time within one boundary.
Amdahl's Law bounds fixed-work speedup when part of the job remains sequential.
A request needing many results can be delayed by its slowest dependency; budget the complete path.
Feasible designs must satisfy mandatory security, cost, and operating constraints before preferences are ranked.
A decision matrix makes weighted judgments explicit; it does not replace correctness evidence or measurements.''')
add(3, '''A browser sends an HTTP request for a resource, and the server returns a response that the browser can display.
An IP address leads toward a machine. Its operating system uses ports and sockets to deliver data to the right program.
TCP carries an ordered byte stream; UDP carries datagrams; QUIC supplies secure streams over UDP. The application still interprets the data.
DNS finds records for a name. Cached answers can remain in use until their permitted lifetime ends.
TLS checks peer identity and protects messages in transit. The application separately checks permission to use a resource.
HTTP/2 shares a TCP connection between streams; HTTP/3 uses QUIC streams. HTTP request and response meanings remain.
A handshake prepares a new connection. Reusing a usable connection avoids repeating that setup for every request.
The four assumed stages take 20 + 40 + 40 + 55 = 155 ms. Reusing setup leaves the same 55 ms request stage.
A forward proxy acts for clients. A reverse proxy receives requests in front of application servers.
A load balancer chooses an application instance. An API gateway can perform common API checks before application work.
L4 routing uses transport addresses and ports. L7 routing can use HTTP content such as the requested path.
Polling repeatedly asks for updates. SSE sends server events; WebSockets allows both ends to send. Missed updates still need recovery.
NAT translates addresses and remembers return mappings. A firewall allows or blocks traffic. Ingress enters a boundary; egress leaves it.
Service discovery supplies possible destinations. A destination can stop after the list is obtained, so callers must handle that change.
A CDN can reuse a permitted nearby copy. Its cache key, freshness rule, and access rules determine whether reuse is valid.
A timeout leaves the remote outcome uncertain. A recorded operation identity can let the client find or retry the original operation.
A connection pool lends reusable connections. Borrowers wait when it is full and must return connections when their use ends.''')
add(4, '''A program is saved instructions. A process runs them. Threads within a process execute work and can share data.
The call stack records unfinished calls. Objects can outlive a call when later work still needs them.
The scheduler chooses a ready thread. A context switch saves one thread’s execution state and restores another’s.
I/O-bound work mainly waits for input or output. CPU-bound work mainly needs instructions to be executed.
A synchronous interface returns completion before the caller proceeds; an asynchronous interface separates starting from receiving the result.
A blocking read holds the calling thread waiting. Nonblocking I/O lets that thread do other work while data is unavailable.
Concurrent work overlaps in progress. Parallel work executes simultaneously. Taking turns can still interfere with shared updates.
A task can pause on an unfinished future. Completion makes it ready; the event loop must still give it a turn.
A pool limits active workers. A separate queue limit controls waiting jobs. Restart recovery also needs saved job records.
Shared memory lets callers change the same value. Message passing can give one owner control of that value.
Both callers read zero before either writes. Protecting the whole read–modify–write sequence lets two increments produce two.
A mutex gives exclusive entry; a semaphore counts permits; an atomic operation protects one action; a condition variable lets a waiter recheck shared state.
Deadlock waits in a cycle; starvation denies one caller progress; livelock repeats activity without completing the work.
Safe publication uses the language’s synchronisation rules so the reader can observe the completed value.
Immutable records stay unchanged. Their mutable collection still needs rules for concurrent access.
If arrivals exceed completions, waiting work grows. Backpressure makes the producer respond to the receiving side’s limited capacity.
A parent scope accounts for its children. Cancellation lets them stop and release resources; saved continuing jobs need a longer-lived owner.''')
add(5, '''Abstraction presents needed behaviour; encapsulation controls representation; polymorphism permits compatible implementations; inheritance specialises a relationship.
Composition combines collaborators, while inheritance requires subclasses to preserve their callers' behavioural expectations.
A contract specifies valid inputs, outcomes, effects, errors, and relevant timing or repetition rules beyond a signature.
Cohesion concerns related work inside a module; coupling concerns dependencies and knowledge between modules.
SOLID offers guidelines for responsibilities, useful extension, substitution, focused interfaces, and dependency direction.
DRY avoids duplicated knowledge; KISS favours understandable required design; YAGNI defers unsupported speculative capability.
The Law of Demeter discourages unnecessary dependence on distant objects' internal structure.
Tell, Don't Ask favours sending intentions to the owner that can protect the relevant state rule.
Command-query separation makes state-changing operations distinguishable from reads without requiring separate deployments.
Immutable values and explicit effects make changes easier to follow, with allocation and execution costs still considered.
Entities retain identity; value objects represent equal values; domain models express meaningful concepts and rules.
Object collaboration describes requests, results, and ownership between components, including partial-failure handling.
Testable design gives controlled inputs and visible outcomes; substitutes and real integration tests establish different evidence.
Refactoring improves structure while preserving the intended observable behaviour.
Pure functions can express decisions, while an explicit effect layer owns durable execution and external calls.''')
add(6, '''Dependency inversion lets important policy rely on suitable abstractions rather than changeable implementation details.
Inversion of Control delegates some calling or construction decisions to an external coordinator or framework.
Dependency Injection supplies collaborators through construction or calls instead of hiding their creation or lookup.
Constructor, setter, and method injection provide dependencies at different points with different validity and lifetime implications.
Dependency inversion concerns knowledge direction; DI concerns supplying collaborators. Either term alone does not establish the other.
A composition root assembles collaborators; a DI container automates selected construction and lifetime rules.
Transient, scoped, and singleton describe reuse within defined framework boundaries, not universal global identity or safety.
Scopes define resource lifetimes for requests, sessions, or jobs; their meanings need explicit ownership and cleanup.
Creating or holding a resource does not determine who owns its disposal.
Cleanup must release owned resources on success, failure, and cancellation under the relevant contract.
Lazy initialisation defers work to first use, requiring concurrency, publication, failure, and latency decisions.
Cycles can signal unclear responsibilities; captive dependencies retain collaborators beyond their valid shorter lifetime.
A service locator hides dependencies behind runtime lookup; DI can make them explicit at the appropriate boundary.
A factory chooses or creates a collaborator; injection supplies it or the factory, with ownership still specified.
Creational patterns organise different construction choices, families, staged assembly, copying, and bounded instance access.
Structural patterns organise interface translation, composition, grouping, added behaviour, simplified access, sharing, and mediation to a target.
Behavioural patterns organise algorithms, notifications, intentions, state transitions, traversal, and coordination at chosen extension points.
Repository, Unit of Work, Specification, and CQRS clarify data access, commit ownership, predicates, and distinct read/write models.''')
add(7, '''Layered architecture separates kinds of responsibility; physical tiers are a separate deployment choice.
A modular monolith has one release unit with enforced internal contracts and data ownership.
Microservices seek useful independent deployment and operation while adding network, version, and coordination work.
Clean Architecture directs source dependencies toward policy through application-owned abstractions.
Hexagonal architecture uses application ports and adapters to separate core operations from external mechanisms.
Onion Architecture organises inward policy dependencies; concrete contracts matter more than diagram shape.
Domain-Driven Design develops a shared business model with domain experts where rules and meanings need clarification.
A bounded context defines a model's valid scope; ubiquitous language makes its concepts consistent within that scope.
An aggregate groups changes requiring one consistency boundary, with a root controlling its members' transitions.
A domain event records a meaningful accepted fact; durable publication needs a separate explicit mechanism.
Module dependency rules limit knowledge and bypass paths, using review and useful enforcement where appropriate.
Business logic decides outcomes, orchestration sequences work, and infrastructure performs technical effects.
Controllers, services, repositories, and adapters are responsibilities, not mandatory class-name conventions.
An anti-corruption layer translates external meanings so they do not silently redefine the local model.
Event-driven components react independently, with delivery, ordering, replay, and progress obligations.
Serverless execution delegates platform work while retaining limits, state, identity, and retry requirements.
Evolutionary architecture changes through evidence while checks protect important required properties.
Business boundaries group capabilities; technical layers organise mechanisms within or across them.
A distributed monolith has multiple processes without useful independent change or operation.
Microservice extraction needs concrete benefits and operating capability sufficient to justify its added coordination cost.''')
add(8, '''An API is a behavioural communication contract, including identity, effects, failures, timing, and supported change.
REST, GraphQL, and RPC styles organise interaction differently; none alone supplies safe retries or compatibility.
Resource modelling gives business objects and operations stable identities and meaningful lifecycles.
Schemas describe structure; validation also checks business meaning, size limits, and safe error behaviour.
Protocol status and business state can differ: a created resource may still represent pending work.
Pagination bounds query and response work using defined order, filtering, size, and access rules.
Keyset cursors continue after ordered keys; offsets skip positions that can shift as data changes.
Compatibility preserves supported meanings and client behaviour across a planned transition.
Idempotency keys bind repeated attempts to one logical operation through scoped durable identity and result rules.
Authentication identifies a caller; authorisation checks the permitted action on the particular resource.
Rate limits control pace and bursts; quotas cap accumulated use under defined scope and failure rules.
Retries spend bounded time and capacity and need safe repetition, particularly for uncertain effects.
Long-running and streaming APIs need explicit ownership, progress, cancellation, buffering, and recovery contracts.
Webhooks are asynchronous deliveries requiring authenticity, stable event identity, and defined acknowledgment behaviour.
Schema evolution must preserve supported interpretation of stored events, historical data, and delayed readers.
Consumer-driven contracts protect meaningful assumptions of actual clients without freezing incidental formatting.
Gateways provide shared boundary policy; BFFs adapt interactions to particular client needs.
Internal APIs still cross trust, version, and failure boundaries; public APIs add explicit audience and support commitments.
Useful API documentation explains complete success and failure histories beyond machine-readable message shape.''')
add(9, '''Storage guarantees state accepted outcomes, observation rules, ownership, retention, and recovery under specified failures.
Relational storage models facts with keys and constraints; SQL expresses operations whose physical cost needs investigation.
Document storage groups nested data by identity, with explicit size, schema, index, and cross-document rules.
Key-value storage serves keyed operations; other queries and expiry need their own supported structures and policy.
Wide-column designs commonly combine partition keys with ordered dimensions, requiring bounded partitions and query-driven modelling.
Graph storage supports relationship traversal whose depth, degree, cost, and access scope need limits.
Time-series data combines measurements, times, and dimensions with explicit cardinality, lateness, and retention handling.
Search indexes are retrieval representations with source-version, freshness, access, and rebuild obligations.
Vector indexes retrieve similarity candidates from embeddings; scores establish neither truth nor access permission.
Object, block, and file interfaces expose different byte-access and lifecycle contracts.
OLTP serves short operational transactions; OLAP serves analytical scans and aggregation, often with different interference costs.
Row and column layouts group physical values differently to support different read and update patterns.
Normalisation reduces repeated facts; deliberate copies require a clear historical or maintained-current meaning.
ER modelling identifies keys, relationships, cardinalities, constraints, and record lifecycles.
Referential integrity protects valid relationships using mechanisms appropriate to the ownership and transaction boundary.
Data ownership includes who changes a fact and who maintains its access, schema, retention, and recovery.
Storage selection follows actual queries and invariants, including the complete cost of another engine.
Retention follows raw and derived copies through expiry, archival, deletion, replay, and recovery.
Polyglot persistence combines engines for useful capabilities while adding operating and cross-store coordination work.''')
add(10, '''A record lookup performs physical and visibility work through indexes, pages, memory, and storage.
Pages organise records; buffer pools cache pages, while query locality determines which work can be avoided.
Ordered trees support ranges and equality; hash indexes target equality under their implementation's rules.
LSM organisation batches sorted writes and compaction, trading ingestion behaviour against read work and amplification.
A query planner chooses physical execution using estimates; compare plans with actual work where safely supported.
Indexes improve selected reads while adding space, maintenance, and write costs.
ACID separates atomicity, invariant preservation, isolation, and conditional durability; application rules still need correct expression.
Commit accepts a transaction under the engine protocol; rollback abandons uncommitted work and cannot reverse unrelated remote effects.
Write-ahead logging preserves recovery information before corresponding data pages, under configured persistence rules.
MVCC retains versions for visibility rules; snapshots alone do not prevent every serialization anomaly.
Locks coordinate conflicting access; optimistic checks validate expected state before applying changes.
Dirty, nonrepeatable, and phantom reads describe different concurrent histories whose occurrence depends on isolation implementation.
Lost updates overwrite work; write skew can violate a multi-row rule even when separate rows are protected.
Isolation behaviour depends on engine, version, and statement form; retries require fresh whole-transaction reasoning.
Serializability concerns serial transaction equivalence; linearizability also concerns operation real-time precedence.
Database pools reuse bounded connections, with acquisition, hold time, and downstream contention included in deadlines.
Related statements need an explicit common transaction when their invariant requires one all-or-nothing change.
Recovery needs tested backups, logs, keys, compatible applications, and an explicit acknowledged-data policy.''')
add(11, '''Caching saves repeated work when reuse outweighs access, storage, and maintenance costs under the required semantics.
Locality and the active working set determine which data can usefully fit and remain in a cache.
In-process caches duplicate local copies; distributed caches add a shared network boundary and its failure behaviour.
Browser, edge, application, and database caches hold different copies with independent freshness and trust requirements.
Cache population and write patterns specify ordering and failure gaps; their names alone do not remove races.
TTL limits intended residence after insertion, not necessarily the source age of the inserted fact.
Invalidation coordinates copies with source changes; stronger freshness can require versions or additional coordination.
LRU, LFU, and FIFO rank eviction differently; admission, bytes, expiry, and approximations also affect behaviour.
A hot key concentrates work on an owner and needs a remedy suited to its actual read or write pressure.
Stampedes, absent-key traffic, and broad expiry need controlled loading and origin protection.
Negative caching stores a scoped absence or failure meaning for a deliberate lifetime.
Stale-while-revalidate serves an allowed older value while refresh proceeds, with a limit on unusable age.
Warming and prefetching spend speculative work that should be justified by actual future reuse.
Redis-like data structures offer specific operations; local command atomicity does not automatically cover a larger workflow.
CDN edges and shields distribute suitable representations under explicit key, capability, freshness, and purge rules.
Cache partitions and replicas need failure, remapping, fallback, and rebuild-capacity policies.
Caching can be harmful when it saves little, weakens scope, hides origin limits, or adds excessive lifecycle work.''')
add(12, '''Vertical scaling enlarges a node; horizontal scaling adds nodes, with gains limited by the work that can divide.
Stateless instances keep no required per-client conversation only locally, while using appropriate external state owners.
Balancing algorithms distribute selections using different load clues whose usefulness depends on request and connection behaviour.
Readiness, liveness, and failover make different decisions and require state and capacity beyond a probe response.
Sticky sessions preserve affinity while adding load-skew and recovery consequences for locally held state.
Autoscaling reacts to workload signals with delay, bounds, warmup, and downstream-capacity constraints.
Replication maintains copies under explicit acknowledgment, authority, lag, and recovery rules.
Sharding distributes partitions among owners, adding routing, query, transaction, and movement requirements.
Range placement supports ordered locality; hashing spreads keys, with different scan and hot-key trade-offs.
Consistent and rendezvous hashing limit some assignment changes without guaranteeing even traffic or moving the data itself.
Rebalancing transfers current data and authority while preserving concurrent writes, routing, validation, and recovery.
Hot partitions require diagnosis of popularity, size, and ownership pressure rather than more unrelated capacity.
Read/write splitting must respect observation and transaction needs, not merely classify by SQL verb.
Replica receipt, persistence, and apply progress can differ and support different freshness or recovery claims.
Database proxies add routing or pooling facilities whose session-state and retry contracts need verification.
Pool saturation includes waiting and held connections; aggregate demand across application replicas must remain bounded.
Bottleneck diagnosis connects useful outcomes and critical-path waits to constrained resources.
Queues absorb temporary mismatch but sustained overload requires admission, capacity, or workload changes.
A single point of failure can be any shared dependency defeating the required service or recovery.
Multi-region operation needs write authority, read freshness, loss, latency, and rejoin policies.
Read scaling can reuse copies; write scaling must divide or reduce ownership work while preserving invariants.
Scale economics includes surviving capacity, coordination, transfer, baseline resources, and operating effort per useful outcome.''')
add(13, '''Large binary objects and mutable workflow metadata need stable identities and an explicit lifecycle handoff.
Direct large-file upload reduces application byte handling while retaining permission, quota, and completion responsibilities.
Resumable or multipart upload tracks confirmed pieces and separately verifies the completed object's identity and integrity.
Checksums detect corruption under algorithm assumptions; content addressing identifies bytes without establishing permission or safety.
Immutable source versions keep changing annotations and processing attempts traceable to the bytes they used.
An inverted index maps analysed terms to document postings, with source and access metadata for safe serving.
Indexing stages need identified inputs, repeat-safe output, validated completion, and an owner for failed progress.
Reindexing builds and validates a new generation while catching up edits and deletes before serving switches.
Batch works on bounded input; streaming maintains continuing progress, with different freshness and recovery costs.
ETL transforms before target loading; ELT transforms after loading, changing raw-data placement and governance work.
CDC transports committed source changes through a supported handoff and ordering mechanism.
Lakes and warehouses organise raw and curated analytics, requiring ownership, catalog, quality, and lifecycle rules.
Stream processing needs keyed state, event/processing time, lateness, corrections, and recoverable progress.
Provenance identifies origins; lineage links transformations so outputs can be investigated and corrected.
Quality checks validate meaning as well as shape, while replay needs stable versions and safe effect handling.
Lifecycle rules follow originals, intermediates, indexes, logs, and recovery copies through required deletion.
Data-intensive design connects versioned transformations with explicit authority, validation, progress, and recovery.''')
add(14, '''Distributed participants observe only parts of an operation, so legal outcomes need explicit message and recovery protocols.
Partial failure permits one participant's effect to succeed while another fails to observe or record it.
Network delay and failure can appear alike; timeouts bound waiting but cannot prove a remote process stopped.
A fault model specifies failures and persistence assumptions a protocol claims to tolerate.
Physical timestamps, elapsed durations, and causal order answer different questions and need suitable clocks or protocols.
Physical clocks estimate time; logical clocks represent ordering relationships without necessarily measuring seconds.
Lamport clocks preserve causal order in one direction; vector comparisons can identify concurrency under their model.
A consistency model defines permitted observations across operations, sessions, and state copies.
Eventual convergence needs stated repair assumptions and conflict semantics; “strong” needs a named precise model.
Linearizability gives operations atomic points between invocation and response while respecting real-time precedence.
Serializability concerns transaction equivalence; strict serializability additionally respects real-time constraints.
Sequential consistency preserves participant program order; causal consistency preserves dependencies while allowing unrelated orders to differ.
Read-your-writes and monotonic reads preserve particular session observations across supported routing and recovery paths.
CAP concerns the incompatibility of defined atomic consistency and availability guarantees under its partition assumptions.
PACELC highlights partition choices and ordinary latency/consistency costs as a design lens, not a complete protocol.
Quorum intersection is a fixed-set property; version, durability, concurrency, and membership rules determine its use.
Split brain creates conflicting authorities; stale actors need prevention or enforcement at the protected effect boundary.
Coordination establishes shared decisions under an explicit failure and progress protocol.
Distributed-computing fallacies expose hidden assumptions about networks, cost, topology, trust, and administration.
Safety excludes bad outcomes; liveness requires progress under specified environmental conditions.''')
add(15, '''Primary/replica topology needs explicit write authority, acknowledgment, promotion, and stale-owner protection.
Leader/follower replication orders updates, while receipt, persistence, commitment, and application can mark different progress.
Multiple write leaders need valid conflict semantics, not just deterministic convergence that discards business meaning.
Leaderless protocols reconcile several replicas with implementation-specific version, repair, and membership rules.
Synchronous replication waits for named milestones; asynchronous acknowledgment can precede another durable copy.
A quorum is a permitted decision set within a protocol whose members preserve the required evidence.
Replicated state machines apply agreed commands deterministically; external effects remain a separate boundary.
Raft combines term-based elections, log freshness, replication, commitment, and membership rules to preserve history.
Paxos preserves chosen decisions through numbered proposals and required prior evidence across intersecting majorities.
A log entry's presence, durability, commitment, and application are distinct claims during replication and recovery.
Membership changes need a supported transition preserving decision safety between old and new configurations.
Fencing epochs reject stale authority only when receivers enforce them atomically with protected effects.
Failure detection produces suspicions under timing assumptions; authority safety must tolerate false suspicion.
Consistent metadata services own small control decisions, with explicit consequences when new decisions cannot proceed.
Locks and leases grant permission with identity and expiry rules, while resumed stale effects may still need fencing.
CRDTs converge through specified update/merge rules but do not enforce arbitrary business invariants.
Regional replication needs authority, acknowledgment geography, conflict, failover, and safe return-to-service rules.''')
add(16, '''Asynchronous submission separates acceptance from completion and needs an owner for the intervening work.
Queues distribute work, logs retain ordered history, and pub/sub follows its stated subscription and retention contract.
Producers, brokers, and consumers acknowledge different stages that must be named to reason about ownership.
Partitions provide ordered lanes; consumer groups and offsets track ownership and progress within those lanes.
Delivery guarantees need a stated record or effect boundary and do not automatically compose across external systems.
At-most-once can lose required effects; at-least-once can repeat them and therefore needs safe effect handling.
Exactly-once guarantees cover only the supported atomic boundary and its identity, retention, and failure assumptions.
Publication, delivery, execution, and effect order can differ when work proceeds concurrently.
Consumer acknowledgment advances broker progress, with loss or repetition gaps around separately committed effects.
Retry and dead-letter policies need bounds, useful error context, ownership, and a safe repair/replay path.
Poison messages need diagnosis and controlled quarantine rather than unlimited identical retries.
Idempotent consumers commit recognition and the protected local effect together, retaining identity for supported replay.
Event sourcing makes interpretable accepted events authoritative, with snapshot, correction, privacy, and replay obligations.
CQRS separates command and query models where their different needs justify projection and freshness work.
A transactional outbox commits publication intent with local state; relay delivery may still repeat.
Sagas coordinate local steps and supported compensations with durable progress and explicit uncertainty.
Choreography distributes event reactions; orchestration gives workflow direction and progress an explicit owner.
Workflow engines persist coordination under a programming model while external activities still need safe effect contracts.
Durable jobs retain identity, input, state, and attempt authority beyond the initiating process.
Scheduling separates stable due occurrences from attempts, with atomic creation, time, overlap, and stale-worker rules.
Backpressure and replay need capacity budgets, retained identity, and useful completion indicators.
Reconciliation compares intended and observed outcomes and repairs partial failure through safe identified operations.''')
add(17, '''Failure domains identify shared causes; isolation limits their spread through resources and dependencies.
Availability concerns useful serving; durability concerns committed data surviving the specified failure model.
Redundancy requires independent failure exposure, valid state, usable takeover, and enough surviving capacity.
Active-active and active-passive assign serving roles for a particular function, each needing tested transitions.
Timeouts bound waiting; overall deadlines include acquisition and stage waits without proving remote nonexecution.
Retries spend bounded capacity and time, with backoff, jitter, classification, and safe effect identity.
Retry storms amplify failure traffic; timing randomisation alone does not bound total attempts.
Circuit breakers limit futile calls and probe recovery without repairing dependencies or inventing valid outcomes.
Bulkheads partition relevant resources so one workload cannot consume another's entire budget.
Rate limiting applies a scoped pace and burst rule with an explicit state-failure policy.
Load shedding rejects selected work early to preserve useful higher-priority outcomes under overload.
Graceful degradation preserves a permitted subset of behaviour with visible freshness and action limits.
Fallbacks substitute defined business outcomes, with their own access, duration, capacity, and recovery risks.
Health probes support bounded local decisions rather than establishing the complete business service guarantee.
RTO targets recovery time; RPO targets acceptable data-loss exposure in time.
Usable backups require independent storage, keys, compatible state, and tested application restoration.
Failover and failback transfer traffic or authority while preserving current history, fencing, and capacity.
Zone and region placement address different correlations while adding propagation, cost, and recovery dependencies.
Chaos exercises test explicit hypotheses with bounded scope, observations, stop conditions, and recovery ownership.
SLO evidence guides reliability investment without hiding critical low-volume harm inside a broad denominator.
Cascading failures spread through resource pressure and retries, including potentially overloaded fallback paths.
Incident analysis links contributing mechanisms to verified corrective changes without substituting blame for explanation.''')
add(18, '''Threat modelling connects assets, actors, abuse paths, and impact to controls and concrete tests.
Trust boundaries mark changes in identity, authority, and confidence that require appropriate validation.
Authentication establishes identity; authorisation grants a particular action on a resource under policy.
Sessions, tokens, and cookies have different state and transport roles with explicit validation and revocation rules.
OAuth delegates access; OpenID Connect adds identity assertions with flow-specific validation.
RBAC assigns scoped role permissions; ABAC evaluates trusted attributes, with enforcement and testing required for either.
Least privilege limits effective identity capabilities to the work and resources actually needed.
Defense in depth combines complementary controls rather than repeating one unverified assumption at several layers.
Secrets need controlled distribution, ownership, rotation, revocation, and protection from accidental exposure.
Transit and storage encryption protect different boundaries under key/access assumptions and do not replace authorisation.
Password hashing uses a purpose-built salted work mechanism with maintained implementations and deployment-appropriate parameters.
Key management tracks data dependencies through creation, rotation, historical recovery, and destruction.
Segmentation restricts network reachability while application identity and resource permissions remain necessary.
Zero-trust principles avoid implicit permission from location alone and make trust evidence and limits explicit.
API security follows how accepted input is used, including ownership, injection, resource, and destination risks.
Tenant isolation must hold across queries, caches, jobs, objects, search, exports, telemetry, and administration.
Data minimisation retains information justified by a stated purpose and lifecycle.
Audit trails record scoped actors, actions, and actual outcomes while protecting integrity and sensitive context.
Privacy lifecycle spans collection, access, correction, retention, deletion, and historical recovery of copies.
Supply-chain controls protect inputs, builds, artifacts, credentials, deployment, and compromised-release response.
Security and usability need a workable safe journey without trading away mandatory isolation or correctness.
Secure reviews follow sensitive operations and changed conditions through every required enforcement boundary.''')
add(19, '''Monitoring follows known signals; observability helps explain behaviour through correlated outputs and instrumentation.
Logs record events, metrics aggregate populations, and traces connect execution work and waits.
Structured logs give fields stable meanings, bounded size, safe content, and explicit event boundaries.
Tracing relates spans while sampled executions still need comparison with wider timing and error evidence.
Trace context links observations across calls or messages and must not be treated as authorisation.
Golden signals connect latency, traffic, errors, and saturation using meaningful eligible outcomes.
RED focuses on serving rate, errors, and duration; USE examines resource utilisation, saturation, and errors.
SLIs measure behaviour; SLOs target it; error-budget burn compares observed shortfall with its allowance.
Useful alerts identify actionable harm or impending objective loss with an owner and response.
Sampling and retention balance diagnostic questions, privacy, cardinality, and telemetry capacity.
Dashboards organise evidence for decisions with clear units, denominators, windows, gaps, and ownership.
Profiling locates runtime work or waits under measured conditions, which must be related to user outcomes.
Diagnosis separates waiting from execution and tests proposed bottleneck mechanisms against evidence.
Incident response coordinates mitigation, decisions, communication, and remaining uncertain business outcomes.
On-call needs useful alerts, access, escalation, rehearsed runbooks, and service ownership that reduces recurring toil.
Cause investigation distinguishes triggers from contributing mechanisms and tests explanations beyond correlation.
Blameless postmortems reconstruct impact and conditions, with specific owned improvements and verification evidence.
Capacity monitoring tracks meaningful approaching limits, growth uncertainty, and the time available to respond.
Asynchronous observability follows accepted work through later attempts, stage waits, and required final outcomes.''')
add(20, '''Environments have different purposes while relevant protocols, state transitions, and configuration meanings need deliberate compatibility.
VMs virtualise hardware with guest systems; typical containers share a host kernel, with actual isolation and failure scope verified.
Containers package execution while runtime controls, persistent-state placement, identity, and shutdown still need design.
Kubernetes reconciles workload resources; application transactions, access, backups, and service objectives remain explicit responsibilities.
Control planes decide configuration and placement; data planes serve traffic with different startup and failure dependencies.
Scheduling selects eligible resources; discovery advertises endpoints whose readiness and shared-state behaviour still need handling.
Autoscaling must include useful signals, startup, draining, durable work, downstream limits, and spending bounds.
Configuration and secret delivery need validation, versions, rollout/reload semantics, and a recovery path.
Immutable infrastructure replaces defined instances, while runtime state, migrations, and emergency drift remain managed concerns.
Infrastructure as Code makes desired resources reviewable without eliminating state, privileges, drift, or destructive-change risks.
CI, delivery, and deployment preserve artifact identity and run checks appropriate to actual release risks.
Rolling, blue-green, and canary exposure need representative verification, compatible state, and sufficient transition capacity.
Feature flags control exposure with ownership and safe defaults, but do not reverse stored effects or replace permission.
Rollback depends on compatible state; expand-and-contract maintains a supported overlap before removing old structures.
Environment values should be validated and explicit without silently changing business meanings.
Twelve-Factor practices guide repeatable service operation while workload-specific correctness and recovery remain required.
Serverless delegates selected platform duties while retaining limits, durable state, identity, and safe retries.
Cloud/on-premises comparisons need equal workload, ownership, procurement, recovery, and verified cost assumptions.
Managed services transfer selected duties while clients retain responsibilities defined by their actual contract.
Deployment topology places execution, state, routes, trust, and failure domains on real infrastructure.
Platform engineering offers reusable operating capabilities whose limits and ownership remain visible to developer users.''')
add(21, '''Performance budgets allocate acceptable end-to-end costs under a workload and remain targets until measured.
Bottlenecks can be computation or waiting at CPU, memory, storage, network, locks, or data services.
Profiles locate runtime work; benchmarks compare controlled conditions with disclosed workloads, versions, variation, and outcomes.
Load, stress, spike, and soak tests answer different expected-load, limit, abrupt-change, and long-duration questions.
Benchmark validity depends on realistic input, sufficient observations, honest failures, and a generator that represents arrivals correctly.
Tail analysis connects timing distributions and representative paths without incorrectly averaging percentile summaries.
Saturation limits useful completion; added arrivals become waiting or rejection, requiring operating margin.
Tuning changes implementation costs; architecture changes alter major ownership or placement and need proportionate evidence.
Horizontal scaling adds baseline and coordination costs whose usefulness depends on divisible work and shared limits.
Total cost follows compute, requests, data, copies, transfer, telemetry, and operating work under explicit rates.
Cost per useful outcome avoids denominators inflated by failed or repeated attempts.
Reserved and elastic capacity trade commitment, idle risk, startup delay, and commercial terms against measured demand.
Cost-performance optimisation compares feasible equivalent service outcomes and checks downstream effects.
Resource efficiency removes unnecessary work and transfer while broader sustainability claims require actual supporting evidence.
Test scopes provide different evidence; choose checks by failures they can detect rather than a mandatory count ratio.
Fault injection targets meaningful interruptions and validates both useful recovery and required state.
Data consistency checks compare identities, versions, relationships, and invariants beyond equal counts.
Architecture fitness checks protect required properties without freezing irrelevant implementation details.
Regression tests preserve important behaviour while allowing deliberate contract changes and tolerating measured noise appropriately.
Design validation traces original requirements to tests, measurements, reviews, and clearly unresolved assumptions.''')

PATTERN_SUMMARIES={
'Factory Method':'Varies a creation operation so processing code can use a product without selecting its concrete implementation.',
'Abstract Factory':'Creates a compatible family of collaborators through one selected construction interface.',
'Builder':'Collects construction choices and validates them before producing a usable value.',
'Prototype':'Creates an object by copying configured state under explicit sharing and ownership rules.',
'Singleton':'Restricts instance access within a specified program or container boundary, without implying global uniqueness or safe mutation.',
'Adapter':'Translates an existing interface or representation into a caller’s required behavioural contract.',
'Bridge':'Uses composition to let two dimensions of variation evolve independently.',
'Composite':'Lets callers use leaves and groups through a compatible interface, with explicit traversal and partial-failure rules.',
'Decorator':'Adds behaviour around a collaborator while retaining its interface, with composition order affecting meaning.',
'Facade':'Offers a focused entry to cooperating subsystem operations without hiding consequential outcomes.',
'Flyweight':'Shares suitable immutable intrinsic state while keeping per-use context separate.',
'Proxy':'Represents a target interface while controlling access, creation, or location with explicit cost and failure behaviour.',
'Strategy':'Supplies an interchangeable algorithm or policy behind a stable behavioural contract.',
'Observer':'Notifies subscribed listeners under defined timing, lifetime, ordering, and failure rules.',
'Command':'Represents a requested action as explicit data and identity for an appropriate handler.',
'State':'Organises behaviour around a lifecycle whose guarded transitions follow entity history.',
'Chain of Responsibility':'Passes a request through ordered handlers with explicit continuation, rejection, and handling rules.',
'Template Method':'Preserves a process skeleton while allowing selected implementation steps to vary.',
'Iterator':'Exposes traversal without revealing collection representation, while retaining ordering and resource-lifetime obligations.',
'Mediator':'Coordinates collaborators through a focused owner instead of many direct relationships.',
'Memento':'Captures and restores supported local state without claiming to reverse independent external effects.',
'Visitor':'Adds operations across a known structure, trading easier new operations for more work when element types change.',
'Repository':'Offers application-oriented persistence operations through a contract defining transactions, bounds, errors, and lifetimes.',
'Unit of Work':'Owns related local changes under one commit and cleanup boundary.',
'Specification':'Names a reusable eligibility or selection predicate whose later state-changing use may need atomic revalidation.',
'CQRS':'Uses different command and query models where their needs justify extra projection and freshness work.'}
