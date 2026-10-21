# Learn · Research · Visualise

A growing library of interactive, research-grounded learning units. Start with [the contents page](index.html).

Each unit has its own folder and opens as a self-contained HTML page. Navigation uses relative paths, so it works under a GitHub Pages repository subpath, on a local HTTP server, or by opening the HTML files directly. No npm install, build service, API key or external font is needed to read the site. Source links open the original research online.

| Unit | Open | Contents |
| --- | --- | --- |
| 01 · Retrieval Methods | [Open the atlas](retrieval-methods/index.html) | Historical timeline; Boolean, lexical, probabilistic, expansion, dense, learned sparse, late interaction, indexes, rankers, fusion, graphs, multimodal, generative/agentic retrieval; evaluation labs and annotated references. |
| 02 · System Design | [Open the atlas](system-design/index.html) | Staged foundations edition: complete 22-unit, 99-chapter blueprint; four fully written Unit 1 chapters, 16 original chapter diagrams, four interactive workbenches, exercises and separate solutions. Units 2–22 and the 12 case studies remain planned. |

## GitHub Pages

This repository publishes through GitHub’s built-in Pages deployment from **main → / (root)**. In **Settings → Pages → Build and deployment**, the source is **Deploy from a branch**. Commit and push site updates to `main`; Pages serves the root `index.html` and each unit folder’s `index.html`. `.nojekyll` keeps the content as plain static files. See [GitHub’s publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

Repository: `NarenMasterofInfinity/Foundational_Works`. The live library is `https://narenmasterofinfinity.github.io/Foundational_Works/`. The 21 October 2026 retrieval revision was verified against the exact HTML served by Pages. The separate custom workflow at `.github/workflows/static.yml` is blocked by the repository’s owner-only action policy; built-in branch publishing succeeds independently.

## Unit structure

```text
index.html                   # Stylish library / contents page
.nojekyll                    # Serve plain static files
retrieval-methods/
  index.html                 # Self-contained published unit
  README.md                  # Scope, demos, references and verification
  src/
    content.py               # Methods, sources, timeline, teaching collection
    teaching.py              # Intuition-first stories, definitions and method lessons
    template.html            # Page shell
    style.css                # Responsive styles
    app.js                   # Navigation and all browser-side calculations
    build.py                 # Standard-library-only HTML builder
    verify_browser.mjs       # Browser, interaction, print and independent-math checks
    math_reference.py        # Independent reference values for 221 calculation cases
```

Add future topics as sibling folders, each with an `index.html`, then add an entry to the root contents page. Keep links relative; do not prefix unit URLs with `/`, which would drop the repository subpath on GitHub Pages.

System Design is also self-contained and built with Python’s standard library:

```bash
python3 system-design/src/build.py
```

See its [editorial blueprint](system-design/BLUEPRINT.md), [completion manifest](system-design/completion-manifest.json), and [production notes](system-design/README.md). The blueprint allocates the entire supplied syllabus; an allocation is explicitly distinct from a produced lesson.

To rebuild Retrieval Methods after an editorial change:

```bash
python3 retrieval-methods/src/build.py
```

To preview locally, serve the repository root with `python3 -m http.server 8000` and visit `http://localhost:8000/`. Opening `index.html` directly also works.
