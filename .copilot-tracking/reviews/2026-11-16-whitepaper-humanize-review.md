# Review: humanize the whitepaper (2026-11-16)

Review executed once. Outcome: conformant with qualifications. Boundary: README.md and main.tex under docs/capstone/thought-leadership/everything-but-the-software/.

* Facts: numbers multiset, link targets, table rows, code fences, hashes, LaTeX macros, labels, cites and brace balance equal to base (scripted).
* Style rules: scripted scan finds no banned words, em or en dashes, not-only-but-also, From-X-to-Y, That's-not-It's, or "Why it matters" in prose. Remaining `harness`, `Leveraging` and `insights` are identifiers, cited titles, URLs and paths.
* Tests: `anc` unit tests show the same 4 failures as the base (native exporter needs a browser; prompt binding, allocation labels and first-person tests fail on base too). One new failure caused by a reworded pinned phrase was fixed.
* Qualifications: (1) `main.pdf` not rebuilt, no TeX engine installed; the PDF text predates this rewrite. (2) Rewriters ran in parallel chunks, so some sentence-level stylistic repetition across chunk boundaries may remain. (3) No scientific or human review claimed. (4) README "I rewrote..." status records were reworded in place, so the historical 16 November record now reads in the author's voice; facts are unchanged.

Follow-ups: rebuild `main.pdf` where pdflatex or tectonic exists; a human read of the abstract and conclusion.
