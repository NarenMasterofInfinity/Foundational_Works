#!/usr/bin/env python3
"""Independent examples and invariants for the complete edition's executable models."""
from pathlib import Path
import sys,tempfile,sqlite3
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'examples'))
import mechanisms as m
r=m.capacity();assert abs(r['average']-5787.037037)<1e-5 and r['active']==81 and r['one_instance_failure']==82
assert abs(m.amdahl(.8,4)-2.5)<1e-12
assert abs(m.mm1_residence(.01,.9)-.1)<1e-12
b=m.TokenBucket(10,2,10)
assert sum(b.spend(0) for _ in range(11))==10
assert sum(b.spend(3) for _ in range(7))==6
old=b.tokens;assert not b.spend(2) and b.tokens==old
for cost in (0,-1,float('nan')):
 try:b.spend(4,cost)
 except ValueError:pass
 else:raise AssertionError('invalid token cost accepted')
lru=m.LRU(3)
for k in 'ABC':lru.put(k,k)
lru.get('A');assert lru.put('D','D')==('B','B')
assert m.vector_relation([1,0],[0,1])=='concurrent'
assert m.vector_relation([1,0],[1,2])=='before'
assert m.lamport_receive(5,9)==10
assert m.majority_intersection(3,2,2) and not m.majority_intersection(3,1,2)
for key in range(1000):
 old=m.rendezvous(key,['A','B','C']);new=m.rendezvous(key,['A','B','C','D'])
 assert old==new or new=='D','Adding owner may only move a key to the new owner'
rows=[(1,1,'A'),(1,2,'B'),(2,3,'C')]
assert m.keyset_page(rows,after=(1,1))==rows[1:]
with tempfile.TemporaryDirectory() as directory:
 db=m.open_demo_store(str(Path(directory)/'demo.sqlite'))
 db.execute('INSERT INTO seats VALUES (1,NULL)');db.commit()
 other=m.open_demo_store(str(Path(directory)/'demo.sqlite'))
 assert m.claim_seat(db,1,'A') and not m.claim_seat(other,1,'B')
 entries=[('payer','USD',-100),('merchant','USD',100)]
 assert m.post_balanced(db,'op1',entries) and not m.post_balanced(db,'op1',entries)
 for invalid in ([('a','USD',-100),('b','USD',99)],[('a','USD',-100),('b','EUR',100)]):
  try:m.post_balanced(db,'bad',invalid)
  except ValueError:pass
  else:raise AssertionError('unbalanced ledger accepted')
 assert db.execute('SELECT count(*) FROM postings').fetchone()[0]==2
 m.record_intent(db,'event1','payload');deliveries=[]
 def deliver(event,payload):
  deliveries.append(event);m.consume_local_event(db,event,'orders')
 m.relay_once(db,deliver,True);m.relay_once(db,deliver)
 assert len(deliveries)==2 and db.execute('SELECT value FROM counters').fetchone()[0]==1
 assert not m.relay_once(db,deliver)
 db.close();other.close()
w=m.Workflow('F1',epoch=8)
assert not w.complete(7,'F1','stale') and not w.complete(8,'F0','wrong-input')
assert w.complete(8,'F1','current');w.deleted=True;assert not w.complete(8,'F1','resurrected')
actor=dict(tenant='A',actions=['read'],active=True)
assert m.permit_demo(actor,dict(tenant='A'),'read') and not m.permit_demo(actor,dict(tenant='B'),'read')
assert {k:sum(v.values()) for k,v in m.cost_options().items()}==dict(single=371,replicated_app=551,partitioned=1402)
comparison=m.architecture_comparison()
assert [comparison[k]['p99_ms'] for k in ('single','replicated_app','partitioned')]==[900,450,600]
assert abs(comparison['single']['availability']-.98901)<1e-12
assert abs(comparison['replicated_app']['availability']-.99899999001)<1e-12
assert abs(comparison['partitioned']['availability']-.997002999)<1e-12
assert comparison['replicated_app']['availability']>comparison['partitioned']['availability']
print('PASS: capacity and queue arithmetic, token budgets, eviction, keyset pagination, vector order, rendezvous remapping, seat claims, balanced/idempotent postings, outbox duplicate delivery with one local effect, fencing, deletion, tenant policy, fictional costs.')
