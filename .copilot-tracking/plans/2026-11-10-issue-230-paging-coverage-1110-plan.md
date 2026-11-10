<!-- markdownlint-disable-file -->
# Plan: issue 230 native browser paging proof (initial coverage)

* Task: `issue-230-paging-coverage-1110`; research `.copilot-tracking/research/2026-11-10-issue-230-paging-coverage-1110-research.md`; details `.copilot-tracking/details/2026-11-10-issue-230-paging-coverage-1110-details.md`.
* Tier: focused (small coverage; no product, infrastructure, SQL, security, workflow or dependency change). Mixed-change rule: strictest applicable is focused, no gate semantics touched.
* Refs #230 and #149 only. No closing keyword. Whole-WCAG, AT, usability, live or production acceptance is not claimed.

## Phases

* [ ] Phase 1: private fixture wrapper and the standalone checker `src/api/checks/programme_paging_browser_check.py`.
* [ ] Phase 2: run the checker under the non-queued heavy lock with concrete origin and served-source assertions; record raw logs externally.
* [ ] Phase 3: documentation of the maintained manual entrypoint in `src/api/README.md`; static (Ruff 0.17.1, mypy 2.4.0) and regression controls.
* [ ] Phase 4: changes record, one self-critique-informed review, scoped commits, witness commit-complete, handoff.

## Success criteria

* Baseline Node tests and story 230 pass unchanged (done, see research).
* New checker passes at 1280 and 320 for the Programme Manager with the assertions in the details.
* No file outside the allowed set changes: new checker, `src/api/README.md` entry, original RPI evidence under `.copilot-tracking/`, one knowledge-base log line only if a knowledge-base file changes (README is not in `docs/reference/`, so none expected).
* Static checks clean; focused unit/Node tests and manifest/needs-inventory controls unchanged.

## Stop conditions

* Heavy lock busy: stop, no queue, spin or bypass.
* Checker cannot establish the existing case/role contract: stop with the exact unsupported contract.
* Any failure against existing paging code or the new checker after the single review: no post-review repair (correction balance UNKNOWN); report only.
