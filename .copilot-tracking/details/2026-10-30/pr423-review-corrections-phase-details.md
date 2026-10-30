---
title: PR 423 review corrections phase details
description: Task-level implementation and validation expectations
ms.date: 2026-10-30
---

## Metadata

Task ID: pr423-review-corrections-2026-10-30.
Plan: .copilot-tracking/plans/2026-10-30/pr423-review-corrections-plan.md.
Research: .copilot-tracking/research/2026-10-30/pr423-review-corrections-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01, P01-T02, P01-T03 |
| P02 | P02-T01/T02 complete; final commit/gate pending at committed snapshot | P02-T01, P02-T02, P02-T03 |

P01 completion evidence: commits 03b53303 and e8d29686 preserve remote child
and main ancestry; main recorded score is byte-identical and no application
runtime differs from pinned main. New transport regression discovery shows
5 failures/1 error before correction, then 72 tests pass after correction.
Current runbook corrected and local replacement body prepared; historical
activation receipts and RPI evidence remain unchanged.

<!-- rpi:phase id=P01 -->
## P01: Preserve ancestry and correct transport

<!-- rpi:task id=P01-T01 -->
### P01-T01: Integrate without rewriting history

Starting bda7975f, remote score child 32cc1f81; pinned main
d986c4c4a1010b6a5c7ba6b00d2c452c4db8f089. Merge remote first, then main,
retaining both parent content in index/log conflicts. Never amend, rebase or
edit historical RPI artifacts. Verify ancestry and main-only changes survive,
including runner additions and trusted score baseline.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Enforce actual resource bounds

C1/C2: download uses offset=0, length=MAX_BLOB+1 and existing timeout;
overflow/changed size is refused. Fake must slice before returning and
capture range; controller test proves finally cleanup after a replaced blob.

Paging should account for exact compact bytes: validate initial head; each
item must fit a complete items-only wrapper; adding an item includes correct
comma overhead. Start a new page only when the current complete page would
overflow, refuse >64 and validate every serialized page before returning.
Do not silently discard empty head page or items. Cover exact limit, one
byte over, reviewer intermediate-page example, oversized head, escaping,
Unicode and many-page round-trip using existing ownership/limits in plan.
Validation: old behavior demonstrably fails new regressions before fix;
after correction run existing codec/controller and infra discovery.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Current operations and truthful handoff

C3/W3/W4: active setup instructions at infra/README.md must not require
source-job tags or removed includeResultRelay. Show restart-only false
and separately approved Blob true with storageAccountName and container-first
order. Correct cleanup: exact transient job is deleted; ciphertext expires
by lifecycle, 30-day soft delete retained, no automatic Blob/tag deletion.
Clearly preserve explicitly dated 2026-10-17/19 receipts as history.
Add a local proposed PR body with historical run9 and explicit pre-gate/as-of
status; no gh pr edit. The final gate outcome belongs to the separate external
handoff specified in P02-T03. Add focused KB navigation and append-only log entry.

<!-- rpi:phase id=P02 -->
## P02: Validate and hand off

<!-- rpi:task id=P02-T01 -->
### P02-T01: Actual local evidence

All heavy checks require the shared lock. From src/api run:

Execution complete: requested API suite 1379 tests / 320 opt-in skips;
Ruff/format/mypy pass; actual local synthetic app/Chromium has 32 passing
assertions. Infra initially lacked PyYAML; after observed-prerequisite pip
restoration, 505 tests pass with zero skips, transport Ruff/format/mypy pass,
and strict rubric adapter/preflight tests pass 51/51. Gate-runner tests pass
35/35. External logs preserve initial adverse outcomes. No web runtime file
changed, so refreshed guidelines have no changed web file to assess.

Before any application script, verify interpreter identity plus required
installed-distribution metadata and editable project paths in the selected
environment. Source imports alone do not prove installation. An actual missing
package result authorizes pip restoration with existing pins, then repeat
the metadata preflight before the following commands.

```bash
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q
ruff check .
ruff format --check .
mypy
```

Use existing tools first; actual missing import/tool failures justify pip
restoration in an external task-owned environment. Keep caches external.
Run infra discovery with installed src packages and offline Bicep only;
run transport Ruff/format/mypy and exact scorecard adapter regressions.
Run existing local design_system_browser_check, which constructs synthetic
data, starts loopback app, checks readiness, uses Chromium/Playwright and
stops its owned app. No actual/live account or model. No changed web runtime
files expected; loaded current guidelines remain applicable if this changes.
Record exits/skips without turning synthetic checks into WCAG acceptance.

<!-- rpi:task id=P02-T02 -->
### P02-T02: One Review

Reconcile all task statuses, actual commands, changes and exceptions.
Independent worker activates rpi-review, reads exact corrected boundary,
writes only its review artifact. Original verdict retained; no repeated Review.

Execution: one independent Review Complete / Residual work, no implementation
defect. Original artifact retained at
.copilot-tracking/reviews/logs/2026-10-30/pr423-review-corrections-review.md.
RV-001/002/003 route existing publication, hosted and live/human dependencies.

<!-- rpi:task id=P02-T03 -->
### P02-T03: Commit and final receipt

Use gh api user for id/login; repository-local noreply email for author and
committer. Commit reviewed implementation and all dated evidence with trailer.
Fetch main; full tools/rpi-checks.py --all --base d986c4c4 --out a new
external directory uses the existing internal flock with 600-second wait.
Do not double-lock. Verify successful receipt; changed base or missing
prerequisite blocks publication. If no receipt succeeds, retain actual
failure external and record unmet AC7 without fabricated status.
No push or remote PR edit.

During local validation, a fresh fetch found origin/main advanced to f168d079
through #592/#590. Read-only merge-tree is clean; d986c4c4 remains the explicitly
requested and implemented baseline. Preserve this distinction and attempt the
final gate without bypassing its current-main-ancestry refusal. Coordinator
owns later-main reconciliation and a new receipt; no new-base claim is made.

After gate execution, write
/home/azureuser/.copilot/session-state/666870ea-9fdc-4d82-bc74-faa18580ce61/files/pr423-final-handoff.json
with full HEAD/tree/base, gate/verification exit status, receipt and log paths,
clean status and coordinator's remaining exact-head/hosted/human gates.
Do not edit committed evidence/body/state after a successful gate. If tracked
changes are necessary, commit them and rerun a fresh complete gate. Original
pre-commit Review is never promoted to post-gate publication assessment.
