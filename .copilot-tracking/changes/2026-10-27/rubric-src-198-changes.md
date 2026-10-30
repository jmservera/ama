---
title: Rubric src cut-over changes
description: Issue 198 implementation and local validation record
ms.date: 2026-10-27
---

## Metadata

Task 198 / rubric-src-198. Full plan:
.copilot-tracking/plans/2026-10-27/rubric-src-198-plan.md.
Details: .copilot-tracking/details/2026-10-27/rubric-src-198-phase-details.md.

## Execution Status

Complete for full implementation plan: P01/P01-T01/P01-T02 and
P02/P02-T01/P02-T02. No remaining active implementation marker.
Write boundary: existing rubric tests, related documentation and
dated tracking artifacts. No production code, registry or workflow change.

## Validation Record

| Check | Result | Boundary |
| --- | --- | --- |
| Before: python3 -m pytest .github/rubric/scripts -q -ra | 18 failed, 355 passed, 7 skipped in 39.41s | Unchanged source at 09099ecd; seven seed failures, ten trigger/path assumptions, one unrelated deck mismatch |
| Real MCP runtime | Unavailable | GH_AW_RUNTIME_DIR absent; seven tests skip |
| Targeted repaired and new migration regressions | 31 passed, 95 deselected in 3.34s | Actual prepare/gate calls and parsed real YAML |
| After: python3 -m pytest .github/rubric/scripts -q -ra | 1 failed, 374 passed, 7 skipped in 42.04s | Sole failure unchanged: executive deck expected excluded but registry wildcard includes it |
| git diff --check | Passed | All changed source/docs |
| Added local Markdown links and anchors | Passed | Four changed durable documents, only added link destinations |
| Production byte invariants | Passed | Workflow Markdown/lock, registry, rubric and latest score unchanged |
| Append-only log prefix | Passed | Original bytes preserved exactly |

## Completed Work

### Stable fixture and current workflow contracts (P01-T01)

Existing gate tests use an explicit synthetic 66-point fixture independent of
latest.json. Prepare deletion test constructs all synthetic criterion scores,
recomputes metadata and checks a real two-point A2 drop, validation and drops.
Existing runtime workflow test asserts exact current event sets, src path
filter behavior and the infra workflow_run chain. No production YAML changed.
An initial 12-pass/1-fail targeted run caught a no-op baseline commit when
only A2 was reset to its existing 5; the full synthetic baseline fixes the
fixture rather than permitting empty commits. Final targeted checks pass.

### Retired paths and trusted registry (P01-T02)

Two added functions cover seven retired paths and the real temporary-Git
transition. A nonempty old fingerprint detects deleted legacy evidence under
the trusted base registry; after merge the new registry excludes it. Existing
src package/test/manifest/Dockerfile/web and vendor/data/build coverage passes.

### Durable guidance and sign-off ledger (P02-T01)

Updated .github/rubric/README.md to distinguish historical MVP/prototype rollout
from current source counting, actual trigger topology and current test status.
Appended dated rubric reconciliation to docs/architecture/cutover-evidence-pack.md:
47 baseline with seven criterion values, carried M1-M6/R1 snapshots, exact
registry removal chronology, 77 vs 77 hosted #499 comparison, source/PR recovery
matrix and acceptance gaps. Updated KB index and appended its log. Production
registry/removal history is verified, not replayed or cosmetically changed.

### Local verification (P02-T02)

All 17 in-scope seed/trigger failures repaired. Net suite case count changes
because six workflow parameters now each check their complete event matrix
instead of duplicating per-event cases, plus eight new parameterized cases.
Complete suite remains failing solely on the disclosed pre-existing deck test.
No application suite: no application code changes. No full/heavy gate:
explicit caller prohibition on --all, optional --changed unnecessary for
bounded tests/docs. No dependency installs, no cloud or scorer dispatch.

## Implementation-Time Plan and Detail Updates

Single critique Complete / Revise preserved. PC-001/002/003 accepted with
explicit synthetic prepare score, pre-deletion fingerprint and full event
matrix. PC-004 rejected: no workspace-only temporary-directory restriction
exists. No new user decision, second critique or historical cleanup.

## Blockers and Follow-Up

No blocker for independent repairs. Historical per-migration scoring evidence
and original dedicated registry sequencing remain incomplete acceptance.
The unrelated deck-selection mismatch is outside scope.

## Pre-Review Reconciliation

All plan markers and details reconciled to actual evidence. Original critique
Complete / Revise and direct dispositions preserved. Validation/follow-ups
current; no implementation blockers. Ready for one independent Review with
explicit known unrelated failure, runtime skips and historical acceptance gaps.
Publication is later execution, not a prerequisite or passing Review claim.
