---
title: Sensor standard-deviation inclusive boundary phase details
ms.date: 2026-10-31
---

## Metadata

Task ID: 188-pr-587-second-correction. Slug: sensor-stddev-boundary-188.
Plan: .copilot-tracking/plans/2026-10-31/sensor-stddev-boundary-188-plan.md.
Research: .copilot-tracking/research/2026-10-31/sensor-stddev-boundary-188-research.md.
No unresolved implementation blocker.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete; requested checks passed | P01-T01, P01-T02 |
| P02 | Original Review Complete / Conformant; completion sealed in containing local commit | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Exact acceptance and validation

Research C1/C4 proves rounded roots reject the exact boundary. Current report
diagnostics remain rounded; only the stddev boolean uses exact rational variance.
Critique passed with no findings; P01-T01 starts the approved source boundary.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Owned boundary regression

Reuse twelve contiguous rows for one home from existing `rows()`. Set both
channels to constant centres (temperature 20, humidity 50), then give one side
nine samples with offsets -1.45 twice, +1.45 twice, zero five times. The
other side is three unchanged constant samples. Side placement selects
boundary index 3 or 9. Both channels, sides and inward/outward changes.

For changed extreme magnitudes 1.45 +/- delta, delta=0.14,0.15,0.16:
expected stddev-error = 2*delta/3; expect accepted, accepted, rejected at 0.1.
Also use delta=0.15 with `math.nextafter(0.1, 0)` and expect rejection.
Target channel uses point tolerance 1 and mean-step 0; unchanged sibling uses
zero tolerance. Assert complete checks dictionary and aggregate `passed`.
Do not use rounded diagnostic error as acceptance oracle.
Maximum one new test method, 32 subcases, no test removals/generated targets.
Capture failure on the unmodified comparator before production edits.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Comparator, documentation and requested validation

Add Fraction and pvariance imports. Small typed private helper accepts two
Decimal sequences and stddev limit, computes pvariance over Fraction values,
then uses guarded symmetric squared inequality. Call independently for each
before/after pair and `all` their booleans. Keep `pstdev` values/subtraction
for unchanged diagnostic keys. Explain guard algebra only where non-obvious.
README describes exact stddev acceptance and rounded diagnostic-only roots.

Use installed isolated pip environment:
`/home/azureuser/.copilot/session-state/395184a9-e42b-4e9b-bed0-3e3e11ad5990/files/sensor-stddev-venv/bin/python`.
Run from `src/core`:

```bash
python -m unittest discover -s tests -p test_sensor_handover.py -q
python -m unittest discover -s tests -p 'test_sensor_*.py' -q
python -m ruff check .
python -m ruff format --check .
python -m mypy src/zava_forward/core/synthetic/sensor_consistency.py
```

Replace `python` with the absolute environment binary. Format through existing
ruff if needed, then rerun checks. Do not add imports through PYTHONPATH.
Record actual tool versions, results, skips and exact limitations. Completion:
seven handover methods and all 32 new subcases passed; core sensor suite
134 tests, one existing opt-in SQL skip. Ruff 0.17.1 full-core lint and format
(115 files) passed; mypy 2.4.0 changed comparator passed. Existing resource
warnings in backfill tests remain unrelated. Initial added-test line lengths
were fixed by ruff format, then lint/format and regression were rerun.

<!-- rpi:phase id=P02 -->
## P02: Review and local commit

<!-- rpi:task id=P02-T01 -->
### P02-T01: One independent Review, original evidence, local persistence

Reconcile P01 markers, details and changes before Review. Invoke rpi-review
once and obtain one independent bounded assessment. Reviewer may read current
canonical artifacts and named sources, writing only original Review artifact:
.copilot-tracking/reviews/logs/2026-10-31/sensor-stddev-boundary-188-review.md.
Review findings become later work rather than another in-task review.

After Review, resolve `gh api user` id/login; configure local noreply email for
author/committer. Check diff/whitespace and explicit staged inventory. Commit
with `fix(sensors): preserve inclusive stddev boundary (Refs #188)` and
`Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
No push or issue changes. Full publication gate, hosted/human review and
live transport/calibration remain unproven and deferred. Original Review is
Complete / Conformant with no implementation defects; RV-004 and RV-005 route
those distinct deferred items. Original reviewer additionally verified all
32 calls, unchanged diagnostic reports and helper edge cases. This completion
snapshot is valid only in its containing local commit; no recursive/self hash
is embedded. Parent verifies commit/trailer, explicit inventory and clean tree.
