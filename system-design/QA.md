# Foundations verification

Verified locally on **21 October 2026**.

- Standard-library build succeeds: 22 units, 99 mapped chapters, 390 exact syllabus topics, four produced chapters, 16 original chapter figures, 11 questions and 11 explained solutions.
- Topic allocation covers each supplied item exactly once. Unit prerequisites are acyclic. Generated element IDs are unique and internal anchors resolve. All twelve mandatory case studies retain all 22 required sections.
- Actual Python behavior passes: invalid title rejection with no write, trimming, durable creation, committed completion, repeated completion, missing-task failure, propagated storage error, reopen recovery, and abrupt process loss before and after commit.
- Browser workbench checks cover early-acknowledgment loss, memory-only loss, durable recovery, commit without an acknowledgment, reset/terminated-state controls, change-propagation scenarios, independently checked preference arithmetic, zero weights, changed priorities, and all four C4 views.
- Global search handles both produced and planned destinations and safely displays arbitrary text. Glossary/source filters handle matches and empty results. Chapter and figure deep links, separate solution links, mobile navigation, and browser-local read marks work.
- All **133 views** fit widths **1440, 1024, 768, 390, and 360 px**. Large SVG diagrams and code scroll inside their own regions rather than widening the page.
- All lessons remain present when JavaScript is disabled. File-based reading requests no external resources. Source links require internet only when opened.
- Print checks show every produced chapter, open advanced sections, and the complete reference desks while excluding all 95 planned chapter bodies. Filters are cleared for print and restored afterward. A tagged A4 foundations PDF is generated.
- The root library lists both atlases, filters each independently, and preserves the Retrieval Atlas’s original links and content.

Commands and the PDF regeneration procedure are in [README.md](README.md). The source/guarantee review and limits of the model are in [SOURCE_REVIEW.md](SOURCE_REVIEW.md).

The browser run uses a dedicated headless Chrome profile. Screenshots in `/tmp/system-design-atlas-qa` were inspected for desktop/mobile composition and representative diagram legibility. This does not substitute for testing later, unwritten chapters or production infrastructure. No deployment was performed.
