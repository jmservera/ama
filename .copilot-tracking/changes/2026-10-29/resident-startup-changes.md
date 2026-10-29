---
title: Resident image startup diagnosis changes
description: Local-only SQL compatibility diagnosis and regression evidence
ms.date: 2026-10-29
---

## Execution Boundary

* Task ID: f568fbf4-e1b7-45d5-ae08-d7034d24a85b; slug resident-startup.
* Scope: full plan, Research -> Plan -> Implement -> Review; local commit only.
* Branch: fix/resident-startup from origin/main d70ee60ab3d7346a9991cf64382d9985f4d09f2e.
* Research: .copilot-tracking/research/2026-10-29/resident-startup-research.md.
* Plan: .copilot-tracking/plans/2026-10-29/resident-startup-plan.md.
* Details: .copilot-tracking/details/2026-10-29/resident-startup-phase-details.md.
* Original critique: Complete / Revise, PC-001 unsupported /tmp restriction
  rejected with explicit repository-required lock evidence; no second critique.
* Constraints: no az, Azure access/mutations, .env, secret/private data reads, real
  cloud SQL, paid models, push, PR or merge.

## Diagnosis

The unmodified main resident image imports and validates all ten app-style
setting names. With constructed MSI values and network none, it reaches SQL
authentication, not missing configuration. With the actual pre-#525 SQL view
on a task-owned local SQL Server it exits 2 before binding: ProgrammingError,
`Invalid column name 'documents_json'`. Applying only the current SQL template
makes that same image/settings serve health 200 on 0.0.0.0:8089, shell 200,
unsigned view 401, wrong Host 403; image HTTP healthcheck command returns 200.
No new mandatory chat/agenda/model setting and no production-code defect found.

This is a demonstrated sufficient LOCAL failure mode, not a claim that the
unavailable Azure console or uninspected live view proves historical causality.
No rollout or live schema remedy was performed.

## P01: Startup Prerequisite and Regression

P01-T01/P01-T02 complete: src/api/README.md diagnosis/order guidance and one
existing-harness real SQL compatibility regression in
src/core/tests/test_resident_showcase_sql.py. It temporarily renames the
document projection, checks actual driver failure on both SELECT paths,
restores the rendered current template in finally, and verifies both reader
output and restricted-principal SELECT. No runtime fallback/grant change.
Ruff formatted the one test file; git diff --check passed.

## P02: Validation and Review

P02-T01 complete. Commands used the external isolated venv's Python. From each
project: `python -m ruff check .`, `python -m ruff format --check .`,
`python -m mypy --cache-dir <external-project-cache>` all exit0.
Core mypy157 source files; API106; format104/56 files respectively.

| Existing suite / check | Actual result |
| --- | --- |
| core `python -m unittest discover -s tests -p 'test_resident*.py' -v` | exit0,306 tests,88 opt-in integration skips |
| api same resident discovery, `PYTHONPATH=../core/tests:../agents/tests` | exit0,135 tests,7 opt-in SQL/browser skips |
| each project's `python -m unittest tests.test_dependency_rule -q` | exit0,2 tests each, no skips |
| core `ZF_TEST_MSSQL=1 python -m unittest tests.test_resident_showcase_sql -v` | exit0,34 tests, no skips, actual owned loopback SQL |
| api `python -m checks.resident_demo_image_check` | exit0,22 assertions; image built and real service/login paths exercised |
| `git diff --check` | exit0 |

General-discovery SQL/Azure/browser skips remain explicit; they are not full
integration passes. The relevant entire SQL module, including the new
regression, was separately executed with zero skips. Image check verifies
non-root/read-only/cap-drop startup, missing/expired config refusals, correct
Host, unsigned/forged-session denial, wrong-password refusal and synthetic
login/own-home isolation. Same-main comparison separately verifies port8089
and old/current view causality; the image contract uses its existing free port.

Shared nonblocking heavy admission succeeded, no foreign holder was bypassed.
All owned SQL/app/check containers were removed, as was the existing image
check's owned image. Diagnostic baseline image retained for evidence.
Sanitized portable observations and external log hashes:
.copilot-tracking/changes/2026-10-29/resident-startup-evidence.json.

## Pre-Review Reconciliation

P01/P01-T01/P01-T02 and P02-T01 complete in plan/details. No remaining source
implementation or local validation blocker. P02-T02 remains open for its
original independent Review and local commit only. Full publication gate,
actual Azure causality and owner/hosted approval remain explicitly unperformed.
No significant divergence or unresolved user-owned decision. Ready for one
Review of this local diagnosis/documentation/regression boundary.

## Original Independent Review

Single independent Review executed Complete / Conformant, zero substantive
findings, at
.copilot-tracking/reviews/logs/2026-10-29/resident-startup-review.md.
Reviewer checked scoped source and all eight external evidence hashes without
duplicating heavy execution. Original critique and Review are unchanged.
No second Review or post-Review source correction.

Implementation/evidence local commit is the remaining P02-T02 action.
Authenticated GitHub account resolved read-only as jmservera, id8036360;
use its repository-local privacy-safe noreply address for author/committer.
No Azure command, push or publication acceptance is part of closeout.

## Final Local Handoff

Reviewed implementation and all original RPI evidence committed locally as
c2c57127ea077d144ff07e10378ab6ea5208e258. Author and committer use the freshly
resolved GitHub account's repository-local noreply address; exact mandated
Copilot trailer verified. Worktree clean immediately after that commit.
This final plan/details/state reconciliation is a separate status-only local
commit, not an amend. The research question table now mirrors the already
recorded locally answered disposition; no new research or Review was performed.

All P01/P02 markers complete. Task completed; automatic session remains running
at Follow-up with no child selected. No push, az command, Azure change, .env,
secret/private-data read, full publication receipt or live readiness claim.
The deployment prerequisite is documented, not applied to Azure. Original
critique and Review remain unchanged; Review Complete / Conformant does not
prove historical cloud causality or approve a rollout.

Ranked residual work: first obtain separate authority for live SQL/view,
identity/secretRef verification before any retry (highest blocker-removal
value); second correct the prior local rollout executor serialization/deadline
findings (engineering-quality leverage). No further discovery or child task
started. Stop/manual-mode choices remain available in state; no choice inferred.

## Amendments and Divergences

No material divergence: investigation found a deployment SQL prerequisite
rather than a demonstrated runtime bug. Document the required compatibility
update instead of inventing a setting or masking missing document facts.

Original external probe harness port error retained separately, corrected
before the causal comparison; see research. Isolated dev dependencies installed
only after actual missing ruff/mypy errors, using existing pinned manifests.

## Evidence Storage and Publication

External root:
/home/azureuser/.copilot/session-state/f568fbf4-e1b7-45d5-ae08-d7034d24a85b/files/.
Raw local-only logs/probe scripts retained there; constructed values only.
Dated source/artifacts will be committed, but no external full publication
gate/receipt, Azure readiness, hosted/human approval or push is claimed.
Full gate uses prohibited az commands; publication remains separately gated.

## Follow-Up Items

* Separately authorized live view/auth/secretRef confirmation and SQL-before-image retry planning.
* Existing rollout executor secretRef/deadline findings remain separate work.
