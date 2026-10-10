---
title: RPI Changes - Proper Warm Exercise PoC Rebuild
description: Local implementation evidence and unmet acceptance gates
ms.date: 2026-10-10
---

## Metadata

* Task ID: exercise-poc-rebuild-2026-10-10
* Plan: .copilot-tracking/plans/2026-10-10/exercise-poc-rebuild-plan.md
* Details: .copilot-tracking/details/2026-10-10/exercise-poc-rebuild-phase-details.md
* Declared scope: full plan, local implementation; live acceptance explicitly blocked.

## Execution Status

Partial against the complete accepted PRD. P01-P04 complete. P05 has a connected
local home-to-financial-closure implementation and later financial/handoff/update
corrections; the complete fixture/role acceptance matrix remains outstanding.
P06 local checks executed and draft PR updated; two prescribed-duration
workloads pass and live/human acceptance remain open. No full end-to-end
acceptance or conformant outcome is claimed.

## Completed Work

### Accepted baseline and reusable contracts

P01/P01-T01: PR #57 merged as 5a6ec60 after exact-head checks. New unpublished
rebuild branch based on merged main. Existing suite ran 270 tests in 44.766s:
OK, 26 live MSSQL tests skipped. No runtime or model success inferred.
Source and bounded planner assessment establish private geography exclusion,
reusable controls/SQL, missing forms/Decision/forecast and eleven/nine-path gaps.

### Domain, provider and fixture contracts

P02: forms.py/test_forms.py implement source-bound text/CSV extraction,
versioned six-template registry, field/protected-human reviews, calculations,
pack export and exact invalidation; 24 local tests passed.
P03: decision.py, decision_tasks.json, test_decision.py implement dedicated
transport/registry/proposal validation and reusable fail-closed guard;
25 fake-only tests passed; conservative provider response shape awaits probe.
P04: exercise.py/forecast.py, manifest/oracles and tests implement wholly
fictional fixtures, six scenarios, independent forecast/sensitivity oracles
and separate scale stream; 19 tests passed. Combined 68 tests passed.
P05: isolated factory/projection, usable labelled source evidence, common
generation guard/provenance, service/UI form reviews, separate financial events,
independent capacity/quality/milestones and cash/invoice closure integrated.
Ten connected integration tests cover the one-home journey, sibling isolation,
source/version invalidation, denied shortcuts, zero-call inference and rejected
application attempt chains. Evidence-support screening minimizes sources to
current field candidates and never approves a field. Unknown template/rule
versions block export; restoring versions preserves stale reviews.

Narrow data contracts add literal-text XLSX preview, at most 25-case coordination
bulk preview, fingerprint-bound explicit commit, idempotent retry/per-row outcomes
and role-projected JSON cohort/history export. Seven tests passed. This is not
arbitrary Excel, authoritative stock ingestion or XLSX full-history export.

P06: Chrome 152.0.7977.75 browser runner passed 22 finite checks, covering eleven
orientation profiles, nine workflow navigation entries, parser conflict,
320/390/1280px form reflow, root text resize, focus/labels/IDs and runtime errors.
The first browser run exposed real narrow-header overflow, fixed by wrapping
navigation/card content and labelled focusable scrolling tables. CSP remained
unchanged; test code was fixed to respect it.

Runtime runner took 200 warm HTTP samples each for list/detail/dashboard/write,
all below their individual thresholds, on one session/writer and 18 fictional
homes. Clean restart retained the exact case; SQLite backup/restore retained
the exact case and audit head. These are not prescribed concurrency/30-minute/
600,000-event scale or crash/RPO/response-loss drills.
The container now copies required evals/registry. Image build and non-root,
read-only exercise startup with writable state pass.

## Implementation-Time Plan and Detail Updates

One final-candidate critique returned Revise. Five compatible planner
corrections added common inference guard, external hazard authority,
generative provenance, actual text/CSV extraction and isolated exercise startup.
All are in the current plan/details; no repeat critique or owner question
needed. Runtime addition ceilings and zero test removals preserved.

## Validation Record

| Check | Scope | Result | Evidence |
| --- | --- | --- | --- |
| Baseline unittests | Existing MVP | Pass | 270 tests, 26 live SQL skips |
| Live Decision 1 and narrative | Required platform evidence | Blocked | No Decision deployment; billable/terms/cost authorization unverified |
| Integrated full suite | Local regression | Pass | 355 tests, 26 live MSSQL skips, 65.989 seconds |
| Changed JavaScript and whitespace | app.js, panels.js, exercise.js and Git diff | Pass | node --check; git diff --check |
| Browser orientation/parser/reflow | Finite engineering checks | Pass | exercise-poc-rebuild-browser-results.json, 22 checks |
| Sampled HTTP/clean backup | One session/writer; 200 samples/operation | Pass | exercise-poc-rebuild-runtime-results.json |
| Container startup | Non-root/read-only plus temporary writable state | Pass | Locally built image includes fictional fixtures/registry |
| Full PRD runtime acceptance | Complete accepted contract | Not run/Blocked | exercise-poc-rebuild-acceptance.md covers every FR/AC/NFR and known gaps |

## Blockers

Actual Decision 1 deployment/access/terms/costs and bounded billable authorization.
Human-adjudicated evaluation labels, paired-effort participants and real UX.
They block corresponding acceptance, not local exercise implementation.

## Remaining Work

P05 complete role/workflow/return fixture acceptance and P06 remaining
permission/cold-start, scheduled RPO/operator reconciliation, screen-reader,
actual models and human evaluation. Later local mixed workload, background
interruption and native zoom evidence is recorded below.
Focused handoff/update/hazard and two prescribed-duration measurements now pass.
Current draft publication preserves one independent review. No completed
full-PRD or observed-benefit claim.

## Pre-Review Reconciliation

Ready for a bounded review of implemented local changes and a complete
requirements-gap assessment, not for a conformant full-PRD verdict. Plan
P05/P06 markers intentionally remain unchecked. Details/state/evidence agree
on partial delivery and blocked live acceptance. Original critique retained.

## Follow-Up Items

None outside the current plan.

## Publication and Review Outcome

The owner explicitly requested continued autonomous implementation after draft
publication. This is a later implementation invocation for routed RV findings,
not a repeat Review. Resume financial invariants first; retain the original
Not accepted review as history and do not infer live/billable authorization.

The one independent implementation Review is
.copilot-tracking/reviews/logs/2026-10-10/exercise-poc-rebuild-review.md:
execution Partial, outcome Not accepted. RV-001 through RV-004 reproduce
financial-chain/cash/rejected-retry defects; RV-005 through RV-007 preserve
full workflow, actual platform and exact runtime acceptance gaps. Later
user-directed rpi-implement owns corrections; no repeated Review or regrade.

Published the partial rebuild as **draft PR #58**:
https://github.com/jmservera/ama/pull/58, implementation commit 7b4b898.
The draft body lists all blockers and prohibits a ready-to-merge/full-acceptance
claim. Final publication regression: 355 tests, OK, 26 live MSSQL skips,
56.257 seconds. CI launched separately; a green pipeline cannot clear the
open reproduced review findings. No rebuild merge or billable activation.

## Later Owner-Directed Implementation

Owner renewed direction to keep implementing after the blocked handoff.
Resume feasible P05/P06 engineering work, beginning building/home navigation
and independent role-projected gates (FR-001/002, AC-001/002/003).
Live activation and participant prerequisites stay blocked; this continuation
does not authorize cloud spending, fabricate evaluation or repeat Review.

P05/P05-T01, RV-001 through RV-004: exact financial predecessor staleness now
propagates through application/award/claim/cash without reactivating history.
Latest current award controls readiness; cumulative externally recorded cash
cannot reset across stale claims and duplicate receipt references are denied.
Unchanged export or pack review cannot correct a rejected submission; even
staling that rejected attempt preserves its exact retry reference requirement.
Finance events retain scheme/route/version/input/review bindings. Exact
reproductions and sibling/rollback invariants pass; original Review remains
Not accepted historical evidence, not a new assessment.

P05/P05-T01, RV-005: explicit sent/received/accepted/returned/escalated/completed
handoffs preserve chase and ownership until acceptance. Independently owned
resident commitments retain purpose/due/basis, proposed/sent state, explicit
reassignment and history; a handoff never clears them. Supplied external hazard
receipt/acceptance/chase are separate from awareness/hold/release authority.
General earlier-stage return records receiver/source/reason/next action;
domain changes still own version invalidation. Malformed commitment dates
fail explicitly and atomically. These are focused engineering contracts,
not the unexecuted full human/profile workflow matrix.

P03/P05, RV-006: scoring and generation share conservative atomic SQLite
upper-liability reservations. Retained charges survive processes, failure and
lower environment baselines; no auto refund/monthly rollover. Guard errors
block transport. Catalog `Microsoft-Decision-1` identity casing is normalized,
without admitting another model/version. Read-only Azure metadata now confirms
model eligibility (version 1, GlobalStandard), not a deployment, price quote,
processing approval or live inference. The returned SKU cost is null. No
resources or billable calls created; actual activation still blocked.

P06/P06-T01, RV-007: fresh Chrome run passes 25 finite checks including actual
32px body text, CSS 4x zoom reflow, visible 24px control targets and declared
palette contrast. CSS zoom is explicitly not native browser zoom; no
screen-reader/user acceptance claimed. Exact separate scale Store probe passes
500-row literal-text import and 25-case coordination commit, source-byte hash,
controlled-field and audit invariants; import preview 0.089397s. Actual process
termination before commit and after commit/before response retains exact
case/audit state and safe rejected retry; not a disaster/RPO drill.

Latest focused validation: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. python3 -m
unittest tests.test_decision tests.test_exercise_workbench -q` from mvp:
48 tests, OK, 15.149 seconds (28 Decision and 20 workbench tests).
Browser and data raw outputs currently reside in the session files folder;
delivery-safe generated summaries now sit beside the acceptance register.
Both core and scale workloads finished; exact results are below. Full regression now passes:
370 tests, OK, 26 live MSSQL skips, 67.562 seconds, after adding 20-way
reservation contention and generation/document zero-transport denial
(30 Decision tests). Changed browser syntax and
`git diff --check` pass. Image sha256
34d79fa11788b453de3b94096788f72377af9cfaccb1468c55fb5516731b306d
passes non-root UID 10001/read-only health 200 with 18 fictional homes and
temporary writable state. Current draft publication remains pending for this
correction batch.

Explicit operator authorization and human-evaluation prerequisites were asked
after read-only eligibility was verified. User unavailable; no deployment,
billable calls, false reviewed flags or participant evidence inferred.

### Completed Prescribed-Duration Measurements

Core: 1800.037 seconds, five authenticated sessions/two coordination writers,
9001 interactions, no failures. List/detail/dashboard/write samples:
4920/2460/900/721; p95 seconds: 0.010124/0.004759/0.006304/0.150626, below
1/1/3/2. Exact clean restart 0.207754s, integrity ok, backup case/audit equality.
Scale: separate 60000 fictional homes/600000 embedded linked traces,
1800.046s, twenty sessions/two writers, 9001 interactions, no failures.
Samples 5100/2550/900/451; p95 0.098890/0.041894/0.048979/0.078726s;
all below thresholds. Restart 3.747456s, integrity ok and exact backup equality.
Complete raw generated JSON retained beside the acceptance register.

Five scheduled interactions/s includes two HTTP requests per write; actual
workload requests/s approximately 5.40 core/5.25 scale, excluding login.
The separate exact 500/25 Store data probe touched other scale homes while
scale soak ran; it is not the prescribed mixed concurrent core HTTP import.
Both servers loaded the initial follow-up snapshot before later stale retry,
date/model-casing and runner corrections; those paths are separately tested,
not claimed covered by these workload runs. No full NFR-002 or RPO acceptance.
Both attached workload processes completed with exit zero; no ongoing soak
process is left running.

### Correction Publication

Published corrections as `0a4de9d9db3d7b0be0436230e14d4f6ca4cd471d` on the
existing coherent branch and updated draft https://github.com/jmservera/ama/pull/58.
Exact correction-head MVP CI (38062257646), MVP validation (38062257659) and
Prototype validation (38062257645) pass. Rubric run 38062257657 recorded
40/100 through concurrent bot commit b7d3ae7, then completed as Cancelled
after branch advancement; no rubric acceptance or later-head check inferred.
Safely merged that rubric-only commit with the publication record without
rewriting history; pushed merge bb5c2d1. New-head checks are separate from
the successful correction-head checks and are not claimed completed here.
Repository is not merged. Full task remains blocked on actual platform/human
prerequisites and explicit local acceptance gaps; P05/P06 remain open.

## Continued Building, Role and Recovery Work

P05/P05-T01: added read-only building context linked both ways to independent
story homes. Shared systems/dependencies/holds/cost stay explicitly unknown
without supplied shared evidence; package identity never proves applicability.
Each home is independently role-projected and contractors see only assigned
homes. Exact projected-state equality and sibling withdrawal/design isolation
are tested. Browser now executes home/building/sibling navigation for eleven
profiles, eleven actual controlled award safe-block tasks, an individually
withdrawn lead versus unchanged sibling, and the resident commitment plus
sent/received/accepted/completed handoff journey. Empty handoff fields now show
explicit unknown destination/receiver/chase/reason rather than disappearing.
Async exercise views refuse to render results for an obsolete route; an initial
browser timeout exposed this race. A separate failed selector was corrected to
target the actual polite action alert, not an unrelated hidden JSON error.

P06/P06-T01: native browser 400% zoom is now executable using installed Xvfb,
headed Chrome and real X11 accelerators, not CSS/CDP emulation. A fresh run
passed 38 finite checks, including actual devicePixelRatio 4, CSS zoom 1 and
319 CSS-pixel content viewport within 1279-pixel native window. Home/building
content has no horizontal page overflow. A later headless run passes 51 checks
with added controlled profile/handoff fixtures. Native display was stopped;
no human/screen-reader/conformance claim. Failed headless preference and
accelerator probes were not counted as native zoom evidence.

Actual background bulk-commit thread interruptions before save and after
commit/before response preserve both homes and the audit chain; safe retries
return the same two-row outcomes without duplicate events. Separate backup/
document restore compares exact case/audit and document SHA-256, detects the
deliberately missing acknowledged Intake-to-Assessment event and marks the
candidate offline. Factory refuses startup while exercise_recovery_pending
exists; no controlled work can resume through the standard exercise launcher.
This is a bounded local restore/blocked-reconciliation probe, not a scheduled
15-minute backup service or completed operator disaster reconciliation.
Hazard receipt/acceptance/chase references must be distinct and supplied
timestamps timezone-qualified; invalid/duplicate evidence leaves state unchanged.

Latest full regression: 374 tests, OK, 26 live MSSQL skips, 66.159 seconds;
24 focused workbench tests pass. All eleven profiles are tested against six
form-creation permissions and eight protected batch denials, retaining exact
denied state and intact audit. This is not the complete role/action inventory.
Latest image builds as
038286a2b812a26493fd99a65994b8a310580160da981c20305acce8236abe30
(superseded by final image below).
The exact scale HTTP-rate run passes: 9000 scheduled requests over 1800 seconds,
twenty sessions/two writers, zero errors and p95 below all four thresholds.
Maximum list/write outliers remain recorded in the raw result; the requirement
is p95, not maximum latency. Strict mixed core also passes for 1800.002 seconds:
518 fictional homes, five sessions/two existing writers, 500 imported rows and
25 bulk cases committed, 20 actual 5000000-byte documents (100000000 total)
and exactly 150 story-home non-approval upload/note events.
List/detail/dashboard/write p95 are 0.006812/0.002796/0.005147/0.034023s, with
zero errors; import preview 0.056826s. Core schedules five interactions/s
(9720 HTTP requests plus four import/bulk requests), not five requests/s.
An initial oversized document fixture failed before startup. An intermediate
run used 100 MiB and a third import writer, with an inaccurate top-level
population label. Neither is the strict baseline; limits, identity and label
were corrected before the fresh strict run.

Independent read-only post-run comparisons verify all eleven controlled field
groups on all 518 core and 60000 scale homes, all 600000 exact scale trace
contents, twenty document hashes, frozen 150 story-home events, exactly two
writers and intact full audit chains. Seed comparison applies only the
documented legacy funding initialization default. Raw results and independent
invariant reports are retained beside the acceptance register. Initial cold
startup was not separately timed; clean restart timings are not relabelled.

Final combined headed Chrome/Xvfb run passes 53 finite checks, including
actual native 400% zoom, eleven controlled role tasks, bidirectional building
navigation, distinct consent/design and handoff/update journey. Both virtual
display instances were stopped. Latest image
b363aa5e87e3151da36079deec472e55e35a06dedc9699ea99b179bf16ee1c4e
passes UID 10001/read-only startup, health 200 and 18 fictional homes.
Requirement-level AC-001/003/035 and FR-033 now pass their exact constructed
fixtures; all unrelated/incomplete full requirements stay Not run/Blocked.
