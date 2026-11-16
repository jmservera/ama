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

## Business Alignment

* None. Development extras correction preserves approved package/runtime intent.

## Remaining Work

* Reproduce RV-001, correct component development extras and run focused fresh
  tests/types. Commit original Review and correction, integrate current main
  as authorized, then validate a clean external candidate.
* Full gate, verified receipt, independent exact-head assessment, push/PR and
  observed hosted CI. No bypass or live activation.
