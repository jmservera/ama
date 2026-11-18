# Plan: #164 / PR #1641 merge with main f1df574bb

* [x] Phase 1: merge origin/main (no rebase), repo rerere replayed 26 file resolutions; resolve README.md by hand (keep main's new rows and the PR's newer DPIA row, ms.date 2026-11-17); log.md auto-merged.
* [ ] Phase 2: reapply prior reviewed alignment (69367b4f1) so main's chat widget markup and safeguarding redaction win: restore main widget markup, keep safeguarding owners out of staff detail, drop PR tests for dropped behaviour.
* [ ] Phase 3: targeted core/api tests, mypy per project, ruff format check; fix only merge-caused failures.
* [ ] Phase 4: single critique, review, commit.

Details: see details file. Excluded: consent-regrant defects, rpi-checks --all (coordinator, heavy lock). Prior e2d4691b1 format fix reapplied only if the format check still fails.
