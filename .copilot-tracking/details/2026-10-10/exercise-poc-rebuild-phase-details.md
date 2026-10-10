---
title: RPI Phase Details - Proper Warm Exercise PoC Rebuild
description: Current execution boundaries and expected evidence
ms.date: 2026-10-10
---

## Metadata

* Task ID: exercise-poc-rebuild-2026-10-10
* Task slug: exercise-poc-rebuild
* Plan: .copilot-tracking/plans/2026-10-10/exercise-poc-rebuild-plan.md
* Initial direction: reuse current workbench and SQL contracts; inspect gaps rather than rewrite blindly.
* Readiness: ready for local implementation; one critique executed and five direct corrections incorporated. Live inference acceptance remains blocked.

## Phase Index

| Phase | Name | State |
| --- | --- | --- |
| P01 | Exercise contracts | Complete |
| P02 | Forms | Complete locally |
| P03 | Scoring | Adapter/tests complete; live blocked |
| P04 | Fictional fixtures and forecast | Complete locally; scale workload not run |
| P05 | Connected workbench | Home-to-closure local journey complete; full handoff/update/fixture contracts partial |
| P06 | Evidence and delivery | Browser/HTTP/clean-backup/image checks executed; complete acceptance and publication pending |

<!-- rpi:phase id=P01 -->
## P01: Exercise contracts

<!-- rpi:task id=P01-T01 -->
### P01-T01: Fixture, journey and capability map

The current Store has resident/technical/quality/procurement/finance mixins,
and SqlStore persists case JSON transactionally. Factory defaults to JSON;
accepted demo must use SQLite and avoid the private geography generator.
The browser already has panels for these controls. Preserve current behavior
for legacy data while adding clearly isolated exercise configuration.
Inspect underlying tests and define exact input/output fixtures.
Completion evidence: capability map, fictional fixture contract, frozen
validation boundaries and successful PRD merge.

<!-- rpi:phase id=P02 -->
## P02: Forms

<!-- rpi:task id=P02-T01 -->
### P02-T01: Versioned form contracts

Own mvp/properwarm_mvp/forms.py and mvp/tests/test_forms.py only.
Use stdlib, plain JSON-compatible state and pure or copy-on-write operations,
compatible with Store/SqlStore integration by the primary implementer.
Every candidate has home/source/version/hash/locator/raw/parser lineage.
Allow only same-home, permitted evidence. Preserve alternatives and unknowns.
Only designated human actions may supply declaration/signature/choice fields.
Support actual readable UTF-8 labelled text and CSV tables. Hash raw bytes
and retain line/row locators; extraction is not a generative summary.
Source metadata is authorized independently of embedded text; unsupported/
unreadable scans become manual tasks. Independent tests compare raw bytes,
values/hash/locator, conflicting EPCs and embedded-instruction non-execution.
Versioned approved schemas must include competitive/allocation/award-return/
claim and non-funding technical/invoice templates, conditional/required fields,
calculated funding totals and exact transitive dependency sets.
Completion evidence: independent tests for readiness, wrong units/currency/
eligibility, stale sets, sibling isolation, protected fields and export fidelity.

<!-- rpi:phase id=P03 -->
## P03: Dedicated scoring

<!-- rpi:task id=P03-T01 -->
### P03-T01: Provider and task registry

Own new mvp/properwarm_mvp/decision.py, registry JSON and focused provider tests
only. Read the current official API guide before freezing request/response
validation; do not import old TypeSafe assumptions.
Use existing managed-identity conventions with explicit optional injected token
for local testing; secrets never enter logs, fixtures, output or repository.
Validate response IDs/keys/types/probabilities and identity/usage. Store
input hash, source/question/version, application-owned explanation, selected
candidate or no-match, margin/threshold and Not reviewed. No model rationale.
Only approved registry tasks can use inference; no autonomous decisions.
Live access is blocked; fake transport checks are API tests, not real inference.

<!-- rpi:phase id=P04 -->
## P04: Fictional fixtures and forecast

<!-- rpi:task id=P04-T01 -->
### P04-T01: Fixture and cohort contracts

Own new exercise.py, forecast.py, test_exercise_forecast.py, one exercise
manifest and one independent forecast-outcome JSON. Never read private
geography or answer keys. Use test-compatible case shape, wholly fictional
addresses/contacts, eleven declared profile paths mapped to existing roles
and nine workflows with implemented/deferred status, lead home and sibling
in one building. Default fresh SQLite state is generated outside repository.
Forecast exactly 16 homes (12 ready, four held), independent concurrent
install/QA stages; no next-stage start in same week. Four central/sensitivity
oracles and six scenario variants retain version/as-of/unknown/coverage.
Scale generator specifies 60,000 fictional homes/600,000 events separately;
do not claim load acceptance from merely generating it.
Completion: independent fixed-oracle tests, missing-input abstention,
withdrawal/hold/QA-return isolation, deterministic reruns, versions/denominators.

<!-- rpi:phase id=P05 -->
## P05: Connected workbench

<!-- rpi:task id=P05-T01 -->
### P05-T01: Integrate human workflow

Primary owns Store/SqlStore/server/projection integration and browser panels.
Implement explicit exercise launcher/factory mode: versioned fictional seed,
compatible named SQLite state, local documents only; refuse inherited private
seed/external backend and incompatible persisted state without accessing,
mixing, reseeding or deleting them.
Primary also owns a shared fail-closed inference authorization guard in
existing ai.py/ai_tasks.py plus decision.py integration. Inherited AI_ENDPOINT
alone never authorizes calls in exercise mode. Require approved registry task/
capability/source scope and explicit operator activation with reviewed terms,
cost/quota and no active spend-pause; keep all transport disabled in this run.
Retain generative response identity/version/usage/latency and task/source
binding, and separate provider failure from successful manual/template output.
Tests use only injected transport and record zero calls for denied cases.
Adapt hazards in exercise mode: intake/referral is editable, release/
classification/closure authority remains external. Deny legacy release and
record only supplied fictional external decision source/authority/version/
evidence via a dedicated reference action. Record receipt separately from
acceptance and retain follow-up, independent of AI. No sufficiency judgement.
Existing grant flow skips application; add separate version-bound application
and claim events without silently migrating old grant histories or treating
export as submission. Keep human-entered external references separate.
Exercise seed is fictional, versioned and independently reusable; browser
must disclose exercise status and expose blockers, evidence and next action.
Forecast oracles are [0,2,4,6], [0,1,2,3], [0,3,6,9], [0,0,0,2].
Acceptance tests follow the same home and separate identities across phases.
No real sends, payments, permissions hidden only client-side or artificial
live/model evaluation claims.

Later owner-directed implementation disposition: exact predecessor staleness,
latest-award readiness, cumulative cash and corrected rejected retry controls
now have reproductions, including stale rejected reference retention.
Explicit handoff stages and independently owned resident commitments have
focused tests; supplied hazard receipt/acceptance/chase remain separate from
clock/release authority. General return records source/receiver/next action but
does not invent domain changes or professional approval. Shared SQLite
upper-liability reservations persist across inference processes; no automatic
refund/rollover or invoice reconciliation is claimed. Full role/workflow
fixture completion remains unexecuted; P05 marker stays open.

<!-- rpi:phase id=P06 -->
## P06: Validate and publish

<!-- rpi:task id=P06-T01 -->
### P06-T01: Evidence and PR

Primary owns integrated tests, runtime/browser/recovery/performance evidence,
README and requirement-result reporting. Retain all existing tests and CI gates.
Use PYTHONPATH=. python3 -m unittest discover -s tests in mvp, syntax-check all
changed browser files and perform exact endpoint/field denial checks.
Record Not run/Blocked for required live inference, adjudicated 60 held-out
families, net-effort trial and real human UX until actually executed.
One independent post-implementation review, then publish the branch/PR.
Do not claim full accepted PRD completion while essential gates remain unmet.
Retain eleven perspective/nine workflow scripts, accessibility engineering
sizes/focus/status/chart equivalence, small-cell complementary suppression,
30-minute performance and scale workload/sample requirements and exact
recovery drills. Execute feasible local checks without reclassifying a smaller
run as the prescribed workload. Unknown observations stay unknown.
Test additions/removals and ownership are frozen in the plan validation budget.

Later validation: 370 tests, OK, 26 live MSSQL skips; fresh browser 25 finite
checks; image non-root/read-only health 200 with 18 fictional homes. Actual
process exits before commit and after commit/before response retain exact
case/audit and safe retry. Separate 500-row import/25-case Store workload passes,
not concurrent core HTTP import. Two 1800-second HTTP workloads pass, with
complete samples/errors/thresholds retained beside the acceptance register;
five/twenty sessions, two writers and five interactions/s, not exactly five
HTTP requests/s. Native browser
zoom, screen-reader/human UX, background/RPO drill and actual model/evaluation
acceptance remain open. Original Partial/Not accepted Review is unchanged;
later implementation does not regrade it or run a second Review.

Further continuation executes actual building/sibling and handoff/resident
browser fixtures with eleven controlled profile safe-block tasks. Final
headed Chrome/Xvfb run passes 53 finite checks, including native browser
400% zoom proven by devicePixelRatio/viewport, not CSS emulation.
Background batch interruption and isolated exact document-byte restore
are tested; missing acknowledged event is explicit and pending-recovery
marker prevents standard launcher startup. This is not scheduled backup
RPO or completed operator reconciliation. Updated runner starts separate
five-HTTP-request/s scale and mixed core import/bulk/document/event workload
for 1800 seconds. Exact scale passes, with raw p50/p95/max/error counts
retained. Strict mixed core passes with decimal evidence limits, exactly two
existing writers and 500/25 committed HTTP rows. Independent full controlled
field/trace/document/audit comparisons pass; initial cold startup was not
separately timed. Latest regression passes 374
tests with 26 live SQL skips; focused eleven-profile/six-template/eight
protected batch permission matrix passes, not all role/action combinations.
