#!/usr/bin/env python3
"""Independent Python reference values consumed by the real-browser verifier.

Uses the documented equations and the published teaching corpus, not the page's
JavaScript functions or rendered scores. Outputs JSON; standard library only.
"""
import json
import math
from collections import Counter
from itertools import product

from content import CORPUS

COUNTS = {d['id']: Counter(d['text'].lower().split()) for d in CORPUS}
IDS = [d['id'] for d in CORPUS]
GRADE = {d['id']: d['rel'] for d in CORPUS}
VOCAB = sorted(set().union(*COUNTS.values()))
LENGTH = {id: sum(count.values()) for id, count in COUNTS.items()}
TOTAL = sum(LENGTH.values())
assert len(IDS) == 8 and TOTAL == 71
assert COUNTS['D1']['battery'] == 2
assert sum('battery' in c for c in COUNTS.values()) == 3
assert all('batteries' not in c for c in COUNTS.values())

CASES = []

def emit(kind, args, ids=None, values=None):
    CASES.append(dict(kind=kind, args=args, ids=ids, values=values))

def sorted_scores(scores):
    return sorted(scores, key=lambda id: (-scores[id], id))

def bm_scores(query, k1=1.2, b=.75):
    # Query repetition is intentionally ignored in this BM25 variant.
    result = {}
    for id in IDS:
        contributions = []
        for token in set(query.lower().split()):
            count = COUNTS[id][token]
            if not count:
                continue
            documents = sum(token in counts for counts in COUNTS.values())
            weight = math.log(9 / (documents + .5))
            adjustment = k1 * (1 - b + b * LENGTH[id] / (TOTAL / 8))
            contributions.append(weight * (k1 + 1) / (1 + adjustment / count))
        result[id] = math.fsum(contributions)
    return result

for query, k1, b in product(
        ['solar battery storage', 'battery', 'battery battery', 'batteries', 'storage'],
        [0, 1.2, 3], [0, .75, 1]):
    scores = bm_scores(query, k1, b)
    order = sorted_scores(scores)
    emit('bm25', [query, k1, b], order, [scores[id] for id in order])

for query, mode in product(
        ['solar battery storage', 'battery battery', 'batteries', 'night electricity'],
        ['cosine', 'dot']):
    query_counts = Counter(query.split())
    vocabulary = sorted(set(VOCAB) | set(query_counts))
    weights = {t: math.log(9 / (1 + sum(t in c for c in COUNTS.values()))) + 1 for t in vocabulary}
    qnorm = math.sqrt(math.fsum((query_counts[t] * weights[t]) ** 2 for t in vocabulary))
    scores = {}
    for id in IDS:
        raw = math.fsum(query_counts[t] * COUNTS[id][t] * weights[t] ** 2 for t in vocabulary)
        dnorm = math.sqrt(math.fsum((COUNTS[id][t] * weights[t]) ** 2 for t in vocabulary))
        scores[id] = raw / (qnorm * dnorm) if mode == 'cosine' and qnorm * dnorm else raw
    order = sorted_scores(scores)
    emit('lexical', [query, mode], order, [scores[id] for id in order])

for query, mu in product(['solar battery storage', 'battery battery', 'night electricity'], [1, 100, 300]):
    scores = {}
    for id in IDS:
        logs = []
        for token in query.split():
            collection_count = sum(c[token] for c in COUNTS.values())
            probability = (COUNTS[id][token] + mu * collection_count / TOTAL) / (LENGTH[id] + mu)
            logs.append(math.log(probability))
        scores[id] = math.fsum(logs)
    order = sorted_scores(scores)
    emit('likelihood', [query, mu], order, [scores[id] for id in order])

SEMANTIC = dict(zip(IDS, [.91, .98, .2, .6, .08, .8, .72, .03]))

def fusion(depth, k, alpha, duplicate, mode):
    word_scores = bm_scores('solar battery storage')
    words = [id for id in sorted_scores(word_scores) if word_scores[id] > 0][:depth]
    meanings = sorted_scores(SEMANTIC)[:depth]
    ids = set(words) | set(meanings)

    def normalize(ids, scores):
        low, high = min(scores[id] for id in ids), max(scores[id] for id in ids)
        return {id: (scores[id] - low) / (high - low) if high != low else 0 for id in ids}

    if mode == 'score':
        wa, wb = normalize(words, word_scores), normalize(meanings, SEMANTIC)
    else:
        wa = {id: 1 / (k + i + 1) for i, id in enumerate(words)}
        wb = {id: 1 / (k + i + 1) for i, id in enumerate(meanings)}
    scores = {id: alpha * wa.get(id, 0) * (2 if duplicate else 1) + (1 - alpha) * wb.get(id, 0) for id in ids}
    return sorted_scores(scores), scores

for args in product([1, 4, 8], [0, 60, 100], [0, .5, 1], [False, True], ['rrf', 'score']):
    order, scores = fusion(*args)
    emit('fusion', list(args), order, [scores[id] for id in order])

for depth, lam in product([4, 8], [0, .5, 1]):
    order, scores = fusion(depth, 60, .5, False, 'rrf')
    scale = max(scores.values())
    selected, selected_values = [], []
    while order:
        current = {}
        for id in order:
            tokens = set(COUNTS[id])
            redundant = max((len(tokens & set(COUNTS[chosen])) / len(tokens | set(COUNTS[chosen]))
                             for chosen in selected), default=0)
            current[id] = lam * scores[id] / scale - (1 - lam) * redundant
        winner = min(order, key=lambda id: (-current[id], -scores[id], id))
        selected.append(winner)
        selected_values.append(current[winner])
        order.remove(winner)
    emit('mmr', [depth, lam], selected, selected_values)

CLUSTERS = [
    ((.3, .25), [('A1', (.24, .3)), ('A2', (.44, .47))]),
    ((.7, .65), [('B1', (.54, .5)), ('B2', (.77, .8))]),
    ((.2, .85), [('C1', (.3, .85)), ('C2', (.12, .9))]),
]
for probes, y in product([1, 2, 3], [.1, .5, .9]):
    q = (.5, y)
    near_groups = sorted(CLUSTERS, key=lambda c: math.dist(q, c[0]))[:probes]
    exact = sorted([p for _, points in CLUSTERS for p in points], key=lambda p: math.dist(q, p[1]))[:2]
    found = sorted([p for _, points in near_groups for p in points], key=lambda p: math.dist(q, p[1]))[:2]
    recall = len({id for id, _ in exact} & {id for id, _ in found}) / 2
    emit('ivf', [probes, y], [id for id, _ in found], [recall])

orders = [sorted(IDS, key=lambda id: (-GRADE[id], id)),
          sorted(IDS, key=lambda id: (GRADE[id], id)),
          sorted_scores(bm_scores('solar battery storage')),
          ['D3', 'D1', 'D5', 'D2', 'D8', 'D6', 'D4', 'D7']]
for order, k in product(orders, range(1, 9)):
    prefix = order[:k]
    useful_positions = [i + 1 for i, id in enumerate(prefix) if GRADE[id] > 0]
    precision = len(useful_positions) / k
    recall = len(useful_positions) / 5
    rr = 1 / useful_positions[0] if useful_positions else 0
    gains = [2 ** GRADE[id] - 1 for id in prefix]
    dcg = math.fsum(g / math.log2(i + 2) for i, g in enumerate(gains))
    ideal_gains = sorted([2 ** grade - 1 for grade in GRADE.values()], reverse=True)[:k]
    ideal = math.fsum(g / math.log2(i + 2) for i, g in enumerate(ideal_gains))
    ap = math.fsum(n / rank for n, rank in enumerate(useful_positions, start=1)) / 5
    emit('metrics', [order, k], values=[precision, recall, rr, dcg / ideal, ap, dcg, ideal])

for a, b in [([1, 1], [2, 2]), ([1, 0], [0, 1]), ([0, 0], [1, 2]), ([.65, .85], [.8660254037844386, .5])]:
    dot = math.fsum(x * y for x, y in zip(a, b))
    lengths = math.sqrt(math.fsum(x * x for x in a) * math.fsum(y * y for y in b))
    emit('geometry', [a, b], values=[dot, dot / lengths if lengths else 0])

print(json.dumps(CASES, separators=(',', ':')))
