"""Unit-specific questions and connected explained answers; Unit 1 remains in resources."""
QUESTIONS={}
def add(n,raw):
    QUESTIONS[n]=[tuple(x.strip().replace(' ¶ ','\n\n') for x in row.split(' || ')) for row in raw.strip().splitlines() if row.strip()]
    assert len(QUESTIONS[n])==8 and all(len(x)==2 for x in QUESTIONS[n]),n

add(2, '''Opening a feed appears to be one action. Why might it create many requests and writes? || The browser may fetch a list of posts, request each image, and send analytics. A publish action may save the post once and then write references into many follower feeds. These are separate operations even though the person performed one action. ¶ Count user intentions separately from requests, stored bytes, and physical writes. Otherwise an estimate based only on feed openings or published posts will miss much of the work at the storage and delivery boundaries.
Requests keep arriving faster, but successful completions stay at the same rate. What happens next? || Once a limiting resource cannot complete work faster, excess arrivals must wait, be rejected, or leave before completion. At 200 arrivals/s and 180 completions/s, twenty unfinished requests accumulate each second if none are rejected or abandoned. ¶ Compare offered traffic, useful completions, errors, and queue growth. A steady completion rate can coexist with a rapidly worsening user wait; it does not establish that increasing demand is being handled.
How can a 19.9 ms mean hide a request that took one second? || The 99 fast requests contribute 99 × 10 = 990 ms, and the slow request contributes 1,000 ms. Their total is 1,990 ms, so the mean is 1,990/100 = 19.9 ms. The arithmetic is correct, but the mean compresses very different experiences into one number. ¶ Inspect the slow observations and the distribution. In this particular 100-request set, nearest-rank p99 is the 99th sorted value, which is still 10 ms. Reporting a percentile alone can also miss an extreme observation.
Which requests belong in an event-based error budget? || The requests specified by the objective's eligible population belong in its denominator, and each must be classified using the stated good-outcome rule. Define both before measuring. ¶ At 99.9% success over one million eligible requests, the allowed bad fraction is 0.1% = 0.001. The budget is therefore 1,000,000 × 0.001 = 1,000 failed requests. Excluding the failures the objective was meant to track would make the result misleading. A time-based objective uses time, rather than request count, as its denominator.
When is L = λW useful for estimating work in progress? || Use stable long-run averages measured within the same boundary and in matching units. Here L is the average number present, λ is the arrival rate, and W is mean residence time, including relevant waiting. At 500 operations/s and 40 ms = 0.04 seconds, L = 500 × 0.04 = twenty operations. ¶ The result describes average work in progress, not an exact count at every instant or p99 latency. It does not show that a queue with sustained excess arrivals will become stable.
A traffic spike ends before new instances can start. What protects the service? || Existing spare capacity can serve some excess work before new instances are ready. A bounded queue can hold a temporary excess if the wait is acceptable, while admission limits reject or defer work before downstream resources become overwhelmed. ¶ Measure the spike's height and duration and include retries. An excess of 1,000 requests/s for 30 seconds adds 30,000 queued requests if none are rejected or completed by additional capacity. Starting instances later cannot undo the waits already experienced; the remaining backlog still needs to drain.
Only 80% of a job can run in parallel. What ideal speedup can four workers give? || Imagine a 100-second job: twenty seconds must run sequentially, while eighty can be divided perfectly. Four workers reduce the shareable part to 80/4 = 20 seconds, giving 20 + 20 = 40 seconds overall. The ideal speedup is 100/40 = 2.5 times. ¶ Equivalently, the new duration is 0.2 + 0.8/4 = 0.4 of the original. Coordination can reduce the actual gain further. The unchanged sequential part also limits ideal speedup to five times even with arbitrarily many workers.
Why can requiring fifty parallel calls increase tail latency? || The request waits for its slowest required result. If each call independently has a 1% chance of exceeding a threshold, its chance of staying within the threshold is 0.99. All fifty are fast with probability 0.99⁵⁰ ≈ 0.605. Thus at least one is slow with probability 1 − 0.605 ≈ 0.395, or about 39.5%. ¶ Independence is an assumption; shared dependencies can correlate delays. Parallel initiation removes the need to start calls one after another, but it does not remove the wait for the last required result.''')

add(3, '''A web service listens on port 443. Why might a browser on another machine still fail to reach it? || The listener may be attached only to the local loopback address. Or the request or reply may have no usable route, or a firewall may block it. Check the server address, listening address, and both directions of the path. Reaching the program still leaves the application’s permission checks to perform.
A sender writes HELLO and then WORLD through TCP. Why might the receiver not get two separate reads? || TCP carries an ordered byte stream, not the sender’s write boundaries. One read could contain HELLOWO and the next RLD. The application needs a framing rule to recover its messages, such as a length before each one. UDP instead preserves datagram boundaries; QUIC provides its own ordered streams over UDP.
The DNS address changes. Why do some clients still use the old server? || A resolver or client can still have a usable cached answer. An already open connection may also continue without another lookup. Updating the published record does not replace every saved answer or close existing connections. Their lifetimes affect when traffic moves.
The gateway recognises the signed-in user. Why must the task application still check ownership of task 42? || Knowing who the caller is does not establish which tasks the caller may read. The task application can compare the recognised user with task 42’s owner and enforce the permission rule. The gateway can perform common sign-in and allowance checks, while the application uses its resource information.
What work can SSE or WebSockets save, and what work do they add? || They can avoid repeated empty polls by keeping a path open for messages. The system then maintains connections and buffers and must handle slow or disconnected clients. If updates occur during disconnection, it needs retained events or a fresh snapshot. A new connection alone cannot recover the missing history.
The server saves task 7, but the reply is lost. What does the client learn from its timeout? || It learns only that a reply did not arrive in time. The task can already exist. If the request carried op-9 and the server saved that identity with its result, the client can look up or resend op-9 to recover task 7. Sending a new operation would risk a duplicate.
Our cold request takes 155 ms. Why can the next request take 55 ms with the same server work? || The assumed cold stages are DNS 20 ms, TCP setup 40 ms, TLS setup 40 ms, and request plus work 55 ms. They add to 155 ms. A usable warm connection and lookup remove the first three stages in this model. The 55 ms stage already includes its request and reply travel. These durations are assumed, not measured.
All twenty pool connections are borrowed, but CPU has free time. Why can the next request still wait? || The request needs an available connection, not just CPU time. Existing borrowers may be waiting on storage, locks, or another operation. Find why they still hold their connections and whether every exit returns them. Adding connections helps only if the database can use the extra work effectively.''')

add(4, '''How are a program, a process, a thread, and a source-code module different? || A program is saved instructions; a process is one running instance. Threads execute within a process and can share its data. A module organises source code. Several modules can run in the same process and stop together when it crashes, so separate modules do not automatically create separate failure boundaries.
An upload handler is marked async. Why might other work on its event loop still wait? || The handler may call a blocking library function or keep calculating without yielding. That occupies the loop’s thread. Other tasks can become ready but cannot run there until the current work gives up the thread. Async describes how the operation presents completion; it does not change every library call underneath.
Can one core make progress on two uploads without running them at the same instant? || Yes. A can start, wait for storage, and resume after the core has run B. Their progress overlaps, so they are concurrent. Running instructions for both at the same instant would require parallel execution resources. Taking turns can still cause a race if both use a shared old value.
A transfer changes balances from 100,100 through 90,100 to 90,110. Why are separate atomic writes insufficient? || Each write can be indivisible while the pair still passes through an incomplete state. A reader could see 90,100. Protect both changes as one operation and make readers of the pair follow the same rule, such as taking the same lock. A database transaction can supply a different appropriate boundary for stored balances.
A log says A set the title before B read it. Why do we still need safe publication? || Clock order alone does not supply the language’s memory-visibility guarantee. Use a defined synchronisation relationship. For example, A sets and shares the record while holding a mutex, releases it, and B later acquires the same mutex before reading. Under the required memory-model rules, A’s writes happen before B’s read.
A and B read count zero, then both write one. Which steps must the shared lock protect? || Protect the read, addition, and write together. If A completes those steps first, B reads one and writes two. Protecting only the assignments still allows both to calculate from zero. Separate private locks also fail because neither makes one caller wait for the other.
An upload read completes while a callback uses the only event-loop thread for two seconds. When can the upload task continue? || Its result is ready, but its continuation still needs a turn on the thread. It waits until the callback yields or finishes. The distinction is between a completed I/O operation and execution of the code that uses its result. More queued tasks do not let that one thread run both pieces at once.
150 jobs arrive and 100 finish each second. If all are accepted, how much extra work remains after ten seconds? || Each second adds 150 − 100 = 50 unfinished jobs. Ten seconds add 500, assuming none are rejected or abandoned. More queue space stores the excess without changing its growth. A bounded queue can reject or wait when full, and the producer must react to that feedback for arrivals to slow.''')

add(5, "A service can use two fraud policies and two providers. How does composition help? || The service receives one fraud-policy object and one gateway object. It asks the policy whether to allow the attempt, then asks the gateway to charge. Either part can be replaced without making a service subclass for every combination. ¶ Each replacement must still preserve its operation's meaning. Composition separates the choices; it does not remove the need for clear behaviour between them.\nWhat is missing from the operation charge(100)? || We need the currency and amount units. We also need an operation identifier, valid inputs, possible results, and failure behaviour. In our example, USD 100 minor units means one dollar. Approved confirms a successful charge; declined confirms rejection; uncertain leaves the result unresolved. ¶ The contract must explain supported retries and status checks. A timeout after submission may hide a successful charge, and adding an operation identifier does not by itself make the provider recognise duplicates.\nDoes SOLID require an interface around every class? Explain with the payment gateway. || No. A gateway interface is useful because it lets payment rules use a common operation while each adapter handles provider details. A second provider can then be added without spreading its message fields through the service. ¶ An interface that only adds another forwarding layer may solve no real problem. SOLID helps examine responsibilities, replacements, and dependencies; interface count is not a measure of design quality.\nWhy is Payment 42 an entity while Money(USD,100) is a value object? || Payment 42 keeps its identity as its status changes. Another payment for the same amount has a different identifier and history. Money(USD,100) is recognised by its amount and currency: another equal value can replace it. ¶ Immutability is a separate choice. Money is often immutable, and a payment can also have immutable snapshots linked by identifier 42. Adding money in different currencies still requires an explicit conversion rule.\nWhich part of a function-based payment design makes the real charge? || The outer code performs the provider call. A pure decision function uses explicit inputs and returns a decision or requested action; it makes no charge itself. The outer code records progress and feeds the observed provider result into the next decision. ¶ Calling the pure function again can recompute its decision. It must not automatically repeat a charge that has already run. The code that performs effects still needs operation identity and a way to resolve uncertain results.\nTwo callers each try to reserve 600 from an account with 1,000 available. Why is reserve(amount) alone insufficient? || The method gives the account one place to own the rule. However, if both callers read 1,000 before either writes, both separate checks pass. Merely moving the code into a method does not stop that sequence. ¶ The shared database must make the check and update atomic. After one reservation leaves 400 available, the second check must see insufficient funds and reject 600. A conditional update or suitable transaction can enforce this rule.\nA test confirms every private method call, but the order is paid after a decline. What should the test check? || It should check the required outcome: the payment is declined, the order remains unpaid, and shipment does not begin. A matching sequence of internal calls can still produce the wrong business state. ¶ Also test approval and uncertainty. Keep separate tests using the real adapter and database for message encoding, commits, and provider behaviour. A replacement gateway makes replies controllable but cannot prove how the real provider behaves.\nA refactor changes timeout into decline. Why is that a behaviour change? || Decline means the provider definitely rejected the charge. Timeout means the caller stopped waiting; the charge may already have succeeded before the reply was lost. Replacing uncertainty with decline tells the caller something we do not know. ¶ The caller might then start another payment and charge twice. Preserve the uncertain result and operation identifier until a supported status check or recovery procedure resolves it. Include this case in the refactor's checks.")

add(6, 'A notification service receives a provider SDK through its constructor. Has it necessarily achieved dependency inversion? || It uses DI because another part of the program supplied the SDK. It may still create the provider’s request types and interpret its special status codes. Those are source dependencies on provider details. ¶ Define Sender using the application’s message and outcome meanings. An adapter translates between that contract and the SDK. Passing this adapter into the service combines injection with a dependency direction that keeps provider details outside the notification rule.\nTwo processes each have a singleton sender. Must it be the same object, and is it automatically safe for concurrent calls? || No. The reuse boundary must be stated. Each process can have its own singleton instance, and separate containers may also have separate instances under their rules. ¶ Sharing an instance does not protect its mutable data. If several threads may call it, its implementation must preserve the contract during those calls. Its owner must also keep it valid until its final use.\nA factory returns a connection. What must its contract tell the caller besides how to query it? || It must state who owns the connection and when it stops being valid. A fresh connection may be transferred to the caller, which must close it. A borrowed connection remains under another owner and must be used within that owner’s boundary. ¶ Closing a borrowed connection too early can interrupt another operation. Failing to release an owned connection can leave fewer connections for later callers.\nA constructor receives a container, and the service calls resolve() inside its methods. Why are its dependencies hard to see? || The constructor names the container, but not the sender or repository actually used. We must inspect the lookups in the methods to discover those needs. A missing registration may appear only when a particular branch runs. ¶ This is service-locator behaviour. Obtain the needed objects at the assembly or scope boundary, then pass the service its specific dependencies.\nEach notification chooses email or SMS when it arrives. How can DI and a factory work together? || Startup injects SenderFactory into the notification service. When a notification arrives, the service reads its channel and asks the factory for the corresponding sender. DI supplied the factory; the factory makes the later choice. ¶ The return contract also states whether that sender is application-owned, borrowed from a scope, or newly owned by the caller. The service follows that rule when retaining or closing it.\nAn application-wide service retains request A’s database session. Request A ends. What can go wrong during request B? || Request A may close the session while the service still holds its reference. Request B then reaches a closed resource. Retained request data may also belong to the wrong user. This is a captive dependency. ¶ Pass a valid session for each operation, or inject a focused factory that opens an operation scope. Finish the operation before closing its resources. Keeping all sessions open indefinitely does not preserve the intended request boundaries.\nTwo first requests arrive together for a lazily created report generator. What needs to be decided? || Both can observe that no generator exists and try to create one. Use supported coordination so the intended number is created and other callers receive only a fully initialised object. ¶ Define construction failure as well. Will later callers retry, or receive the saved error? Who releases resources from the failed attempt? The first request also bears the construction delay; essential setup may be better completed before reporting readiness.\nA pool has ten connections. Every failed request keeps one. Why can a later healthy request become stuck? || After one leak, nine connections remain available. Repeated failures can leave all ten held. The later request cannot start its database work even if its own query and the database are healthy. ¶ Use an owning resource block or finally path to return the connection when the operation ends, including supported failure and cancellation paths. Roll back unfinished work as the connection’s reuse contract requires.')

add(7, '''What makes a monolith modular if it has one deployment? || Its modules have clear responsibilities, controlled interfaces, and data ownership. Orders should use a payment contract rather than alter private payment tables. One deployment keeps calls local but does not prevent useful boundaries. Enforce important dependencies through review or appropriate checks.
Why can dependency arrows point differently from runtime calls? || A service can depend on an application-owned repository interface, while a database adapter implements it. At runtime, calls execute the supplied adapter. The source arrow describes knowledge or implementation relationships, not necessarily the physical direction of a message or a separate network service.
Why can catalog Product and fulfilment Item be different valid models? || They describe different business work. Catalog may care about descriptions and categories, while fulfilment tracks units and locations. A bounded context identifies where each meaning applies. Translate between them deliberately rather than forcing both into one schema that obscures their rules.
How should an aggregate boundary follow the rule it protects? || Group state that must change atomically under a root controlling those changes. An order's line values and total may need one consistency boundary. Making the entire shop one aggregate adds contention. Cross-aggregate work needs explicit coordination rather than an assumption that object references create a shared transaction.
What should an architecture fitness check preserve? || A meaningful required property, such as allowed dependencies, migration compatibility, or tenant isolation. It should detect erosion of that reasoned boundary without freezing incidental class names. Update the check when the architecture decision legitimately changes, and keep evidence within the check's actual scope.
An order commits, then the process dies before publishing its event. What is missing? || Publication intent existed only in memory or a separate unsafe step. An outbox can commit that intent with the order so a relay can resume later. The relay may publish again after losing its own progress record, so consumers still need stable event identity and duplicate handling.
Five services share writable tables and always release together. What independence is missing? || They cannot change their contracts or stored representation independently and can remain tightly coupled operationally. The network split adds failure and diagnosis work without delivering much independent deployment. Clarify ownership and boundaries, or consider a modular consolidation where appropriate.
When would extracting a module into a service be justified? || Look for a stable capability with a concrete scaling, fault-isolation, or team-ownership need, plus the ability to operate it. Compare the benefit with network failures, versioning, data coordination, security, and on-call costs. A rapidly changing model alone is not evidence that more process boundaries will help.''')

add(8, '''Why give a refund its own identity and status? || A refund can be requested later, authorised separately, and complete or fail independently of the original payment. Its own identity supports amount checks, retries, and investigation. Treating it as an untracked toggle on paid loses the history and uncertainty needed for recovery.
What does a keyset cursor improve, and what does it leave unresolved? || It continues after a stable ordered key rather than skipping a shifting row count, avoiding some duplicates and omissions from insertions before an offset. It also needs validation and query/tenant scope. Changing records can still affect results; the cursor does not automatically provide one consistent snapshot.
What makes an idempotency key more than a string in a request? || Durable state binds owner, key, payload fingerprint, progress, and result with suitable uniqueness and atomicity. Identical retries recover the same operation; different content conflicts. Retention and provider recovery rules matter too. A separate unprotected lookup and insert can race or forget an external effect.
Why does signing in not grant access to GET /payments/42? || Authentication identifies the caller. Authorisation must still check this caller's permitted action on payment 42 using trusted membership and resource scope. Guess-resistant IDs and gateway authentication do not establish ownership. Apply the rule on every relevant query and effect path.
How can removing an old event decoder break recovery after a successful release? || Historical logs and backups can still contain that version. A restoring or delayed consumer needs to interpret it even when current traffic uses only the newest shape. Keep supported historical samples and transformations, including meanings, defaults, and unknown values, for the required replay horizon.
Does 201 Created for a pending payment mean money was captured? || No. It can mean the payment resource was created successfully while its financial operation remains pending. The body and operation contract describe that later state. HTTP response semantics do not make a provider effect part of the local resource transaction.
Four layers each allow three attempts. How much downstream work can one request cause? || Up to 3⁴ = 81 attempts in the nested worst case. Early success can reduce actual work, but failure can trigger amplification precisely when capacity is scarce. Use an overall retry budget and deadline, and safe operation identity for effects.
A webhook effect commits but its reply is lost. What should redelivery do? || Recognise the stable event identity and avoid repeating the established local effect. Persist recognition and effect together when that is the protected boundary. An unrelated external call needs its own protocol. The sender may legitimately retry because it did not observe acknowledgment.''')

add(9, '''What must be decided before choosing a storage family? || State the important reads and changes, accepted-result boundary, invariants, retention, and supported failures. Identify the authoritative copy and recovery procedure. A product category does not establish configured isolation, durable acknowledgment, or usable backups, so verify the selected implementation against those needs.
Why is a similar embedding result not proof of truth or permission? || An embedding is a derived numerical representation used to find candidates. Approximate similarity can miss items or retrieve imperfect matches. Preserve source versions, verify required evidence, and enforce access. A vector score describes its retrieval relationship, not factual correctness or authorisation.
When is storing an address twice correct? || A profile can hold the current address while a completed order retains the address actually used at purchase. Those records represent different facts. A maintained cache of the current address has another meaning and needs an update policy. State whether repetition preserves history or tracks a changing source.
Why is data ownership broader than creating a table? || The owner defines allowed changes and access contracts and is responsible for schema evolution, retention, incidents, and recovery. If every service writes the table directly, they share release and transaction assumptions despite separate repositories. Ownership needs an enforcement mechanism and operating responsibility.
What work appears when a second storage engine is added? || Backup and restoration, access policy, schema changes, monitoring, expertise, and reconciliation now cross another boundary. If it is a derived search store, also manage lag and rebuilding. Compare the new capability with that ownership cost rather than assuming a specialised engine is automatically a net improvement.
Why do more cold partitions not solve one very busy conversation partition? || The hot conversation's requests still reach its owner. Extra unrelated capacity does not divide that key's work. Measure whether the pressure comes from size, reads, writes, or ordering, then choose supported splitting, read distribution, or a changed data model that preserves the required semantics.
Search still holds a deleted private document. What must the system do? || Enforce the required access and deletion policy when serving, even while asynchronous cleanup catches up. Carry source identity and version so old updates cannot recreate an invalid visible record. Track physical cleanup and derived-copy lifecycle rather than treating a successful delete in the source as completion everywhere.
What prevents an older backup from restoring deleted content into live service? || Recovery must apply the relevant deletion history and lifecycle rules before exposing restored copies. Track raw and derived data, including indexes and replay paths. A narrowly retained marker can help prevent resurrection, but has its own minimisation and retention needs.''')

add(10, '''Why might range and equality queries need different indexes? || An ordered tree can locate the first key in a range and continue through neighbouring entries. A hash index locates equality candidates using a hash and does not provide that ordered walk. An ordered tree can also serve equality queries, so equality alone does not require a hash index. ¶ Compare the query conditions, ordering, output size, storage locality, update cost, and indexes supported by the engine. The useful choice is the structure that reduces the actual work for the required operations.
Why does an ACID transaction not automatically preserve every business rule? || The application and constraints must express the rule correctly. In our transfer, both account changes can commit atomically even if the application calculates the wrong amount. Atomicity groups the changes; it does not validate the business calculation. ¶ Check the invariant, the code and constraints that enforce it, the selected isolation level, and the durability configuration. Each answers a different question about whether the transaction provides the promised result.
Why is MVCC alone insufficient to claim serializability? || MVCC retains versions and chooses which version a reader can see. That mechanism can give both doctors a stable view in which the other is still on call. Each can then update a different row, leaving nobody on call if both changes commit. ¶ No correct serial execution of those checks permits that result: the second doctor would see the first off and stay. Check the isolation and conflict rules that prevent this history, rather than inferring serializability from the existence of row versions.
Why state the engine and statement behaviour when discussing isolation? || The same isolation name can have different implementations. A plain read and a locking or updating statement can also have different conflict behaviour. In PostgreSQL 18, ordinary Read Committed SELECTs take statement snapshots; Repeatable Read holds a transaction snapshot and prevents phantoms, but can still allow serialization anomalies. ¶ Use the documented engine, version, level, and statement form when analysing a history. When a transaction fails with a retryable serialization conflict, restart its reads and decisions as part of the whole transaction, using fresh state and bounded attempts.
How do serializability and linearizability differ? || Serializability requires committed transactions to have an effect equivalent to some serial transaction order. It permits their instructions to overlap and does not by itself add a real-time ordering condition. ¶ Linearizability treats each operation as taking effect between its invocation and reply and respects real-time precedence between operations. Strict serializability combines transaction serialization with real-time order. None of these properties automatically brings a provider call outside the database into its local transaction boundary.
Two doctors each see the other on call and both go off duty. What rule was missed? || At least one doctor must remain on call. That invariant covers both rows. Each transaction relied on an earlier read of the other doctor, so the updates can be individually plausible while their combination is invalid. This is write skew, rather than one transaction overwriting the other's row. ¶ Protect the full decision with suitable serializable transactions, coordinated locking, or a shared conflict point. If serialization rejects an attempt, repeat the whole transaction with fresh reads; the remaining doctor must then stay on call.
A conditional seat update changes zero rows. What does that mean? || No row satisfied the condition when the database applied the update, so the seat claim did not occur. In the competing-buyer example, the earlier winner changed the availability or version. More generally, the seat might also be missing; the guarded update alone does not distinguish those causes. ¶ Re-read the relevant state and decide whether to report unavailability, a missing seat, or another supported outcome. Do not report a reservation merely because the SQL statement completed without an error. Success requires the guarded transition and its commit to succeed.
A backup job succeeded. What recovery evidence is still needed? || Restore the backup in a usable environment with the required decryption keys, schema, credentials, and recovery logs. Open it through a compatible application and check meaningful relationships, such as a reservation agreeing with its seat owner. ¶ Measure how long full recovery takes and identify how much acknowledged history can be recovered. File creation and checksums are useful checks, but do not establish that the service can restore the required state and serve correctly.''')

add(11, '''Why does a working set matter more than the full history size for caching? || Reuse concerns the data active in the chosen interval. A small cache can serve a much larger history if most requests reuse a small portion. If the active set exceeds it, eviction and reload can churn. Include bytes, object size, scan traffic, and admission behaviour as well as entry count.
How can cache-aside reinsert an old value after invalidation? || A reader fetches version one, then pauses. A writer commits version two and invalidates the key. The reader resumes and inserts its old value. Ordering a source write before cache deletion alone does not prevent this history; stronger freshness needs suitable version or coordination rules.
Why can a one-minute TTL serve data older than one minute? || TTL starts when the cache inserts the value. If that value already lagged the source by five minutes, another minute of residence can make it six minutes old. Expiry and source freshness are different measurements. Choose the policy according to the operation's tolerated staleness.
For A,B,C,A,D at capacity three, what do ideal LRU and FIFO evict? || Ideal LRU refreshes A's recency, leaving B oldest when D arrives, so it evicts B. FIFO preserves insertion order and evicts A. This fixture explains their difference; real engines can approximate policies and use byte limits or separate expiration rules.
When might removing a cache improve the design? || When reuse saves less than lookup, encoding, memory, and maintenance cost, or when a simpler source improvement meets the requirement with fewer freshness risks. Test the empty and unavailable paths. A warm cache can hide an origin-capacity problem, while a wrongly scoped cache can create a data leak.
A cache restart sends misses to the origin. How can that load be controlled? || Combine same-key loading where useful, bound refresh workers, apply origin admission, and rebuild gradually. Negative caching and expiry jitter address particular patterns. Do not let every new instance independently scan the whole source. Protect recovery capacity as well as normal cache-hit traffic.
A product is created just after “not found” is cached. What should the policy explain? || How long the negative entry may hide the new product and whether creation invalidates it. Distinguish genuine absence from temporary source failure and authorisation denial. Keys and lifetimes must prevent one tenant's response from misleading another.
Refresh keeps failing while stale data is served. What limit is needed? || Define fresh, stale-permitted, and unusable ages or another explicit degradation bound. Serving must stop or change once the allowed stale condition ends. Some descriptions tolerate old values, but correctness-critical operations need their authoritative checks. Do not silently extend stale use forever.''')

add(12, '''The application becomes slow, so the team adds web servers. Under which conditions would you expect more useful completions, and when might the extra servers mainly create more waiting? || More web servers help when they can share the limiting work. If requests spend their time performing independent CPU calculations, additional compute may increase completions while other required resources still have capacity. ¶ If every request instead waits on one saturated database, disk, lock, or provider, extra web servers can send more work to that same constraint. Trace where requests execute and wait, then compare the useful completion rate before and after a change. The intervention should address the stage that limits the required outcome.
A dataset is divided among several storage owners. Explain what changes for routing, queries, and rules that previously fitted inside one database. || The application must now find the owner of each key and account for ownership changes. A query confined to one shard can remain local, while a query spanning shards must contact several owners and combine results. Uniqueness and transactions that cross those owners need more than one shard's local check. ¶ The partition key changes which operations stay together. A tenant key can keep a tenant's records local, but one large tenant can still overload its owner. Choose placement and recovery from the important operations and invariants, rather than assuming that division by itself removes the limit.
In the rendezvous example, owner D is added to A, B, and C. Explain which assignments can change, and why this does not establish balanced request traffic. || For each key, A, B, and C keep the scores they had before. Their previous winner therefore remains the best of those three. Adding D either leaves that winner in place or gives the key to D if D has the winning score. In this model, a changed assignment cannot jump from A to B merely because D was added. ¶ This property concerns key placement. It neither transfers records nor makes clients agree about membership. It also says nothing about popularity: many keys can be evenly placed while one frequently requested key sends most traffic to a single owner. Measure key distribution and request traffic separately.
A dashboard says that a replica has received an update. Why is that insufficient evidence that a read can observe it, or that it will survive the required failure? || Receiving a change, preserving it durably, and applying it to served state are different milestones. A replica may have received newer log records while its read state still reflects an earlier applied position. A read there can therefore miss the update. ¶ Durability depends on the protocol's required persistence milestone and failure assumptions. Identify the source, receipt, persistence, and apply progress relevant to the decision. A freshness decision needs evidence about visibility; a promotion decision must also honour the acknowledgment and possible-loss contract. The phrase “has the update” leaves these distinctions unresolved.
Why should the cost comparison between one larger node and several smaller nodes use the same failure and recovery requirements? || A design that is cheap while every node works may have too little surviving capacity after a required failure. Another may recover quickly but lose more acknowledged data than the requirement permits. Those designs are providing different service, so their healthy-state prices alone are not comparable. ¶ First require each candidate to meet the same workload, response-time, data-loss, and interruption objectives. Then include surviving capacity, copies, coordination, transfer, monitoring, and operating work. Compare cost against successful outcomes, including the retries and recovery work needed to obtain them.
One partition receives 70% of writes while the other partitions are mostly idle. Which evidence would help you choose between splitting it, changing placement, and redesigning the hot operation? || Inspect which keys produce the writes, how large the records are, and where the owner spends time. Many independent hot keys may be divisible between owners. One huge record may create a different cost from many small writes. One entity whose rule requires exclusive updates can remain serial even after unrelated data moves away. ¶ A range split helps when incoming work actually divides across the resulting ranges. More cold partitions do not automatically divide one hot key. Choose a change that reduces the observed pressure while preserving the required query results and ownership rule, and measure the hot owner's queue again.
During a database slowdown, an autoscaler adds application replicas. Explain how this can increase timeouts even though the application now has more machines. || Each application replica may create another connection pool. More instances can therefore produce more simultaneous database borrowers and more competing queries without adding database capacity. If slow queries or lock waits keep connections busy, new callers accumulate both at pools and inside the database. Retries may add further attempts. ¶ Bound aggregate admission across the instances and include acquisition waiting in request deadlines. Inspect connection hold time, query work, and contention before raising limits. Extra application capacity helps only if it increases useful completions rather than increasing the pressure on the same constrained owner.
Two application replicas run on one host. What protection do they provide, and which additional evidence would you need before claiming that they survive a host failure? || One process may continue when the other process alone fails, but losing the host can remove both. The host is a shared failure domain. Process count therefore does not establish machine-failure tolerance. ¶ To survive the required host failure, place suitable serving capacity elsewhere and check its state, routing, and takeover procedure. Inspect other shared dependencies, such as storage, power, configuration, and credentials. Also establish that the survivor has enough capacity. Separated processes provide useful protection only for the failures that do not defeat their remaining common dependencies.''')

add(13, '''Why do acknowledged upload parts not prove the completed file is correct? || Suppose storage has accepted parts 1, 2, 3, and 4. That establishes progress for the identified session, but it does not establish that the parts came from the same source revision or were assembled in the intended order. Completion must name the correct parts and verify the final object's size and integrity under the upload protocol. For example, a source file changed between retries can produce a mixture of versions even though no part is missing. A provider-specific entity tag should be treated as a full-content checksum only if the provider defines it that way for this operation.
Why does a content hash not authorise a download? || A digest is computed from bytes. It can help identify content under the algorithm's assumptions, but its computation contains no decision about who may read that content. A tenant who knows another tenant's file hash must still pass the ownership and access checks for the requested reference. Content integrity also does not establish that the file is safe to process. If deduplication exposes whether a supplied hash already exists, it may disclose information across tenants, so its visibility and scope need deliberate rules.
What does an inverted index record for “blue car” and “blue bike”? || Let D1 contain “blue car” and D2 contain “blue bike.” The posting list for blue contains D1 and D2. The list for car contains D1, and the list for bike contains D2. A query requiring blue and car can intersect their lists and find D1. This assumes the analyser records those words as the terms shown; different tokenisation or normalisation rules can change the terms. The index also needs source versions and appropriate access handling so that finding a candidate does not expose an obsolete or unauthorised representation.
What can go wrong between a snapshot and its CDC stream? || Imagine copying a row's old title, then starting the change stream after the title was edited. The copy contains the old value, and the stream never supplies the intervening edit. A defined snapshot and change position must prevent this gap. The destination also needs stable identities, ordering or version information, supported schema handling, and a way to recognise repeated changes. Even with a complete stream, applying rows separately can expose only part of a source transaction. The handoff and destination serving contract must address the consistency readers require.
What provenance makes an extracted field explainable? || Identify the particular output and connect it to the exact file version, page or region, extractor or model version, relevant parameters, and any human review that changed it. The references should let an investigator locate the evidence that was actually used. A confidence score does not supply these origins and does not prove the value correct. Keep the evidence needed for the investigation under an explicit privacy and retention policy; an unbounded copy of personal source text in an audit record creates its own lifecycle problem.
Updates and deletes continue during reindexing. What must happen before serving switches? || Build the new generation from a defined snapshot or source position, and capture the changes that follow that boundary. Apply updates and deletions through a validated catch-up point, preserving the intended versions. Check document identities, contents, permissions, and deletion handling, then define how changes arriving during the switch reach the live destination. Select the new generation through the serving pointer only once that handoff is established. Keep a usable, compatible rollback path. Matching counts cannot detect a stale document replacing a missing current one.
An event arrives three minutes late. Which time policy matters? || First ask whether the result groups events by when they occurred or by when the processor handled them. An event-time window may need to accept the late event into an earlier interval and revise a published count. Define how long such revisions are allowed, how corrections are identified, and what happens after that allowance ends. Consumers must know whether the first publication is provisional. A watermark estimates progress under lateness assumptions; it cannot prove that an event from an earlier time will never arrive.
Why is deleting only the PDF insufficient? || The PDF may have produced extracted text, a thumbnail, search postings, logs, and recoverable copies. Those artifacts can retain its information after the original disappears. Record the deletion intent, locate the relevant copies, and track required removals so failed steps can be retried. A worker already holding the input must also be prevented from publishing after deletion, for example by an atomic completion check against deleted state. Recovery from older data must apply the relevant deletion history before restored content becomes available.''')

add(14, '''A payment provider commits a charge, but its reply never reaches the order service. Why is this a partial failure, and how should the order service proceed? || The provider completed its part while the order service failed to learn the result. The local order may remain pending even though the charge exists. Keep that uncertainty in a durable operation record and query the provider using the stable reference where supported. Then reconcile the local order with the observed outcome. Rolling back local data cannot erase the charge, and blindly submitting another charge can repeat the effect.
A Lamport event has value 5 and another has value 9. What can you conclude from those numbers alone? What extra information can a vector comparison provide? || The numbers alone do not prove that event 5 happened before event 9. Lamport's guarantee works in the other direction: if one event happens before another, the later event receives a larger value under the algorithm. Independent events can also receive different values. With correctly maintained vector clocks for the same participant set, componentwise comparison can distinguish a recorded dependency from concurrency. Neither clock decides how conflicting business updates should be merged.
A register starts at 1. A write of 2 completes before another client's read begins, and no other write occurs. What must a linearizable read return? How does the answer change if the read overlaps the write? || The later read must return 2 because the completed write must precede it in the allowed order. If the operations overlap, the read may return 1 or 2, provided its result fits a legal common history. We can place the read before or after the write within their invocation-to-response intervals. A write whose reply times out is different from a confirmed failed write: its effect may still need to be included.
Two live replicas cannot communicate during a partition. One accepts and acknowledges a write. Explain why CAP prevents promising both atomic consistency and completion of every request reaching either side. || A later read on the other side cannot learn the new value while communication is cut off. Returning its old value can violate atomic consistency; waiting indefinitely or refusing the operation sacrifices the formal availability requirement. CAP concerns these defined properties for the shared object under the partition model. It does not classify an entire product permanently or determine normal-operation latency. Specify which operations wait, reject, or return an explicitly weaker result.
Can a booking service prevent double sales while failing to provide useful service? Explain why the progress requirement must be stated carefully. || Yes. It can leave accepted bookings pending forever without ever assigning one seat twice. This preserves the safety rule but violates a promise that accepted bookings eventually resolve. Rejecting every request also avoids double sales, and leaves no accepted booking to violate that particular promise. To rule out this second behaviour, require useful progress for valid requests under stated healthy and reachable conditions. Safety, completion of accepted work, and admission of useful work are distinct requirements.
A session reads version 10 of a profile. Its next request reaches another replica and returns version 9. Which guarantee has failed, and what could the serving replica do instead? || If monotonic reads were promised, the second response violates them because the session lost progress it had already observed. Carry a required version or replication position with the session. A replica below that position can wait to catch up, route to a sufficiently current owner, or report unavailability for that promised read. The progress information also needs a defined path through failover and device changes; ordinary sticky routing alone does not cover those transitions.
A design uses three fixed replicas, requires two write acknowledgments, and reads two replicas. Explain what R=2, W=2, N=3 proves and what remains to be shown before claiming linearizability. || Because R+W=4 is greater than N=3, every read set intersects every write set. A read therefore contacts a participant from a completed write's quorum, assuming both use the same fixed membership. The protocol must still explain what acknowledgments persist, how versions and concurrent writers are ordered, how reads treat unfinished writes, and how recovery and membership changes preserve that evidence. For example, a read must not expose a pending write and then allow a later read to forget it without an intervening write. Set overlap does not establish those rules.
Leader A pauses with epoch 7. Leader B obtains epoch 8 and begins taking over. A later resumes. Where and how should writes from the earlier owner be prevented? || The resource accepting the protected effect must enforce authority. For example, it can atomically check the fencing epoch with each write and reject epochs below the highest one it has accepted. Once epoch 8 is established there, A's epoch-7 request is rejected. The takeover must establish the needed fence before relying on exclusive new-owner effects, and the authority record must survive the failures covered by the contract. A timer in A's process cannot provide this enforcement. Test delayed messages and resumed processes as well as clean crashes.''')

add(15, '''A primary waits for a replica before reporting success. What must “synchronous replication” specify about that acknowledgment? || Name the required replicas and the event each reply establishes: receipt in memory, durable storage, or application to readable state. These events provide different protection. A record held only in memory can disappear when the replica process restarts, while a durably stored record may survive that restart without yet appearing in local reads. ¶ Also state the failure assumptions and which histories are eligible for promotion. Waiting for a durable copy is useful only if failover preserves the promised history. The extra wait adds latency and can prevent success while a required replica is unreachable.
Replicas agree to apply “create task” in the same log position. Why can choosing a random identifier independently on each replica still break the design? || The same ordered command must produce equivalent state from equivalent starting state. If replicas choose different identifiers, their task collections differ despite agreement about command order. Include the chosen identifier in the agreed command, or use a supported mechanism that makes the decision consistent. Reading current time independently creates the same kind of problem. ¶ This is deterministic command application. It also has a boundary: applying one command on several replicas must not produce several unprotected external charges. External effect ownership, duplicate handling, and recovery require their own mechanism.
A Raft leader sees an entry on two of three replicas. What else must be established before treating that entry as committed? || The participants must belong to the valid voter configuration, follow the durable-state rules, and have elected an eligible leader under Raft's term and log-comparison rules. For the direct majority-replication rule, the entry being used to advance commitment must belong to the leader's current term. Its commitment also commits the preceding prefix. ¶ An arbitrary earlier-term entry on a majority does not satisfy that rule: a later eligible leader could still replace such an uncommitted entry in some histories. This is why copy counts must be interpreted within the full protocol. Membership changes and reads also need their specified rules.
Why can replacing a voting group abruptly with a disjoint group allow conflicting decisions? || The old group can still form one majority while the new group forms another. If those decision sets share no participant carrying the earlier evidence, each group may accept a different history. Having a safe group before the change and another safe group afterward does not make the change safe. ¶ Use the implementation's supported membership protocol. Raft's joint-consensus transition temporarily requires the relevant majority of each configuration before moving to the new configuration alone. Catch new members up appropriately, preserve persistent identities, and test a leader failure during the transition.
Two disconnected regions each sell the last item they see. Why can a convergent counter still fail the stock rule? || Both regions start from a view containing one available item and accept a sale without observing the other sale. A merge that retains both decrements can make every replica agree on a negative balance. Agreement has preserved the updates, but the rule “never allocate more items than exist” has already been violated. ¶ Convergence concerns the result of the data type's update and merge rules; it does not enforce arbitrary business invariants. Exclusive allocation needs coordination, separately assigned spending rights, or another design whose allowed operations preserve the stock rule.
A worker carrying epoch 7 resumes after epoch 8 has become current for the attempt. Where and how must the old effect be rejected? || The receiver accepting the protected effect must know that epoch 8 is current and reject the request carrying 7. It must compare authority and apply the permitted effect atomically, so authority cannot change between a successful check and the update. The required authority state must survive the failures covered by the contract. ¶ A token recorded only in the coordinator is insufficient if the external store never checks it. Likewise, a local workflow completion check protects that local update; it does not automatically protect a remote file write or payment. Establish how every protected receiver learns and enforces the current generation.
A paused leader misses heartbeats and is falsely suspected of failure. What must remain safe while the system attempts recovery? || The suspicion must not allow incompatible accepted decisions or effects. The old leader may still run and send delayed requests. A replacement must obtain authority through the protocol's voting, log-eligibility, and persistence rules; a timeout alone cannot grant that authority. Protected external receivers may also need fencing against the old owner. ¶ Timeout tuning changes recovery speed and how often false suspicions occur. Safety must tolerate those suspicions being wrong. A received heartbeat, meanwhile, does not guarantee spare capacity or that an ordinary request can finish within its deadline.
A repaired old primary is reachable again. What must happen before it accepts authoritative writes? || It must rejoin under the current ownership and membership rules and establish a history compatible with the committed history. Depending on the protocol and its stored state, it may need to catch up, repair an uncommitted suffix, reconcile permitted conflicts, or be rebuilt. Its former leader role does not authorise it now. ¶ Keep obsolete writes fenced and apply the application's acknowledged-data policy when considering promotion. Verify routing and readiness before sending write traffic. Test this return path, called failback, as well as the initial failover; resuming an old primary prematurely can create a second inconsistency after the visible outage.''')

add(16, '''An ephemeral subscriber is disconnected when an event is published. Why can it not automatically replay that event on return? || The publication policy may retain no record for an absent subscriber, so there is nothing to replay. Recovery requires retained records and a stored way to locate the next work, such as a log position. Check the broker's actual retention and subscription policy; pub/sub alone does not promise durable replay.
A consumer can acknowledge before or after its required effect. How does each order behave if it crashes between the two events? || Acknowledging first can leave the broker finished while the effect is missing. Applying the effect first can leave the effect completed while broker progress is missing, causing another attempt. An atomic inbox and local effect transaction can make that repetition safe. Neither acknowledgment position alone covers an unrelated external provider.
A stream processor claims exactly-once behaviour. Which work can its transaction cover, and what must be checked before extending that claim to an email? || Its supported protocol can cover the records and consumed progress it commits atomically, under its fault assumptions. An arbitrary email server lies outside that transaction unless a further protocol covers the send. Name the protected effect and identity scope. Idempotency may give repeated executions one relevant result; it does not mean execution started only once.
Why can an outbox relay publish the same event twice even though the order and outbox row committed together? || The relay can publish successfully and crash before recording that it sent the event. Recovery still sees a pending row and publishes again. A stable event identity and consumer duplicate handling address this repetition. The original database transaction saved the obligation to publish; it did not include the entire network delivery.
A saga refunds a payment after checkout fails. Why is that compensation not necessarily an undo? || The refund is a further action. It can fail, remain uncertain, happen later, and have different fees or user-visible consequences from the original payment. Persist its progress and reconcile uncertainty. Because some effects cannot be perfectly reversed, the business must define an acceptable recovery outcome.
A local effect commits, but the message is delivered again. How can the consumer preserve one local update? || Store the unique event identifier and the local update in the same transaction. If it commits, a duplicate finds the established identity and skips another update; if it rolls back, neither fact is committed. Retain recognition for the supported replay horizon. An external call substituted for the local update needs its own protocol.
A worker continues running after its lease expires and a replacement starts. What protects later effects? || Check the current epoch when accepting local completion so an obsolete attempt cannot overwrite the replacement's result. The actual effect receiver also needs suitable fencing or a stable duplicate identity. Lease expiry cannot stop the old process. Distinguish effects already accepted before replacement from later stale attempts, and reconcile outcomes that remain uncertain.
A payment remains locally pending after its provider reply is lost. Why should recovery avoid resending it as a new operation? || The provider may already have charged the card. A new identity can create a second financial effect. Query by the original stable operation identity and repair local progress, or use the provider's supported safe retry protocol. Reconciliation establishes what happened to the existing intention; pending local state is not evidence that it never ran.''')

add(17, '''Why are two replicas not necessarily enough surviving capacity? || Assume each replica can meet its target at 100 requests per second. At 70% each, the pair serves 140 requests per second. Losing one leaves capacity for only 100, so the service needs more headroom or a permitted way to reduce or reject work. Continuing to queue the excess will not solve a sustained gap. ¶ Also check independence, usable state, and traffic movement. A second replica cannot take over if the same storage or configuration failure disables it too.
Why include pool acquisition in the overall deadline? || The caller spends its permitted lifetime waiting for a connection as well as executing the query. If every stage starts a fresh full timeout, the combined operation may continue after its result is no longer useful. Calculate the remaining time before each stage and release owned resources when work ends. ¶ A timeout still leaves a remote effect uncertain if the request may have reached the provider. Stopping the wait does not establish that the write never happened.
What does a circuit breaker help, and what remains unresolved? || An open breaker rejects selected calls promptly, reducing repeated waits and resource use while a dependency is failing. Half-open probes admit limited work to test recovery before ordinary calls resume. The policy must define which outcomes open or close the breaker and bound the probes. ¶ The dependency still needs to recover, and the application still needs an acceptable response. Rejecting or retaining a pending payment can preserve its meaning; fabricating approval cannot.
How can separate worker pools still share a failure bottleneck? || Email and payment workers may use separate pools but share one database or host. If email fills the database connection limit or exhausts memory through an unbounded queue, payment can still stop. Trace the resource through which harm spreads, bound its use, and measure saturation and rejection for each allocation. ¶ The combined limits must fit shared capacity. Partitioning also has a cost: one pool can be idle while another rejects work.
How do RTO and RPO differ? || RTO is the target time to restore the defined service. RPO specifies the acceptable gap in recoverable data history relative to the incident. A noon incident followed by service return at 12:20 gives twenty minutes of interruption. Recovering data only through 11:55 gives five minutes of data-loss exposure. ¶ Compare these separate measurements with the agreed targets. Count detection, restoration, validation, and traffic return in the recovery journey; measure actual lost records separately from the time-based exposure.
How should an end-to-end design limit a retry storm? || First identify which layer owns retries and enforce an overall attempt budget and deadline across the path. Four independently retrying layers can multiply work even if each has a modest local limit. Backoff with jitter spreads timing but does not reduce the configured total by itself. ¶ Bound admission and resource use, keep a stable identity where the receiver supports safe repetition, and track useful intents and completions separately from attempts. Reserve capacity for recovery and for resolving effects whose outcomes remain unknown.
Can a default cached balance replace an unavailable ledger? || A stale observed balance may be displayed only under a contract that permits that observation, with the necessary freshness and access rules. A made-up default does not establish the account's state. Neither can supply authority for a financial action that requires a current ledger decision. ¶ A cached help page has a different meaning: an older explanation may remain useful. Decide what the particular substitute permits, which actions must pause, and what the user should be told.
Why not send traffic straight back to a repaired primary? || The repaired primary may hold history from before failover and no longer have write authority. It must catch up or be rebuilt from the current history before a controlled handover. Fence any owner that should no longer write, then verify capacity and routing. ¶ Existing connections and cached addresses can still direct calls along old paths. Test failback through the user-visible journey, including an old owner's attempted write, rather than declaring success when its process starts.''')

add(18, '''Why is an internal network address not proof of a caller's identity? || An internal address tells us something about the route, but does not by itself identify the requesting workload or grant resource permission. A compromised internal worker can use that same route. Validate the caller's credential at the receiving boundary and check the requested action against the actual resource. If identity arrives in forwarded headers, accept those headers only from the configured trusted source.
How do OAuth 2.0 and OpenID Connect differ in purpose? || OAuth 2.0 supports delegated permission to access resources. OpenID Connect adds a defined identity layer, including an ID token for the client. In a login journey, the client validates the intended identity result; the API separately validates its access credential. Issuer, audience, expiry, and required flow context matter. An arbitrary access token cannot be substituted for a login assertion.
Why use purpose-built password hashing rather than a fast hash? || An attacker with the database can test guesses offline. A fast hash permits many cheap guesses; password hashing deliberately adds work, with salts preventing reuse of the same precomputed result across users. Use a maintained implementation and current deployment-appropriate settings. Store the settings for later upgrades and protect the separate online login and recovery paths.
Which paths need tenant isolation beyond the database query? || Follow a document through cache keys, job messages, worker inputs and outputs, search, export objects, download capabilities, telemetry, and administration. Each path needs trustworthy tenant and resource context. If A and B both have document 7, a shared cache key of 7 merges distinct records even when the database query was correct. Include the tenant in the identity and enforce permission on delivery.
Does an artifact's valid signature prove its code is safe? || A checked signature can establish the expected signing relationship and that the signed content has not changed, under the scheme's assumptions. It does not establish that the signer, dependency, or build was safe. Connect reviewed inputs to the artifact actually deployed, control build and release privileges, and retain a way to identify and replace affected releases.
A tenant A administrator guesses a tenant B document ID. What denies access? || Validate the actor, resolve A's permitted tenant context, and load or select the document under that scope. B's document must fail the resource and action policy: the administrator role applies to A. Apply the same rule to direct download, cache, export, and worker paths so another route cannot bypass the denial. Knowing the identifier and possessing a valid session do not grant the missing permission.
A backup survives but its only decryption key is destroyed. What went wrong? || The recovery plan preserved ciphertext but lost a required dependency. The backup needs the key version that encrypted its data, any protected data key, and the credentials or authority needed to use those keys. Test an actual restore with those dependencies before retiring an old version. Keeping the backup bytes alone does not make the data recoverable.
Membership is revoked after an export is queued. Where must that policy be enforced? || State the revocation contract first. If revoked members must receive no newly published exports, check current membership at execution and publication as required, coordinate those checks with publication, and durably record denial or cancellation. Protect download according to its own contract. A capability already issued may remain usable until expiry unless the delivery mechanism can revoke it; do not assume the queue-time decision covers these later stages.''')

add(19, '''How do logs, metrics, and traces complement one another? || Metrics summarise a population, so a latency distribution can establish how widespread a slowdown is. A trace connects one execution's work and waits, helping locate its delay. Logs record particular events and context, such as an attempt's outcome class. Stable operation identities help relate the appropriate records. Compare individual histories with the population, allowing for sampling, dropped records, and collection limits; one trace or missing log does not establish every user's outcome.
Why is a trace ID not an access credential? || A trace ID labels diagnostic context. A caller may supply it without proving who they are or whether they may access a resource. Validate or replace incoming context according to policy, then use the intended authentication and authorisation evidence for the action. Propagating tracing context connects evidence about the operation; it grants no resource permission.
Why can low CPU coexist with severe request delay? || A request waiting for a connection, lock, storage response, or remote call may use little processor time. RED can show rising request duration while USE exposes pressure on the resource holding up progress. For a full pool, inspect waiting requests and the work occupying its connections. Extra CPU will not by itself release those connections, so locate the delay before choosing capacity to add.
What is tenfold budget burn for a 99.9% success target? || The allowed bad fraction is 100% − 99.9% = 0.1%, or 0.001. An observed 1% bad fraction is 0.01, so burn rate is 0.01 / 0.001 = 10. The observed fraction is ten times the allowed fraction for the defined eligible events. State the windows and denominator. Remaining budget and event volume are also needed to judge how long the allowance will last; the ratio alone does not supply that duration.
Why avoid unique request IDs as ordinary metric labels? || Each combination of label values identifies a time series. A new request ID can therefore create another series, making the number of series and its storage and processing cost grow with requests. Use bounded metric dimensions for population measurements. Keep detailed operation identities in appropriate logs or traces, with retention and sampling chosen for the investigation they support.
A five-second request waits 4.6 seconds for a connection. Where should investigation focus? || Acquisition takes 4.6 / 5 = 0.92, or 92%, of this request's elapsed time. Examine pool occupancy, queueing, connection hold times, and the work holding connections, including relevant transactions or lock waits. Compare normal and slow paths and population measurements before extending the explanation. The trace locates a wait; it does not establish why the pool is full. Faster execution of this path's 100 ms query would remove little of its five-second duration.
Serving recovers but charges remain uncertain. Why is recovery incomplete? || A responsive API establishes that new serving work can proceed, but it does not resolve previously accepted payment outcomes. Some operations may still need provider-status reconciliation or required local postings. Follow their durable identities through the supported recovery path to safe final states. Verify those outcomes and assign any remaining recovery work; an infrastructure alert clearing supplies no proof that every accepted charge is resolved.
HTTP 202 is fast while jobs wait for hours. Which indicators are missing? || Measure acceptance-to-start delay, stage waits and processing durations, useful completions, and acceptance-to-required-outcome duration. Also track the age of unfinished work, especially the oldest unfinished operation: completed-job durations exclude jobs that never finish. Follow stable operation identity across attempts and stage commits to locate stuck work. HTTP acceptance measures the beginning of this journey and can remain fast while later progress stops.''')

add(20, '''What important boundary differs between a VM and a typical container? || A VM supplies a guest operating system on virtualised hardware; containers commonly share a host kernel while isolating processes. Both need resource, identity, network, storage, and image management. Check actual isolation and shared failure domains rather than treating packaging as a complete security or reliability guarantee.
How can a control-plane outage differ from a serving outage? || Existing workloads may keep serving while new placement or configuration changes cannot proceed. Replacement may need a dependency that current requests do not use. Draw control and data paths separately and define cached-configuration validity. Avoid unnecessary fresh control decisions in each request.
Why must a canary receive representative traffic? || A candidate exposed only to cheap reads can appear healthy while failing the expensive checkout path. Select cohorts and indicators that exercise the release risks, with stop conditions and sufficient observations. A small exposure is useful only when it tests behaviour relevant to the broader rollout.
Why can an old executable fail as a rollback? || New code may have written data or a schema that the old reader cannot understand. Expand-and-contract preserves an overlap period before obsolete state is removed. Identify when contraction ends safe rollback and what forward repair remains. Reversing traffic does not reverse every stored or external effect.
Which duties remain with a team using a managed database? || Schema, access, retention, application transaction use, acknowledgment choices, and validation of recovery still require owners. Provider tasks vary by contract. Test maintenance, throttling, failover, and credential changes instead of assuming “managed” covers every application correctness need.
Scale-down kills a worker holding an unrecorded job. What was missing? || Durable accepted-work identity and a safe drain or transfer protocol. Stop new claims, persist progress, and let another valid owner recover as required. Killing a process cannot preserve work that existed only in its memory, regardless of how well the platform schedules replacements.
A feature is disabled after writing a new data format. What risk remains? || Old code and clients may still read the new state. A flag changes exposure, not stored compatibility or past effects. Keep migration and reader support explicit, including what rollback or forward repair is supported after the new data exists.
Why do two successfully scheduled replicas not necessarily form a correct shared service? || Each may use an unrelated local database or incompatible configuration. Placement establishes running instances, not common state ownership. Define the shared or coordinated data model, identity, and failure behaviour before distributing requests across them.''')

add(21, '''What must accompany a reusable benchmark result? || Workload, data distribution, hardware or capacity, versions, warmup, concurrency, duration, success definition, variability, and relevant failures. A function microbenchmark cannot establish full application throughput. Preserve enough setup to reproduce and interpret the claim rather than presenting one number without its conditions.
How can coordinated omission hide waiting? || A generator waits for a slow reply before issuing later work that independent real arrivals would already have submitted. Some queueing and delay disappear from the observed population. Choose a generator model matching the workload and record offered, completed, failed, and abandoned work.
Why is a short measured throughput maximum not a safe production target? || Real operation includes variance, maintenance, background work, and required failure capacity. Near saturation, extra arrivals sharply worsen waiting or rejection. Locate the useful knee and reserve margin against the actual objective rather than running indefinitely at one short benchmark's ceiling.
Why can cost per attempt hide increasing cost per useful outcome? || Retries and failures can enlarge the attempt denominator without producing additional completed orders or documents. Define successful business outcomes and the accounting period, while retaining technical breakdowns. Compare candidates with equivalent correctness and service objectives.
What should an architecture fitness function protect? || A meaningful required property such as module dependencies, tenant isolation, compatibility, or tested recovery. It should permit harmless implementation changes and be updated when a valid architecture decision changes the requirement. Its pass establishes only its covered evidence, not universal correctness.
An index fixes the slow query. Why might sharding have been a poorer first step? || Sharding changes ownership, routing, transactions, and migration while the avoidable scan may remain. A targeted implementation fix can address the measured mechanism with less risk. Architectural change is justified when the underlying limit actually requires it, not because it sounds more scalable.
What does killing a process only before work begins fail to test? || It misses gaps such as commit before reply, output write before completion record, or resumed work after lease expiry. Inject faults at the boundary in question and check both serving and required state. Successful restart alone does not establish that accepted work survived.
Source and destination counts match but tenant owners differ. Why did validation miss it? || A count compares quantity, not identity or meaning. Compare keys, versions, relationships, ownership, and business invariants as appropriate. State whether the check examines all records or samples. Migration, replay, and recovery need evidence that the right data reached the right scope.''')

THOUGHT={2: 'How would simultaneous retries change an estimate based on average user sessions?',
 3: (((('Our application used to call a local function. Now it calls a service in another region. What new '
 'events can affect the result?')))),
 4: 'The client disconnects after an upload job is accepted. Should processing stop?',
 5: 'We replace payment objects with pure functions. Which requirements remain?',
 6: (('A saved notification job runs after its creating request and user session have ended. How should it '
 'obtain resources and permission to act?')),
 7: 'What evidence would justify extracting payments into a separate service?',
 8: 'Can finite storage support a permanent promise to recognise every old idempotency key?',
 9: 'How should restoration from a historical backup respect later deletion decisions?',
 10: 'What changes when one local transaction is divided across independent databases?',
 11: 'When should a product stop serving rather than return a stale cached result?',
 12: 'Every caller competes for one globally hot resource that can have only one exclusive owner. Can adding '
     'many partitions make these ownership decisions independent? Explain what a valid improvement would '
     'have to preserve.',
 13: 'How would you investigate an extracted field after both source and model have changed?',
 14: 'During a partition, exclusive seat allocation cannot obtain valid authority. Which other operations '
     'could remain useful, and how should their promises and recovery differ?',
 15: 'A failed region has been repaired and can receive traffic. What evidence would you require before '
     'allowing authoritative writes there again?',
 16: 'How could one broker transaction be exactly-once while two emails are sent?',
 17: 'How can a disaster drill restore infrastructure yet fail the business recovery requirement?',
 18: 'What should revocation mean for an issued object capability and a queued export?',
 19: 'What evidence would support a latency explanation beyond correlation with a release?',
 20: 'How can rollback restore old code while leaving incompatible data or effects?',
 21: 'When could a more expensive architecture be simpler to operate overall?'}

THOUGHT_ANSWERS={2: 'Retries add attempts without adding new user intentions. A daily session estimate therefore undercounts '
    'offered work when failed requests are repeated. If many callers retry at once, those attempts can '
    'arrive while the same dependency is still overloaded, creating another concentrated burst.\n'
    '\n'
    'Model the timing and maximum number of attempts separately from normal sessions. Bound retries and '
    'admission, and test useful completions, queue growth, and recovery under that burst. A peak factor '
    'based only on ordinary user arrivals may not cover the retry wave.',
 3: (((('The request must travel to another machine and the reply must travel back. Setup and travel add time. '
 'The server can finish while the reply is lost, leaving the caller uncertain. The interface now needs '
 'a waiting limit and a way to recognise or find the original operation when repeating it could cause '
 'another effect.')))),
 4: (((('First decide what acceptance promised. If the job must continue, its saved record and a worker '
 'outside the request scope own the remaining work. Request-owned children can stop and release their '
 'resources. If cancellation of the job is allowed, record that decision so later workers can obey it. '
 'Closing the connection alone neither deletes the saved job nor reverses work already completed.')))),
 5: (('The amount units, currency rules, permitted states, operation identity, and outcome meanings stay the '
 'same. Given the same state and provider result, the function should make the same business decision.\n'
 '\n'
 'The outer code must still perform and record effects safely. A timeout can still hide a completed '
 'charge, and a database write can still fail after that charge. Changing methods into functions does '
 'not combine those separate events or make replay safe automatically.')),
 6: (('Save the necessary job data and identifiers rather than an open connection or session object. The '
 'worker opens its own scope, obtains current resources, loads the data, performs the work, and '
 'releases those resources.\n'
 '\n'
 'The application also needs an explicit permission rule. Some jobs carry out work validly accepted '
 'earlier; others must check current permission before acting. Choose that rule for this operation. An '
 'old session object cannot silently stand for permission that remains current forever.')),
 7: 'Look for stable capability ownership, different scaling or isolation needs, and an operating team '
    'prepared for network and version failures. Compare those benefits with added data coordination and '
    'recovery. Preserve existing payment invariants and histories through migration. A separate deployment '
    'is useful only when the required independence can actually be exercised.',
 8: 'Not for an unbounded set of arbitrary distinct operations unless another constraint supplies a bound or '
    'persistent evidence elsewhere. Define key retention, expiry, reuse, and client expectations. A '
    'permanent business identity may require a durable record rather than an expiring cache. Make the '
    'promise fit the information the system can retain.',
 9: 'Restore into a controlled path, apply relevant deletion decisions, and reconcile raw and derived copies '
    'before serving. Rebuild indexes from the permitted current state rather than blindly expose an older '
    'snapshot. Keep deletion evidence narrow and purpose-limited. The backup and live-data lifecycle need a '
    'combined recovery procedure.',
 10: 'The two changes no longer automatically share one commit decision. Suppose the seat update commits in '
     'one database but inserting the reservation fails in another. Each store can behave correctly locally '
     'while the combined booking is incomplete.\n'
     '\n'
     'First identify which invariant needs agreement. A distributed transaction may supply a suitable shared '
     'decision if the stores and operating requirements support it. Alternatively, a workflow can represent '
     'intermediate states explicitly and use retries, reconciliation, or compensation to reach an acceptable '
     'outcome. That choice must define what the caller sees while work is incomplete. Separate local commits '
     'alone do not preserve the former all-or-nothing business promise.',
 11: 'Stop when the operation requires current authority or the permitted stale interval has ended. An old '
     'description may be allowed, while allocating scarce stock or deciding current access may not be. State '
     'which actions degrade and which wait or reject, with visible status and a recovery path.',
 12: 'Extra partitions can distribute unrelated records, but they do not divide the decision about this one '
     'exclusive resource. Two partitions independently granting ownership could accept incompatible winners '
     'and break the rule. The hot decision still needs a protocol that establishes the permitted owner.\n'
     '\n'
     'Read copies or batching may reduce suitable surrounding work, and a different allocation model may be '
     'possible if the requirements permit it. For any proposal, explain which work it removes or distributes '
     "and how it prevents conflicting grants. Measure the hot owner's actual work instead of inferring "
     'progress from the number of partitions.',
 13: "Locate the disputed output's own identity first. Follow its provenance to the exact source version and "
     'region, the model or transform version, relevant parameters, and any review decision. Compare the '
     'field with that retained source evidence. Running the current model on the current document examines '
     'different inputs and cannot establish what produced the old value. Even rerunning the recorded version '
     'may not reproduce a nondeterministic execution exactly. State that limitation separately from missing '
     'provenance, and retain the evidence the investigation requires within the applicable lifecycle policy.',
 14: 'A public event description can be served from a cached copy if its permitted age and access rules '
     'allow it. A feed read may also continue under an explicitly weaker freshness contract. These responses '
     'do not grant a seat, so they can have different serving rules from allocation. The allocation request '
     'must wait or fail explicitly where authority cannot be established. Make any stale view clear enough '
     'that it is not mistaken for a confirmed booking. When communication returns, reconcile pending '
     'allocations against the authoritative decision and resume eligible work without issuing a second '
     'winner.',
 15: 'Reachability shows that communication is possible; it does not establish authority or a safe history. '
     'Require the current ownership and voter configuration, a history compatible with committed decisions, '
     'and the durable copies required by the acknowledgment policy. An old leader may need rebuilding and '
     'must remain fenced while obsolete authority could still act.\n'
     '\n'
     'Also verify that routing directs writes to the authorised participants and that the region has enough '
     'capacity to resume its assigned work. Apply the supported rejoin procedure and reconcile uncertain '
     'external effects. The evidence should cover safe failback under current state, rather than assuming '
     'that restoring the old machines restores the old permission to lead.',
 16: 'The broker can atomically commit consumed progress and produced records while email remains outside '
     'its transaction. A consumer can send an email, lose the completion reply, and send again during '
     "recovery. Use the provider's contract, stable identity where supported, and reconciliation. The "
     "broker's scoped guarantee does not automatically cover the email effect.",
 17: 'Machines can run while restored data is too old for the RPO, backups lack usable keys, accepted jobs '
     'are missing, or competing owners can still write. Validation and traffic return may also push useful '
     'service beyond the RTO even when machine startup is fast.\n'
     '\n'
     'Test the full business journey with its required state, identities, authority, credentials, and '
     'recovery objectives. Include unresolved effects and catch-up work. A successful drill provides '
     'evidence for the scenario it exercised, rather than every possible disaster.',
 18: 'Define when each form of authority stops working. A queued export can check current membership before '
     'the later actions required by policy. An already issued object capability may remain usable until '
     'expiry unless the delivery mechanism supports earlier revocation. If immediate download denial is '
     'required, choose a delivery design that can enforce it rather than relying on expiry alone. Test '
     'revocation before execution, before publication, and after link issuance, and describe the resulting '
     'lifetime accurately to users.',
 19: 'Locate the extra wait or execution on affected paths and compare them with normal paths and population '
     'measurements. If the hypothesis is that a release holds connections longer, inspect changed request '
     'behaviour, connection hold times, occupancy, and acquisition waits in the timeline. Consider competing '
     'explanations and test a focused intervention under comparable conditions. Support is stronger when the '
     'mechanism predicts the symptom and changing that mechanism changes the observed behaviour; a release '
     'marker alone establishes timing.',
 20: 'Old code can return while new schemas, values, provider calls, and published messages remain. Maintain '
     'compatibility during overlap and identify the point where contraction ends safe rollback. Some '
     'outcomes need forward repair or compensation. Restoring an artifact cannot reverse every state '
     'transition it previously performed.',
 21: 'Compare total work for people as well as the invoice. A managed service may reduce patching, backup, '
     'or recovery burden while adding charges and leaving application responsibilities. Evaluate the same '
     'correctness and service goals with explicit staffing assumptions. Choose the design the team can '
     'understand, change, and recover reliably.'}

TASKS={2: ('Implement a capacity worksheet with explicit user activity, peak, and per-instance inputs.',
     'Make daily users, requests per user per day, peak multiplier, tested RPS per instance, and target '
     'utilisation explicit inputs. Validate positive workload and capacity values and require a utilisation '
     'fraction strictly between zero and one. Calculate daily requests, divide by 86,400 seconds/day, and '
     'multiply by the peak factor.\n'
     '\n'
     'The defaults give about 5,787.04 average requests/s and 28,935.19 peak requests/s. At an assumed 600 '
     'requests/s per instance and a 60% operating target, each contributes 600 × 0.6 = 360 requests/s of '
     'planned capacity. Dividing peak demand by 360 gives about 80.38; rounding upward gives 81 active '
     'instances. Providing 82 leaves 81 after one instance is lost.\n'
     '\n'
     'Keep the inputs and intermediate results in the output so changes can be checked. The arithmetic '
     'covers this request-serving resource and one-instance loss; database capacity, image delivery, '
     'routing, and failures that remove several instances still need their own evidence.'),
 3: ('Write a cold/warm request calculator. How will you check it?',
 'Store each stage’s time in milliseconds and add the stages actually needed. Check that 20, 40, 40, '
 'and 55 total 155, and that reusing setup leaves 55. Reject negative and non-finite times rather than '
 'producing a misleading total. Also check zero-duration stages and a request that reuses only some '
 'setup.'),
 4: ('Build a lost-update demonstration and a bounded upload queue. What should each show?',
 'Arrange for A and B to read zero before either writes, producing one. Then protect the complete '
 'update with a shared lock and show two. For uploads, set limits on both workers and waiting '
 'identifiers. Fill the queue and show the busy response. Also make conversion fail and check that its '
 'files and other resources are released. An in-memory demonstration needs saved job records before it '
 'can promise restart recovery.'),
 5: ('Supply a recording gateway that returns uncertain. What should the small test assert?',
 'Give the gateway a list of received commands. Its charge method appends a copy of the command and '
 'returns uncertain. Pass this gateway into pay instead of constructing a real provider inside pay.\n'
 '\n'
 'Assert that pay returns uncertain and that exactly one command was recorded with operation P7, USD '
 'currency, and amount_minor=100. This checks the collaborator boundary. It does not establish '
 "persistence, duplicate handling, or the order's state after the result."),
 6: ('Demonstrate transient, scoped, and singleton identity across two scopes. Then show why retaining a '
 'scoped resource does not keep it valid.',
 'Resolve a scoped object twice inside scope A and twice inside scope B. The identities should be A1,A1 '
 'and B1,B1. Transient lookups should create new instances, while singleton lookups within the stated '
 'container boundary should return S. Compare identity rather than equal values.\n'
 '\n'
 'Give the scoped resource a closed flag and record cleanup on scope exit. Exercise both normal '
 'completion and an exception. Retain a reference after exit and show that its use is rejected. Then '
 'obtain a fresh resource for a new operation and close it at that operation’s end.'),
 7: ('Implement shopping modules and one meaningful dependency-boundary check.',
     'Let orders use a payment contract without importing private payment storage or writing its tables. '
     'Check that boundary, then replace the provider adapter while preserving the order rule. Avoid a test '
     'tied to every internal class name; protect the dependency whose violation would spread provider '
     'details or bypass ownership.'),
 8: ('Implement keyset continuation and a durable operation-key model for synthetic payments.',
     'Use a stable ordered pair for continuation and test an insertion before a page boundary. Bind actor, '
     'key, fingerprint, progress, and result under appropriate atomicity. Identical retries return the old '
     'operation; changed payloads conflict. A dictionary lookup followed by an unrelated insert does not '
     'protect concurrent or restarted callers.'),
 9: ('Model profiles, financial entries, chat history, events, and PDFs from their required operations.',
     'List access patterns, rules, identity, retention, and recoverability before choosing stores. Several '
     'needs may share an engine. Keep immutable bytes distinguishable from metadata and derived search '
     'results. Explain how each copy is rebuilt or recovered, rather than assigning one product family per '
     'data type without a reason.'),
 10: ('Run the conditional last-seat claim with two connections to one store.',
      'Open two connections to the same database file and create one available seat. Call claim_seat for A '
      'through one connection, then for B through the other. Assert that A returns true, B returns false, '
      'and a fresh read shows A as the owner. Two separate in-memory databases would not test competing '
      'claims on one seat.\n'
      '\n'
      'Inspect the guarded UPDATE and its transaction: owner changes only where the seat exists and owner IS '
      'NULL, and success is based on one affected row. Test rollback of an equivalent guarded update before '
      'commit and confirm that another connection can still claim the seat afterward. These checks establish '
      'the local ownership rule. Payment, expiry, and a genuinely overlapping concurrency stress test '
      'require their own checks.'),
 11: ('Run ideal LRU, then reproduce stale cache-aside population after invalidation.',
      'A,B,C,A,D at capacity three evicts B. Next pause a reader with version one, commit version two and '
      'invalidate, then resume old population. Show the stale result. Apply a justified version or '
      'coordination rule if the freshness requirement forbids it; shortening TTL alone does not remove the '
      'race.'),
 12: ('Run the provided rendezvous example with owners A, B, C, and then D. Count assignments before and '
      'after, and send most simulated requests to one key. What should the two measurements reveal?',
      'For every key whose assignment changes, check that its new owner is D. The existing scores for A, B, '
      'and C do not change, so adding D cannot make one of those owners overtake their previous winner. '
      'Count keys per owner to inspect placement in this fixture.\n'
      '\n'
      'Next count requests per owner while most requests use one selected key. That key still selects one '
      'owner, so its popularity can produce very uneven traffic despite a reasonable distribution of key '
      'counts. Explain what would reduce its actual pressure: suitable read copies, reduced repeated work, '
      'or a safe change to write ownership. Moving an assignment alone still requires data transfer and '
      'coordinated routing.'),
 13: ('Implement source-version and attempt checks, then plan a safe index-generation switch.',
      'In Workflow.complete, reject completion if the document is deleted, the supplied epoch differs from '
      'the current epoch, or the supplied input version differs from the required input. For epoch 8 and '
      'file-version-2, the worked example rejects epoch 7 and file-version-1, then accepts the matching '
      'pair. A real store must perform the check and output publication atomically and validate the '
      'artifact. Keep transform identity and source evidence as well. For the index switch, build from a '
      'defined boundary, catch up updates and deletes, validate versions and access, and maintain a '
      'continuous ingestion handoff before selecting the new generation. The local predicate does not '
      'implement that wider protocol.'),
 14: ('Use the mechanism collection to evaluate lamport_receive(5,9), vector_relation([1,0],[0,1]), and '
      'vector_relation([1,0],[1,2]). Then enumerate the two-member read and write sets of A,B,C and explain '
      'their intersection.',
      'lamport_receive(5,9) returns max(5,9)+1=10. The first vector comparison returns concurrent: the first '
      'entry is larger in [1,0], while the second is larger in [0,1]. The next returns before because every '
      'entry of [1,0] is no larger than the corresponding entry of [1,2], and at least one is smaller. The '
      'two-member sets are {A,B}, {A,C}, and {B,C}; any read/write pair shares at least one member. These '
      'calculations agree with the supplied code. To claim a storage guarantee, still specify the version '
      'order, acknowledgment durability, read handling of unfinished writes, and membership rules.'),
 15: ('Implement a receiver that rejects stale attempt epochs. Which update must be atomic, and how would '
      'you check its behaviour?',
      "Keep the attempt's current epoch and workflow state in persistent storage. When epoch 8 is "
      'established as owner, a completion request for epoch 7 must not alter the state. Perform the epoch '
      'comparison and the permitted state transition in one transaction or atomic conditional update. '
      'Checking the epoch first and writing in a later unprotected step leaves a race with an ownership '
      'change.\n'
      '\n'
      'Check that completion at 7 fails after takeover at 8, that the valid completion at 8 can succeed, and '
      'that restart retains the authority decision. Define repeated completion behaviour according to the '
      "workflow's contract. Then identify external effects separately: this receiver protects its own stored "
      'transition. Any remote effect that could be caused by the resumed old worker also needs suitable '
      'receiver-side authority enforcement.'),
 16: ('Crash the outbox relay after publication, then process the duplicate with a local inbox transaction.',
      'The fixture should show two deliveries of the same event and one counter change. The unique event '
      'identity and local increment must commit together, so a duplicate skips the established effect. If '
      'the counter is replaced conceptually by email, identify the missing provider protocol: the local '
      'inbox transaction cannot include an arbitrary external send across its failure gap.'),
 17: ('Calculate nested retry amplification and design a bounded provider-outage policy.',
      'With three attempts at each of four nested layers, the worst-case downstream allowance is 3×3×3×3 = '
      '81 attempts for one logical request. This includes the initial attempt at each layer; deadlines or '
      'earlier success may stop execution sooner.\n'
      '\n'
      'Give the operation an overall retry budget and deadline, bound admission, and isolate the resources '
      'at risk. Use backoff and jitter for retry timing and limited probes for recovery. Return a permitted '
      'pending or failure result rather than fabricated payment approval. After the provider returns, '
      'reconcile uncertain operations using their retained identities.'),
 18: ('Test the synthetic tenant predicate, then trace all data paths using that decision.',
      'The shown assertions permit active actor A to read an A resource and reject reading a B resource. '
      'Also test an inactive actor and an action absent from its permissions: both should be denied. These '
      'checks test the predicate with supplied attributes, not credential validation or completeness of the '
      'attributes. Then trace trusted tenant scope through cache keys, job resolution, object access, '
      'export, and search. A correct predicate cannot protect a path that bypasses it.'),
 19: ('Build the five-second trace model and an asynchronous completion indicator.',
      "Use the fixture's sequential stages: 300 ms elsewhere + 4,600 ms pool acquisition + 100 ms query = "
      '5,000 ms. Check that pool acquisition accounts for 4,600 / 5,000 = 92%. These assertions check the '
      'constructed accounting, not a measured cause of saturation. For jobs, record accepted_at and the '
      'required outcome under a durable operation identity. For an unfinished job compute now − accepted_at; '
      'for a completed job compute outcome_at − accepted_at. Track useful completions and oldest unfinished '
      'age alongside stage wait and processing times. Store detailed identities in suitable records and '
      'aggregate with bounded metric dimensions.'),
 20: ('Plan and test an expand-and-contract release with old and new readers.',
      'Add compatible state, deploy overlap-safe readers, backfill with bounded progress, and verify. Retire '
      'old readers before removing obsolete schema. Test rollback before that point and identify what '
      'requires forward repair afterward. Expose representative traffic to a canary, including important '
      'expensive paths.'),
 21: ('Compare the three fictional architectures against equal requirements and costs.',
      'cost_options totals 371, 551, and 1,402 monthly units. Keep these inputs separate from measured '
      'capacity and reliability. Use the constructed latency and independent-component examples only within '
      'their assumptions, then state which real tests would establish each candidate meets the original '
      'workload and service goals.')}

DESIGN={2: ('A team sizes servers from daily average RPS alone. Identify the missing evidence and propose a safer '
     'estimation process.',
     'Begin with the user journeys, required outcomes, and operation mix. Estimate the requests, physical '
     'writes, stored bytes, and transfer each journey causes. Calculate an average with explicit units, then '
     'add separate peak and growth assumptions, including peak duration and the delay before scaling takes '
     'effect.\n'
     '\n'
     'Measure per-instance capacity using a representative workload and the required latency and error '
     'targets. Choose operating headroom and check whether the remaining instances can handle traffic during '
     'the failures the design must tolerate. Size the database and image path separately.\n'
     '\n'
     'Treat the worksheet as a workload to test. Verify user latency, rejection, queue growth, and recovery '
     'under normal, peak, and degraded conditions. A calculated instance count alone cannot establish that '
     'the complete design meets its requirements.'),
 3: ('“Read” appears twice after a create request times out and is sent again. How would you change the '
 'request flow?',
 'Give the original request a stable operation identifier. Save the new task and that operation’s '
 'result together. An identical retry uses the same identifier and receives the saved result; a changed '
 'request must not reuse that identity as if it were identical. This repairs task creation within the '
 'stored-operation rules. A remote provider would need its own repetition and recovery rules.'),
 4: ('Every upload starts another background task. How would you limit the work and keep accepted jobs '
 'through a restart?',
 'Use a worker limit for active conversions and a queue limit for waiting jobs. Store large file bytes '
 'separately and queue small references. Give each accepted job a saved identity, input reference, and '
 'progress record. Replacement workers can then find unfinished jobs after restart. Return acceptance '
 'only after the required record is saved; define a clear busy or waiting result when capacity is '
 'unavailable.'),
 5: ('How would you split a class that parses requests, calculates fees, calls a provider, and stores '
 'results?',
 'First record the results and state changes for approval, decline, timeout, and storage failure. '
 'Extract fee calculation and compare the same inputs and outputs. Then separate request parsing, '
 'provider translation, and storage in small steps, checking the same behaviours after each move.\n'
 '\n'
 'Pass the gateway into the payment service. Keep provider field names in the adapter and amount units '
 'in the gateway contract. Preserve uncertainty: a failed local save after a successful remote charge '
 'does not undo that charge. The design should make each responsibility easier to locate without '
 "changing the caller's promised results."),
 6: ('An application-wide notification service looks up a request connection in a global container and '
 'stores it. Propose a clearer arrangement.',
 'There are two problems. The global lookup hides the connection dependency. Storing the connection '
 'retains a request-owned resource in an object that outlives the request.\n'
 '\n'
 'Keep the service’s lasting dependencies valid for its lifetime. Pass a valid unit of work into each '
 'database operation, or inject a narrow factory that creates an operation scope. The request or job '
 'owns that scope, supplies the correct user context, and closes resources after the work ends.'),
 7: ('Several services share tables and require simultaneous releases. Review whether the deployment split '
     'is useful.',
     'Map who owns decisions and data, what changes together, and what fails together. A modular '
     'consolidation may be simpler, or revised contracts and ownership may justify separation. Compare '
     'independent operation with the actual network, migration, and incident costs.'),
 8: ('A payment API returns a Boolean and provides no operation status. Redesign it for an uncertain '
     'provider reply.',
     'Create a stable intent identity, explicit pending/approved/declined/uncertain semantics, validated '
     'money units, and scoped repeat-key handling. Offer status recovery. Define compatibility and '
     'permission as well as field shape so clients know what repeating the request means.'),
 9: ('A search engine holds the only copy of private document text. Review ownership, recovery, and '
     'deletion.',
     'Keep a recoverable source and exact identity/version relationships for derived entries. Enforce access '
     'while indexing lags, and track deletion across copies and restores. If search truly owns the '
     'authoritative data, it needs the corresponding complete durability and recovery contract rather than '
     'assumptions borrowed from a projection.'),
 10: ('Two doctors can each go off call after seeing the other available. Propose a transaction design '
      'preserving at least one on call.',
      'One design runs every operation that changes this on-call rule in a serializable transaction. Read '
      'the relevant doctors, check that another doctor will remain on call, and only then mark the '
      'requesting doctor off. Commit before reporting success. If a serialization failure occurs, retry the '
      "complete transaction with fresh reads and bounded attempts. Once one doctor has left, the other's new "
      'attempt must refuse to leave.\n'
      '\n'
      'An alternative uses a shared coordination row for the rota with Read Committed isolation. Every '
      'participating transaction locks that row before issuing the reads that check the doctors and making '
      'its change. A waiting transaction performs those reads after acquiring the lock, so its new statement '
      "snapshot includes the preceding transaction's committed decision. All writers must follow the same "
      'protocol. Locking only the doctor being changed leaves the original write-skew history possible. Keep '
      'external notifications safe under retries and release them only under a deliberate completion '
      'policy.'),
 11: ('A cache-aside reader repopulates old data after the writer invalidates it. Define and repair the '
      'actual freshness requirement.',
      'Trace old read, new commit, invalidation, delayed old insertion. If that stale result is forbidden, '
      'use a supported version or coordination protocol. If bounded staleness is allowed, state its limit '
      'and validate authoritative state for critical actions. TTL is not a universal repair.'),
 12: ('After the team doubles application replicas, database timeouts increase. Describe an investigation '
      'and a correction that would preserve service while testing the cause.',
      'Start with the request path. Measure offered work, useful completions, connection acquisition time, '
      'connection hold time, query execution, and lock waiting. Count the pools across all instances and '
      "compare their aggregate demand with the database's connection budget. This can distinguish an "
      'application compute limit from pressure created by the new callers.\n'
      '\n'
      'Bound admission and retain capacity needed for recovery while investigating. If a particular query or '
      'contention pattern is responsible, change that access path or resource use where the evidence '
      'supports it. Then compare completions, queues, timeouts, and slower responses again. Increasing every '
      'pool can merely relocate waiting into the database, so the correction must address the demonstrated '
      'cause.'),
 13: ('A reindex copies records while updates and deletions continue. Design the handoff to a new serving '
      'generation.',
      'Keep generation A serving while B is built from a defined source snapshot and change position. '
      'Capture changes after that position, including deletes, and apply them to B without letting an older '
      'version overwrite a newer one. Track progress to a catch-up boundary. Validate source identities, '
      'versions, representative query results, access scope, and deletion outcomes; row counts alone are '
      'insufficient. Establish how live ingestion continues across the switch, then select B through an '
      'explicit serving pointer or routing version. Retain A only as long as the rollback and retention plan '
      'requires, and keep it current enough for any promised rollback. Preserve the source and '
      'transformation evidence needed to rebuild again.'),
 14: ('A partition separates three replicas into A and the pair B,C. Both sides receive requests to allocate '
      'the same exclusive seat. Propose a policy that preserves one winner, including the steps needed when '
      'communication returns.',
      'Use a suitable authority protocol, such as one requiring a majority decision in the fixed '
      'three-member configuration, together with enforcement at the seat store. B and C can potentially '
      'establish the required decision; A alone cannot issue a new exclusive allocation. Before the new '
      "owner's effects are relied on, establish the authority fence so a delayed or resumed older owner "
      'cannot also succeed. Requests without valid authority wait or receive an explicit failure. Operations '
      'explicitly permitted to use stale information may continue separately. On recovery, discover and '
      'retain the authoritative allocation, reconcile pending requests, and bring the old participant up to '
      'date before allowing it to act. Two conflicting successful sales cannot be repaired merely by calling '
      'them a merge.'),
 15: ('A worker pauses beyond lease expiry. A new owner begins work, and the old worker returns. Design '
      'protection against stale effects and stale release requests.',
      'Give each ownership grant an ordered generation and a distinct owner identity through an '
      'authoritative coordinator. Carry the generation with protected work. At every protected receiver, '
      'establish the applicable current generation and atomically compare it with the incoming request '
      'before applying the effect. Persist this state as required by the failure model. Once epoch 8 is '
      'established there, an epoch 7 action must fail.\n'
      '\n'
      'Require release and renewal to match the owner and generation, so an old holder cannot remove or '
      "extend the new holder's permission. Specify how a new generation becomes known at each receiver; "
      'merely issuing a token does not fence an unaware store. Finally, separate stale actions from effects '
      'already accepted before the change. Fencing does not undo those earlier effects or make an unrelated '
      'external API enforce authority.'),
 16: ('An order commits but its event is never published. Design durable publication and repeated-delivery '
      'handling.',
      'Commit the order change and outbox intent in one local transaction. Have a relay retry pending '
      'publication with a stable event ID, allowing for a crash after publication but before its sent '
      'marker. A subscriber should commit recognition of that event ID with its local effect. Other external '
      'effects need their own identity and reconciliation contract.'),
 17: ('A provider slowdown holds every connection and triggers layered retries. Break the cascade without '
      'inventing business success.',
      'Start with the resource history: slow calls retain connections, queues grow, and retries add work to '
      'the reduced capacity. Apply an overall deadline and release owned resources; bound admission, queues, '
      'and retries; isolate optional workloads; and use a breaker with limited recovery probes.\n'
      '\n'
      "Return failure or a valid pending or degraded outcome according to the operation's contract. Preserve "
      'identities and track uncertain external effects so they can be reconciled. Reserve recovery capacity '
      'and test the fallback under the combined failed traffic, since it can become another bottleneck.'),
 18: ('A private export is authorised at submission but its worker trusts the old tenant field forever. '
      'Review the complete journey.',
      'Resolve the requester and permitted tenant from trusted state, select scoped resources, and durably '
      'record the export operation. Queue a reference to that operation; let the worker resolve its scope '
      'and enforce the chosen current permission policy. Limit its input and output authority, keep the '
      'result private, and control publication and download. Track cancellation and deletion so retries '
      'cannot publish obsolete output. Record meaningful audit outcomes. Test membership removal between '
      'submission, execution, publication, and download, including the behaviour of any capability already '
      'issued.'),
 19: ('HTTP acceptance stays fast while background jobs stop finishing. Redesign the service indicators and '
      'alert.',
      'Define which accepted jobs are eligible, which terminal outcomes satisfy the service, and the '
      'relevant age limits. Preserve operation identity across delivery, attempts, stage commits, retries, '
      'and final outcomes. Track queue delay separately from processing duration, useful completions, and '
      'current age of unfinished work. Break down the stage or owner where progress stops. Alert on '
      'actionable completion harm or oldest unfinished age, with an owner and a procedure for locating and '
      'recovering the work. Keep detailed operation IDs out of ordinary metric labels; use drill-down '
      'records to investigate individual jobs.'),
 20: ('A blue-green release shares one database and removes a column needed by the old version. Review its '
      'rollback plan.',
      'Parallel app environments do not make shared state reversible. Use compatible expansion and '
      'overlap-safe readers, backfill and verify, then retire old readers before contraction. Mark the end '
      'of safe rollback and the forward repair path. Test representative mixed-version traffic.'),
 21: ('A faster and cheaper benchmark configuration omits failures and disables authorisation. Can it '
      'replace the original design?',
      'It tests a different workload and service contract. Restore mandatory correctness and access checks, '
      'include failed and waiting work, disclose setup, and compare useful outcomes under the original '
      'requirements. A favourable number cannot compensate for removing the properties the service must '
      'provide.')}

CASE_ASSESSMENT=[('conceptual',
  'C1',
  'A short-link click count is temporarily behind, while two buyers are trying to claim one seat. Why can '
  'these operations use different consistency rules?',
  'The delayed count can often be corrected by processing identified click events later. During the delay, '
  'the displayed total is less fresh, but no exclusive resource has necessarily been allocated twice.\n'
  '\n'
  'A seat claim must decide who owns the seat before confirmation. If two callers both win and the records '
  "converge later, the service has already broken its promise. State each operation's observable rule and "
  'failure behaviour: delayed aggregation may suit the count, while the claim needs one coordinated '
  'ownership decision.'),
 ('conceptual',
  'C2',
  'A chat service returns a persisted receipt, then the recipient disconnects before receiving a live frame. '
  'What has the receipt established, and how should delivery recover?',
  'The receipt establishes that the accepted message is retained under the stated storage contract. It does '
  'not establish that a recipient device received the frame or that a person read the message.\n'
  '\n'
  'The returning device fetches history after its known sequence, detects gaps, and recognises repeated '
  'messages by identity. Device-delivery and human-read evidence are tracked separately. This makes a missed '
  'live frame recoverable without changing the meaning of the persistence receipt.'),
 ('conceptual',
  'C3',
  'Worker A pauses at epoch 7. Its lease expires, and worker B receives epoch 8. Why does the lease alone '
  'not guarantee one external execution?',
  "Lease expiry changes who currently has permission to work; it does not stop A's paused process. A can "
  "resume and perform an action alongside B. An atomic current-epoch check rejects A's local completion, "
  'preserving local progress.\n'
  '\n'
  'The external receiver needs supported stable effect identity or enforced fencing to protect its own '
  'boundary. Fencing requires the receiver to reject stale authority; merely attaching an epoch is '
  'insufficient. An effect accepted before authority changed may still require reconciliation. Neither the '
  'lease nor the local completion check by itself establishes one external execution.'),
 ('conceptual',
  'C4',
  'Two document replicas finish with equal text. What else must be checked before calling the collaborative '
  'editor correct?',
  'Equal text establishes only that final comparison for that history. The replicas may both contain an '
  'unauthorised edit, invalid rich-text structure, incorrect Unicode treatment, or broken undo behaviour.\n'
  '\n'
  'First check convergence under the chosen protocol and its supported operation context. Then test access, '
  'structural validity, identity-based repetition, and reconnect from snapshots and retained history. '
  'Include offline clients whose access has changed. These properties need separate evidence; convergence '
  'does not supply them automatically.'),
 ('conceptual',
  'C5',
  'An extraction worker finishes without an exception. What further conditions may be needed before a '
  'document-processing workflow is complete?',
  'The output must be usable, permitted, and linked to its exact source and pipeline versions. It may still '
  'need structural validation, human review, or publication. A worker finishing only establishes progress '
  'through that attempt.\n'
  '\n'
  'Track extraction, review decisions, and publication separately. Preserve the evidence, actor, and version '
  'needed to explain the result. If deletion or authority changes before publication, current-state checks '
  'must still prevent stale output from becoming available. Define complete in terms of the required output '
  'journey.'),
 ('scenario',
  'S1',
  'A payment succeeds after its seat hold has expired. Another buyer may now own the seat. What may the '
  'booking service safely do?',
  'Read the current authoritative ownership and apply the documented recovery policy. The service may '
  'reacquire the seat only through a valid claim if it is still available. Otherwise, it must follow a '
  'refund or another supported resolution; the successful payment cannot justify issuing against another '
  "buyer's confirmed seat.\n"
  '\n'
  'Keep the provider operation identity and reconcile the financial result. Expiry does not erase a charge '
  'that happened externally. Seat ownership and payment recovery must both be resolved without allowing one '
  "to overwrite the other's evidence."),
 ('scenario',
  'S2',
  'A provider charges successfully, the process stops before recording its reply, and the client retries. '
  'How can the service avoid another logical charge?',
  'Persist intent and stable provider operation identity before submission. On retry, recover that operation '
  "rather than inventing a new key. Use the provider's supported safe-repeat or status protocol and "
  'reconcile its existing effect before considering another submission.\n'
  '\n'
  'Apply verified evidence through an idempotent local transition that creates one valid balanced posting '
  'set. The local key and transaction protect local records; they cannot impose unsupported deduplication on '
  'an arbitrary provider. If available evidence cannot resolve the effect yet, retain uncertainty instead of '
  'declaring failure and charging afresh.'),
 ('scenario',
  'S3',
  'An epoch-7 extraction worker finishes after the document is deleted or its attempt is superseded. What '
  'must stop the old artifact from being published?',
  'At the authoritative completion boundary, check current epoch, input version, and live deletion state '
  "together with the state change. Reject the artifact's completion if those conditions no longer hold. A "
  'check performed only before computation can become stale while the worker runs.\n'
  '\n'
  'Publication and derived serving paths must respect the same current lifecycle state. Sending a '
  'cancellation message is insufficient because the worker may already be running, paused, or unreachable. '
  'The persisted conditional transition supplies the local protection independently of worker timing.'),
 ('design',
  'D1',
  'Review a short-link service at 100,000 redirects/s when its cache becomes unavailable. What assumption '
  'has changed, and what must the design demonstrate?',
  'With a warm 90% hit ratio, only 10% of 100,000 redirects/s reaches the source: 10,000 reads/s before '
  'retries or coalescing. Cache loss removes that assumption, so fallback demand can approach the full '
  'offered rate.\n'
  '\n'
  'Define bounded origin admission and the permitted response when capacity is exhausted. Test cold-cache '
  'capacity, hot links, and recovery while preserving expiry and revocation rules. Extra cache replicas can '
  'reduce some failures, but do not establish safe fallback or immediate invalidation. Record the supported '
  'degraded outcome and the evidence for it.'),
 ('implementation',
  'I1',
  'Choose one case study and implement its failure exercise. Which invariant will you check, where will you '
  'interrupt execution, and what recovered state should result?',
  'Name the exact protected boundary and an observable invariant before writing the test. For example, a '
  'short-link creation may commit its mapping and operation result, lose the reply, then return that same '
  'mapping on a repeated key without a second creation. A seat exercise can instead check that an old expiry '
  'never releases a newer reservation.\n'
  '\n'
  'Inject the interruption at the relevant boundary and inspect recovered records, including repeats or '
  'stale work. Explain why the mechanism enforces the result. Use the provided fixtures as examples, while '
  'keeping external guarantees within the actual mock, provider, or editing-protocol contract. A passing '
  'local exercise does not establish unsupported external behaviour.'),
 ('thought_experiment',
  'T1',
  'You can fund another region, tested restores, or stronger reconciliation first. How would you choose '
  'which work reduces the most important risk?',
  'Start with the most harmful unmet requirement and a failure history showing the gap. If the sole copy can '
  'be destroyed, reconciliation cannot recreate its missing bytes. If provider effects have no recoverable '
  'identity, another region repeats the same uncertainty. A restore test addresses a different question: '
  'whether saved data can become a usable recovered system.\n'
  '\n'
  'Compare the risk reduced, operating work added, and evidence each option can provide. Record why the '
  'selected change addresses the present gap and what observation would justify reconsidering the choice. '
  'Additional infrastructure is useful when it repairs the required failure behaviour.')]
