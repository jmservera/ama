<!-- markdownlint-disable-file -->
---
description: Required fresh-development-install correction and exact-candidate publication evidence
ms.date: 2026-11-16
---

# RPI Changes: Agent observability publication

## Execution Status

* Task: agent-observability-publication.
* Declared scope: P04-T01 in the reused
  [.copilot-tracking/plans/2026-11-16/agent-observability-implementation-plan.md](../../plans/2026-11-16/agent-observability-implementation-plan.md),
  including accepted RV-001 correction.
* Status: Partial. P04 and P04-T01 remain unchecked.
* Original Review: Complete / Defects found, preserved unchanged after closeout.
* No second critique or Review phase; exact-head publication assessment remains required.

## Completed Work

* Research and plan reused: direct install metadata establishes the bounded
  correction. No new business requirement or architecture decision.
* RV-001 reproduced before correction: fresh agents environment installed with
  base core and agents[dev] fails importing telemetry_support with
  ModuleNotFoundError: opentelemetry.sdk. It contains no aggregate core-dev install.
* API development reuses core's telemetry extra; agents declares the same
  two pinned SDK/exporter packages directly in dev to retain its established
  single core-without-extras identity dependency guard. The first core-extra
  attempt failed that guard (1 of 79 tests), so it was corrected without
  weakening the test. Runtime locks and hosted/gate commands are unchanged.

## Validation Record

* Original aggregate-environment limitation reproduced before correction.
* Fresh agents install: 79 focused tests, strict mypy (57 source files) and
  pip check pass, including the unchanged core-without-extras guard.
* Separate fresh API install, with no core[dev]: 10 HTTP/composition tests,
  strict mypy (305 source files) and pip check pass.
* Full gate and hosted CI remain outstanding. New main includes previously
  accepted IoT work; integrate as authorized and validate the resulting head.
* Authorized merge completed at `4df29ff87c4cc72796bea21521b8d086ddbb2d78`,
  descending from current main `18d3de459f20018e91fab3af87ab0d89123661c6`.
* Clean external candidate full gate stopped in required Docker preflight:
  the isolated gate HOME selects `/var/run/docker.sock`, which this account
  cannot access. The existing user-owned rootless context works, but is not
  inherited by the canonical runner. No socket permissions, gate semantics,
  daemon configuration or shared services were changed.
* Failed receipt: `/var/tmp/ama-og-4fsxlE/run/receipt.json`. No full test matrix,
  successful receipt, implementation push/PR or hosted CI is claimed.
* Native capstone Build and Verify both pass on the merged candidate, retaining
  55 slides/notes, navigation, timing and protected cost evidence. Previously
  recorded diagram provenance failures still make delivery acceptance Partial.
* Owner reported Docker login restored. Explicit default-context recheck still
  fails socket permission before registry authentication; the existing rootless
  engine remains available. No unchanged full gate was rerun merely to repeat
  that failure. Owner direction is needed on supported rootless gate support
  versus restoring approved canonical socket access.
* Owner explicitly authorized the narrowly scoped, reviewed rootless gate fix.
  Plan D6 now requires explicit local-Unix `DOCKER_HOST`, matching subprocess
  and receipt identities, preserved environment isolation and no skipped checks.
  This changes gate semantics and retains the full validation tier.
* Implemented explicit local-Unix `DOCKER_HOST` in isolated subprocesses and
  Docker tool identity; the same endpoint is required to verify receipts.
  Default remains the rootful socket. Remote/malformed values fail explicitly;
  no caller Docker context, credentials or other environment are inherited.
* Added three focused regressions. All 106 gate tests and canonical Ruff/
  formatting checks pass with Python 3.12 on PATH. The bytecode smoke fixture's
  mocked installer now exposes installed third-party dependencies to its child
  through a path-only `.pth`; scratch source paths and no-bytecode assertions
  remain unchanged. This repairs the new mandatory public OTel API import.
* Real `docker --host unix:///run/user/1000/docker.sock version` succeeds.
  Full validation will use that explicit endpoint with a new exact candidate
  and receipt. Independent endpoint/receipt assessment remains pending.
* First rootless full gate passed tool preflight but agents failed 1 of 487
  tests: the existing direct-import authority guard lacked the newly introduced
  content-free telemetry module. Added only that module to its closed
  allowlist; forbidden store/SQL/consent imports remain rejected. Preserve this
  adverse run and rerun the corrected exact candidate; no failed receipt reuse.
* Corrected adapter guard plus existing focused worker tests: 101 pass in the
  separate agents development environment; affected-file Ruff/format pass.
* Completed adverse full run at `d7f976ff`: core fails its clock/UUID-free
  preview import probe; orchestrator fails its driverless `-S` command probe.
  Both share eager OTel context import, which creates random keys even when
  telemetry is disabled. Correct by deferring third-party imports and span
  contexts until telemetry is enabled, not by weakening either guard.
* Other failed-run blockers include exact opt-in skip accounting and source
  bytecode contamination. Current main `a612ba00` includes the owner-approved
  #1831 gate fixes for those; merged as already authorized. No failed receipt
  is promoted or reused, and all required SQL/browser/image groups still run.
* Disabled operations now use a null context and never import OTel; enabled
  paths retain real SDK spans/propagation. Observation methods and the SQL
  attribute call guard the absent span. Removed the earlier smoke-fixture
  dependency-path workaround because the root import defect is now corrected.
* After correction/main integration: core telemetry/diagnostic/determinism
  27 tests pass; driverless rescan 10 pass; focused worker 101 pass; actual API
  HTTP/assistant composition 10 pass; gate regression suite 111 pass.
  Strict mypy passes core 329, agents 57 and API 306 source files. A disabled
  SQL call initially exposed one missing null-span guard, now fixed and covered
  by both enabled and disabled API composition cases.
* Current-main skip accounting also accepts all three actual API discovery
  transcripts from the failed run. That targeted check is not execution of
  the now-required SQL/browser suites and is not full-gate acceptance.
* Second complete run at `ee8c8c61`, base `a612ba00`: 16 of 17 groups passed,
  including all five projects, browser, infra, migration and four image scans/
  contracts. MSSQL stopped before tests because `libltdl.so.7` was absent.
  Failed receipt remains `/var/tmp/ama-og-4fsxlE/final2/receipt.json`.
* Restored official Ubuntu `libltdl7` 2.5.4-9 only into the task-owned portable
  Python library prefix, using its existing ELF RPATH. No global installation,
  loader wrapper, gate-source change, credential inheritance or permission
  change. Exact isolated native SQL load/import now passes.
* A separately owned, heavy-lock-protected, loopback-only SQL Server diagnostic
  confirms native driver connection and a real query; its container was removed
  in finally. This is prerequisite proof, not the full required SQL suite.
* Main advanced to `4c3f1d13` (map-check readiness fix). Integrate as authorized
  and start an entirely new full run: native input/base changes invalidate reuse
  of the previous passing groups.

## Business Alignment

* None. Development extras correction preserves approved package/runtime intent.

## Remaining Work

* Reproduce RV-001, correct component development extras and run focused fresh
  tests/types. Commit original Review and correction, integrate current main
  as authorized, then validate a clean external candidate.
* Full gate, verified receipt, independent exact-head assessment, push/PR and
  observed hosted CI. No bypass or live activation.
