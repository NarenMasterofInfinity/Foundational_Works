# Current revision: integrated release and Unit 4 review

The 27 October 2026 release integrates the merged chapter companions into the committed HTML and complete PDF. The renderer requires the expected companion modules and chapter keys, checks their lesson/diagram counts, and records their source paths in the completion manifest. It registers only figures that appear in the HTML.

Unit 4 is the focused editorial and visual scope. Its four chapters retain the existing uploaded-file narrative and stable topic/figure links. Duplicate introductions and supplemental prose are removed. The 17 custom figures have captions that explain the visible evidence, with separate compositions for desktop and phones. Counter values, worker and semaphore limits, lock names, and overload rates agree with the lessons. Deadlock shows both held-lock ownership and the complete waiting cycle. Phone figures fit without horizontal panning and use labels of at least 12 rendered CSS pixels at 360 and 390 px viewports.

A fresh, context-free read of Chapter 4.3 identified terminology, lost-update, transfer-example, and condition-variable clarity gaps. Those findings are incorporated. The Go memory model and Python threading/task documentation support the synchronization and cancellation distinctions; illustrative rates remain assumptions.

The release pipeline follows the actual hosting mode: committed files from main, published by built-in branch Pages. Shell-only CI preserves the repository’s local-actions policy, rejects stale generated files, and verifies a source identifier inside both HTML and PDF. Source, HTML, blueprint, manifest, PDF, and release record must ship together.

Earlier Units 5 and 6 language revisions remain. Companion additions in other units are integrated, but have not received the Unit 4 quality review in this pass. This release makes no blanket claim that all 99 chapters meet the textbook revision standard. See [QA.md](QA.md) for checks and [README.md](README.md#release) for release commands.
