---
title: Sensor backfill implementation phase details
ms.date: 2026-10-27
---

Task: #177 / sensor-backfill-177. Research: dated sibling research artifact.

<!-- P01 -->
## P01: Source and branch foundation

P01-T02: #178 source selection cannot override existing owner direction or
active PR #425. Preserve the conditional HadUK context/OGL evidence, missing
RH and pending underlying paired-source terms. One issue comment, not repeat
requests or unchecked factual claims. Evidence-only branch and draft PR.

P01-T01: Commit current state/research/plan/details/critique on parent first.
All five children fork that common commit. Separate branch changes stay
unmerged. No stash, history rewrite, retargeting #425 or hidden integration.

<!-- P02 -->
## P02: Isolated components

P02-T01: Extract existing indoor equation into a typed projection helper,
retaining exact operation order, RNG call order and legacy exercise constants.
The legacy wrapper continues its existing API. Validate supported dwelling,
age and construction factors and outdoor inputs in the supported exercise API
domain -80..60 C and zero-to-100 RH. Construction factors must be one of the
existing documented 0.75..1.20 values. Reject NaN/infinity, the Magnus
singularity and out-of-domain values explicitly. These limits are not sourced
climatic or safety bounds. Include the helper in revision_sources and bind its
version/domain/parameter classification in generated manifest parameters.
New tests compare an independently written old equation across representative
inputs and assert deterministic bounds, endpoint/domain errors, helper byte
fingerprint sensitivity and manifest use. Explicitly label climate-derived
historical/physical acceptance as not established.

P02-T02: Independent `retrofit_effects` module takes immutable measures
(home ID, kind, completion timestamp, synthetic flag). Reject unsupported
measure types, duplicate measure IDs, invalid/naive time, missing home IDs and
non-synthetic claims. Canonical sort. Effects multiply loss factors only for
matching home and `completion <= observed_at`; no history yields 1.0.
No actual register or #173 private data read. Writer integration remains #183.

P02-T03: Independent `household_conditions` module draws profiles from
versioned ID/seed-specific RNG. Equal schedule choices, uniform setpoint,
ventilation multiplier and moisture/drying increment are documented exercise
distributions. Generate dated conditions only for explicitly granted synthetic
monitoring; declined and unknown yield no observations, including no inferred
profile. Unsupported monitoring choice/seed/home/time is an explicit error.
No demographic inputs, behavioural ranking or resident attribution.

P02-T04: #183 evidence-only child records real `_shape`/identity mismatch and
legacy loader incompatibility. Do not silently shorten/reassign IDs or call
legacy `validate_reading` a #110 contract. One issue blocker comment.

P02-T05: Install core editable with pip only after observed import failure
(already observed). External virtualenv/test output, no checkout caches.
Run named unittest modules via test-only PYTHONPATH, not application paths.
New code Ruff/mypy; each PR records exact checks and partial acceptance.

<!-- P03 -->
## P03: Independent review and publication

P03-T01: Fresh independent reviewer activates rpi-review, reads common base
plus each child diff without source edits, writes one dated Review. Boundary:
bounded components and evidence, not scientific/whole-issue/live acceptance.
Route findings to later work, no repair-and-repeat Review loop. Each finding
records severity, affected child SHA, original outcome and disposition.
Unresolved substantive defects leave that component blocked/unaccepted; a
draft is transparent evidence only, not a way to turn a defect into a pass.

P03-T02: Parent changes record lists child SHA/PR and check outcomes. Commit
original Review and accurate state. No child code silently copied to parent.

P03-T03: Save transient logs externally. Inspect visible `git clean -ndx` before
`git clean -fdxq`; only task-owned scratch may be removed. Fetch main, run the
runner's own `--lock-timeout 0` (confirm exact option before use) to acquire
`/tmp/ama-rpi-heavy.lock`; do not outer-flock the same lock and deadlock it.
Exactly one `--changed` invocation, new external out, foreground, no nohup.
Only verify a successful receipt with `--required-scope partial --base
<current-fetched-origin-main-sha>`. Failed receipts remain adverse evidence;
stale HEAD/base/input blocks rather than authorizing a second run.
No Docker/Azure
fallback or gate bypass. Draft parent PR may report a failed/blocked gate;
do not call it publication-ready.
