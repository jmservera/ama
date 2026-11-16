# Research: humanize the "Everything but the Software" whitepaper (2026-11-16)

Task slug: whitepaper-humanize. Base: origin/main 0fec16bab717734a9086c6e0cbd80e6a00aeb903. Branch: docs/humanize-whitepaper-everything-but-the-software.
Research disposition: executed. Planning Readiness: Ready.

## Scope

* `docs/capstone/thought-leadership/everything-but-the-software/README.md`: 2303 lines, about 20.8k words. A dated source-package and revision record. Mixed prose, tables, link targets.
* `.../main.tex`: 2012 lines, about 12.9k words. Prose lines 70-1223 and the source register 1916-2012. Lines 1224-1911 are the bibliography (cited titles, not edited). `\input` files in `anc/` are out of scope.
* `main.pdf`: pdflatex, tectonic, latexmk and xelatex are not installed. The PDF cannot be rebuilt and stays unchanged; record this.

## Baseline pattern scan (before edits)

* Banned words in prose: README `subsequently` (1, line 471), `harness` as ordinary prose (lines 808, 845, 1985, 2167-2168); `insight(s)` only in a filename/link (exempt, path).
* main.tex: `harness` appears only in cite keys, a label (`sec:harness`, referenced from `anc/`), bibliography titles, URLs and file paths (identifiers and titles, exempt); `Leveraging` appears only inside a cited title (exempt).
* No em dashes in either file. README `---` hits are YAML frontmatter and table separators. README lines 586-587 contain en dashes in "A-E" and "F1-F10" style ranges (ASCII range characters to review).
* No "why it matters", "not only ... but also", or "From ... to ..." hits at baseline other than one `From X to Y` pattern to confirm.

## Constraints

* Preserve numbers, citations, `\ref`/`\cite`/`\label`, environments, tables, equations, links, code, hashes, YAML frontmatter.
* Humanizer skill: file mode, change prose only.
* Existing prose is already direct. Main tells expected: stacked qualifiers, "We then"/"Finally" sequencing, repeated sentence openings, passive voice, "The X records" changelog patterns, hyphenated modifiers after nouns, grammar slips ("Despite of").

## Method decision

Split into line-range chunks, rewrite in parallel in a scratch directory, reassemble, then verify with diff-based number/macro integrity checks and regex scans.

## Validation available

Regex scans, `\ref`/`\label`/`\cite` set comparison against base, number multiset comparison, Markdown link target comparison, `anc/test_paper_tooling.py` if it runs, `git diff --check`.
