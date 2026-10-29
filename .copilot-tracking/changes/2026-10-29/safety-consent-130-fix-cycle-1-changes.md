---
title: Issue 130 PR 509 fix cycle 1 changes
description: Regression, implementation, validation and local completion evidence
ms.date: 2026-10-29
---

Task ID: issue-130-pr-509-fix-cycle-1. Refs #130, PR #509.
Declared implementation scope: full plan, with P03 review/commit coordinated
after implementation handoff.

## Initial Boundary

Clean worktree, branch docs/safety-consent-130, matching open PR #509.
git pull --rebase returned Already up to date at ebcc0a16.
No prior source changes were present. Existing historical artifacts retained.
User authorizes local source fixes, constructed tests, RPI evidence and commit,
not push, Azure or operational activation. latest.json is not hand-edited.

## Plan and Critique

Plan/details use safety-consent-130-fix-cycle-1 under dated 2026-10-29 folders.
One independent critique Complete / Revise, original preserved. PC-001 led
to UUID IDs instead of incomplete legacy counter recovery; PC-002/003 resolved
by removing deletion changes. PC-004 rejected: unsupported worker-only /tmp
restriction, contrary to explicit user /tmp/mv selection and available tools.
No significant unresolved user decision or additional critique.

## P01: Regression and Implementation

P01-T01 complete: three new shared JSON/SQLite regression methods; existing
core/API correction fixtures use returned identifiers. No methods removed.
Before runtime edits, the six explicit JsonResidentDecisions and
SqlResidentDecisions selectors for test_tenure_intake_preserves_accepted_status_and_heuristic_priority,
test_nomination_identity_survives_retention_deletion_and_failed_intake, and
test_nomination_identity_after_legacy_deletion_without_high_water_mark all
failed (6 tests, 0.689s, exit 1). Tenure returned Not recorded instead of
Accepted; both deletion scenarios reused NOM-1 on each backend.
Command prefix: cd src/core &&
PYTHONPATH=src:tests:../agents/src:../agents/tests /tmp/mv/bin/python -m unittest -v.

P01-T02 complete: the private _resident_decision_gate holds the original
non-tenure validation unchanged. resident_gate retains its tenure fast-path;
resident_status delegates to decision validation only. Nomination creation uses
NOM- plus full uuid4 hex, with existing id/version correction lookup unchanged.
No deletion or retention metadata changes. Existing intake README documents
opaque IDs and decision/readiness separation. P01 complete.

## P02: Validation

Tools verified: /tmp/mv Python 3.12.3, Ruff 0.17.1, mypy 2.4.0.
Installed editable packages point to another worktree, so commands will
explicitly select this worktree's src and test directories via PYTHONPATH.
No shared venv mutation or dependency installation is needed.

All commands below exited 0 from this worktree:

```bash
cd src/core
PYTHONPATH=src:tests:../agents/src:../agents/tests /tmp/mv/bin/python -m unittest -v \
  test_resident_decisions.JsonResidentDecisions.test_tenure_intake_preserves_accepted_status_and_heuristic_priority \
  test_resident_decisions.SqlResidentDecisions.test_tenure_intake_preserves_accepted_status_and_heuristic_priority \
  test_resident_decisions.JsonResidentDecisions.test_nomination_identity_survives_retention_deletion_and_failed_intake \
  test_resident_decisions.SqlResidentDecisions.test_nomination_identity_survives_retention_deletion_and_failed_intake \
  test_resident_decisions.JsonResidentDecisions.test_nomination_identity_after_legacy_deletion_without_high_water_mark \
  test_resident_decisions.SqlResidentDecisions.test_nomination_identity_after_legacy_deletion_without_high_water_mark
/tmp/mv/bin/ruff check .
/tmp/mv/bin/ruff format --check .
/tmp/mv/bin/mypy
PYTHONPATH=src:tests:../agents/src:../agents/tests /tmp/mv/bin/python -m unittest -q \
  test_resident_decisions test_hazard_referral test_consultation_controls \
  test_quality_procurement test_dependency_rule
PYTHONPATH=../api:../api/src:../api/tests:src:tests:../agents/src:../agents/tests \
  /tmp/mv/bin/python -m unittest -q test_resident_api
cd ../api
/tmp/mv/bin/ruff check tests/test_resident_api.py
/tmp/mv/bin/ruff format --check tests/test_resident_api.py
/tmp/mv/bin/mypy tests/test_resident_api.py
```

| Check | Result |
| --- | --- |
| Six new regression selectors | 6 tests, OK, no skips, 0.893s |
| Complete core Ruff | All checks passed |
| Complete core formatting | 110 files already formatted |
| Complete core mypy | No issues in 163 source files |
| Five core modules | 384 tests, OK, 90 skipped, 65.216s |
| Resident API module | 16 tests, OK, 1 skipped, 17.792s |
| Changed API test Ruff/format/mypy | Pass; 1 formatted file; no issues in 1 source file |
| git diff --check | Pass |

Core skips are existing opt-in Azure/owned-loopback MSSQL and JSON-vs-SQL
backend-specific non-applicable tests; none is acceptance evidence. The
inherited new MSSQL selectors remain skipped, not represented as executed SQL
Server coverage. The API skip is its existing opt-in Azure path. Expected
injected recovery-error traces and missing synthetic law-store warnings were
emitted by passing existing tests; law readiness remains Unknown, not a pass.
Module-origin probe resolved resident_decisions.py under this worktree's core
source and this worktree's agents source first on the namespace path.

P02-T01/T02 complete: code, markers, details and evidence reconcile; no required
check failed after the source fix. P02 complete. No new implementation
divergence beyond the recorded pre-implementation UUID plan amendment.

## Amendments and Divergences

Planning amendment before implementation: full UUID-based opaque IDs supersede
the initial cumulative counter. This handles pre-existing deletions without
inventing a recovered high-water mark, new retained metadata or deletion
transaction guarantees. Existing legacy IDs remain addressable.

## Remaining Work and Limits

Local commit pending. Independent Review complete; no post-Review source
changes. No material source finding or failed required check blocks this local
candidate. Publication remains outside scope.
No full publication gate, SQL Server, Azure, real model, browser, participant,
human approval or hosted check is claimed. Existing issue criteria stay open.

## P03 Review Handoff

Assess working candidate based on ebcc0a16, exactly these four changed tracked
files: core resident_decisions.py, shared core resident test, core README and
one API fixture. Dated current-task artifacts are new; all historical evidence
is untouched. Fresh reviewer may write only the dated review record. Remaining
parent actions are P03-T01 outcome reconciliation and P03-T02 local commit.
Publication and exact-final-commit independent assessment are not claimed.

## P03: Independent Review and Local Commit

P03-T01 complete: exactly one independent Review at
.copilot-tracking/reviews/logs/2026-10-29/safety-consent-130-fix-cycle-1-review.md.
Execution Complete; outcome Conformant with justified divergence; zero
substantive RV findings or Review blockers. UUID amendment is justified and
consistent with user intent. Assessment boundary is the four-file working
candidate against ebcc0a16, not the later final committed head.

Authenticated GitHub identity resolved with gh api user: login jmservera,
id 8036360. Required local noreply address:
8036360+jmservera@users.noreply.github.com, to be configured repository-locally
and supplied to both author and committer. Local commit and final evidence
reconciliation remain P03-T02. No push.
