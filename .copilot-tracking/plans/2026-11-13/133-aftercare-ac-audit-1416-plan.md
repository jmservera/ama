<!-- markdownlint-disable-file -->
# Plan: Issue #133 literal acceptance-criteria evidence audit

* Task: `133-aftercare-ac-audit-1416`; Refs #133, #89; tier Focused (tracking-only, no production code)
* Research: [research](../../research/2026-11-13/133-aftercare-ac-audit-1416-research.md)
* Details: [details](../../details/2026-11-13/133-aftercare-ac-audit-1416-details.md)

## Phases

* [x] Phase 1: Plan critique (independent `rubber-duck`, approve with changes, all applied): [critique](../../critiques/2026-11-13/133-aftercare-ac-audit-1416-critique.md)
* [x] Phase 2: Execute the five aftercare test modules in `/tmp/venv-133-1416`, record counts, skips and exits
* [x] Phase 3: Probe AC5 denylist and AC1/AC6 served-surface gaps read-only (throwaway, not committed as source)
* [x] Phase 4: Write the per-criterion proof table (`file:line` plus test method) into changes.md
* [ ] Phase 5: Independent `code-review`, clean up `/tmp/venv-*`, commit tracking-only package

## Success criteria

* Each of AC1..AC6 has a verdict `PROVEN` or `NOT FULLY PROVEN` with the exact missing clause and gate owner
* Test counts and SQL skips recorded exactly from the run, not inferred
* No source, test, issue or remote change; `git status --short` empty and `git diff --check` clean after commit
