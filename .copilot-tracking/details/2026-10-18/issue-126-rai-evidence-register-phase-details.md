---
title: Issue 126 RAI evidence register phase details
ms.date: 2026-10-18
---

Task ID 126; stable slug issue-126-rai-evidence-register. Status: P01/P02/P03
complete; PR #409 published. Scope and test budget unchanged. Sole original Review
Complete / Conformant for bounded engineering, no RV findings, correction count 0.
Final handoff metadata does not alter reviewed source or either original assessment.
Plan: .copilot-tracking/plans/2026-10-18/issue-126-rai-evidence-register-plan.md.

<!-- P01 -->
## P01: Core and API engineering

<!-- P01-T01 -->
### P01-T01: Failing-first tests

Extend test_governance.py with an isolated tiny public dataset fixture independent
of finance designations. Exercise JSON/SQLite plus opt-in UUID local MSSQL factory.
Inventory has literal expected 22 IDs, all open; read must leave bytes/audit/data
unchanged and detached. Reopen verifies exact server actor/time, event and revision.
Test distinct source/task/release changes, baseline replay, malformed claims,
unknown/promotional fields, unrelated/contractor/forged/removed/demoted actors.

<!-- P01-T02 -->
### P01-T02: Governance document

Keep all schema/logic in governance.py, no new service/module/table. Fixed original
baseline full commit and dates/status/verdict preserved. Closed primitive validators;
exact assessment is caller-declared context, never deployment attestation. Claims
record evidence_class constructed-fixture and verification unverified. Aggregate
disposition completeness counts distinct eligible finding IDs (maximum 22),
never closes findings. Separate history-record count may exceed 22. Eligibility
requires exact declared assessment and immutable baseline. Missing context yields
coverage Unknown; baseline source replay yields zero current coverage. Twenty-two
distinct supplied dispositions may be complete while adequacy remains insufficient,
acceptance Unknown and every finding Open. Test duplicate, all22 and stale contexts.

| Field | Required primitive and bound |
| --- | --- |
| finding_id | Exact inventory string |
| baseline_commit | Exact immutable full baseline commit |
| assessment | Exact five-key object; source_commit lowercase 40 hex |
| task_id/task_version/release_version | All nonblank strings <=200, reason null; OR all null and reason nonblank <=600 |
| evidence_tier | Exact five-value enum from plan |
| result / limitations | Nonblank string <=2000 / <=2000 |
| references | List of 1..20 nonblank strings, each <=500; no objects/fetch |
| decision_maker_status | Unknown, Unappointed, Unverified reference |
| decision_maker_ref | Null for Unknown/Unappointed; nonblank <=500 only for Unverified reference |
| event_ref | Nonblank string <=200 |
| expected_revision | Exact int >=0; bool refused |

No unknown keys, nested result objects, implicit string coercion or missing keys.
Test chosen limits and one beyond, wrong primitives, contradictory fields,
boolean/negative revisions. All supplied result text remains inert claim text.

Use outer refresh lock, _actor, existing manager roles, change_validation actor
guard, pending-audit snapshot. Append to governance.rai_claims only.
SqlStore.save immediate governance witness after COMMIT before other hooks and
refreshed snapshots; operation owns _discard with prior pending or empty when
committed. Suppress generic rollback/recovery when this witness says committed.
JSON restore best-effort in-process failure, no cross-file crash atomicity claim.

<!-- P01-T03 -->
### P01-T03: Existing API

Only GOVERNANCE_ACTIONS and governance GET/POST blocks may change in server.py.
GET optional assessment JSON parameter, reject unknown/repeated/invalid parameters.
POST evidence-record action; committed acknowledgement returns HTTP409 with
outcome committed and reload instruction. Serialize result before headers so
response-encoding failure is also reconciled. Existing other action behavior stays.
New API test file runs real local HTTP/login with explicitly constructed data.

<!-- P02 -->
## P02: Validation and documentation

<!-- P02-T01 -->
### P02-T01: Tests and parity

Selected original governance and assistant-release suites; new JSON/SQLite/adverse
tests. SQL inject audit failure after insert, changed document competing writer,
actor demotion between validation and BEGIN, recovery failure, postcommit ack.
Local MSSQL uses fresh task-owned container, loopback ephemeral port and per-test
UUID databases, random process-only credential, cleanup promptly, no secrets logged.
Run configured project Ruff/mypy and report actual failures, not imagined passes.

<!-- P02-T02 -->
### P02-T02: Hardened image

Build existing src/api/Dockerfile with src context. Run UID10001/read-only root,
tmpfs writable test/state paths, mounted only public tests/fixtures. Execute
focused governance and API HTTP tests against installed image distributions.

<!-- P02-T03 -->
### P02-T03: Supported docs

Update existing README missing-register statement to bounded engineering only.
Add dated current section without rewriting historical report or acceptance.
No memory edits; KB log append only. No new legal/currentness assertion.

<!-- P03 -->
## P03: Review and publish

<!-- P03-T01 -->
### P03-T01: One original Review

Use rpi-review once after implementation. Preserve original assessment artifact
bytes and hash. Findings route to coordinator, not another Review or hidden repair.
Correction count must remain zero. Reconcile test counts/skips and phase markers.

<!-- P03-T02 -->
### P03-T02: Publication

Resolve gh authenticated id/login and repo-local noreply email. Conventional commit
with required Copilot trailer. Normal push, main PR containing Refs #126 only.
Verify closingIssuesReferences empty, head/base and full changed inventory.
No issue updates, merge, rebase, board or acceptance checks.

## Same-Task Authorized Integration

The P03 publication constraints above describe the original loop. Subsequent
explicit coordinator authority permits only owned-topic rebase onto exact
`9403dc6a8f52f1f04c5ad910faab11a57c29ee78` and the specified old-head lease.
Integration is bookkeeping/validation, not another P01/P02/P03 or assessment.
Correction count stays 0. Original adverse critique and sole original Review
are byte-identical; no new assessment is substituted for either.

Full original30 patch parity, six-source-path parity, all nonowned upstream
bytes/modes and exact server/log additive unions were checked. No persistence
conflict or intent change. Fresh local tests cover governance JSON/SQLite,
ten actual HTTP cases, assistant release and consultation/procurement controls.
Configured formatter passes with existing exclusions; explicit excluded-file
diagnostics retain drift at both original and integrated source heads.
No generic formatting or exception changes. No SQL/image broad rerun; original
16 actual SQL cases and hardened image 107/16 skips remain historical.

Commands, raw outputs, hashes, full inventories and publication boundary:
.copilot-tracking/changes/2026-10-18/issue-126-rai-evidence-register-integration/receipt.md.
No human/live approval, role grant, closing action, issue/board or merge operation.
