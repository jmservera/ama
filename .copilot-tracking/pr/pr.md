---
title: "feat(src): enforce scoped resident decisions and representative authority"
description: PR description for issue 86, expanded with the committed changes record when published
ms.date: 2026-10-15
---

## Summary

Recorded supplied human resident decisions against exact home/measure/scope/
design revisions in the migrated core/API. Added current representative authority
and measure-scoped release checks, without inferring consent from contact,
access, AI output or historical case-wide answers.

Refs #86

## Changes

* Added versioned scope/source decisions and representative task, evidence,
  wishes, review-date and safe-contact authority. Expired, unclear, disputed,
  revoked, superseded or changed-contact authority stopped representative
  consent/disclosure reliance. Direct resident statements remained recordable.
* Bound work-order versions and quality records to explicit current measure
  contexts. Pause/withdrawal marked only its measure for human review.
  Independent siblings remained releasable; restart required new supplied
  acceptance and human-review evidence. SQL transaction guards rechecked
  dependencies before commit.
* Added independent review tied to an actual recorded decision and a distinct
  human reviewer. Complaint/review records did not change resident answers,
  hazards or retrofit state and remained available after pause or closure.
* Removed the misleading case-wide answer editor, started supplied-answer
  selectors blank, protected authority/source/wishes projections and detached
  histories before redaction. Scoped currentness replaced legacy answer labels
  in lists/cards/AI sources. Existing configured AI proposals, release controls
  and human approvals remained enabled; no model could record consent.
* Added JSON/SQLite semantics and real loopback HTTP regressions, updated
  affected synthetic fixtures, component guides and reference index/log.
  Committed the complete Research, Plan, critique, Implement and Review evidence.

All new code/tests stayed in `src/` under Accepted ADR 0006 and the parity matrix.
No new SQL schema/dialect, workload dependency, image dependency or deployment
was added. Core imported no workload; API's existing agents dependency remained
within the pre-#144 boundary. `mvp/`, `.env`, `.vscode` and
`.copilot-tracking/github-issues` were untouched. No private resident data was used.

## Acceptance and evidence boundary

* [x] Resident decisions stayed separate, never inferred/prefilled, and started
  Not recorded. Exact context, supplied-source and nonmutation tests passed.
* [x] Local negative controls stopped expired, unclear or disputed
  representative authority for disclosure and consent reliance, including
  current authority rechecks and safe-contact changes.
* [x] Pause/withdrawal affected only its measure, flagged dependent human review
  and blocked its bound release while independent sibling work/QA remained usable.
* [ ] Residents could actually reach independent human review and the formal
  complaints route without detriment. Local owned records and state-independence
  tests were delivered, but actual service routing, human accessibility/
  independence and resident acceptance were not evidenced.
* [ ] Operational representative roles/authority/retention were ratified.
* [ ] Actual model inference, SQL Server/Azure workflow and container evidence
  were produced. Synthetic adapter/SQLite/local app evidence was not live evidence.

This intentionally used **Refs #86**, not an auto-closing reference.

## Local validation

Dependencies were installed with pip only, after missing-module/tool probes:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -q -e 'src/core[dev]' -e 'src/agents[dev]' -e 'src/api[dev]' -e 'src/orchestrator[dev]' -e 'src/importer[dev]'
```

From each project directory, `../../.venv/bin/python -m unittest discover -s
tests -q` ran with no extra PYTHONPATH for core/agents/importer,
`PYTHONPATH=../core/tests:../agents/tests` for API and
`PYTHONPATH=../core/tests` for orchestrator.

| Project | Final full suite | Ruff check / format check / mypy |
| --- | --- | --- |
| core | 343 passed | Passed / 19 files / 72 source files |
| api | 479 run, 97 skipped, passed | Passed / 10 files / 38 source files |
| agents | 70 passed | Passed / 11 files / 16 source files |
| orchestrator | 17 passed | Passed / 5 files / 8 source files |
| importer | 39 passed | Passed / 11 files / 10 source files |

Per-project checks used `../../.venv/bin/ruff check . &&
../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy`.
After the final transaction cleanup, full core and the 16 API resident/document
control tests were rerun successfully, along with core/API quality checks.

`tests/test_resident_api.py` actually started the app on a loopback ephemeral
port with synthetic data, exercised `/healthz`, `/app`, authenticated resident/
authority/redress endpoints and SQLite reopen. This was not source-only app
inspection. No live inference was claimed.

From `src/api`, `../../.venv/bin/python -m checks.design_system_browser_check`
passed with Chromium 156.0.8078.4: 320/390/1280px reflow, keyboard scrolling and
activation, reduced motion, forced colours/status text and no uncaught JS.
The five namespace entrypoints, namespace distribution assertion, existing
dependency-rule suites, three `node --check` commands, state JSON, added relative
documentation links and `git diff --check` also passed.

`docker info --format '{{.ServerVersion}}'` failed with permission denied on
`/var/run/docker.sock`. No permission escalation or local image build/run was
claimed; image checks were left to CI.

Initial wrong-directory/import-path, fixture and typing failures plus their
corrections are recorded in the full command/result appendix below and in
`.copilot-tracking/changes/2026-10-15/resident-decisions-86-changes.md`.

## RPI Review and remaining work

One independent final-candidate critique ran, with all six compatible findings
directly dispositioned. One post-implementation Review ran: execution
**Complete**, outcome **Residual work**. No implementation defect was established
within the bounded assessment, and no second implementation/Review loop ran.

The Review routed three distinct follow-ups: owner/compliance ratification
(RV-001), actual complaints/independent-review human acceptance (RV-002), and
authorized live runtime/CI container evidence (RV-003). Full issue acceptance
was not claimed. The owner retains the merge decision.

Canonical committed artifacts:

* `.copilot-tracking/research/2026-10-15/resident-decisions-86-research.md`
* `.copilot-tracking/plans/2026-10-15/resident-decisions-86-plan.md`
* `.copilot-tracking/plans/2026-10-15/resident-decisions-86-critique.md`
* `.copilot-tracking/details/2026-10-15/resident-decisions-86-phase-details.md`
* `.copilot-tracking/changes/2026-10-15/resident-decisions-86-changes.md`
* `.copilot-tracking/reviews/logs/2026-10-15/resident-decisions-86-review.md`
* `.copilot-tracking/rpi-sessions/2026-10-15/resident-decisions-86-state.json`

## Branch and CI

The named topic branch was based on the already merged src moves #296-#302.
At the publication fetch, `origin/main` had advanced by #315 and #316 (two
commits). No merge, rebase, force push or history rewrite was performed; the
structured PR diff used the merge base. Hosted checks/mergeability must be
assessed against the current base before owner merge.

PR #319 is **blocked by conflicts**, not ready to merge. GitHub reports
CONFLICTING/DIRTY and no hosted checks. A read-only merge-tree diagnostic
identified `docs/reference/log.md`, `src/api/README.md`, `src/core/README.md`
and `src/core/src/zava_forward/core/ai_tasks.py`. No branch merge/rebase or
source correction was performed after Review. Owner-authorized integration
and affected validation must precede CI/merge; CI is not reported as passed.
