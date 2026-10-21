# Learn · Research · Visualise

A growing library of interactive, research-grounded learning units. Start with [the contents page](index.html).

Each unit has its own folder and opens as a self-contained HTML page. Navigation uses relative paths, so it works under a GitHub Pages repository subpath, on a local HTTP server, or by opening the HTML files directly. No npm install, build service, API key or external font is needed to read the site. Source links open the original research online.

| Unit | Open | Contents |
| --- | --- | --- |
| 01 · Retrieval Methods | [Open the atlas](retrieval-methods/index.html) | Historical timeline; Boolean, lexical, probabilistic, expansion, dense, learned sparse, late interaction, indexes, rankers, fusion, graphs, multimodal, generative/agentic retrieval; evaluation labs and annotated references. |

## GitHub Pages

This repository includes `.github/workflows/static.yml`, which deploys the static site on pushes to `main`. In **Settings → Pages → Build and deployment**, use **GitHub Actions** as the source. Commit and push site updates to `main`; the workflow serves the root `index.html` and each unit folder’s `index.html`. `.nojekyll` keeps the content as plain static files. See [GitHub’s publishing-source instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

Repository: `NarenMasterofInfinity/Foundational_Works`. The expected default Pages address is `https://narenmasterofinfinity.github.io/Foundational_Works/` once Pages is enabled and deployed. This is a setup address, not a claim that deployment has been performed.

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

To rebuild Retrieval Methods after an editorial change:

```bash
python3 retrieval-methods/src/build.py
```

To preview locally, serve the repository root with `python3 -m http.server 8000` and visit `http://localhost:8000/`. Opening `index.html` directly also works.
