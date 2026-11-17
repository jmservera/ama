---
title: Issue 1845 withdrawn-sensor canary review
description: Original post-implementation review of the test-only canary repair, with outcome Partial
ms.date: 2026-11-17
ms.topic: reference
---

## Execution

* Review executed once, by the implementing worker, directly against the
  actual `git diff` and the recorded evidence. It is not independent
  exact-head assessment; the coordinator owns that.
* Assessed boundary: working tree on `test/withdrawn-sensor-canary-1845`
  atop `main` f1df574bba2b94cd83bb2a783079ec94cd584c90, one modified test
  file plus original dated RPI artifacts.
* Outcome: **Partial**. The scoped repair meets its local acceptance
  evidence; the FULL-tier evidence and review gates are not yet available.

## Acceptance criteria

| Criterion | Assessment | Evidence |
| --- | --- | --- |
| Deterministically demonstrate the timestamp collision without the clock | Met | Constructed metadata `1794924123.7340033`, `1794924123.7119958`, `1794924124.9123`: old substring check True for `23.7` and `24.9`; old assertion fails through the real test with injected timestamps (`work/out/before-old-assertion-collision.log`); a unit test asserts the collision and its acceptance. |
| Accept clean numeric metadata; still detect original and edited text in the applicable projections | Met locally | Fixed test passes with injected timestamps; original and edited text injected one at a time into detail, list, export and sensors each fail on the named projection (8 of 8, `work/out/after-mutations.log`). |
| Preserve existing disclosure coverage | Met | Same four projections, same canaries, same follow-on findings/provenance assertions; positive controls kept (now immune to timestamps). No assertion deleted. |
| Directly relevant quality-sensor tests with zero unexpected skips | Met, with expected gated skips | Module: 193 tests, OK, 94 skipped, all `Mssql*` (`needs disposable SQL Server`); targeted selectors 3 tests, 0 skips. |
| No production, authorization, provider, permission or gate-bypass change | Met | Diff touches only `src/api/tests/test_quality_sensors.py` (plus RPI artifacts). |
| Dated RPI artifacts; independent exact-head assessment and hosted CI | Partly | Artifacts present; exact-head assessment and hosted CI pending (coordinator). |

## Findings

| ID | Severity | Finding | Routing |
| --- | --- | --- | --- |
| R-1 | Minor, residual | A numeric leaf exactly equal to a canary is treated as exposure, and a string that embeds a canary (for example an id such as `sensor-v23.7`) still matches by substring. This is conservative and no weaker than before, but not a universal clean-metadata guarantee. | Accept; stated in plan, critique and changes. Revisit only if such a field appears. |
| R-2 | Process | FULL tier is selected for a privacy guard. The complete local gate and receipt are not produced in this launch (no heavy admission); browser and MSSQL coverage for the 1837 nomination remain unverified. | Coordinator runs the full gate on the frozen candidate; resume point below. |
| R-3 | Adverse, preserved | The original defect was a rare collision; the baseline run on this head passed. The retained 1837 failure was not independently re-observed, because the receipt is not mounted. | None; disclosed. |
| R-4 | Scope | #1641 consent-regrant defects are not addressed or cleared. | Separate issue. |

No open blocking or significant finding on the diff itself.

## Divergences and process disclosure

* The matcher design changed once after the single critique (regex to
  parsed-structure walk); both are recorded.
* Witness events: launch (coordinator), research-open seq 2, plan-done seq 3,
  implement-start seq 4, implement-done seq 5, all `ok`. They are local
  observations, not host or model attestation.
* HVE artifact checks: not applicable. No web UI change is in scope.

## Planned full-gate resume point

On the committed, clean candidate: `python3 tools/rpi-checks.py --all
--base <reviewed-main-sha> --out <new-external-directory>`, then
`--verify-receipt` against current `origin/main` before publication, plus
independent exact-head assessment and hosted CI. A partial or `--changed`
receipt does not satisfy this. The coordinator may assess a focused downgrade
from the actual diff (only the matcher semantics narrowed on a test-only
change, positive controls added); that is a proposal, not an exemption.
