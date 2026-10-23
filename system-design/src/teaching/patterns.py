"""Pattern mechanisms, applications, and costs in the notification example."""
PATTERN_LESSONS={4: [('Factory Method',
  'Suppose an exporter always writes the same rows, but one version produces CSV and another produces '
  'HTML. We can keep the export steps in a base class and let each subclass choose its writer.\n'
  '\n'
  'The base operation calls `make_writer()`, then uses the returned writer. `CsvExporter` overrides '
  'that creation operation to return `CsvWriter`; `HtmlExporter` returns `HtmlWriter`. This overridable '
  'creation operation is the **Factory Method**. The export code knows the writer contract without '
  'choosing the concrete class.\n'
  '\n'
  'This fits an existing class hierarchy with a varying creation step. If there is no reason for '
  'exporter subclasses, passing a writer into one exporter can be simpler. Both arrangements separate '
  'choice from use, but the override is what defines Factory Method here.',
  ['Base exporter calls make_writer',
   'CSV subclass returns CsvWriter',
   'Exporter calls writer.write',
   'HTML subclass can choose HtmlWriter'],
  'class Exporter:\n'
  '    export(rows):\n'
  '        writer = self.make_writer()\n'
  '        return writer.write(rows)\n'
  '    make_writer(): raise NotImplemented\n'
  '\n'
  'class CsvExporter(Exporter):\n'
  '    make_writer(): return CsvWriter()'),
 ('Abstract Factory',
  'An HTML email renderer expects HTML templates. A plain-text renderer expects plain-text templates. '
  'Choosing them independently can produce a pair that cannot work together.\n'
  '\n'
  'An **Abstract Factory** supplies a whole family of related objects. Choose '
  '`HtmlNotificationFactory`, then obtain both its renderer and its template. The caller uses their '
  'common contracts. Switching to the plain-text factory switches both choices together.\n'
  '\n'
  'The family must actually preserve compatibility: the HTML factory cannot return a plain-text '
  'template merely because the method names match. This arrangement helps when several products vary '
  'together. If we need only one sender, a factory for that single sender is enough.',
  ['Choose the HTML family',
   'Factory creates HTML renderer',
   'Factory supplies HTML template',
   'Renderer uses the matching template'],
  'family = HtmlNotificationFactory()\n'
  'renderer = family.renderer()\n'
  'template = family.template()\n'
  'output = renderer.render(template, data)'),
 ('Builder',
  'A notification needs a recipient and template, while expiry and delivery options may arrive from '
  'later steps in a form. We can collect these choices in a **Builder**.\n'
  '\n'
  "Calls such as `to(recipient)` and `template(template_id)` update the builder's draft settings. "
  '`build()` checks that required fields are present and that the options agree. Only then does it '
  'return a usable notification. An incomplete builder is allowed; an invalid finished notification is '
  'rejected.\n'
  '\n'
  'The builder should copy any mutable settings the finished object must own. Otherwise, changing the '
  'builder later might change an already built notification. When all inputs are already available '
  'together, a constructor with named arguments and validation may express the same task more simply.',
  ['Collect recipient and template',
   'Add optional expiry',
   'build checks the complete settings',
   'Return a valid notification'],
  'builder.to(recipient).template(template_id)\n'
  'notification = builder.expires_at(deadline).build()\n'
  '# build rejects missing fields and copies owned settings'),
 ('Prototype',
  'Many notification layouts start from the same configured layout. Rather than repeat its setup, we '
  'can create a new layout by copying that example. The configured example is a **Prototype**.\n'
  '\n'
  'The copy must have its own editable values. If both layouts refer to one mutable list of paragraphs, '
  'editing the copy can change the original too. `clone_owned_values()` copies that list and the '
  'editable paragraph data it contains. Immutable font data can remain shared because neither layout '
  'changes it.\n'
  '\n'
  'Decide what copying means for each field. A live connection or lock usually cannot be duplicated '
  'like paragraph text. Prototype is useful when copying the supported configuration is clearer than '
  'rebuilding it; it does not make every object safe to clone.',
  ['Start with configured prototype',
   'Copy its editable owned values',
   'Keep immutable font data shared',
   'Edit the copy independently'],
  'layout = prototype.clone_owned_values()\n'
  'layout.title = "Monthly report"\n'
  'layout.paragraphs[0].text = "Your summary"\n'
  '# Original editable values stay unchanged'),
 ('Singleton',
  'Several parts of one application need the same immutable routing configuration. A **Singleton** '
  'restricts access to one instance within a defined boundary.\n'
  '\n'
  'In a traditional implementation, callers cannot invoke the constructor directly. An accessor '
  'constructs the instance on first use and returns that same instance afterward. If callers can arrive '
  'concurrently, the construction step needs coordination. Here the lock protects the check and '
  'construction together.\n'
  '\n'
  'The boundary in this example is one loaded module in one process. Another process has its own '
  'instance. Reusing one object also does not make its mutable fields safe for concurrent changes.\n'
  '\n'
  'A DI container can provide similar reuse without a global accessor: create one configuration at '
  'startup and inject it wherever needed. That often makes the dependency easier to see.',
  ['Caller uses the restricted accessor',
   'Lock protects first construction',
   'Later calls return the same instance',
   'Other processes have their own instances'],
  '# Module-private constructor and state; illustrative pseudocode\n'
  'instance = None\n'
  'get_configuration():\n'
  '    with creation_lock:\n'
  '        if instance is None:\n'
  '            instance = Configuration.load()\n'
  '        return instance')],
 5: [('Adapter',
  'Our service calls `send(message)`, but an older SMS library accepts a phone number, text, and '
  'provider-specific options. We want to use that library without making the service learn its '
  'interface.\n'
  '\n'
  "An **Adapter** receives the application's message, converts it into the library's arguments, and "
  'calls the library. It then converts the reply into the outcomes expected by `Sender`.\n'
  '\n'
  'The reply conversion matters as much as the argument conversion. If the provider says “queued,” the '
  'adapter must not report “delivered.” When an outcome cannot be represented faithfully, the contract '
  'needs to expose that difference. An adapter translates an interface; it cannot create a guarantee '
  'the provider does not offer.',
  ['Service supplies its message',
   'Adapter converts provider arguments',
   'Provider returns its own outcome',
   'Adapter maps the outcome faithfully'],
  'send(message):\n    raw = sdk.submit(encode(message))\n    return map_provider_outcome(raw)'),
 ('Bridge',
  'We send both receipts and alerts, and each can travel by email or SMS. A subclass for every '
  'combination would give us EmailReceipt, SmsReceipt, EmailAlert, and SmsAlert. A third transport '
  'would add still more classes.\n'
  '\n'
  'With a **Bridge**, the message object holds a transport object. `Receipt` formats receipt data and '
  'passes the result to its transport. `Alert` formats alert data in its own way. Either can receive an '
  'email or SMS transport through the same sending contract.\n'
  '\n'
  'The two choices can now vary separately: message behaviour and transport behaviour. Their contract '
  'must still fit real constraints. If SMS has a length limit, the design must define splitting or '
  'rejection rather than assume any email body can be sent unchanged.',
  ['Choose Receipt or Alert',
   'Supply EmailTransport or SmsTransport',
   'Message object formats the content',
   'Transport handles channel delivery'],
  'class Receipt:\n'
  '    constructor(transport): self.transport = transport\n'
  '    deliver(data):\n'
  '        text = format_receipt(data)\n'
  '        return self.transport.send(text)'),
 ('Composite',
  'A notification can target one person or a group containing people and smaller groups. Callers should '
  'not need a separate traversal algorithm for every nesting level.\n'
  '\n'
  'A **Composite** gives a person and a group the same operation, such as `recipients()`. A person '
  'returns their identifier. A group asks its children for their recipients and combines the results. '
  'The caller can start with either kind.\n'
  '\n'
  'Give every person and group a distinct identifier. Our groups may overlap, so the traversal records '
  'visited identifiers. A person in two groups then appears once. The same check stops a group cycle '
  'from looping forever. This defines membership expansion, not delivery: sending to the resulting '
  'people still needs its own per-recipient outcomes and failure handling.',
  ['Start at a person or group',
   'Group visits its children',
   'Seen identifiers prevent repeats',
   'Return the unique recipient list'],
  'Person.recipients(seen):\n'
  '    if self.id in seen: return []\n'
  '    seen.add(self.id)\n'
  '    return [self.id]\n'
  '\n'
  'Group.recipients(seen):\n'
  '    if self.id in seen: return []\n'
  '    seen.add(self.id)\n'
  '    return flatten(child.recipients(seen)\n'
  '                   for child in self.children)\n'
  '\n'
  'people = root.recipients(set())'),
 ('Decorator',
  'We want to time sends without putting timing code into every provider adapter. A `TimingSender` '
  'holds another sender and offers the same `send` operation.\n'
  '\n'
  'It records the start time, calls the inner sender, and records the duration when that call ends. '
  'This is a **Decorator**: it adds behaviour around a collaborator while keeping its interface. The '
  '`finally` step records duration when the send raises an error too.\n'
  '\n'
  'Order changes what is measured. `TimingSender(RetrySender(sender))` times the whole call, including '
  'retries. `RetrySender(TimingSender(sender))` times each attempt. Before adding retries, define how '
  'repeated attempts avoid unwanted duplicate sends. Wrapping the call does not settle that delivery '
  'question.',
  ['Timing wrapper records start',
   'Wrapper calls the inner sender',
   'Inner call returns or raises',
   'Finally records elapsed time'],
  'send(message):\n'
  '    start = clock()\n'
  '    try: return inner.send(message)\n'
  '    finally: metrics.observe(clock() - start)'),
 ('Facade',
  'Submitting a notification requires checking its fields, preparing a rendering plan, and saving a '
  'delivery request. A caller should not have to coordinate all three helpers for every submission.\n'
  '\n'
  'A **Facade** offers a focused entry point such as `submit(command)`. It performs those steps in the '
  'required order and returns a useful result. The helpers remain responsible for their own work; the '
  'facade provides a simpler way to use them together.\n'
  '\n'
  'Here success means the delivery request was saved. Actual sending happens later, so the facade '
  'returns an accepted identifier rather than claiming delivery. A simple entry point must still expose '
  'meaningful outcomes, such as invalid input or failure to save the request. Simpler calling code '
  'should not require guessing what happened.',
  ['Caller submits one command',
   'Facade validates the fields',
   'Facade prepares and saves the plan',
   'Result identifies accepted work'],
  'submit(command):\n'
  '    validated = validate(command)\n'
  '    plan = render_plan(validated)\n'
  '    return intents.persist(plan)'),
 ('Flyweight',
  'Ten thousand notifications use the same template version. Parsing a separate copy of that template '
  'for every message wastes memory.\n'
  '\n'
  'A **Flyweight** shares the part that is the same across uses. We store one parsed, immutable '
  "template for that version. Rendering supplies the recipient's name and other changing values "
  'separately. Two messages can use the same template without sharing their personal data.\n'
  '\n'
  "This separation is essential. Putting a recipient's name into the shared template would let one "
  'render change what another sees. Keep shared data unchanged and pass per-message values as separate '
  'context. The collection holding shared templates also needs a size or eviction policy if new '
  'versions keep arriving; sharing does not make an unlimited collection small.',
  ['Find shared template version',
   'Supply recipient A’s values',
   'Supply recipient B’s values',
   'Keep shared template unchanged'],
  'template = parsed_templates.get(version)\n'
  'output_a = render(template, context_a)\n'
  'output_b = render(template, context_b)'),
 ('Proxy',
  'A caller wants to read a saved notification, but it must first have permission. We can place an '
  'object with the same read operation in front of the actual storage object.\n'
  '\n'
  "This **Proxy** checks the actor's access and only then calls the target. The caller uses the "
  'familiar read interface. The proxy controls access to the object behind it.\n'
  '\n'
  'Other proxies can delay creating an expensive target or represent a remote target. Their purpose '
  'should be clear to the caller where it affects behaviour. A remote read can time out even though an '
  'ordinary local field read would not. Our access proxy must also prevent callers from bypassing its '
  'check through another unguarded route.',
  ['Caller requests saved notification',
   'Proxy checks the actor’s access',
   'Allowed call reaches the target',
   'Target returns the result'],
  'read(notification_id, actor):\n'
  '    authorize(actor, notification_id)\n'
  '    return target.read(notification_id)')],
 6: [('Strategy',
  'Our service renders a message as plain text or HTML. The caller chooses a format, but the service '
  'should not contain the details of every rendering algorithm.\n'
  '\n'
  'A **Strategy** puts each algorithm behind the same operation, such as `render(data)`. The service '
  'receives the chosen renderer and calls it. Supplying another renderer changes how the content is '
  'produced without changing the calling steps.\n'
  '\n'
  'The shared contract must specify the output. An HTML result needs to be identified and escaped '
  'appropriately; it cannot silently be treated as safe plain text. A function can serve as a strategy '
  'when one operation is enough. The useful separation is the replaceable algorithm, rather than a '
  'required class hierarchy.',
  ['Caller chooses rendering format',
   'Service receives that strategy',
   'Strategy renders the data',
   'Service handles its stated output type'],
  'renderer = renderers.for_format(command.format)\n'
  'content = renderer.render(command.data)\n'
  'require(content.format == command.format)'),
 ('Observer',
  'After accepting a notification, the service updates a counter and refreshes an on-screen list. We do '
  'not want the acceptance code to call every interested component by name.\n'
  '\n'
  'With **Observer**, interested objects subscribe to an event source. When acceptance occurs, the '
  'source calls the registered listeners with the event. A subscription records this interest; removing '
  'it ends that interest.\n'
  '\n'
  'In this example, callbacks run synchronously in registration order. The source copies the listener '
  'list before calling them, so changes during a callback affect the next event. It records a '
  "listener's error and continues to the next listener.\n"
  '\n'
  'These are chosen rules, not automatic guarantees of Observer. A process crash can lose an in-memory '
  'event, and a slow callback delays this call. Delivery that must survive a restart needs saved event '
  'data and a recovery mechanism.',
  ['Listeners subscribe to acceptance',
   'Source snapshots the listener list',
   'Source calls each listener',
   'One listener error is recorded'],
  'for listener in snapshot(subscribers):\n'
  '    try: listener.on_accepted(event)\n'
  '    except Exception as error: record_listener_error(error)'),
 ('Command',
  'A worker may need to send a receipt later. Instead of immediately calling a sender, the application '
  'can create a value describing the requested action: `SendReceipt(order_id, operation_id)`.\n'
  '\n'
  'This value is a **Command**. A handler reads it, loads the required order, checks the permitted '
  'action, and performs the work. The request is separate from its execution. That makes it possible to '
  'queue or record the request.\n'
  '\n'
  'The command should contain stable data, not an open request connection. If it is saved for later, '
  'its format also needs to remain readable by the worker. Replaying the same command can repeat an '
  'email unless the handler and provider use a defined duplicate-handling protocol. Recording an '
  'intention does not itself make retries safe.',
  ['Create SendReceipt command',
   'Queue or pass the command',
   'Handler loads and checks current data',
   'Handler performs the requested action'],
  'command = SendReceipt(order_id, operation_id)\n'
  'handler.handle(command)\n'
  '# Handler obtains its own valid resources'),
 ('State',
  'A draft notification can be edited. Once it has been submitted, editing that same delivery request '
  'is no longer allowed. After confirmed delivery, sending it again is also a different action.\n'
  '\n'
  'The **State** pattern puts behaviour for each lifecycle stage in a state object. The notification '
  'delegates an action to its current state. `Draft.submit` can save the accepted request and move to '
  "`Queued`. `Queued.edit` rejects the edit. The object's history determines which behaviour is "
  'active.\n'
  '\n'
  'State changes need evidence: a delivery confirmation can permit the transition to Delivered, while '
  'an unverified caller request cannot. A small transition table may be simpler than separate state '
  'classes. Either form must enforce the same allowed changes. Unlike selecting a rendering strategy, '
  'selecting a convenient state cannot bypass those lifecycle rules.',
  ['Notification begins in Draft',
   'Draft accepts a valid submission',
   'Notification moves to Queued',
   'Queued rejects an edit'],
  'submit(notification):\n'
  '    return notification.state.submit(notification)\n'
  '\n'
  'Draft.submit(notification):\n'
  '    save_submission_and_state(notification, next_state="Queued")\n'
  'Queued.submit(notification): raise AlreadySubmitted'),
 ('Chain of Responsibility',
  'Before a notification request reaches the service, we check its caller, enforce a request limit, and '
  'parse its input. Each step can either stop the request or pass it onward.\n'
  '\n'
  'A **Chain of Responsibility** connects these handlers in order. Authentication first rejects an '
  'unknown caller. An allowed caller reaches the request-limit check. A request still allowed then '
  'reaches parsing and the application.\n'
  '\n'
  'Each handler must say when it calls the next one. Forgetting that call can swallow a request; '
  'calling it twice can repeat the work. Order matters too: rejecting an over-budget request before '
  'expensive parsing avoids work we did not intend to admit. This chain organises calls in one '
  'execution. It does not save progress for recovery after a process crash.',
  ['Check caller identity',
   'Reject work beyond its limit',
   'Parse admitted input',
   'Invoke the application'],
  'handler = auth(rate_limit(parse(application)))\n'
  'response = handler(request)\n'
  '# Each wrapper either returns a rejection or calls next once'),
 ('Template Method',
  'Every notification preparation must validate input, render content, and save the prepared result. '
  'Email and SMS use different rendering steps, but both need that same order.\n'
  '\n'
  'A **Template Method** defines the shared sequence in a base class. Its `prepare` operation calls '
  '`validate`, the overridable `render`, and then `save`. An email subclass supplies HTML rendering; an '
  'SMS subclass supplies text rendering. Callers use the shared `prepare` entry point.\n'
  '\n'
  'The extension rules matter. The subclass should replace the permitted rendering step without '
  'bypassing validation. Keep resource cleanup around the whole operation if any step acquires '
  'resources. When several steps vary independently, passing separate strategies may be easier than '
  'creating a subclass for every combination.',
  ['Shared prepare validates input',
   'Subclass supplies rendering step',
   'Shared prepare saves the result',
   'Callers use the shared entry point'],
  'class Preparation:\n'
  '    prepare(input):\n'
  '        validate(input)\n'
  '        content = self.render(input)\n'
  '        return save(content)\n'
  '    render(input): raise NotImplemented\n'
  '\n'
  'class SmsPreparation(Preparation):\n'
  '    render(input): return render_sms_text(input)'),
 ('Iterator',
  'A caller wants to read saved notifications one at a time. It should not have to know whether they '
  'are stored in an array, a tree, or rows fetched from a database.\n'
  '\n'
  'An **Iterator** keeps the traversal position and supplies the next item until there are no more. A '
  'loop asks for each item through that operation. The contract should state the ordering and what '
  'happens if the underlying collection changes.\n'
  '\n'
  'A database iterator may fetch rows only as the caller advances. It can therefore keep a connection '
  'open throughout the loop. Use it inside an owning resource block so leaving early or raising an '
  'error closes the cursor. For a small bounded result, fetching a list first may let the connection '
  'close sooner.',
  ['Caller requests the next record',
   'Iterator advances its position',
   'Caller consumes the record',
   'Completion or scope exit closes cursor'],
  'with open_bounded_cursor(query) as rows:\n    for row in rows:\n        consume(row)'),
 ('Mediator',
  'In a notification editor, changing the channel affects the template choices and the recipient field. '
  'If every control calls all the others, each must know much of the form.\n'
  '\n'
  'A **Mediator** coordinates these interactions. The channel selector reports its change to a form '
  'coordinator. The coordinator updates the template choices and recipient field. The controls know the '
  "coordinator instead of knowing one another's detailed APIs.\n"
  '\n'
  "The coordinator owns this form's interaction rules. It should not grow into the owner of every "
  'application rule. Validation and saving can still live in their own collaborators. Mediator '
  'simplifies who communicates with whom; it does not remove the need to understand the order and '
  'effects of those updates.',
  ['User changes delivery channel',
   'Selector informs the mediator',
   'Mediator updates template choices',
   'Mediator updates recipient input'],
  'channel_changed(channel):\n'
  '    templates.show_for(channel)\n'
  '    recipient_field.use_format(address_format(channel))'),
 ('Memento',
  'A person edits a notification draft and wants to undo the last edit. Before the change, the draft '
  'can provide a snapshot of the state it supports restoring.\n'
  '\n'
  "That snapshot is a **Memento**. The editor keeps it without rewriting the draft's internal fields. "
  'If the edit is unwanted, the editor gives the snapshot back to `restore`. The draft decides which '
  'values to restore and how.\n'
  '\n'
  'The saved values must not change along with the draft. A snapshot that only points to the same '
  'editable paragraph list would fail this test; the draft must copy its owned editable data. Restoring '
  'this local draft cannot unsend a notification already delivered. Undoing values and reversing an '
  'external effect are different operations.',
  ['Draft captures its editable values',
   'Editor keeps the snapshot',
   'Edit changes the current draft',
   'Draft restores the saved values'],
  'before = draft.snapshot_owned_values()\n'
  'draft.apply(edit)\n'
  'draft.restore(before)\n'
  '# Restores local draft data, not external deliveries'),
 ('Visitor',
  'A message document contains text and image nodes. We want to export both kinds to HTML, then add '
  'another operation that checks accessibility. Putting every new operation into every node class would '
  'spread the work.\n'
  '\n'
  'A **Visitor** groups the handling for one operation. During traversal, a text node calls '
  '`visit_text` and an image node calls `visit_image` on the supplied visitor. An HTML visitor provides '
  'export behaviour; an accessibility visitor provides checks.\n'
  '\n'
  'This works well when the node kinds are fairly stable and new operations are common. Adding a new '
  'node kind, such as video, means updating visitors that must support it. Unknown kinds need an '
  'explicit result rather than silently disappearing. Pattern matching can offer a simpler alternative '
  'in languages that support it.',
  ['Traversal reaches a text node',
   'Node calls visitor.visit_text',
   'Image node calls visitor.visit_image',
   'Another visitor supplies another operation'],
  'TextNode.accept(visitor): return visitor.visit_text(self)\n'
  'ImageNode.accept(visitor): return visitor.visit_image(self)\n'
  '\n'
  'class HtmlVisitor:\n'
  '    visit_text(node): return escape_html(node.text)\n'
  '    visit_image(node): return render_image(node)')],
 7: [('Repository',
  'The service needs to find a saved notification and change its delivery status. It should not have to '
  "know the database's table names to do this.\n"
  '\n'
  'A **Repository** offers data operations in application terms, such as `get(notification_id)` and '
  '`save(notification)`. Its implementation performs the storage queries. The service loads the '
  'notification, applies the delivery rule, and asks the repository to save the changed value.\n'
  '\n'
  'The contract must explain what these calls promise. A missing identifier needs a defined result. '
  'Concurrent changes need a conflict rule. Loading and saving do not automatically form one '
  'transaction merely because they use the same repository. In this example, a Unit of Work supplies '
  'that transaction. A test repository can check service decisions, but only real storage checks '
  'establish actual database behaviour.',
  ['Service loads a notification',
   'Repository performs storage access',
   'Service applies its status rule',
   'Repository stages the changed value'],
  'with unit_of_work() as uow:\n'
  '    notification = uow.notifications.get(notification_id)\n'
  '    notification.record_delivery(verified_receipt)\n'
  '    uow.notifications.save(notification)\n'
  '    uow.commit()'),
 ('Unit of Work',
  'Accepting a notification adds a message record and a delivery-job record. Saving only the message '
  'would leave accepted work with no job to send it.\n'
  '\n'
  'A **Unit of Work** tracks the records added, changed, or removed during an operation and coordinates '
  'saving them. In this example, both repositories use one transaction in the same database. `commit()` '
  'writes the pending changes and asks the database to commit them together. If the operation exits '
  'before a successful commit, the owning block rolls back unfinished work and releases its resources.\n'
  '\n'
  'This groups the local changes. Calling an email provider inside the block would not put the provider '
  'into that database transaction. Database rollback cannot retract an email. The boundary follows the '
  'actual participating storage, not the indentation of the code.',
  ['Open one local transaction',
   'Track message and job additions',
   'Commit both database changes',
   'Roll back unfinished work on exit'],
  'with unit_of_work() as uow:\n'
  '    uow.notifications.add(notification)\n'
  '    uow.delivery_jobs.add(job)\n'
  '    uow.commit()'),
 ('Specification',
  'A scheduled notification is ready only if its scheduled time has arrived and it has not been '
  'cancelled. We want this rule to have one clear name.\n'
  '\n'
  'A **Specification** expresses a condition as a test, such as `ReadyToSend.satisfied_by(notification, '
  'now)`. A test returning true or false is a **predicate**. Small specifications can be combined when '
  'the application needs reusable combinations of rules.\n'
  '\n'
  'A true result describes the values just tested. Another caller could cancel the notification before '
  'we claim it for sending. The final update must therefore recheck the required current conditions. '
  'Here `claim_if_still_ready` checks the saved version and readiness rule atomically, and returns no '
  'claim if either changed. A plain function is enough when no rule-composition machinery is needed.',
  ['Load notification and its version',
   'Evaluate the named readiness rule',
   'Concurrent cancellation may intervene',
   'Atomic claim checks readiness again'],
  'if ReadyToSend.satisfied_by(notification, now):\n'
  '    claim = repository.claim_if_still_ready(\n'
  '        notification.id, notification.version, now)\n'
  '    # No claim means the current conditions did not permit it'),
 ('CQRS',
  'Submitting a notification needs rules that prevent invalid changes. A progress screen needs a '
  'convenient list of recipients, times, and statuses. Those jobs may benefit from different data '
  'models.\n'
  '\n'
  '**Command Query Responsibility Segregation**, or **CQRS**, separates the model used for changes from '
  'the model used for reads. A command goes through the change rules. A query reads the view prepared '
  'for its needs.\n'
  '\n'
  'A process called a **projection** can update the reading view from accepted changes. If it runs '
  'later, the screen may briefly lag behind a successful command. The application must explain that '
  'delay and arrange recovery when projection work fails.\n'
  '\n'
  'The models can share one process and database. CQRS does not require saving every change as an event '
  'or deploying separate services. When one simple model serves both jobs well, maintaining two models '
  'may add unnecessary work.',
  ['Command checks a submission',
   'Write model records accepted work',
   'Projection updates progress view',
   'Query reads that view with stated freshness'],
  'accepted = commands.submit_notification(command)\n'
  'rows = queries.notification_progress(account_id)\n'
  '# A separately updated progress view may lag behind acceptance')]}
