---
title: Issue 115 digest anchor PR description
description: Publication content for the bounded source correction
ms.date: 2026-10-18
---

## Summary

Refs #115

**Correction ONE after coordinator NOT ACCEPTED:** one Medium tightly coupled
false green was found on prior head bbb13521dcdd8d7a760324619fc0f8f612f08ad6:
prefix-only objects could count as anchors without meaningful payloads.
Qualification now enforces existing publisher filename/count/year and required
main/SHA-256/count/head/year/first_prev invariants. Malformed candidates return
fixed invalid-anchor problems and ALERT/exit1, never OK, even beside valid anchors.
No remote object names/content are printed, no blob overwrite/delete.

Failing-first:3 methods yielded112 assertion failures/30 malformed-data errors
against unchanged source; exact base and prior-head CLI false green independently
replayed as implementation probes. After correction25 focused/coupled and44
orchestrator tests pass, zero skips; configured Ruff/format/mypy pass. Existing
head/year/unrelated/truncation/rewrite/sealed-year/create-only controls pass.
This is implementation evidence, NOT independent acceptance. Same coordinator
must follow up on corrected exact head. One of maximum two correction cycles
used; no new/amended original Review. Full commands/errors/results/source/log
hashes: `.copilot-tracking/changes/2026-10-18/issue-115-digest-anchor-correction-one.md`
and five adjacent correction-one logs.

Reject remote verification when there are no recognized head or year digest
anchors, even if the container lists unrelated JSON. The report explicitly
identifies missing anchors; the injected CLI returns1/LEDGER_DIGEST_ALERT and
never LEDGER_DIGEST_OK. Preserve valid head OR sealed-year behavior and
unrelated-blob neutrality. No new storage adapter, schema, policy or schedule.

Exact base: `c803614e8ca7c604e509f1c088f8b8f90f3063ef` (merged PR #403).
Source candidate: `d53a7c68245dc708c628bb37853c308d9811fcbe`.
Delivery head is appended from the actual published Git/PR metadata below;
Initial delivery commits contained evidence/state only; correction ONE now
changes the same three orchestrator source/test/guide paths as recorded above.
No explicit issue dependencies; parent #114 is hierarchy, not ordering.
The issue's local-only delivery statement is stale: remote publish/read-back
already exists. This PR does not establish whole #115/#114 acceptance.

## Ordered RPI and Independent Evidence

Research executed Wider -> Deeper -> Contrarian, Ready. Plan executed with one
independent critique: Complete / Revise, one Medium PC-001. Its compatible
task-owned TMPDIR correction was adopted; original remains byte-exact.
Implementation ran failing-first -> minimal guard/README -> passing local gates.
Historical one original independent Review: Complete / Residual work; bounded source
Conformant, no implementation defects at that assessment. Coordinator later
returned NOT ACCEPTED as recorded above. Correction ONE used, no second
critique or original Review; originals remain byte-exact.

Original critique SHA-256:
`d1add2a5642689cb9a615f3aaa989871a3b405f7f5cab076689fdcc0110314e0`.
Original Review SHA-256:
`dc72719806ba648af00d34c9ef6b0c0d049ed87372d60ee49e959b328694186e`.

## Historical Initial Local Validation

All fixture tests used sanitized env, explicit worktree TMPDIR and installed
src distributions, existing FakeImmutableContainer with env={} transport,
no inherited cloud credentials or private inputs.

* Before production edit:17 tests/four expected behavioral failures, zero
  errors/skips; only-unrelated CLI returned0 rather than1. Source matched base.
* After:21 focused/coupled tests and40 full orchestrator discovery tests passed,
  zero skips. Eight new methods, zero removals; fake and prior nine tests unchanged.
* Configured Ruff0.17.1 check/format and mypy2.4.0 passed; digest files retain
  pre-existing format/type exemptions, not strict coverage.
* Independent Review reran21/40, quality and exact-base failure replay; additional
  CLI/report and prior-test/fake preservation checks passed.
* git diff --check passed after stripping only two trailing spaces in captured
  unittest progress output. Raw/normalized receipt hashes are disclosed.

Commands from root:

```bash
env -i PATH=/usr/bin:/bin TMPDIR=/home/azureuser/source/ama-wt/issue-115-digest/.digest-anchor-tmp PYTHONPATH=src/core/tests:src/orchestrator/tests <task-venv>/bin/python -m unittest test_digest_blob test_recovery.YearLedgerTests -v
```

From src/orchestrator:

```bash
env -i PATH=/usr/bin:/bin TMPDIR=/home/azureuser/source/ama-wt/issue-115-digest/.digest-anchor-tmp PYTHONPATH=../core/tests <task-venv>/bin/python -m unittest discover -s tests -v
<task-venv>/bin/ruff check . && <task-venv>/bin/ruff format --check . && <task-venv>/bin/mypy
```

`<task-venv>` is
`/home/azureuser/.copilot/session-state/afd14196-e65e-4c89-b2cb-12c95fe860b4/files/digest-venv`.
Exact commands/results/errors/skips/source hashes and stdout receipts are in the
changes artifact and four adjacent logs. Initial system validation lacked local
packages/Ruff/mypy; only after that actual failure were editable src packages
and configured dev tools installed with pip in the task-owned venv.
Reviewer shell rg was unavailable; direct reads completed the same assessment.

## Artifact Set

* Research: `.copilot-tracking/research/2026-10-18/issue-115-digest-anchor-research.md`
* Plan: `.copilot-tracking/plans/2026-10-18/issue-115-digest-anchor-plan.md`
* Details: `.copilot-tracking/details/2026-10-18/issue-115-digest-anchor-phase-details.md`
* Original critique: `.copilot-tracking/reviews/plans/2026-10-18/issue-115-digest-anchor-plan-critique.md`
* Changes/commands/hash receipts: `.copilot-tracking/changes/2026-10-18/issue-115-digest-anchor-changes.md`
* Original Review: `.copilot-tracking/reviews/logs/2026-10-18/issue-115-digest-anchor-review.md`
* State: `.copilot-tracking/rpi-sessions/2026-10-18/issue-115-digest-anchor-state.json`

## Limits and Unmet Gates

RV-001 routes publication and coordinator complete independent exact-final-head
review. RV-002 retention duration and actual irreversible lock approval/evidence,
RV-003 real hosted scheduler/log contract/alert delivery/missing-run/recovery
acceptance and RV-004 second-human first-publication historical reconciliation
remain unmet distinct follow-ups. No retention period or lock authority inferred.
An anchored prefix/year does not independently anchor all later/local state.
An explicit zero-count GENESIS remote head retains narrow existing empty-ledger
behavior; this is not digest-schema validation or proof of prior authenticity.

SQL Server, Docker, browser and Azure validation N/A/not run for this bounded
offline source delta; the coupled SQLite unit is not external SQL/recovery
acceptance. No SQL/Docker/infra/IAM/Graph/retention-policy change, service,
deployment, spending, production/private dataset access or irreversible action.
No new mvp, loadcheck, web/KB inventory changes or issue/board/check-box updates.
Do not merge: stop for SAME coordinator corrected-exact-head follow-up.

## Actual Publication

PR404 is OPEN at https://github.com/jmservera/ama/pull/404, targeting main.
Initial publication head: `211458f94c25a705971b0f912b1990f0b8de7aec`.
Main remained the pinned base before/after that push. Initial final receipt-only commit
reconciles delivery and stopped state without changing source or frozen originals.
Exact final head is appended from live Git/PR metadata below. Hosted checks are
not presumed passed; coordinator complete independent exact-head review remains
required. Correction ONE supersedes those initial source bytes; all original assessments
remain frozen. No merge or issue closure.

Correction ONE source commit:
`d0088301ba64cba8c632b6d0b4dcd80474580e41`, normally pushed to same branch.
Final receipt-only commit updates actual publication/handoff without changing
those corrected source bytes. Exact corrected final head appended from live Git
metadata below. STOPPED for SAME coordinator, no artificial independent Pass.
