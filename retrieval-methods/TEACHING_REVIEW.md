# Intuition and calculation review · 21 October 2026

Every method family, the overview, the timeline, evaluation and the reading-room introduction were reviewed for an explanation of the underlying problem before unfamiliar names or notation. All 52 method notes receive a concrete explanation and definitions before their optional formal account. Fourteen chapter diagrams explain the transition from an input to a decision; they are labeled illustrative examples.

| Chapter | First intuition | Important clarification |
| --- | --- | --- |
| Boolean | Tick only pages that obey a stated rule. | Actual indexed bodies are visible. `battery` and `batteries` differ unless an explicit processing rule connects them. Matching has no relevance scores. |
| Lexical | Some words reveal more than others. | Counts within a page differ from counts of documents; vector length differs from token count. |
| Probabilistic | Repetition helps, with diminishing extra credit. | BM25 is not a probability. The alternative word-probability model is not a chatbot. |
| Expansion | Ask in words the writer used. | Word-form changes, synonyms, judged feedback and generated hypotheses are distinct. |
| Dense | Put related meanings near one another. | Real dimensions are distributed; cosine ignores pure scaling while dot product does not. |
| Learned sparse | Keep a weighted dictionary with few active clues. | Learned expansion and pruning are visible; vocabulary coordinates need not be literal input words. |
| Late interaction | Find support for each part of a request. | MaxSim adds one maximum per query token, including only one value for tied duplicate columns. |
| Indexes | Organize places to look before searching. | Index approximation error differs from relevance error; all point distances can be inspected. |
| Ranking | Read a manageable shortlist more carefully. | Word-only candidates exclude nonmatches; a reranker cannot recover D2 without a source adding it. |
| Fusion | Combine searchers without confusing their score units. | Rank, score, source weight, result depth and RRF smoothing are different. Constant-list normalization is explicitly stated. |
| Structured | Join facts or move between detail levels. | A two-hop lookup is not the full GraphRAG pipeline; unsupported edges cannot justify an answer. |
| Multimodal | Preserve the type of evidence the question needs. | Good text extraction can preserve structure; retaining pixels does not guarantee model correctness. |
| Generative/agentic | Search for what is still missing. | Generated IDs, generated hypotheses and retrieved evidence have distinct roles. |
| Evaluation | Check what was recovered and how early. | Judgments, gains, cutoffs, denominators and single-query versus mean measures are explicit. |

The mathematical review uses the equations and the published synthetic corpus to calculate independent Python reference values, then compares them with the actual browser functions. It covers 221 cases, including repeated queries, absent terms, BM25 `k₁=0`, length-adjustment endpoints, zero and full source weights, duplicate-source votes, one-item normalization, MMR endpoints, all IVF probe counts and every evaluation cutoff for several orders. UI tests additionally check phrase matching, NOT precedence, plural nonmatches, the explicit word-form fixture, MaxSim, pruning, graph evidence and aspect coverage.

The BM25 review caught a floating-point tie artifact: at `k₁=0`, multiplying by a repeated-term count and later dividing it out could leave an epsilon-sized difference. Computing the repetition multiplier first makes mathematically equal repetition credit exactly equal in this case. The displayed contribution trace and scorer now share those contributions, and the independent reference checks verify them.

Teaching references (original explanations and diagrams here are newly written):

- [Stanford: Boolean retrieval](https://nlp.stanford.edu/IR-book/html/htmledition/boolean-retrieval-1.html)
- [Stanford: stemming and lemmatization](https://nlp.stanford.edu/IR-book/html/htmledition/stemming-and-lemmatization-1.html)
- [Sentence Transformers: retrieve and rerank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)
- [Google ML course: measuring similarity from embeddings](https://developers.google.com/machine-learning/clustering/dnn-clustering/supervised-similarity)
