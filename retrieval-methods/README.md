# Unit 01 · Retrieval Methods

Open [index.html](index.html), or enter from the [library](../index.html). The page embeds its styles, content, calculations and diagrams; it needs no network connection except when you follow external references.

The guide has an overview, a historical timeline, thirteen retrieval/system families, a separate evaluation tab, and an annotated reading room. The categories distinguish models, representations, execution indexes and orchestration rather than presenting all search techniques as interchangeable algorithms.

Fourteen labs cover Boolean expression parsing with phrases and metadata filters, TF–IDF cosine and dot products, BM25 and Dirichlet query likelihood, query expansion, dense-vector geometry, sparse expansion/pruning, MaxSim, IVF-style probing, candidate-limited reranking, rank/score fusion and MMR, graph traversal, visual evidence retention, scripted agentic search, and reorderable evaluation.

The browser calculates the advertised arithmetic. Embeddings, sparse weights, token-similarity matrices, neural reranker scores and semantic scores are explicitly synthetic teaching fixtures. No neural model, LLM or external API runs. Graph/visual/agent demonstrations are deterministic schematics, not implementations of GraphRAG, ColPali or Self-RAG. The demonstrations are not performance benchmarks.

The shared eight-document collection is synthetic. Its titles are labels; lexical labs index only the shown bodies, using lowercase alphanumeric tokens without stemming or stopword removal. Five documents have positive relevance grades for the fixed evaluation query, “solar battery storage”. The evaluation lab separates single-query RR from MRR, relevance recall from ANN recall, and states its nDCG gain convention and AP prefix denominator.

Sources were checked on **20 October 2026**. The reading room contains papers, surveys, book chapters, official practical guides and a first-person research retrospective. Historical milestone dates distinguish first preprints, publications and approximate development periods. Recent work includes Qwen3 Embedding, DIVER and BRIGHT-Pro; no universal or permanent state-of-the-art winner is claimed.

Tabs support arrow keys and Home/End, links use stable anchors (such as `#timeline`, `#fusion`, `#ranking`, `#sources`), mobile has a chapter menu, and the print button expands all families and method notes. Sliders, forms and controls have labels; result regions announce changes. The page respects reduced-motion preferences.

Rebuild: `python3 src/build.py` from this folder, or `python3 retrieval-methods/src/build.py` from the repository root.

`src/verify_browser.mjs` uses Node 22's built-in WebSocket client to check a dedicated headless Chrome debug session. It exercises the actual rendered controls, reference formula outcomes, responsive layouts, direct anchors and local navigation. No third-party JavaScript dependencies are needed.
