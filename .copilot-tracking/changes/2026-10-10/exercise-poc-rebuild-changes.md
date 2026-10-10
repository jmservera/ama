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

### Continuation publication and exact-head checks

Implementation c421f7d was published to existing draft PR #58 after a safe
non-rewriting merge of concurrent rubric-only commit 7a6809f. Published source
head d35e0be75bb58878924f439e34aac36a0341163b passed MVP CI 38067801576,
MVP validation 38067801569 and Prototype validation 38067801672.
Later documentation or rubric-bot heads have separate checks; no result is
inferred for them. Draft description now separates executed local shapes from
remaining complete matrix, recovery, accessibility, live-model and human
acceptance. Original Review remains Partial/Not accepted and was not repeated.
No merge, cloud change, billable call or task completion was performed.

## Renewed Resident and Service Acceptance Implementation

P05/P05-T01 resumes under the owner's renewed autonomous implementation
request. Current write boundary is existing resident/technical controls,
integration fixtures and directly related evidence. Execute exact two-measure
choice/design/representative and accessible service/redress fixtures, preserving
history and independent resident decisions. Repair only coupled defects
with reproductions. Existing critique and Review remain unchanged; actual
model authorization and human evaluation remain unavailable.

The exact API fixtures exposed unrestricted service accessibility/contact
references for roles without a recorded need. Projection now minimizes those
fields and decision representative references, preserving Unknown/None.
An initial projection fix exposed a shallow resident-decision view alias:
redacting a response changed stored representative history. Decision views
now deep-copy versions; tests compare raw state before/after all-role reads
and exports. Model source labels do not contain contact-reference tokens.

The real browser complaint journey exposed a deeper existing form-rendering
defect: nested child arrays became literal HTML element strings, leaving
all `actForm` inputs absent. The shared DOM helper now recursively flattens
children rather than one level. This is a directly coupled root fix, not a
weakened test selector. Exact rendered-control assertions remain in the
browser runner; source/date/authority controls are not bypassed.

Validation: 27 workbench tests pass; full regression 377 tests, OK, 26 live
MSSQL skips, 69.747 seconds. Final headed Chrome/Xvfb run passes 57 finite
checks, including actual accessible complaint intake, service-owner closure
refusal, independent redress closure and native 400% zoom. Fresh 18-home
initial startup is separately measured at 0.323109s to first health 200; no
cloud/scale cold-start claim. All virtual display/browser/server processes
were stopped. Image 8d6799aa548f2c96d4c506816f6050a014502b37f98d0caeaef72158532d5c2e
passes UID 10001/read-only health 200 with 18 fictional homes.
FR-014/045/046 and AC-017/037/055/056 pass their exact constructed local
contracts; full PRD, human effectiveness and real obtained consent are not
claimed. Published workload results remain historical snapshots before this
projection/DOM batch; no rerun is inferred for those source changes.

Published implementation b68e140 on existing draft PR #58 after safe merge of
rubric-only 194b23c; exact source head
7605194b6018d054628a6932ff78cf836832aec5 passed MVP CI 38068654678,
MVP validation 38068654793 and Prototype validation 38068654643.
Later documentation/bot heads have separate checks. Renewed exceptional
deployment/billable authorization and human-evaluator availability request
returned user unavailable. No consent, deployment, model call, evaluator,
value outcome or full task completion is inferred. Affected live/value
acceptance remains blocked; remaining local matrix/return/recovery/accessibility
work is explicit. Original Review and draft/unmerged boundary are unchanged.

## Explicit Return Scope Implementation

P05/P05-T01 resumes with named technical sign-off and same-home form-field
re-review scopes on return/reopen. This is an immediately relevant current
state update under FR-009/010/043, not a new approval workflow: preserve
source/choice/sibling/history, use existing sign-off and form-version helpers
and refuse invalid scope atomically. Empty scope remains routing-only.
Write boundary: existing Store/event UI/tests and directly related evidence;
validation: exact stale-set, financial ancestry and versioned return oracles.

Implemented explicit `affected_signoffs` and `affected_form_fields` on return.
Named sign-offs use the existing competent-role return helper; named fields
advance existing input versions and invalidate exact transitive review/
calculation/financial lineage. Administrative empty scope remains routing-only.
Versioned return IDs preserve original reason/source/authority/receiver/next
action and prior history. Reopened case display stage and status reason now
match its actual return target/owned next action, not a stale Completed label.
Sources, resident decisions, unaffected claim draft/sibling and historical cash
remain intact. Non-Finance views omit restricted form-scope details.

Three new fixtures cover all 36 earlier-stage pairs, per-role denial,
ten atomic invalid-scope shapes and exact scoped invalidation with GBP 3000
cash retained. Real browser controls reject malformed JSON without advancing,
return the named design sign-off and display versioned source/owner/next-action
history without altering works withdrawal. Final full regression: 380 tests,
OK, 26 live MSSQL skips, 72.684s. Headed native-browser: 60 checks, zero failed.
Image 5709b3b6d1dd0325591e1a1f2665c579052426871b9075baa3a6ee7667e5336a
passes UID 10001/read-only health 200 with 18 fictional homes.
FR-010 and AC-012 pass exact local disposition contracts. Full quality/
procurement/milestone return invalidation, other role/workflow coverage,
scheduled recovery, human/screen-reader and actual-model/value gates remain
open. Existing Review is unchanged; no full task acceptance is claimed.

Published scoped-return source d77937296ffa9df74ba5a98cb4525fe0b9565a0b
on existing draft PR #58. Exact-source MVP CI 38069313144, MVP validation
38069313023 and Prototype validation 38069313054 all succeeded. Later
documentation/bot head checks remain separate. Working source and results
are persistent; draft description preserves the outstanding complete-domain,
operational recovery/accessibility and actual-model/human gates.
No authorization was inferred from autonomous implementation direction;
no deployment, billable call, merger or repeated Review was performed.

## Milestone Re-Review and Financial Continuation

P05/P05-T01 resumes within existing return/Finance controls. Add explicitly
named same-home milestone re-review scope and recheck current milestone
evidence before payment-status or financial closure continuation. Preserve
historical milestone/approval/payment records and independent human renewal.
Write boundary: Store, Finance, return UI/tests and direct evidence;
validation: exact stale-ref/unchanged-history and renewed-review fixtures.

Implemented `affected_milestones` validation, retained milestone evidence
history and scoped staleness. Existing invoice matcher refuses stale evidence;
payment-status continuation rechecks current evidence before mutation, and
closure uses the same matcher. Existing independent milestone renewal clears
staleness only through its role/stage/source checks. Paid invoices and external
cash stay unchanged; restricted milestone details/history/scopes are omitted
from non-Finance projections.

Exact tests cover paid/unpaid refusal, independent renewal, preserved
invoice/QA/resident/cash/unaffected milestone history, persistence and
invalid/foreign/duplicate scope atomicity. Full regression: 382 tests, OK,
26 live SQL skips, 73.493s. Headed Chrome/Xvfb: 61 checks, zero failures;
actual milestone input refuses a foreign reference without advancing stage.
Initial test invocations without module path and headed Chrome without Xvfb
failed; corrected commands used the existing module path and isolated Xvfb.
Final image `f3dbc0af7306b6b2ac51b00116d9ba27d6fc22aedeb0f88f959529ccf64ecd90`
passes UID10001/read-only/no-capabilities startup and health 200. The inherited
`PW_DATA` first correctly refused exercise startup; the isolated run explicitly
cleared it. All test browser/server/Xvfb/container processes are stopped.

E27/E28 recorded without promoting incomplete requirements. All 115 requirement
rows remain unique. Full quality/procurement/milestone-version, role/workflow,
scheduled recovery, screen-reader, actual-model and human acceptance remain
open. P05/P06 remain unchecked, original Review stays Partial/Not accepted,
and draft PR #58 is not ready to merge. Earlier core/scale measurements loaded
earlier snapshots; they are not evidence for this latest payment/return path.

Published milestone implementation as
`d5bbd7984d44ac399a1dcbcdceccad695d16f2eb` on existing draft PR #58.
Exact-source MVP CI `38069962278`, MVP validation `38069962289` and Prototype
validation `38069962430` succeed, including live SQL/image CI checks.
Rubric `38069962358` was pending at handoff; no score or acceptance inferred.
This later handoff commit is separate from the validated source snapshot.
Mode remains manual, automatic session stopped, Implement blocked on incomplete
full-plan gates. No second Review, merge or full-completion claim.
