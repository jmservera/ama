---
title: Indoor derived bounds phase details
description: Evidence-led tasks for issue 179
ms.date: 2026-10-27
---

Task: 179 / indoor-derived-bounds-179. Plan:
.copilot-tracking/plans/2026-10-27/indoor-derived-bounds-179-plan.md.
Research C1--C7 is sufficient. No blocking decision remains.

<!-- rpi:phase id=P01 -->
## P01: Model and regression implementation

<!-- rpi:task id=P01-T01 -->
### P01-T01: Shared per-record bounded projection

Keep input validation in project/project_composed; pass validated outdoor pair,
loss, setpoint and moisture increment (divided by ventilation in composed mode)
to a common typed helper. Compute B using the unchanged outdoor cold/solar terms;
V = sat(outdoor)*outdoor_RH/100 + model moisture contribution.
Bound each Gaussian residual to +/-3 sigma; draw temperature then RH, exactly
once each. RH clamps only at physical saturation, not exercise output clips.
Publish temperature/RH envelope equations in both parameter mappings and
increment model versions to v2. Preserve ingestion BOUNDS and payload schema.
Done when the fixed 8/15/98 clips are absent from both projection equations
and provenance captures versioned behaviour.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Independent semantic and regression tests

Amend the old exact-reference test to the independently spelled-out v2
equations while retaining RNG state comparison across forms/ages/schedules.
Replace fixed floor assertions with independently computed envelopes.
Use adversarial deterministic gaussian draws to hit both tails and saturation;
prove nominal outputs can pass the former 8 C, 15% and 98% limits.
Exercise supported endpoints, every fabric dimension and composed household/
dated loss, with unchanged explicit refusals.
PC-001: composed numeric reference must use non-unit ventilation and an active
dated multiplier as well as neutral 1.0, compare both outputs and RNG state to
exactly two independent reference draws, and record Gaussian arguments/order/
count in ordinary, forced-tail and saturation cases for both entry points.

Read only the same public ERA5 raw/metadata used in test_climate_history,
with both literal SHA pins. Project the whole 17,544-hour sequence through
legacy and composed generator paths for a small synthetic dwelling sample,
including an explicit dated measure. Independently reconstruct per-record
model inputs and verify both rounded CSV values against derived envelopes
(at most 0.005 rounding tolerance). No injected faults in this nominal test;
existing fault suites prove intentional corruptions separately. Assert
SYNTHETIC labels, unchanged pair input and byte/deterministic replay.

<!-- rpi:phase id=P02 -->
## P02: Evidence, validation and publication

<!-- rpi:task id=P02-T01 -->
### P02-T01: Related documentation

Replace current README fixed-bound/unmet/unchanged-default statements with
v2 equations, assumptions, causal envelope and versioned-byte change. Preserve
historical outcomes in the synthesis; add a dated #179 criterion audit, update
the index and append a log entry. No memory/specification change.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Local validation

Use the isolated session venv after the initial uninstalled baseline failed
with ModuleNotFoundError. Core baseline: 4 tests passed after editable core/
agents/API installation. Use installed distributions, never package-path
workarounds. Run the existing relevant suites (including household, measures,
climate, faults, stock, privacy, history, provenance and consumer), changed-file
ruff/mypy and API discovery using its documented test-helper PYTHONPATH.
Capture command, count, skips and failures. No --all or scoped heavy gate for
this small change. No data regeneration, cloud or hosted acceptance inference.

<!-- rpi:task id=P02-T03 -->
### P02-T03: Single Review and delivery

Review complete diff and exact criteria once with a fresh independent reviewer.
Record execution separately from outcome; preserve unresolved findings and
route later work instead of rerunning Review. Configure repository-local
privacy-safe identity from gh api user, commit implementation and all evidence
with Conventional Commit/trailer, push only the existing branch and open one
PR to main. Use Closes #179 only if all story criteria pass; other issues Refs.
Keep required human approvals explicitly unperformed.

## Execution Reconciliation

P01/P02-T01/P02-T02 complete. Combined relevant core: 142 run/141 pass/one
existing own-local-SQL skip; dependent resident sensors nine passes. Changed
Python ruff/format/mypy passed. Ten canonical methods passed after formatting.
API discovery: 744 passed/310 skipped/four missing-SDK import errors; installing
the unchanged API manifest into the isolated session venv and retrying only
four affected modules produced 61 passed/six skipped/zero errors (67 run).
No unresolved test failure or source change. One independent Review:
Complete / Conformant, no findings. P02-T03 is complete: initial implementation
and original evidence committed as 3d24537a, topic branch pushed and one main
PR opened at https://github.com/jmservera/ama/pull/502. Final evidence-only
bookkeeping does not change the reviewed model/test bytes or imply merge/
hosted/operational approval.

## Correction cycle 1 details (2026-10-27)

P03-T01: introduce explicit containing snapshot versions in sensor_backfill;
use them in default/stock/fault/integrated manifests and loader admission.
Keep reading schemas, fault-packet algorithm and stock identity/fabric versions
unchanged. Privacy must recognize current stock snapshots and still audit old
stock snapshots, not misclassify either as scale fixtures.
Rename historical equality test to versioned payload golden; assert literal
default v3 / projection v2 and new reading SHA while retaining unchanged
scale/register hashes. Add at most four methods covering all manifest modes,
stale version refusal and legacy/current privacy treatment. No test removal.
Before updating the golden, independently reconstruct the old equation/clips
using identical draws to demonstrate the old SHA and isolate changed row fields.

P03-T02: update core README, determinism/versioning synthesis, reference index
and append-only log. Record prior/new full hashes, causal comparison, unchanged
boundaries and old-revision replay requirement. Use installed core with its
declared dev extra, exactly Python 3.12 as CI:

```bash
cd src/core
python -m unittest discover -s tests -v
ruff check . && ruff format --check .
mypy
```

Keep complete output external to the repository; append counts, durations,
skips, failures and successful retries honestly. No --changed/--all gate.

P04-T01: one bounded independent correction-cycle Review, preserving original
outcomes and recording execution separately from acceptance. Reconcile plan,
details, changes and state. Fast-forward the known rubric-bot upstream commit
without moving existing modifications; configure privacy-safe local identity
from gh api user, commit all correction evidence with Conventional Commit and
Copilot trailer, push the same branch without force and update PR #502.
No new PR, merge, live seeding or hosted acceptance inference.

PC-C1-001 direct disposition: stale-version refusal must change only the
version of an otherwise valid current default/stock/composed snapshot, retain
current generator_revision and payload hashes, assert the specific version
refusal reason and zero scratch/write/consumer/schema/SQL calls. Retain the
existing successful current-version loads as positive controls.

Implementation clarification: legacy load_into already opens an empty temporary
context before verification; P03-T01 requires no replay writer/output/schema/
SQL for that path. Composed stale admission additionally precedes temporary
scratch allocation. Preserve this distinction rather than refactor unrelated
legacy loader control flow.

Correction-cycle execution: P03-T01/P03-T02 complete; P04-T01 pending.
Final source/test candidate ran the exact full CI core suite successfully:
1,437 run, 1,251 passed, 186 skipped, zero failures/errors, 433.719 seconds.
Full-project lint/format (100 files) and mypy (153 files) pass. Earlier initial
static failures and full-suite run are retained in changes; final full-suite
rerun follows all source/test edits. No unresolved decision or implementation
task. Independent correction Review and same-branch publication remain.

Correction-cycle independent Review Complete / Conformant, no findings;
its original append-only record includes independent-probe limitations.
P04-T01 still awaits actual commit/push/PR update. No source/test edits
follow the assessment; owner and hosted acceptance remain separate.

P04-T01 complete: 13042a9b pushed to feat/indoor-derived-bounds-179, PR502
description updated with hashes, exact CI results and independent-probe
limitations; published head verified. All correction tasks complete.
No force/main push, new PR, source change after Review or hosted approval.
