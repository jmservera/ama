# Details: #441 checker design

* Language: stdlib Python 3, read-only, deterministic output sorted, JSON summary to stdout.
* Files: `docs/brds/agentic-retrofit-programme-brd.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0007-contractor-intake-staff-mediated-proposal.md`, `docs/architecture/README.md`, plus every docs target they link to (existence only).
* Link check: markdown `[t](target)` outside fenced code; skip http(s)/mailto; resolve relative to file; fragment matched to GitHub-style slugs of headings (lowercase, strip punctuation except hyphen, spaces to hyphens, duplicate suffix -N) in the target md.
* Status check: regex assertions listed in the plan, each reported PASS/FAIL/INFO with file:line.
* Numbering: collect table-row ids `| FR-nnn |`, `AC-nnn` definitions (`AC-nnn:` or table first cell), report duplicates and required ranges.
* Formula: parse the BRD table cells by label; recompute G=B*U*V etc. only where inputs are in the table: N=G-H-J-S, F=N-O, I/O relations, and check F matches within 0.011; check PRD 35.4U-2.96 break-even 8.36% and F(25/50/75).
* Blob SHAs via `git hash-object` and `git rev-parse HEAD:path`.
