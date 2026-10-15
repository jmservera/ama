---
title: Issue 176 src determinism implementation review
description: One-pass comparison of engineering evidence and remaining issue acceptance
ms.date: 2026-10-15
---

## Opening Review State

Review goal: assess the implemented src reproducibility and protected-refresh
slice once, without claiming all issue acceptance. Task #176, slug
issue-176-src-determinism; automatic parent orchestration.
Evidence ready: research, plan, phase details, independent critique and
implementation commands/results. P01/P02 complete, P03 delivery pending.
Acceptance basis: bounded plan requirements plus issue's three original ACs.
First comparison boundary: source behavior versus deterministic/date/refresh
contracts, followed by validation and disclosed limitations.
Read-only scope: source and evidence; writes only to this review record.
No initial blocker to reviewing the bounded engineering slice.

## Compared Artifacts

* .copilot-tracking/research/2026-10-15/issue-176-src-determinism-research.md
* .copilot-tracking/plans/2026-10-15/issue-176-src-determinism-plan.md
* .copilot-tracking/details/2026-10-15/issue-176-src-determinism-phase-details.md
* .copilot-tracking/reviews/2026-10-15/issue-176-src-determinism-critique.md
* .copilot-tracking/changes/2026-10-15/issue-176-src-determinism-changes.md
* src/core/src/zava_forward/core/synthetic/provenance.py
* src/core/src/zava_forward/core/synthetic/scale_fixture.py
* src/core/src/zava_forward/core/synthetic/sensor_backfill.py
* src/core/tests/test_synthetic_determinism.py
* src/agents/evals/registry.json, core README and reference synthesis/index/log

## Execution and Outcome

Review execution: Complete. Outcome: Residual work.
The bounded src engineering slice meets its plan; issue #176 as a whole is
not accepted/closed. No in-scope blocking defect found in this comparison.
No second critique or post-implementation Review was executed or requested.

## Plan and Implementation Comparison

| Boundary | Assessment | Evidence |
| --- | --- | --- |
| P01-T01 source revision and parameters | Satisfied | Length-delimited stable source basenames/bytes; both manifests record seed/version/as-of/revision; sensor includes scale dependencies |
| P01-T01 exact output hashing | Satisfied | Every non-manifest file, including estimate/register/shards, hashed by streaming file_digest; existing aggregate hashes retained |
| P01-T01 explicit sensor date | Satisfied | Half-open UTC window resolved before output creation, passed into estimate/outdoor/readings; omitted date preserves existing START even for custom days |
| P01-T01 safe refresh | Satisfied within declared non-concurrent scope | Nonempty/direct-symlink targets rejected, no force flag; stale shards cannot survive a refresh write; unchanged idempotent loader is not a reset path |
| P01-T02 byte-level tests | Satisfied | All output bytes/file sets compared, three sensor shards, seed/date sensitivity, pre-change payload digests, every dependency mutation |
| P01-T02 semantic coverage | Satisfied | Every reading timestamp within requested window/cadence, counts/hash metadata, historical-default date, estimator/CLI agreement, year-0001 ISO format and invalid-input preservation |
| P02-T01 docs/registry | Satisfied | Stale absent-sensor claim corrected; core recipes, proposed policy boundary, index and appended log; scale registry version synchronized |
| P02-T02 tests and local run | Satisfied locally, with explicit unavailable evidence | Five src suites, all lints/types; actual local process and synthetic data; actual model not configured, Docker denied |
| ADR 0006 / user boundaries | Satisfied | All new executable code/tests under src/core; core imports no workload; agents metadata only, no SQL/blob extras; no mvp/env/VS Code/issue-tracking edits |
| P03-T02 delivery | Pending parent action | Commit/push/PR explicitly authorized, not represented as already done |

## Critique and Implementation-Time Decisions

PC-001: typed writer/revision boundaries and strictly checked new helper/tests
resolve the new-test typing issue, with existing exemptions unchanged.
PC-002: source inventories include initializer/provenance/insights/scale,
plus sensor itself; mutation and path/order tests cover them.
PC-003: requested start reaches estimate and estimate-only CLI; recorded
estimate equals emitted estimate and CLI result.
PC-004: captured old payload hashes pass; default/custom-days dates preserved,
seed/date changes tested separately from scale metadata-only date changes.
PC-005: complete representable date-window validation precedes output prep;
invalid values preserve absent/empty destinations.
PC-006: no in-scope blocker found; unapproved/external evidence remains open
without a conformant issue-wide claim. No post-Review fix loop.

The minimum-year timestamp correction and registry synchronization preserve
approved intent and are recorded in changes/details; no material unapproved
scope revision, discarded test, new exemption or user decision occurred.
Plan P01/P02 markers and pending P03 handoff agree with implementation evidence.

## Validation Assessment

* Passed: core 268, agents 70, api 459 (92 skipped), orchestrator 17,
  importer 39; 853 total discovered, 761 non-skipped.
* Passed: seven new snapshot/semantic tests; five existing sensor loader tests;
  historical payload hashes; migrated support-generator regressions included
  in full core suite.
* Passed: ruff check, format check and mypy for all five projects; final core
  rerun after timestamp boundary correction passed 268 tests and strict gates.
* Passed: five distributions import as one five-path PEP 420 namespace;
  migration tool regressions pass 25 tests after missing-package restoration.
* Passed: 980-case generated local API, health/app/authenticated case routes,
  ZF_AI=on summary path; template result unapproved; no workflow/consent mutation.
* Initially failed then recovered: incorrect interpreter cwd, lint closure/
  line-length warnings, agents PYTHONPATH module collision, migration-test
  missing packages. All are recorded, not suppressed.
* Unavailable: Docker daemon permission denied; image builds/non-root/no-SQL
  or blob identity checks and SQL Server-backed cases rely on CI.
* Not run: actual Azure model or deployment, real climate/device integration,
  full-stock two-year sensor generation, private-register reproduction,
  human-approved refresh/reset. No such outcome is implied by local success.

## Findings and Routing

### RV-001 [Medium]: Private stock-register determinism remains unevidenced

Evidence: issue #176 AC1/AC2, research C2/C6, synthesis reproducibility table.
The private OSM-anchored register generator is absent; fictional scale rows
cannot stand in for it. Impact: neither whole-generator determinism nor
all-generator manifests can be accepted.
Destination: rpi-research, distinct follow-up owned by the project owner to
provide the original generator and immutable input snapshot/provenance, then
produce byte-level reproduction evidence. Do not invent private records.

### RV-002 [Medium]: Refresh defaults require owner acceptance

Evidence: issue AC3, synthesis "proposed defaults", no approval supplied.
Impact: code-level output protection is implemented, but does not approve
cadence, data owners, versioning or live reset authority.
Destination: rpi-plan / owner decision on cadence, approver, versioning,
retention of prior snapshots and scope of reset permission. All issue ACs
remain unchecked; existing live records and tenant bindings remain protected.

### RV-003 [Low]: Full-scale and external runtime evidence remains separate

Evidence: Docker probe, local app result, core sensor documentation and
declared P02 boundary. Small synthetic tests cannot prove billion-row storage
costs, actual Azure inference, image isolation or SQL Server execution.
Destination: distinct validation follow-up: CI for images/SQL Server; owner-
approved Azure model smoke and storage/cost decision for full-stock run.
No deployment or new inference spend is authorized by this record.

## Follow-Up Ranking and Parent Handoff

1. Owner refresh-policy decision (RV-002): lowest implementation effort,
   enables controlled future refreshes without fabricating approval.
2. Recover private stock-generator/input provenance (RV-001): highest
   remaining issue-specific acceptance value; needs unavailable owner evidence.
3. CI and authorized Azure/full-scale evidence (RV-003): platform quality
   leverage, but requires environment permissions/cost decisions.

Return to automatic parent for explicit topic-branch commit/push/PR, preserving
Refs #176 and residual-work outcome. No source changes or child task are
authorized by this handoff. Review findings must not become fake AC closure.
