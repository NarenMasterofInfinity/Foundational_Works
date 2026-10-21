#!/usr/bin/env python3
"""Small executable atlas mechanisms. Standard library; no network or credentials.

These demonstrate bounded local contracts, not production consensus, authentication,
accounting, or provider integrations. See each chapter for missing system boundaries.
"""
from collections import OrderedDict
from dataclasses import dataclass
from hashlib import sha256
from math import ceil, isfinite
import sqlite3


def capacity(users=10_000_000, requests_per_day=50, peak_factor=5,
             tested_rps_per_instance=600, target_utilization=0.6):
    if min(users, requests_per_day, peak_factor, tested_rps_per_instance) <= 0:
        raise ValueError('positive workload and capacity required')
    if not 0 < target_utilization < 1:
        raise ValueError('target utilization must be between zero and one')
    average=users*requests_per_day/86400
    peak=average*peak_factor
    active=ceil(peak/(tested_rps_per_instance*target_utilization))
    return dict(average=average,peak=peak,active=active,one_instance_failure=active+1)


def amdahl(parallel_fraction, workers):
    if not 0 <= parallel_fraction <= 1 or workers < 1:
        raise ValueError('invalid model parameters')
    return 1/((1-parallel_fraction)+parallel_fraction/workers)


def mm1_residence(service_seconds, utilization):
    """Illustrative stable M/M/1 mean, not a production tail prediction."""
    if service_seconds <= 0 or not 0 <= utilization < 1:
        raise ValueError('stable queue and positive service time required')
    return service_seconds/(1-utilization)


@dataclass
class TokenBucket:
    capacity: float
    rate: float
    tokens: float
    last: float=0

    def __post_init__(self):
        if not all(isfinite(x) for x in (self.capacity,self.rate,self.tokens,self.last)):
            raise ValueError('finite values required')
        if self.capacity <= 0 or self.rate <= 0 or not 0 <= self.tokens <= self.capacity:
            raise ValueError('invalid bucket')

    def spend(self, now, cost=1):
        """Caller must make this whole transition atomic for a shared bucket."""
        if not isfinite(now) or not isfinite(cost) or cost <= 0:
            raise ValueError('finite time and positive cost required')
        elapsed=max(0,now-self.last)
        available=min(self.capacity,self.tokens+elapsed*self.rate)
        allowed=available>=cost
        self.tokens=available-cost if allowed else available
        self.last=max(self.last,now)
        return allowed


class LRU:
    def __init__(self, capacity):
        if capacity < 1:raise ValueError('positive capacity required')
        self.capacity=capacity;self.data=OrderedDict()

    def put(self,key,value):
        self.data[key]=value;self.data.move_to_end(key)
        if len(self.data)>self.capacity:return self.data.popitem(last=False)
        return None

    def get(self,key):
        value=self.data[key];self.data.move_to_end(key);return value


def rendezvous(key,owners):
    if not owners:raise ValueError('at least one owner required')
    return max(owners,key=lambda owner:(sha256((str(key)+'\0'+str(owner)).encode()).digest(),str(owner)))


def vector_relation(a,b):
    if len(a)!=len(b):raise ValueError('same participant set required')
    if a==b:return 'equal'
    if all(x<=y for x,y in zip(a,b)):return 'before'
    if all(x>=y for x,y in zip(a,b)):return 'after'
    return 'concurrent'


def lamport_receive(local,received):return max(local,received)+1


def majority_intersection(n,r,w):
    if not all(type(x) is int for x in (n,r,w)) or n<1 or not 1<=r<=n or not 1<=w<=n:
        raise ValueError('invalid fixed membership set sizes')
    return r+w>n


def keyset_page(rows,after=None,limit=2):
    """Rows are (time, unique_id, value); real cursors also require validation."""
    if limit<1:raise ValueError('positive page size required')
    return [row for row in sorted(rows) if after is None or row[:2]>after][:limit]


def open_demo_store(path=':memory:'):
    db=sqlite3.connect(path)
    db.executescript('''
      CREATE TABLE IF NOT EXISTS seats(id INTEGER PRIMARY KEY, owner TEXT);
      CREATE TABLE IF NOT EXISTS postings(operation TEXT, account TEXT,
        currency TEXT, amount INTEGER, UNIQUE(operation,account));
      CREATE TABLE IF NOT EXISTS processed(event_id TEXT PRIMARY KEY);
      CREATE TABLE IF NOT EXISTS counters(name TEXT PRIMARY KEY,value INTEGER);
      CREATE TABLE IF NOT EXISTS outbox(event_id TEXT PRIMARY KEY,payload TEXT,sent INTEGER DEFAULT 0);
    ''')
    return db


def claim_seat(db,seat,owner):
    with db:
        result=db.execute('UPDATE seats SET owner=? WHERE id=? AND owner IS NULL',(owner,seat))
    return result.rowcount==1


def post_balanced(db,operation,entries):
    """One local posting set per operation; entries: (account,currency,integer amount)."""
    balances={}
    if not entries or len({account for account,_,_ in entries})!=len(entries):
        raise ValueError('nonempty distinct-account demonstration entries required')
    for account,currency,amount in entries:
        if type(amount) is not int:raise ValueError('integer minor units required')
        balances[currency]=balances.get(currency,0)+amount
    if any(balances.values()):raise ValueError('postings must balance per currency')
    normalized=sorted(entries)
    with db:
        previous=db.execute('SELECT account,currency,amount FROM postings WHERE operation=?',(operation,)).fetchall()
        if previous:
            if sorted(previous)!=normalized:raise ValueError('operation payload conflicts')
            return False
        db.executemany('INSERT INTO postings VALUES (?,?,?,?)',[(operation,*row) for row in entries])
    return True


def consume_local_event(db,event_id,counter):
    """Atomic inbox plus local effect. Does not cover external side effects."""
    with db:
        inserted=db.execute('INSERT OR IGNORE INTO processed VALUES (?)',(event_id,))
        if not inserted.rowcount:return False
        db.execute('INSERT INTO counters VALUES (?,1) ON CONFLICT(name) DO UPDATE SET value=value+1',(counter,))
    return True


def record_intent(db,event_id,payload):
    with db:db.execute('INSERT INTO outbox(event_id,payload) VALUES (?,?)',(event_id,payload))


def relay_once(db,publish,crash_after_publish=False):
    row=db.execute('SELECT event_id,payload FROM outbox WHERE sent=0 ORDER BY event_id LIMIT 1').fetchone()
    if row is None:return False
    publish(*row)
    if crash_after_publish:return True
    with db:db.execute('UPDATE outbox SET sent=1 WHERE event_id=?',(row[0],))
    return True


@dataclass
class Workflow:
    input_version: str
    epoch: int=1
    deleted: bool=False
    artifact: str|None=None

    def complete(self,epoch,input_version,artifact):
        if self.deleted or epoch!=self.epoch or input_version!=self.input_version:return False
        self.artifact=artifact;return True


def permit_demo(actor,resource,action):
    """Synthetic policy predicate only; not a credential-validation system."""
    return (actor.get('tenant')==resource.get('tenant') and
            action in actor.get('actions',()) and actor.get('active') is True)


def cost_options():
    """Fictional monthly units, with no equivalence claim about capacity or reliability."""
    return {
      'single':dict(compute=40,data=300,cache=0,storage=1,transfer=20,telemetry=10),
      'replicated_app':dict(compute=160,data=300,cache=50,storage=1,transfer=20,telemetry=20),
      'partitioned':dict(compute=320,data=900,cache=100,storage=2,transfer=40,telemetry=40)}


def architecture_comparison():
    """Constructed latency traces and an independent-failure toy model, not predictions.

    All redundant app instances are interchangeable; at least one must be up.
    A partitioned operation here requires all three data owners. Shared failures,
    failover time, capacity loss and repair dynamics are deliberately excluded.
    """
    samples = {'single': [190]*98+[900,1400],
               'replicated_app': [140]*98+[450,800],
               'partitioned': [110]*98+[600,1600]}
    app_counts = {'single': 1, 'replicated_app': 4, 'partitioned': 8}
    return {name: {'monthly_cost': sum(cost_options()[name].values()),
                   'p99_ms': sorted(trace)[98],
                   'availability': (1-.01**app_counts[name])*.999**(3 if name=='partitioned' else 1)}
            for name,trace in samples.items()}


if __name__=='__main__':
    print('Assumed social workload:',capacity())
    print('Amdahl, 80% parallel, 4 workers:',amdahl(.8,4))
    b=TokenBucket(10,2,10)
    print('Initial grants:',sum(b.spend(0) for _ in range(11)))
    print('Grants after three seconds:',sum(b.spend(3) for _ in range(7)))
    print('Vectors [1,0] and [0,1]:',vector_relation([1,0],[0,1]))
    print('Fictional cost totals:',{k:sum(v.values()) for k,v in cost_options().items()})
    print('Synthetic architecture comparison:',architecture_comparison())
