# Changes: humanize the whitepaper (2026-11-16)

Files changed: `docs/capstone/thought-leadership/everything-but-the-software/README.md` and `main.tex`. Prose reworded in all prose chunks (README 6 chunks, main.tex abstract through back matter and the register intro). Bibliography, preamble code, tables, figures, equations and `anc/` inputs unchanged.

* Removed not-X-but-Y contrasts, staged closers, bold decoration, passive chains, stacked qualifiers, the ungrammatical abstract opening ("Despite of").
* README prose "harness" became "procedure"/"tooling"; the historical v2 note titles now say "procedure" to match the current section title. `harness` stays only in cite keys, `\label{sec:harness}`, bibliography titles, URLs and paths.
* `subsequently`, `ecosystem-wide`, `bridge` and en dashes in ID ranges (H1-H7, F1-F10) removed.
* One reword reverted after `anc/test_measurement_provenance.py` pinned the phrase "offer design inputs for a future study" and "require separate development and review".
* Trailing whitespace stripped in main.tex prose ranges.
* `main.pdf` not rebuilt: pdflatex, tectonic, latexmk and xelatex are not installed. The committed PDF predates this wording change.

Validation: number multiset, link targets, table row count (192), code fences, hashes, LaTeX macro/label/cite multiset, brace balance and `\%` count identical to base. Regex scans clean for prose. `git diff --check` clean. anc tests: 4 failures, same as on base (74 run).
