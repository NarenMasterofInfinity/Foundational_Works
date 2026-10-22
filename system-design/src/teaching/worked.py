"""Small mechanisms and explanations of what their results establish."""
CASE_FOR_UNIT={2: 5,
 3: 1,
 4: 12,
 5: 9,
 6: 4,
 7: 8,
 8: 9,
 9: 12,
 10: 8,
 11: 5,
 12: 1,
 13: 12,
 14: 5,
 15: 10,
 16: 8,
 17: 9,
 18: 12,
 19: 9,
 20: 1,
 21: 1}
CODE={2: ('Python · examples/mechanisms.py',
     'from mechanisms import capacity, amdahl\nprint(capacity())\nprint(amdahl(.8, 4))',
     'The capacity() defaults assume ten million users making fifty API requests each day. That is 500 '
     'million requests/day. Dividing by 86,400 seconds/day produces about 5,787.04 average requests/s, and '
     'the assumed peak factor of five gives 28,935.19 requests/s.\n'
     '\n'
     'The assumed instance capacity is 600 requests/s, with a 60% utilisation target. Planned capacity is '
     'therefore 600 × 0.6 = 360 requests/s per instance. Peak demand divided by this allowance is about '
     '80.38 instances. Rounding upward gives 81 active instances; providing 82 leaves 81 when one instance '
     'is lost. The worksheet sizes only this assumed request-serving resource. Database capacity, image '
     'delivery, routing, and the placement of instances across possible failures need separate checks.\n'
     '\n'
     'The second call, amdahl(.8, 4), uses a parallel fraction of 0.8 and four workers. Its remaining '
     'sequential fraction is 0.2, so the ideal duration is 0.2 + 0.8/4 = 0.4 of the original. The printed '
     'speedup is 1/0.4 = 2.5. This model keeps the amount of work fixed and omits the cost of coordinating '
     'workers.'),
 3: ('Python · arithmetic model',
 'cold = dict(dns=20, tcp=40, tls=40, request_and_work=55)\n'
 'assert sum(cold.values()) == 155\n'
 'warm = dict(request_and_work=55)\n'
 'assert sum(warm.values()) == 55',
 'The first assertion checks 155 ms. The second checks 55 ms. Both use assumed durations; the code '
 'performs arithmetic rather than measuring a network connection.'),
 4: ('Pseudocode · fifty workers and at most one hundred waiting jobs',
 'waiting = bounded_queue(capacity=100)\n'
 '\n'
 'def accept(upload):\n'
 '    file_id = save_temporary_upload(upload)\n'
 '    if not waiting.try_put(file_id):\n'
 '        delete_temporary_upload(file_id)\n'
 '        return "busy"\n'
 '    return "queued for this run"\n'
 '\n'
 'def worker():\n'
 '    while True:\n'
 '        file_id = waiting.take()\n'
 '        try:\n'
 '            convert(file_id)\n'
 '            record_success(file_id)\n'
 '        except ConversionError:\n'
 '            record_failure(file_id)\n'
 '        finally:\n'
 '            close_job_resources()\n'
 '            delete_temporary_upload(file_id)\n'
 '\n'
 'start_workers(worker, count=50)',
 'When fifty workers are busy and one hundred jobs are waiting, the next attempted queue insertion '
 'fails. That upload’s temporary file is removed and its caller receives “busy.” When a worker '
 'finishes, it takes another waiting identifier.\n'
 '\n'
 'This example assumes the shown storage and cleanup operations succeed. Its queue is in memory, so '
 'restart loses queued entries. To promise restart recovery, store a job record before reporting '
 'durable acceptance and let replacement workers find unfinished records.'),
 5: ('Python · injected collaborator',
     'class RecordingGateway:\n'
     '    def __init__(self): self.calls = []\n'
     '    def charge(self, command):\n'
     '        self.calls.append(command)\n'
     '        return "uncertain"\n'
     '\n'
     'def pay(command, gateway):\n'
     '    return gateway.charge(command)\n'
     '\n'
     'gateway = RecordingGateway()\n'
     'assert pay({"amount_minor":100,"currency":"USD"}, gateway) == "uncertain"',
     'The recording gateway receives the command, appends it to calls, and returns “uncertain.” The pay '
     'function returns that result unchanged, so the assertion passes. Inspecting gateway.calls would also '
     'show the supplied USD amount of 100 minor units. Passing the gateway as an argument lets us exercise '
     'this behaviour without contacting a provider.\n'
     '\n'
     'This example isolates the collaborator boundary. It does not validate money, supply an operation '
     'identifier, persist progress, or reconcile a real charge. A complete payment service needs those '
     'responsibilities and tests of its resulting business state. Preserving the uncertain result here '
     'matters: the caller has not been given evidence of either approval or decline.'),
 6: ('Python · lifetime identities',
     'singleton = object()\n'
     'def new_scope(): return {"scoped": object()}\n'
     'a, b = new_scope(), new_scope()\n'
     'assert a["scoped"] is a["scoped"]\n'
     'assert a["scoped"] is not b["scoped"]\n'
     'assert object() is not object()\n'
     'assert singleton is singleton',
     'The code creates one singleton reference and two separate scope dictionaries, a and b. Each scope '
     'stores one object under "scoped". Looking up that key twice in a returns the same object; looking it '
     'up in b returns a different object. Calling object() twice models two transient creations, while '
     'reading singleton twice returns the one application-owned reference.\n'
     '\n'
     'The assertions compare identity, meaning whether two references point to the same object. They '
     'demonstrate reuse rules in one process. They do not implement a DI container, actual request handling, '
     'or disposal. A real scoped resource also needs cleanup at scope exit, and a long-lived service must '
     'not keep using it after that boundary.'),
 7: ('Pseudocode · module contract',
     'place_order(command):\n'
     '    priced = catalog.quote(command.items)\n'
     '    reservation = inventory.reserve(command.items)\n'
     '    payment = payments.authorize(command.operation_id, priced.total)\n'
     '    return orders.record_outcomes(priced, reservation, payment)\n'
     "# Modules expose contracts; they do not update each other's private tables.",
     "The modules communicate through their operations rather than writing each other's private tables. "
     'Their results let the caller record what actually happened.\n'
     '\n'
     'Calling three remote services in this order does not create one atomic transaction. Some local changes '
     'can share a deliberate transaction, while external effects need a workflow and recovery rules.'),
 8: ('Python · keyset continuation',
     'from mechanisms import keyset_page\n'
     'rows = [(1,1,"A"), (1,2,"B"), (2,3,"C")]\n'
     'assert keyset_page(rows, after=(1,1)) == rows[1:]',
     'The ordered time/ID pair gives equal timestamps a stable tie-breaker. Continuing after (1,1) returns '
     'the later rows in this fixed fixture.\n'
     '\n'
     'A real cursor also needs validation, query and tenant scope, and a rule for changes between pages. '
     'Keyset continuation does not itself freeze a changing dataset.'),
 9: ('Pseudocode · bytes and metadata',
     'upload = create_authorized_upload(tenant, expected_size)\n'
     'object = store_and_verify_bytes(upload)\n'
     'with transaction():\n'
     '    insert_document(tenant, object.version, object.digest)\n'
     '    insert_processing_intent(object.version)\n'
     '# Orphan-byte cleanup handles incomplete metadata handoff.',
     'The metadata points to a verified immutable object version and records the processing obligation. If '
     'metadata commit fails, the object can remain orphaned and needs reconciliation or cleanup.\n'
     '\n'
     'The local transaction does not include the earlier separate object upload. Track that handoff '
     'explicitly instead of describing it as one cross-service commit.'),
 10: ('Python · conditional seat claim',
      'from mechanisms import open_demo_store, claim_seat\n'
      'db = open_demo_store()\n'
      'db.execute("INSERT INTO seats VALUES (1,NULL)")\n'
      'db.commit()\n'
      'assert claim_seat(db, 1, "A")\n'
      'assert not claim_seat(db, 1, "B")\n'
      'db.close()',
      "The store begins with seat 1 available: its owner is NULL. A's call executes an UPDATE guarded by "
      "owner IS NULL. It changes one row and commits, so claim_seat returns true. B's later call checks the "
      'same condition, now finds the seat owned by A, and changes zero rows. Its false result tells the '
      'application that B did not acquire the seat.\n'
      '\n'
      'This SQLite example checks availability directly; it does not use the version-seven column from the '
      'earlier optimistic-control example. Both place the check and change in one database operation. The '
      'executable mechanism collection also checks claims through two connections to the same file-backed '
      'store. These calls demonstrate the local ownership result; they are not a test of every overlapping '
      'schedule.\n'
      '\n'
      'The protected rule is that only an available seat can be claimed. A complete booking also needs '
      'deliberate rules for its reservation record, payment, hold expiry, and stale callbacks. This local '
      'transaction cannot atomically perform an external charge.'),
 11: ('Python · ideal LRU',
      'from mechanisms import LRU\n'
      'cache = LRU(3)\n'
      'for key in "ABC": cache.put(key, key)\n'
      'cache.get("A")\n'
      'assert cache.put("D", "D") == ("B", "B")',
      'After A,B,C,A, ideal LRU considers B the least recently used. Adding D evicts B, as the assertion '
      'checks.\n'
      '\n'
      'The fixture models entry count and exact recency. Actual caches can approximate the policy and use '
      'byte or expiry limits. Eviction alone says nothing about whether a loaded value is current.'),
 12: ('Python · stable rendezvous mapping',
      'from mechanisms import rendezvous\n'
      'for key in range(1000):\n'
      '    old = rendezvous(key, ["A","B","C"])\n'
      '    new = rendezvous(key, ["A","B","C","D"])\n'
      '    assert old == new or new == "D"',
      'The loop examines the 1,000 integer keys from 0 through 999. For each key, the first call selects its '
      'rendezvous owner among A, B, and C. The second call includes D as an additional candidate. The '
      'variables old and new hold those two selected owners.\n'
      '\n'
      'The assertion permits two outcomes: the key keeps its old owner, or its new owner is D. This follows '
      'from stable scores for each key-owner pair. A, B, and C retain their previous ordering, so their '
      'earlier winner cannot be displaced by another of those same owners merely because D joins. Only D can '
      'introduce a new winning score. The loop checks this property over the fixture; it does not assert '
      'that any particular fraction of keys moves.\n'
      '\n'
      "The code calculates assignments without moving stored data or synchronising clients' membership "
      'information. A real handover still needs those procedures. Also, every key has one selected owner in '
      'this model. If most requests use one key, they still reach that owner even when the counts of '
      'assigned keys look well spread.'),
 13: ('Python · source and attempt fencing',
      'from mechanisms import Workflow\n'
      'run = Workflow("file-version-2", epoch=8)\n'
      'assert not run.complete(7, "file-version-2", "old")\n'
      'assert not run.complete(8, "file-version-1", "wrong-input")\n'
      'assert run.complete(8, "file-version-2", "current")',
      'The workflow starts with file-version-2 as its required input and epoch 8 as the current attempt. The '
      'first call supplies epoch 7. Although its input version matches, complete returns False and leaves '
      'the result unset because the attempt is old. The second call supplies epoch 8 but names '
      'file-version-1, so it is rejected for using the wrong input. The third call supplies both current '
      'values and stores the artifact named current.\n'
      '\n'
      'These checks prevent the two illustrated stale completions from replacing the intended result. '
      'Workflow also rejects completion when its deleted flag is set, although the displayed calls do not '
      'exercise that condition.\n'
      '\n'
      'This is a local state model. In a real store, checking authority and publishing the result must '
      'happen atomically, or deletion or replacement could occur between the check and the write. The '
      'artifact itself still needs validation. Provenance should name the transformation version and '
      'relevant source evidence as well as the output location.'),
 14: ('Python · ordering models',
      'from mechanisms import vector_relation, lamport_receive\n'
      'assert vector_relation([1,0], [0,1]) == "concurrent"\n'
      'assert vector_relation([1,0], [1,2]) == "before"\n'
      'assert lamport_receive(5, 9) == 10',
      "The code first compares [1,0] with [0,1]. The first vector is ahead in A's entry and behind in B's "
      'entry. Neither contains all the progress recorded by the other, so vector_relation returns '
      '"concurrent". The first assertion checks that result.\n'
      '\n'
      'Next it compares [1,0] with [1,2]. The A entries are equal, and the B entry has advanced from 0 to 2. '
      'Every component of the first vector is no greater, with one strictly smaller, so the function returns '
      '"before". Finally, lamport_receive(5,9) takes the larger value, 9, and adds one, giving 10.\n'
      '\n'
      'These assertions check ordering calculations for the supplied values and a common participant set. '
      'They do not simulate message delivery, persistence, or agreement among replicas. A smaller Lamport '
      'number alone does not prove a dependency, and a vector relation does not choose how conflicting '
      'account edits should be merged. Those behaviours need their own application and protocol rules.'),
 15: ('Pseudocode · three replicas, one partition',
      'A,B,C contain committed index 8\n'
      'partition isolates old leader A\n'
      'B and C elect eligible B in term 5\n'
      'B appends index 9, term 5\n'
      'B and C durably replicate index 9\n'
      'Raft commit rule establishes committed prefix\n'
      'A cannot acknowledge a new quorum-committed write alone\n'
      'rejoin: A follows term 5 and repairs uncommitted suffix',
      'The trace begins with three fixed voters A, B, and C, all containing committed history through index '
      '8. Assume that participants follow the protocol rather than behaving maliciously, and that required '
      'protocol state is durable across the allowed crashes. A partition isolates the old leader A while B '
      'and C can still communicate.\n'
      '\n'
      "B becomes leader in term 5 only after satisfying Raft's election rules, including log eligibility and "
      "the required majority of persisted votes. B appends index 9 with term 5. B's durable copy and C's "
      "durable copy form a majority of the three voters. Because index 9 belongs to the current term, Raft's "
      'commit rule lets B establish commitment through index 9, including the preceding prefix. Replicas '
      'then apply committed commands in order; durable storage alone is a different milestone from '
      'application.\n'
      '\n'
      'A has only its isolated vote and cannot acknowledge a new quorum-committed write alone. It may remain '
      'alive and retain uncommitted work, which is why isolation must not be treated as proof that the old '
      'process stopped. On rejoining, A observes term 5, follows the current leader, and repairs an '
      "incompatible uncommitted suffix under Raft's rules. Committed history must be preserved.\n"
      '\n'
      'This pseudocode follows one history; it does not implement elections, log matching, recovery, '
      'membership changes, or fresh reads. Use the full supported protocol for those operations. In '
      'particular, an isolated node must not serve a supposedly current read merely because it still '
      "believes it is leader, and changing the three-voter configuration requires the implementation's "
      'membership procedure.'),
 16: ('Python · duplicate delivery, one local effect',
      'from mechanisms import open_demo_store, consume_local_event\n'
      'db = open_demo_store()\n'
      'assert consume_local_event(db, "E1", "orders")\n'
      'assert not consume_local_event(db, "E1", "orders")\n'
      'assert db.execute("SELECT value FROM counters").fetchone()[0] == 1\n'
      'db.close()',
      'The first call receives E1 and returns True. Within its transaction, it inserts E1 into the '
      'processed-event table and increments the orders counter from zero to one. The second call uses the '
      'same E1, finds that identity already present, returns False, and leaves the counter at one. The '
      'assertion checks this committed local result.\n'
      '\n'
      'Event recognition and the counter update share one transaction. If that transaction rolls back, '
      'neither change is committed, so recovery can try again. If acknowledgment is lost after commit, '
      'repeated delivery can safely find E1. This example protects a local database effect. Replacing the '
      'increment with an external email or payment call would require another protocol because the provider '
      'is outside that transaction.'),
 17: ('Python · retry amplification',
      'attempts_per_layer = 3\n'
      'independent_retry_layers = 4\n'
      'assert attempts_per_layer ** independent_retry_layers == 81',
      'The assertion calculates 3⁴ = 81 permitted downstream attempts in the nested worst case. The first '
      'layer can make three attempts; each can cause three at the next layer, giving nine, then '
      "twenty-seven, then eighty-one. Each layer's three attempts include its initial attempt. Actual "
      'execution can stop earlier after success or when another limit is reached.\n'
      '\n'
      'The code checks the arithmetic, not an outage policy. Use an overall retry budget and deadline to '
      'bound the whole path, protect capacity for useful work and recovery, and retain operation identity '
      'under a supported repetition rule. Jitter changes when attempts occur; it does not reduce the '
      'configured total by itself.'),
 18: ('Python · synthetic tenant policy',
      'from mechanisms import permit_demo\n'
      'actor = {"tenant":"A", "active":True, "actions":["read"]}\n'
      'assert permit_demo(actor, {"tenant":"A"}, "read")\n'
      'assert not permit_demo(actor, {"tenant":"B"}, "read")',
      'The first assertion returns True: the active actor belongs to tenant A, the resource belongs to A, '
      "and read is in the actor's allowed actions. The second returns False because the resource belongs to "
      'B. The predicate also requires active to be exactly True and the action to appear in actions.\n'
      '\n'
      'The example assumes that actor and resource attributes have already been supplied by a trustworthy '
      'source. It does not authenticate credentials, load current membership, or validate malformed identity '
      'records. In a real path, establish those facts before evaluating permission, and ensure that a denial '
      'stops the effect. Trace the same tenant scope through cache keys, queued jobs, object access, '
      'exports, and search; the two assertions alone do not verify those paths.'),
 19: ('Python · one trace accounting model',
      'stages_ms = {"other":300, "pool_wait":4600, "query":100}\n'
      'assert sum(stages_ms.values()) == 5000\n'
      'assert stages_ms["pool_wait"] / sum(stages_ms.values()) == .92',
      'The dictionary assigns durations to three sequential stages of one constructed request. Their sum is '
      '300 + 4,600 + 100 = 5,000 ms, so the first assertion checks the five-second total. The second divides '
      '4,600 ms of pool acquisition by 5,000 ms overall: 0.92, or 92%. The query accounts for only 100 ms. '
      'Halving that query time would save 50 ms if the other stages stayed unchanged.\n'
      '\n'
      'The model directs investigation toward the acquisition wait, but it neither collects a real trace nor '
      'establishes why connections are occupied. Inspect hold times, relevant transactions and locks, and '
      'normal as well as slow request populations before attributing the incident to a particular mechanism. '
      'The dictionary also assumes sequential accounting; real traces can contain overlapping spans whose '
      'durations cannot simply be added.'),
 20: ('Pseudocode · safe release progression',
      'add_compatible_schema_field()\n'
      'deploy_mixed_version_safe_code()\n'
      'backfill_with_bounded_progress()\n'
      'verify_old_and_new_readers()\n'
      'retire_old_readers()\n'
      'remove_obsolete_schema_only_when_safe()',
      'Old and new readers coexist during compatible expansion and backfill. Retire old readers before '
      'removing the structures they need.\n'
      '\n'
      'Rollback is safe only while its state and protocol assumptions still hold. Destructive contraction or '
      'external effects may require forward repair. Verify the actual running artifact and configuration '
      'too.'),
 21: ('Python · fictional comparison',
      'from mechanisms import cost_options\n'
      'totals = {name:sum(parts.values()) for name,parts in cost_options().items()}\n'
      'assert totals == {"single":371, "replicated_app":551, "partitioned":1402}',
      'The monthly totals are 371, 551, and 1,402 fictional units. They show how component costs add, rather '
      'than how the deployments actually perform.\n'
      '\n'
      'Check equal requirements before ranking price. The additional latency and availability models have '
      'explicit synthetic inputs; real capacity, tails, and recovery require corresponding tests.')}

# Context comes before the code in these introductory units.
CODE_CONTEXT={3: ((('The following Python code adds the four times in our example. The dictionary stores a name and '
 'duration for each stage. On the warm path, the earlier setup is reused, so only the request-and-work '
 'stage remains.'))),
 4: ((('Let us connect the worker pool to a definite acceptance rule. This pseudocode stores each upload as a '
 'temporary file and tries to add its identifier to a queue. A full queue returns “busy”; it does not '
 'accept that job. An accepted entry is queued for this process run.\n'
 '\n'
 'The queue holds at most 100 waiting identifiers. Fifty copies of worker run. try_put adds an '
 'identifier only if there is space; take waits while the queue is empty. convert either finishes or '
 'raises ConversionError. The finally block releases that job’s resources on either exit.\n'
 '\n'
 'These limits cover conversion jobs. The service also needs separate limits on file sizes and '
 'simultaneous upload reception, since accept saves the file before checking queue space.')))}
