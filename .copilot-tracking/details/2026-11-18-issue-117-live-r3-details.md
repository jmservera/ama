# Issue 117 live r3 details (2026-11-18)

* Phase 2: the note `docs/reference/research/issue-117-live-r3-closure-2026-11-18.md` holds the table; update `docs/reference/README.md` (issue 117 paragraph) and append to `docs/reference/log.md`.
* Phase 3: markdown link check on touched files, `git diff --check`, and a secret scan of the raw folder. Not applicable: mypy, ruff, unit suites beyond the offline document tests already run.
* Excluded by owner decision: Azure billing reconciliation, DPO and Legal approval, person-run assistive-technology testing.
* Not done by design: setting `ZF_SCANNER=defender` on the running demo API.
