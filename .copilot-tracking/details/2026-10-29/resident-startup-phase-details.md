---
title: Resident startup phase details
description: Scoped documentation, SQL compatibility regression and local validation
ms.date: 2026-10-29
---

## Metadata

* Task ID: f568fbf4-e1b7-45d5-ae08-d7034d24a85b
* Task slug: resident-startup
* Plan: .copilot-tracking/plans/2026-10-29/resident-startup-plan.md
* Research: .copilot-tracking/research/2026-10-29/resident-startup-research.md

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01, P01-T02 |
| P02 | Complete | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Preserve startup prerequisite

Context: pre-#525 view lacks documents_json, which the reader selects before
HTTP binding. The same main container serves when only the local view changes.
Scope: documentation and one regression, no runtime fallback or grant change.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Document SQL-before-image ordering and local diagnosis limits

Target src/api/README.md near resident deployment/configuration guidance.
State missing column versus empty/unknown document data, SQL SELECT-before-bind,
same port 8089 and Host-aware health probe. No new mandatory chat setting;
optional agenda is not an activation remedy. A qualified operator must review
the current existing SQL boundary via the established separately approved
process before any image retry. No command in this task may invoke az/live apply.
Completion: precise documentation checked against source and local evidence.

Completion evidence: src/api/README.md now has a startup compatibility section,
linking the existing separately authorized SQL process, distinguishing local
causality and optional settings, preserving port/Host-aware probe behavior.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add SQL compatibility regression

Target existing SqlBoundaryTests in src/core/tests/test_resident_showcase_sql.py.
Use its constructed case and own database. Alter only the task-owned test view
so documents_json is absent; assert actual driver refusal, not empty output.
Restore using current script.render in finally before any later test can run.
Then assert reader output and restricted principal SELECT still work, while
existing permission tests cover denial of base/write rights. No dependency or
fixture duplication. Maximum one new test, no removals.

Completion evidence: one new SqlBoundaryTests method temporarily renames the
document projection, asserts driver rejection for list and single-case reads,
restores the current rendered template in finally, and checks restored reader
and restricted-principal projection output.

<!-- rpi:phase id=P02 -->
## P02: Validate and review

<!-- rpi:task id=P02-T01 -->
### P02-T01: Execute static, unit, real SQL and image checks

Use external venv at
/home/azureuser/.copilot/session-state/f568fbf4-e1b7-45d5-ae08-d7034d24a85b/files/venv.
Run core/API ruff check/format and mypy with existing project configurations.
Run resident-related core and API unit suites and dependency boundaries using
documented cross-project test fixture paths. Opt-in SQL suite must actually
run against an owned loopback container with constructed dummy credentials.
Run existing resident_demo_image_check against that container to cover real
image refusal, health, host/session and login paths. Use shared heavy lock
nonblocking; do not interrupt a foreign holder or inspect foreign output.
Record exact results and cleanup, including any genuine skips/blockers.

Original critique PC-001 is rejected for its unsupported /tmp prohibition.
Repository-authorized actual admission mechanism is nonblocking
`flock -n -E 75 /tmp/ama-rpi-heavy.lock`; already successfully used for research.
Use it without replacing the lock or interrupting a foreign holder. A busy
lock blocks heavy validation rather than authorizing bypass.

Completion evidence: both projects' full ruff lint/format and mypy passed;
resident discovery core306/88 skipped, API135/7 skipped; dependency suites2+2;
real opted-in resident showcase SQL34/0 skipped; existing resident image check
passed all22 assertions. General discovery skips are opt-in integration checks,
not inferred passes; relevant SQL module was executed separately without skips.
Owned containers removed. Sanitized durable results and external log hashes:
.copilot-tracking/changes/2026-10-29/resident-startup-evidence.json.

Pre-Review reconciliation: P01 complete and P02-T01 complete; P02-T02 remains
the intended original Review and local commit. No source work or validation
blocker remains inside the authorized local scope.

<!-- rpi:task id=P02-T02 -->
### P02-T02: One independent Review and local commit

Reconcile P01 completion and P02 validation into changes/state before Review.
Fresh reviewer activates rpi-review, reads scoped diff/evidence, writes only
.copilot-tracking/reviews/logs/2026-10-29/resident-startup-review.md.
No follow-on source corrections inside this task after that single Review.
Record outcome independently of execution status; route findings later.
Resolve gh api user (not Azure) for local privacy-safe identity; stage intended
files and commit with exact mandated trailer. Do not amend/push/open PR.
Full publication gate, Azure causality and owner approval remain outside this
local completion, not claimed.

Completion evidence: original independent Review Complete / Conformant, no
substantive findings. Reviewed implementation/original evidence committed as
c2c57127ea077d144ff07e10378ab6ea5208e258; author/committer privacy-safe identity
and mandated trailer verified, worktree clean immediately afterward. Final
tracking reconciliation is a separate status-only local commit, not an amend.
P01/P02 fully complete; no post-Review source correction, second Review or push.
