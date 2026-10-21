"""Pattern mechanisms, applications, and costs in the notification example."""
PATTERN_LESSONS={4: [('Factory Method',
      'An exporter has a stable job: obtain a writer and ask it to write the rows. A CSV exporter needs a '
      'CSV writer, while another exporter may choose a different format. We can put that construction '
      'decision in make_writer(). The shared export operation calls it and then uses the returned writer '
      'through the writer contract.\n'
      '\n'
      'Factory Method makes this creation operation a point that a concrete creator can customise. In an '
      'inheritance-based implementation, a specialised exporter overrides make_writer(); in a smaller '
      'design, a supplied creation function may express the same needed variation. The processing code does '
      'not have to name each concrete writer.\n'
      '\n'
      'Use this arrangement when the creator genuinely needs a construction choice. A direct constructor '
      "call is clearer if the choice never varies. Also define the returned writer's ownership: if it holds "
      'an output stream, someone must close it after writing. Abstract Factory addresses a related but '
      'larger choice, producing a compatible family of objects rather than customising one creation '
      'operation.',
      ['Exporter calls factory method',
       'Concrete creator selects CSV writer',
       'Writer satisfies output contract'],
      'export(rows):\n    writer = make_writer()\n    writer.write(rows)'),
     ('Abstract Factory',
      'An HTML notification needs a renderer and a template that use the same content model. If the '
      'application chooses each independently, it could accidentally pass a plain-text template to an '
      'HTML-specific renderer. The two objects form a compatible family.\n'
      '\n'
      'We first select HtmlNotificationFactory. The client asks that factory for renderer() and template(), '
      'then passes the template and data to the renderer. A plain-text factory can supply the corresponding '
      'plain-text family through the same product contracts. Abstract Factory keeps these related creation '
      'choices together, so clients can switch families without assembling each combination themselves.\n'
      '\n'
      'The arrangement is useful when complete families really vary. Its maintenance cost appears when we '
      'add a new kind of product: every supported factory may need another creation operation. If one stable '
      "renderer and template are all the application needs, direct assembly can be clearer. The family's "
      'contracts must still explain compatibility and any resource ownership; using one factory does not by '
      'itself validate every possible input.',
      ['Select HTML family', 'Create HTML renderer and template', 'Both share compatible content model'],
      'family = HtmlNotificationFactory()\n'
      'renderer = family.renderer()\n'
      'template = family.template()\n'
      'renderer.render(template, data)'),
     ('Builder',
      'A notification needs a recipient and a template. A caller may also choose its locale and expiry. With '
      'a Builder, the caller records these choices in stages: set the recipient, select the template, and '
      'optionally set an expiry. The builder holds the unfinished choices until build() is called.\n'
      '\n'
      'The build step checks required fields and their relationships. For example, it can reject an expiry '
      'earlier than the permitted send time, or a template that does not support the chosen locale. Only '
      'after those checks does it return a usable notification. The partly configured builder is therefore '
      'distinct from the completed value; code should not send it as if it were already valid.\n'
      '\n'
      'Builder is helpful when staged assembly makes a complicated set of choices easier to express. It '
      'solves a different problem from Abstract Factory, which selects compatible kinds of products. For a '
      'small notification value, a constructor with named arguments may collect and validate every field '
      'just as clearly. Add the stages when they help the caller construct a valid result.',
      ['Set recipient and template', 'Add optional expiry', 'Build validates required fields'],
      'builder.to(recipient).template(template_id)\n'
      'notification = builder.expires_at(deadline).build()\n'
      '# build rejects missing recipient or incompatible fields'),
     ('Prototype',
      'A report layout already contains carefully chosen margins, sections, styles, and a title. We want a '
      'second layout with most of those settings and a different title. Prototype creates it by copying the '
      "configured instance, then allowing the copy's owned values to change.\n"
      '\n'
      'Follow what happens to a nested editable section. A shallow copy of the layout may leave both layouts '
      'pointing to the same section. Editing that section through the copy then changes what the original '
      'sees too. A clone operation can copy the mutable values that should belong to the new layout while '
      'retaining references to suitable immutable data, such as shared font definitions.\n'
      '\n'
      'The copying contract must identify these choices. A deeper copy is not automatically correct: copying '
      'a connection handle does not create another independently owned connection. Resource ownership needs '
      'its own rule. Prototype is useful when copying configured values is clearer than reconstructing every '
      'setting; fresh per-request state built from immutable configuration may be simpler when the ownership '
      'rules would otherwise be difficult to follow.',
      ['Configured layout prototype', 'Copy layout-owned values', 'Do not duplicate resource ownership'],
      'layout = prototype.clone_owned_values()\n'
      'layout.title = "Monthly report"\n'
      '# Shared immutable font data remains shared'),
     ('Singleton',
      'Suppose the application loads immutable configuration once at startup. Each service can receive the '
      'same configuration object because they all use the same values and none changes them. A Singleton '
      'arrangement restricts access to an instance within a stated program or container boundary.\n'
      '\n'
      'State that boundary explicitly. Process A can have instance S1, while process B has S2. Neither is a '
      'single object shared across every host. A container-managed singleton describes a reuse lifetime; a '
      'class that constructs its own sole instance and offers global access also determines how callers '
      'obtain it. These are related arrangements with different effects on visibility and testing.\n'
      '\n'
      'An application-owned instance can be passed to its users through ordinary injection. Its owner '
      'remains responsible for any required cleanup. Sharing mutable request data in one instance is '
      "riskier: concurrent callers can interfere, and tests can retain one another's state. A singleton "
      'lifetime does not make an object safe for concurrent use or make its shorter-lived dependencies valid '
      'indefinitely.',
      ['Process A has instance S1', 'Process B has instance S2', 'Global uniqueness is not implied'],
      'configuration = load_immutable_configuration()\n'
      'service = Service(configuration)\n'
      '# One application-owned instance; no hidden global lookup')],
 5: [('Adapter',
      'Our application asks a Sender to send a message and return an outcome such as accepted, declined, or '
      'uncertain, together with a reference when available. An SMS provider instead expects its own request '
      'format and returns its own status codes. An Adapter connects these different interfaces.\n'
      '\n'
      'The service calls adapter.send(message). The adapter encodes the message for sdk.submit(), invokes '
      "the provider, and maps the provider's response into the application's outcome. The service can then "
      'apply notification policy using its own vocabulary. SDK request objects and exceptions can stay '
      'inside the adapter rather than spreading through the service.\n'
      '\n'
      'The mapping must preserve meaning. If a timeout leaves it unclear whether the provider accepted the '
      'message, the adapter must not report a definite decline merely to fit a convenient branch. Check '
      'these mappings against the provider contract and its real integration behaviour. A Decorator usually '
      "retains an interface while adding behaviour around it; an Adapter's main purpose is to reconcile a "
      'mismatch in interface or representation.',
      ['Application Sender contract', 'Translate request and outcomes', 'Foreign SMS provider API'],
      'send(message):\n    raw = sdk.submit(encode(message))\n    return map_provider_outcome(raw)'),
     ('Bridge',
      'Notifications vary in content: an alert and a receipt format different information. They also vary in '
      'transport: either might go by email or SMS. If we create a subclass for every combination, changes to '
      'content and transport become tangled across AlertEmail, AlertSms, ReceiptEmail, and ReceiptSms.\n'
      '\n'
      'A Bridge separates these dimensions through composition. A Receipt receives a transport object during '
      'construction. Its deliver(data) operation formats receipt content and calls transport.send(content). '
      'An Alert can use the same transport contract while formatting different content. We can add a '
      'transport implementation without rewriting every content class, provided it supports the agreed '
      'contract.\n'
      '\n'
      'The contract still needs to accommodate the actual transports, including their limits and outcomes. '
      'This separation earns its cost when both dimensions vary independently. One fixed sender may need far '
      'less structure. Adapter commonly reconciles an existing interface mismatch; Bridge deliberately '
      'arranges two kinds of variation so they can develop separately.',
      ['Alert or receipt content', 'Composes transport interface', 'Email or SMS transport'],
      'class Receipt:\n'
      '    constructor(transport): self.transport = transport\n'
      '    deliver(data): return self.transport.send(format_receipt(data))'),
     ('Composite',
      'A notification audience may be one user, a department group, or a group containing other groups. The '
      'caller needs to obtain the recipients without writing separate traversal code for every shape. '
      'Composite gives an individual audience and a group a compatible operation.\n'
      '\n'
      'A leaf returns its authorised recipient. A group applies the same operation to its children and '
      'combines the results. Repeating this rule lets the caller traverse a nested audience. The example '
      'records visited node identifiers in seen so revisiting a node does not continue the same traversal '
      'indefinitely. The recipient contract must also say how repeated users from different groups are '
      'deduplicated.\n'
      '\n'
      'Real audience graphs need depth or size bounds and a policy for cycles and failures. A group send can '
      'reach some recipients before another send fails; the common interface does not make all deliveries '
      'atomic. Separate recipient selection from delivery where useful so the caller can inspect a bounded '
      'plan. When the domain has no meaningful nested structure, a simple collection and loop may be easier '
      'to understand.',
      ['Audience group contains audiences',
       'Leaf is one authorized recipient',
       'Traversal bounds and deduplicates'],
      'recipients(node, seen):\n'
      '    if node.id in seen: return []\n'
      '    seen.add(node.id)\n'
      '    return node.users_or_recursive_children(seen)'),
     ('Decorator',
      'We want to measure Sender.send() without placing timing code inside every provider adapter. A '
      'TimingSender receives another Sender, called inner. Its send(message) records a start time, calls '
      'inner.send(message), and records the elapsed time when that call finishes, including an error exit. '
      'It returns the original result or lets the original error continue.\n'
      '\n'
      'This is Decorator: an object adds behaviour around a collaborator while retaining its interface. '
      'Because TimingSender is also a Sender, the service can use it through the same contract. Startup code '
      'makes the added behaviour visible by assembling the wrapper around the selected adapter.\n'
      '\n'
      'Wrapper order matters. TimingSender(RetrySender(sender)) measures the whole logical call, including '
      'its attempts and waits. RetrySender(TimingSender(sender)) measures each attempt separately. A retry '
      'can also repeat an external effect, so it needs a contract for safe repetition and uncertain '
      'outcomes. Metrics alone cannot provide that contract. Keep essential notification decisions visible '
      'instead of scattering them through a long, difficult-to-inspect stack of wrappers.',
      ['Metrics wraps Sender', 'Sender returns explicit outcome', 'Wrapper records duration and result'],
      'send(message):\n'
      '    start = clock()\n'
      '    try: return inner.send(message)\n'
      '    finally: metrics.observe(clock() - start)'),
     ('Facade',
      'A client that submits a notification should not have to coordinate every internal step itself. The '
      'subsystem may validate the command, select a template, build a delivery plan, and save a notification '
      'intent. A Facade offers a focused entry operation, such as submit(command), that carries out this '
      'coordination for its clients.\n'
      '\n'
      'In the example, submit first validates the command. It constructs the plan from the validated data '
      'and asks the intent store to persist it. The returned intent identifier tells the caller which '
      'accepted piece of work it can inspect later. Internal responsibilities can remain in separate '
      'collaborators even though the caller uses one entry point.\n'
      '\n'
      "The facade's response must state what has happened. Saving an intent is different from completing "
      'delivery to the recipient. Keep the facade focused on a coherent subsystem; adding every unrelated '
      'operation makes it difficult to change. A Proxy usually represents the same conceptual target while '
      'controlling its use. A Facade primarily simplifies how a caller works with several cooperating parts.',
      ['Client uses one submit operation',
       'Facade coordinates subsystem roles',
       'Returns accepted intent identity'],
      'submit(command):\n'
      '    validated = validate(command)\n'
      '    return intents.persist(render_plan(validated))'),
     ('Flyweight',
      'Suppose ten thousand notifications use the same version of a template. Parsing that template '
      'separately for every notification repeats data that does not change. Flyweight shares the reusable '
      "part while keeping each use's changing context separate.\n"
      '\n'
      'The application obtains one immutable parsed template for the selected version. To render '
      "notification A, it supplies A's recipient and variables; to render B, it supplies B's context to the "
      'same template. The template contains the common structure. The per-recipient context contains the '
      'information that must remain separate. This division reduces repeated storage without making '
      'recipients share their personal values.\n'
      '\n'
      'Putting recipient fields into the shared object could let one rendering affect another or disclose '
      "another user's data. Keep the shared part suitable for its allowed concurrent use. Measure memory "
      'pressure before adding complex pools: ordinary immutable reuse may be sufficient. Version selection, '
      'expiry, cache bounds, and lifetime still need their own rules. Flyweight identifies what can be '
      'shared; it does not supply a complete cache-management policy.',
      ['Shared immutable template parse', 'Recipient A context separate', 'Recipient B context separate'],
      'template = parsed_templates.get(version)\n'
      'output_a = render(template, context_a)\n'
      'output_b = render(template, context_b)'),
     ('Proxy',
      'A caller wants to read a document through read(document_id, actor). A Proxy presents that operation '
      'and controls access before forwarding it to the actual document reader. In the example, it checks the '
      "actor's current permission and calls target.read(document_id) only when the check permits it.\n"
      '\n'
      "The caller works through the target's interface while the proxy handles a particular aspect of its "
      'use. Other proxies can defer creating an expensive target until first use, or represent an object '
      'reached through a network. In each case, the proxy stands in for the same conceptual target, with '
      'additional rules around reaching it.\n'
      '\n'
      'Those rules remain part of the observable contract. A remote read may take time or fail with an '
      'uncertain result; a local-looking method name does not remove that behaviour. Avoid hiding unbounded '
      'retries or unlimited loading behind the interface. Facade usually offers a simpler entry to a '
      'cooperating subsystem, while Proxy controls access to a target that the caller conceptually already '
      'wants to use.',
      ['Client requests document read', 'Proxy checks current access', 'Authorized target returns data'],
      'read(document_id, actor):\n    authorize(actor, document_id)\n    return target.read(document_id)')],
 6: [('Strategy',
      'A shop calculates an order price using either its ordinary pricing policy or an agreed partner '
      'policy. The order operation needs the resulting price, but it need not contain every formula. '
      'Strategy supplies the selected algorithm through a shared operation such as calculate(order).\n'
      '\n'
      'Assembly or policy-selection code chooses a strategy, and the caller invokes that strategy through '
      'the calculation contract. Adding another pricing policy then adds an implementation rather than '
      'another branch throughout the callers. The strategies must agree on what the result means: its amount '
      'and currency, permitted rounding, errors, and any effects. Matching a method name alone is '
      'insufficient.\n'
      '\n'
      'A function can serve as a strategy when that is the simplest expression of the algorithm. One stable '
      'formula may need no additional structure. Strategy varies a policy that can be selected for an '
      "operation. State, by comparison, varies behaviour according to an entity's valid lifecycle: a caller "
      "cannot choose a payment's captured state simply as a different calculation preference.",
      ['Policy selects strategy', 'Caller invokes stable operation', 'Algorithm returns defined result'],
      'price = pricing_strategy.calculate(order)\nrequire(price.currency == order.currency)'),
     ('Observer',
      'A local draft changes, and both a preview and a word-count display should update. The draft can keep '
      'a set of subscribed observers and notify them after a change. Each observer implements the agreed '
      'callback, so the draft does not have to know the concrete preview or counter. This is Observer, a '
      'one-to-many arrangement for reactions to change.\n'
      '\n'
      'First an observer subscribes. After the subject changes, it obtains the defined subscriber set and '
      'calls each observer according to the notification policy. The example takes a snapshot of the set for '
      "traversal, so subscription changes during a callback do not silently change that traversal's "
      'membership. The policy must still define ordering and whether callbacks run inline.\n'
      '\n'
      'If one callback is slow or throws, decide whether later observers continue and how the problem is '
      'reported. End subscriptions when their owners finish, or the subject may retain unwanted objects. '
      'These callbacks and subscriptions live in process memory. A reaction that must survive a crash needs '
      'durable publication and recovery rules in addition to local observation.',
      ['Subject changes state', 'Subscribed observers notified', 'Failure policy defines isolation'],
      'for observer in snapshot(subscribers):\n    notify_under_defined_failure_policy(observer, event)'),
     ('Command',
      'Instead of immediately calling a receipt-sending function, the application can create '
      'SendReceipt(order_id, operation_id). This object represents a requested action as explicit data. A '
      'handler later reads the command, checks whether the action is currently allowed, and performs it. '
      'This is Command.\n'
      '\n'
      'Giving the intention its own representation lets the application pass it between components, record '
      'it for audit, or schedule it for later execution. The order identifier names the subject, while the '
      'operation identifier can help identify repeated attempts under a defined duplicate-handling policy. '
      'An event serves a different purpose: it records a fact already accepted, rather than asking a handler '
      'to act.\n'
      '\n'
      'If commands must survive restart, save versioned, serialisable domain data. A closure holding a '
      "request's open connection cannot provide that lifetime. At execution, the handler obtains valid "
      'resources and applies the chosen authorisation and current-state rules. Repeating a command can '
      'repeat an external effect unless the handler and provider protocol prevent it. Representing or '
      'storing the intention alone does not establish safe retry behaviour.',
      ['Command: send receipt', 'Queue stores versioned intention', 'Handler validates and executes'],
      'command = SendReceipt(order_id, operation_id)\n'
      'handler.handle(command)\n'
      '# Handler checks current authorization and state'),
     ('State',
      'A payment awaiting capture and a captured payment permit different actions. The captured payment may '
      'accept a refund request; the pending one must not behave as if money has already been captured. State '
      "organises these behaviour changes around the payment's lifecycle.\n"
      '\n'
      'When evidence arrives, the application checks whether the pair of current state and event is an '
      'allowed transition. It then computes the next state and saves the related changes atomically at the '
      'required persistence boundary. In the example, verified settlement moves a pending payment to '
      'captured. An event without the required evidence, or one that is invalid from the current state, must '
      'be handled explicitly.\n'
      '\n'
      'Separate state objects can hold the behaviour for each lifecycle stage, but a small transition table '
      'is often clearer. The central requirement is that lifecycle rules control the change. A pricing '
      'Strategy may be selected as an interchangeable policy; a payment state follows its history and '
      'evidence. The caller cannot bypass those rules by selecting whichever state would permit the action '
      'it wants.',
      ['Pending payment', 'Verified settlement transition', 'Captured state permits refund request'],
      'require((payment.state, event.kind) in allowed_transitions)\n'
      'payment.state = next_state(payment.state, event)'),
     ('Chain of Responsibility',
      'An incoming request must be authenticated, checked against its request budget, and parsed before the '
      'application handles it. We can connect handlers into a Chain of Responsibility. Each handler applies '
      'its part of the contract and either rejects, handles, transforms, or passes the request onward.\n'
      '\n'
      'In the example, authentication runs first. If it permits the request, rate limiting decides whether '
      'to admit the work. Parsing then produces the input for the application. The nested expression '
      'auth(rate_limit(parse(application))) assembles that order; it does not mean every request necessarily '
      'reaches the innermost handler. A rejecting handler ends its path according to the response contract.\n'
      '\n'
      'Continuation must be explicit. Forgetting to call the next handler can silently swallow work, while '
      'changing the order can change cost or policy. For example, expensive parsing before admission '
      'consumes resources even for work that will be rejected. This arrangement coordinates calls during '
      'execution. A multi-stage operation that must continue after a process crash also needs persisted '
      'progress and recovery; the chain alone provides neither.',
      ['Authenticate', 'Apply request budget', 'Parse and invoke next handler'],
      'auth(rate_limit(parse(application)))(request)\n'
      '# Each handler has explicit rejection and continuation rules'),
     ('Template Method',
      "Every supported import must validate its input, transform it into the application's representation, "
      'and commit the result in that order. CSV and another format may need different transformations, but '
      'neither should skip validation. Template Method keeps the shared sequence in one operation while '
      'exposing selected steps for customisation.\n'
      '\n'
      'In the example, run(input) calls validate(input), then transform(input), then commit(result). A '
      'specialised implementation supplies the format-specific transformation. Inheritance commonly '
      'expresses this arrangement: the base process defines run, and subclasses implement a permitted step. '
      'The fixed process must still arrange resource cleanup when any step fails.\n'
      '\n'
      'The extension contract determines which steps may vary and which ordering rules must hold. If a '
      'subclass can bypass validation or commit an incomplete transformation, the template no longer '
      'protects the intended process. When several steps need independent variation, composed strategies can '
      'be easier to combine than a growing subclass hierarchy. Use Template Method where one stable process '
      'has a small set of controlled extension points.',
      ['Fixed validate step', 'Overridable transform step', 'Fixed commit and cleanup'],
      'run(input):\n    validate(input)\n    result = transform(input)\n    return commit(result)'),
     ('Iterator',
      'A caller wants to read records one at a time without knowing how they are stored. An Iterator '
      'maintains the current traversal position and supplies the next item until the sequence ends. The '
      'underlying collection can be an array, a tree, or a database query.\n'
      '\n'
      'This hides traversal mechanics while leaving their important behaviour in the contract. The caller '
      'needs to know the ordering, how end-of-stream is reported, and what happens if the underlying data '
      'changes during traversal. A lazy database iterator may fetch more rows only when the caller asks for '
      'them. It can therefore keep a cursor and connection open between iterations.\n'
      '\n'
      'In the example, the iterator is used inside a bounded cursor scope. Finishing the loop or exiting '
      'through an error must release the associated resources. A slow consumer can otherwise occupy a scarce '
      'connection for a long time, and closing the owner early can make the next read fail. For a small '
      'bounded result, fetching a list and releasing the connection before returning may offer a simpler '
      'lifetime contract.',
      ['Client requests next item', 'Iterator owns traversal position', 'End or close releases resources'],
      'with open_bounded_cursor(query) as rows:\n    for row in rows:\n        consume(row)'),
     ('Mediator',
      'Checkout needs to coordinate inventory and payment. If each collaborator directly calls the other '
      'whenever something happens, their knowledge of one another can grow difficult to follow. A Mediator '
      'receives their outcomes and decides the next action for this particular process.\n'
      '\n'
      'In the example, the coordinator asks inventory for a reservation and asks payments for authorisation '
      'under an operation identifier. It then interprets both outcomes and chooses the permitted next step. '
      'Inventory need not know the payment API, and the payment collaborator need not know the reservation '
      'implementation. The coordination rule has a clear home.\n'
      '\n'
      'The mediator still needs explicit treatment of failure and uncertain outcomes. Keep its '
      'responsibility focused so it does not become an object containing every application rule. If these '
      'calls cross systems and progress must survive restarts, a durable workflow orchestrator may implement '
      'the coordination with saved state and recovery. Mediator names the object relationship; it does not '
      'itself make the sequence persistent or make inventory and payment one atomic operation.',
      ['Inventory reports reservation',
       'Mediator decides next action',
       'Payment collaborator receives command'],
      'reservation = inventory.reserve(command)\n'
      'outcome = payments.authorize(command.operation_id)\n'
      'coordinate_outcomes(reservation, outcome)'),
     ('Memento',
      'Before changing a draft, the editor asks it for a snapshot of the values needed to restore its '
      'present local state. After an unwanted edit, the editor passes that snapshot back to restore(). '
      'Memento supports this capture and restoration without requiring every caller to read and rewrite the '
      "draft's internal fields.\n"
      '\n'
      'The draft defines what belongs in the snapshot. If editable paragraph data is copied appropriately, '
      'later edits do not change the saved version. If the snapshot merely stores a reference to the same '
      'mutable paragraph object, an edit can change both the current draft and the supposed snapshot. '
      'Ownership and copying rules are therefore part of making restoration meaningful.\n'
      '\n'
      'Restoration has a defined local scope. Returning the draft to earlier values cannot retract an email '
      'that was sent during the intervening operation or reverse a payment at a provider. Those effects '
      'require their own recovery or compensation arrangements. Use Memento when the supported state and '
      'restoration behaviour are clear; backups, event histories, and external compensation address broader '
      'and different recovery questions.',
      ['Capture local draft snapshot', 'Apply editable change', 'Restore supported local state'],
      'before = draft.snapshot_owned_values()\n'
      'draft.apply(edit)\n'
      'draft.restore(before)\n'
      '# No claim about undoing external effects'),
     ('Visitor',
      'A document tree has known node kinds, such as text and image. We want to add an export operation that '
      'handles each kind without placing all export logic inside the node classes. A Visitor groups the '
      'type-specific behaviour for that operation.\n'
      '\n'
      'During traversal, each node dispatches to the appropriate visitor operation, such as export_text or '
      'export_image. The example expresses the same decision with pattern matching on node.kind. Another '
      'visitor can perform validation over those same known kinds. This is useful when the structure is '
      'fairly stable and we expect to add operations over it.\n'
      '\n'
      'The trade-off appears when the structure changes. Adding a new node kind may require updating every '
      'visitor so each operation can handle it correctly. Define unknown-node handling: silently skipping an '
      'unfamiliar node could lose content during export. Some languages make pattern matching simpler than a '
      'separate visitor class hierarchy. Choose the representation that makes the known variants and each '
      "operation's coverage clear.",
      ['Known document node variants',
       'Visitor supplies export operation',
       'Each node dispatches appropriate behavior'],
      'visit(node):\n'
      '    match node.kind:\n'
      '        case "text": return export_text(node)\n'
      '        case "image": return export_image(node)\n'
      '        case _: raise UnsupportedNode')],
 7: [('Repository',
      'A reservation service needs to load a reservation, apply its confirmation rule, and save it. A '
      "Repository offers these data operations in the application's vocabulary while a concrete adapter "
      'performs SQL or other storage work. The service can use a repository contract without knowing table '
      'names and query syntax.\n'
      '\n'
      'In the example, get_for_update(reservation_id) obtains the reservation under the required update '
      'rules. The service calls confirm(payment_evidence), then asks the repository to save the changed '
      'record. The contract must state whether these calls share a transaction, who commits, and which '
      'outcomes represent missing data, conflict, or storage failure. Returning a record must also say '
      'whether it remains usable after a connection closes.\n'
      '\n'
      'The right boundary follows the data rule. A repository for each table can split values that need to '
      'change atomically as one aggregate. Also bound queries and expose relevant costs: a simple method '
      'name must not conceal an unlimited remote load or an unowned live cursor. A test substitute helps '
      'check service decisions, but real storage checks are needed to establish actual commit and recovery '
      'behaviour.',
      ['Domain operation', 'Repository contract', 'Concrete persistence adapter'],
      'reservation = repository.get_for_update(reservation_id)\n'
      'reservation.confirm(payment_evidence)\n'
      'repository.save(reservation)'),
     ('Unit of Work',
      'To reserve a seat, the application changes inventory and inserts a reservation record. If both are in '
      'one transactional database, we want one commit decision: save both local changes or save neither. A '
      'Unit of Work groups the changes and owns the transaction resources for that operation.\n'
      '\n'
      'The application opens the unit, asks its inventory repository to reserve the seat, and asks its '
      "reservation repository to add the record. These repositories use the unit's transaction instead of "
      'committing independently. The explicit commit then makes the grouped changes durable according to the '
      "database's contract. If the operation fails before commit, the owning scope must roll back unfinished "
      'work and release resources.\n'
      '\n'
      'Keep this boundary short and precise. A remote payment provider is not a participant in the local '
      'database transaction merely because its call appears inside the same language scope. Rolling back the '
      'database cannot undo a provider charge. External effects need their own identity, outcome, and '
      "recovery protocol. The Unit of Work's atomicity follows the actual transaction boundary, rather than "
      'the indentation of the program.',
      ['Begin local transaction', 'Apply related local changes', 'Commit both or roll back'],
      'with unit_of_work() as uow:\n'
      '    uow.inventory.reserve(seat)\n'
      '    uow.reservations.add(record)\n'
      '    uow.commit()'),
     ('Specification',
      'A refund rule may ask whether a payment is captured, still within its refund period, and otherwise '
      'eligible. We can express that decision as a named predicate: RefundPolicy.satisfied_by(payment, now). '
      'A predicate returns whether the supplied values meet a condition. Specification gives a reusable rule '
      'such an explicit form and, where useful, lets rules be combined.\n'
      '\n'
      'The evaluation uses the payment state and time supplied to it. A successful result does not reserve '
      'that state. Another operation could refund the payment before this caller writes its change. In the '
      'example, refund_if_still_eligible(payment.version) performs the transition only if the relevant '
      'current conditions or version still permit it. The rule and the atomic update must agree.\n'
      '\n'
      'A specification may also be translated into a storage query for selection. That translation must '
      'preserve the same time, null-value, and access semantics as the in-memory decision. A plain function '
      'is often enough for one rule. Add a composable expression framework when shared rule composition or '
      'query translation gives a concrete benefit.',
      ['Evaluate refund predicate', 'Concurrent state may change', 'Atomic transition rechecks invariant'],
      'eligible = RefundPolicy.satisfied_by(payment, now)\n'
      'if eligible:\n'
      '    repository.refund_if_still_eligible(payment.version)'),
     ('CQRS',
      'Capturing a payment needs a model that checks allowed transitions and records a valid change. '
      'Displaying an account statement needs a convenient arrangement of dates, descriptions, and amounts. '
      'Command Query Responsibility Segregation, or CQRS, separates the models used to change data and to '
      'answer queries when these needs differ enough to justify it.\n'
      '\n'
      "A command such as capture(payment_id, operation_id) goes through the write model's rules. A query "
      "such as account_statement(account_id) uses the read model's shape. A projection can update the read "
      'model from accepted changes. If that work runs later, a successful command may be followed by a '
      'statement that has not caught up yet. The query contract must explain that freshness, and the '
      'projection needs defined recovery and rebuilding behaviour.\n'
      '\n'
      'The models can live in one process and use one database. Event sourcing and separate services are '
      'additional decisions, rather than requirements of CQRS. With one simple model that already supports '
      'both operations, separate models may add more synchronisation and maintenance than they save. Choose '
      'the separation for actual differences in rules, access patterns, or query needs.',
      ['Command enforces invariant', 'Projection updates read model', 'Query serves explicit freshness'],
      'commands.capture(payment_id, operation_id)\n'
      'statement = queries.account_statement(account_id)\n'
      '# Projection lag is part of the query contract')]}
