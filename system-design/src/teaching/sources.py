"""Selected production references and access evidence from 21 October 2026."""
from resources import VERIFIED,CHAPTER_REFS
SOURCES=dict(VERIFIED)
def add(url,title,kind,use):SOURCES[url]=(title,kind,use)
add('https://sre.google/workbook/implementing-slos/','Implementing SLOs — The SRE Workbook','Engineering book','Service indicators, objectives, and error budgets; not a source of the atlas workload numbers')
add('https://doi.org/10.1287/opre.9.3.383','A Proof for the Queuing Formula: L = lambda W — John D. C. Little, 1961','Original research · publisher record','Long-run queue accounting; publisher record inspected, full proof access may depend on access rights')
add('https://www.rfc-editor.org/rfc/rfc9000.html','RFC 9000: QUIC Transport, 2021','Original specification','QUIC streams and transport behavior; application walkthrough is author-created')
add('https://www.rfc-editor.org/rfc/rfc8446.html','RFC 8446: TLS 1.3, 2018','Original specification','Secure transport handshake and protocol scope')
add('https://go.dev/ref/mem','The Go Memory Model','Language specification · accessed 21 Oct 2026','One concrete memory-model contract; other languages differ')
add('https://refactoring.guru/design-patterns/catalog','The Catalog of Design Patterns — Refactoring Guru','Engineering teaching reference','Pattern taxonomy; miniature examples and judgments are original to this atlas')
add('https://martinfowler.com/bliki/BoundedContext.html','Bounded Context — Martin Fowler, 2014','Original engineering explanation','Model boundaries and language')
add('https://martinfowler.com/articles/microservices.html','Microservices — James Lewis and Martin Fowler, 2014','Original engineering article','Architecture characteristics and costs; no exact company architecture is asserted here')
add('https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/','Architecture styles — Microsoft Architecture Center','Official guidance · accessed 21 Oct 2026','Style comparisons; provider-specific recommendations are not mandatory in the atlas')
add('https://www.postgresql.org/docs/18/transaction-iso.html','PostgreSQL 18: Transaction Isolation','Official versioned documentation','Specific PostgreSQL isolation behavior; no all-database equivalence claim')
add('https://www.postgresql.org/docs/18/indexes-types.html','PostgreSQL 18: Index Types','Official versioned documentation','Supported access structures and their purposes')
add('https://www.postgresql.org/docs/18/wal-intro.html','PostgreSQL 18: Write-Ahead Logging','Official versioned documentation','Logging and recovery ordering; durability remains configuration-dependent')
add('https://github.com/facebook/rocksdb/wiki/RocksDB-Overview','RocksDB Overview','Official implementation documentation · accessed 21 Oct 2026','An LSM-based engine; exact tuning is implementation-specific')
add('https://www.rfc-editor.org/rfc/rfc9111.html','RFC 9111: HTTP Caching, 2022','Original standard','HTTP cache semantics; application cache races are separate examples')
add('https://redis.io/docs/latest/develop/reference/eviction/','Redis: Key eviction','Official documentation · accessed 21 Oct 2026','Implementation policies can approximate ideal LRU/LFU')
add('https://www.cloudflare.com/learning/cdn/what-is-a-cdn/','Content delivery networks — Cloudflare Learning Center','Official engineering explanation','CDN role; atlas delivery and traffic numbers are illustrative')
add('https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store','Dynamo: Amazon’s highly available key-value store, 2007','Original research · author organization','Replication, partitioning, and reconciliation ideas; capstones are original designs, not Dynamo deployments')
add('https://learn.microsoft.com/en-us/azure/architecture/best-practices/index-best-practices','Application best practices — Microsoft Architecture Center','Official guidance · accessed 21 Oct 2026','Scaling and application boundary review')
add('https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex','Elasticsearch: Reindex documents','Official documentation · accessed 21 Oct 2026','Implementation reindex controls; full generation-switch protocol in the atlas is an original design')
add('https://openlineage.io/docs/','OpenLineage: core model and documentation','Official specification documentation · 1.54.0 at access','Dataset, job, and run lineage concepts')
add('https://kafka.apache.org/41/design/design/','Apache Kafka 4.1: Design','Official versioned documentation','Partitioning and scoped transactional/processing behavior; external effects are separate')
add('https://users.ece.cmu.edu/~adrian/731-sp04/readings/GL-cap.pdf','Brewer’s conjecture and the feasibility of consistent, available, partition-tolerant web services — Gilbert and Lynch, 2002','Original research · university-hosted paper','CAP assumptions and impossibility; PDF text extraction is imperfect, original page inspected')
add('https://jepsen.io/consistency','Jepsen: Consistency models','Primary practitioner research reference','Formal-history distinctions and references to underlying literature')
add('https://lamport.azurewebsites.net/pubs/paxos-simple.pdf','Paxos Made Simple — Leslie Lamport, 2001','Original research','Conceptual consensus safety; atlas does not present toy code as production Paxos')
add('https://arxiv.org/abs/1608.03960','A Conflict-Free Replicated JSON Datatype — Kleppmann and Beresford','Original research · 2017 revision','One formal CRDT model; the miniature tie-break exercise is not this complete implementation')
add('https://learn.microsoft.com/en-us/azure/architecture/patterns/saga','Saga distributed transactions pattern — Microsoft','Official engineering guidance','Local transactions and compensation; compensation is not always a perfect inverse')
add('https://sre.google/sre-book/handling-overload/','Handling Overload — Google SRE','Engineering book','Admission, capacity, and overload response')
add('https://docs.cloud.google.com/architecture/dr-scenarios-planning-guide','Disaster recovery planning guide — Google Cloud','Official guidance · accessed 21 Oct 2026','Recovery planning, distinct from a measured achievement of an objective')
add('https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html','Reliability Pillar — AWS Well-Architected','Official guidance · 2024 revision at access','Reliability review lenses and operations; provider-neutral teaching uses the concepts')
add('https://www.rfc-editor.org/rfc/rfc9700.html','RFC 9700: OAuth 2.0 Security Best Current Practice, 2025','Original protocol security guidance','OAuth threat and flow guidance; implementation should use maintained protocol libraries')
add('https://openid.net/specs/openid-connect-core-1_0.html','OpenID Connect Core 1.0, errata set 2','Original specification · December 2023','Identity layer and validation requirements; distinct from API authorization')
add('https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html','OWASP: Password Storage','Official project guidance · accessed 21 Oct 2026','Password-specific hashing and current deployment parameter guidance')
add('https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html','OWASP: Authorization','Official project guidance · accessed 21 Oct 2026','Least privilege, deny by default, and per-resource enforcement')
add('https://opentelemetry.io/docs/concepts/context-propagation/','OpenTelemetry: Context propagation','Official documentation · accessed 21 Oct 2026','Trace context relationships; trace identity does not authorize access')
add('https://opentelemetry.io/docs/concepts/signals/','OpenTelemetry: Signals','Official documentation · accessed 21 Oct 2026','Complementary observability signals')
add('https://sre.google/workbook/alerting-on-slos/','Alerting on SLOs — The SRE Workbook','Engineering book','Budget burn and actionable alerts')
add('https://sre.google/workbook/canarying-releases/','Canarying Releases — The SRE Workbook','Engineering book','Representative rollout evaluation and stop conditions')
add('https://martinfowler.com/articles/practical-test-pyramid.html','The Practical Test Pyramid — Ham Vocke','Original engineering article','Test scope and feedback trade-offs, not a mandatory test-count ratio')
add('https://research.google/pubs/the-tail-at-scale/','The Tail at Scale — Dean and Barroso, 2013','Original research','Tail-latency considerations; atlas probabilities and latency examples are author-calculated')
add('https://www.rfc-editor.org/rfc/rfc6455.html','RFC 6455: The WebSocket Protocol, 2011','Original standard','Bidirectional transport framing; not durable chat delivery')
add('https://www.rfc-editor.org/rfc/rfc8216.html','RFC 8216: HTTP Live Streaming, 2017','Original protocol description · Informational RFC','One adaptive streaming protocol; do not confuse Informational RFC with Standards Track')
add('https://www.rfc-editor.org/rfc/rfc2697.html','RFC 2697: A Single Rate Three Color Marker, 1999','Original protocol description · Informational RFC','Token-based traffic metering example; atlas admission bucket is a simpler model')
add('https://postgis.net/docs/ST_DWithin.html','PostGIS: ST_DWithin','Official implementation documentation · accessed 21 Oct 2026','Coordinate-system-aware proximity predicate, not exclusive dispatch assignment')
add('https://sre.google/sre-book/distributed-periodic-scheduling/','Distributed Periodic Scheduling — Google SRE','Engineering book','Durable scheduling concerns; atlas schedule architecture is an original worked design')
R={
2:['https://sre.google/workbook/implementing-slos/','https://doi.org/10.1287/opre.9.3.383','https://research.google/pubs/the-tail-at-scale/'],
3:['https://www.rfc-editor.org/rfc/rfc9110.html','https://www.rfc-editor.org/rfc/rfc9000.html','https://www.rfc-editor.org/rfc/rfc8446.html'],
4:['https://pages.cs.wisc.edu/~remzi/OSTEP/','https://go.dev/ref/mem'],
5:['https://doi.org/10.1145/361598.361623','https://refactoring.guru/design-patterns/catalog'],
6:['https://martinfowler.com/articles/injection.html','https://refactoring.guru/design-patterns/catalog'],
7:['https://learn.microsoft.com/en-us/azure/architecture/guide/architecture-styles/','https://martinfowler.com/bliki/BoundedContext.html','https://martinfowler.com/articles/microservices.html'],
8:['https://www.rfc-editor.org/rfc/rfc9110.html','https://api-security.owasp.org/editions/2023/en/0x11-t10/','https://www.rfc-editor.org/rfc/rfc9700.html'],
9:['https://db.cs.cmu.edu/courses/','https://www.postgresql.org/docs/18/indexes-types.html'],
10:['https://www.postgresql.org/docs/18/transaction-iso.html','https://www.postgresql.org/docs/18/indexes-types.html','https://www.postgresql.org/docs/18/wal-intro.html','https://github.com/facebook/rocksdb/wiki/RocksDB-Overview'],
11:['https://www.rfc-editor.org/rfc/rfc9111.html','https://redis.io/docs/latest/develop/reference/eviction/','https://www.cloudflare.com/learning/cdn/what-is-a-cdn/'],
12:['https://learn.microsoft.com/en-us/azure/architecture/best-practices/index-best-practices','https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store'],
13:['https://openlineage.io/docs/','https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-reindex','https://kafka.apache.org/41/design/design/'],
14:['https://jepsen.io/consistency','https://lamport.azurewebsites.net/pubs/time-clocks.pdf','https://users.ece.cmu.edu/~adrian/731-sp04/readings/GL-cap.pdf'],
15:['https://pdos.csail.mit.edu/6.5840/','https://raft.github.io/raft.pdf','https://lamport.azurewebsites.net/pubs/paxos-simple.pdf','https://arxiv.org/abs/1608.03960'],
16:['https://learn.microsoft.com/en-us/azure/architecture/patterns/saga','https://microservices.io/patterns/data/transactional-outbox.html','https://kafka.apache.org/41/design/design/'],
17:['https://sre.google/sre-book/handling-overload/','https://docs.cloud.google.com/architecture/dr-scenarios-planning-guide','https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html'],
18:['https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html','https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html','https://www.rfc-editor.org/rfc/rfc9700.html','https://openid.net/specs/openid-connect-core-1_0.html'],
19:['https://opentelemetry.io/docs/concepts/signals/','https://opentelemetry.io/docs/concepts/context-propagation/','https://sre.google/workbook/alerting-on-slos/'],
20:['https://12factor.net/','https://kubernetes.io/docs/concepts/overview/components/','https://sre.google/workbook/canarying-releases/'],
21:['https://martinfowler.com/articles/practical-test-pyramid.html','https://sre.google/sre-book/handling-overload/','https://research.google/pubs/the-tail-at-scale/']}
CASE_SOURCES={
1:[R[8][0],R[11][0],R[12][0]],2:['https://www.rfc-editor.org/rfc/rfc2697.html',R[17][0]],
3:['https://www.rfc-editor.org/rfc/rfc6455.html',R[16][2],R[10][0]],4:[R[6][0],R[16][1],R[16][2]],
5:[R[11][0],R[12][0],R[16][2]],6:['https://www.rfc-editor.org/rfc/rfc8216.html',R[11][0],R[13][0]],
7:['https://postgis.net/docs/ST_DWithin.html',R[10][0],R[16][0]],8:[R[10][0],R[16][0],R[8][0]],
9:[R[10][0],R[16][1],R[18][0]],10:['https://sre.google/sre-book/distributed-periodic-scheduling/',R[15][1],R[16][2]],
11:['https://arxiv.org/abs/1608.03960','https://www.rfc-editor.org/rfc/rfc6455.html',R[18][0]],
12:[R[13][0],R[13][2],R[18][0],R[16][1]]}
