# Plan: humanize the whitepaper (2026-11-16)

Task slug: whitepaper-humanize. Details: `.copilot-tracking/details/2026-11-16-whitepaper-humanize-details.md`. Research: `.copilot-tracking/research/2026-11-16-whitepaper-humanize-research.md`.

## Phases

* [ ] Phase 1: split README.md and main.tex into line-range chunks in a scratch directory (12 prose chunks; the bibliography chunk stays untouched).
* [ ] Phase 2: rewrite each chunk with the humanizer skill plus the user's "Humanize the output" rules, in parallel, without changing facts, numbers, citations, macros, labels, tables or link targets.
* [ ] Phase 3: reassemble, then run integrity checks (macro/label/cite sets, number multiset, link targets, table row counts, line structure of LaTeX environments) against the base.
* [ ] Phase 4: run banned word, dash, `not only ... but also`, `From ... to`, `That's not ... It's`, `Why it matters` scans; fix residue.
* [ ] Phase 5: keep README and main.tex consistent (same claims and phrasings where they repeat the abstract or results).
* [ ] Phase 6: note that `main.pdf` cannot be rebuilt (no TeX engine). Leave it unchanged.
* [ ] Phase 7: single critique and single review, then commit with trailers on the topic branch. No push.

## Critique (one pass, recorded here)

* Risk: parallel rewriters drift on terminology and numbers. Mitigation: automated number and identifier diff; a shared glossary in every chunk prompt.
* Risk: rewriting changelog history misstates what happened on past dates. Mitigation: keep dates and verbs of record, change only wording.
* Risk: LaTeX breakage from edited braces and percent signs. Mitigation: brace balance and environment pairing checks per chunk; escape `\%` preserved.
* Verdict: proceed. No conflict with confirmed decisions.
