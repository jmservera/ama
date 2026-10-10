---
title: Proper Warm Rebuild Requirement and Evidence Register
description: Exact PRD requirement inventory and independently bounded results
ms.date: 2026-10-10
---

## Interpretation

This register covers all 46 FRs, 56 ACs and 13 NFRs from the accepted PRD
v0.12.0. The result column is the **complete requirement**, not a proxy for
implementation or one passing unit test. Not run means its whole acceptance
shape was not executed; Blocked identifies a missing prerequisite; Fail
identifies a known implementation gap. No full-PRD acceptance is claimed.
The PRD's historical Not run columns are preserved unchanged.

## Executed Engineering Evidence

| ID | Evidence | Result and boundary |
| --- | --- | --- |
| E01 | mvp/tests/test_forms.py | 24 tests: six schemas, readable text/CSV, source lineage, conflicts, protected fields, validation, export and stale-set oracles. |
| E02 | mvp/tests/test_decision.py | 30 fake-only tests: registry/guard/response/abstention, catalog identity casing, retained cross-process liability, 20-way contention and generation/reading zero-transport denial. No actual model run or validated provider response schema. |
| E03 | mvp/tests/test_exercise_forecast.py | 19 tests: wholly fictional fixtures, exact central/sensitivity oracles, missing-input abstention and stage-pool independence. |
| E04 | mvp/tests/test_exercise_workbench.py | Twenty SQLite/API tests: one-home journey through cash/invoice closure, independent humans, source/sibling invalidation, exact financial reproductions including stale rejected retry, explicit handoff/commitment/hazard, atomic invalid-input and process-interruption probes. Focused finance fixtures explicitly freeze Handover and are not journey evidence. |
| E05 | mvp/tests/test_exercise_data.py | Local declared-workbook/bulk/export tests; inspect final suite count and implementation review for exact disposition. Narrow contract, not arbitrary stock import or XLSX export. |
| E06 | exercise-poc-rebuild-browser-results.json | Chrome 152.0.7977.75: 22 checks pass. Eleven role orientation views, nine navigation entries, parser conflict, form reflow at 320/390/1280px, root text resize, keyboard focus, input labels and no duplicate IDs/runtime errors. Not eleven completed role tasks or nine complete browser workflows. |
| E07 | exercise-poc-rebuild-runtime-results.json | 200 warm HTTP samples each: list p95 0.00164s, detail 0.00187s, dashboard 0.00364s, coordination write 0.00977s. One session/writer, 18 fictional homes and 201 update events; not the prescribed core/scale shape. Exact clean-restart case and backup case/audit-head equality pass. |
| E08 | mvp/Dockerfile | Image built; non-root/read-only exercise startup with writable temporary state passes. Includes required evals/registry. No deployed service, production readiness or Trivy result inferred. |
| E09 | Full MVP regression command | Latest follow-up: 370 tests, OK, 26 live MSSQL skips, 67.562 seconds. Original publication: 355 tests, OK. Existing legacy 60,000-row timing checks are not the new fictional 600,000-event workload. |
| E10 | mvp/tests/test_exercise_workbench.py financial reproductions | RV-001 through RV-004 corrected locally: exact predecessor staleness, current award readiness, cumulative cash across stale claims, unchanged rejected content refusal. Stale rejected attempts still require exact retry reference. Original Review remains Partial/Not accepted, not regraded. |
| E11 | exercise-poc-rebuild-browser-followup.json | Fresh Chrome run: 25 finite checks pass, including actual 32px body text, CSS 4x reflow, visible control targets >=24px and declared palette contrast >=4.5. Not native browser zoom, comprehensive contrast audit, screen-reader or representative human tasks. |
| E12 | exercise-poc-rebuild-data-results.json | Exact separate Store-level scale probe: 500 imported rows, 25 committed coordination cases, preview 0.089397s, source hash/controlled-field/audit invariants pass. Not concurrent core HTTP import or arbitrary stock ingestion. |
| E13 | mvp/tests/test_exercise_workbench.py process interruption | Actual child exits before save and after save/before response: exact case/audit retention, no partial commit and duplicate retry refusal. Not interruption during SQL commit/background tasks or disaster/RPO drill. |
| E14 | Shared inference liability guard | Scoring/generation reserve conservative upper charges atomically across SQLite connections/processes; 20 simultaneous callers at USD 400 with USD 1 charges admit exactly four before USD 405 pause. No refunds/rollover; actual price/invoice/operator reconciliation remains unavailable. |
| E15 | exercise-poc-rebuild-core-soak-results.json | 1800.037s, five authenticated sessions/two coordination writers, 9001 scheduled interactions, no failures; list/detail/dashboard/write samples 4920/2460/900/721, p95 0.010124/0.004759/0.006304/0.150626s, all below 1/1/3/2s. Clean restart 0.207754s and exact case/audit-head backup equality pass. |
| E16 | exercise-poc-rebuild-scale-soak-results.json | Separate 60000 fictional homes/600000 linked traces, 1800.046s, twenty authenticated sessions/two coordination writers, 9001 interactions, no failures; list/detail/dashboard/write samples 5100/2550/900/451, p95 0.098890/0.041894/0.048979/0.078726s, all below 1/1/3/2s. Clean restart 3.747456s and exact case/audit-head backup equality pass. |

The raw E06/E07 JSON files sit beside this register. Scripts and fictional
fixtures are reproducible; measured latencies are machine-specific observations.
These tests do not establish resident comfort/energy outcomes, reduced staff
effort, public funding approval, legal satisfaction or real company validation.

E15/E16 schedule five interactions/s, not exactly five HTTP requests/s:
coordination writes each perform preview and commit, yielding approximately
5.40/5.25 workload requests/s respectively, excluding login. E12 ran on a
different set of scale homes while the scale session was active; its import
was not a concurrently authenticated core HTTP import. Scale traces are
embedded linked fixture history, not 600000 separately posted audit events.
Both servers loaded the follow-up snapshot before later stale-retry/date/
model-casing/test-runner corrections; those later paths are separately covered
by E02/E04/E09, not claimed exercised by the workload. Full prescribed mixed
workload/RPO acceptance remains Not run despite these passing measurements.

## Functional Requirements

| Requirement | Full result | Engineering evidence or remaining boundary |
| --- | --- | --- |
| FR-001 | Not run | E04 home/building links; complete shared-building navigation not executed. |
| FR-002 | Not run | E03/E04 sibling independence; full shared-system applicability/cost view incomplete. |
| FR-003 | Not run | E04/E06 service checks and eleven orientation views; full role/action matrix outstanding. |
| FR-004 | Not run | Local blockers/queues; complete definitions/filter/default matrix outstanding. |
| FR-005 | Not run | E01/E04/E05 attributed edits; full permitted-field/history acceptance outstanding. |
| FR-006 | Not run | E05/E12 exact 25-case Store coordination preview/commit; full role/browser acceptance outstanding. |
| FR-007 | Not run | E04/E05 denied controlled bulk paths; complete action-denial inventory outstanding. |
| FR-008 | Not run | E04 independent gates and safe blocks; full gate matrix outstanding. |
| FR-009 | Not run | E01/E04 source/quality and earlier-stage returns; full domain invalidation/reopen matrix outstanding. |
| FR-010 | Not run | E04 retained source/quality and return receiver/source/next-action history; complete cross-view acceptance outstanding. |
| FR-011 | Not run | E04 explicit sent/received/accepted/returned/escalated/completed states and independent ownership/chase now tested; full role/browser fixture outstanding. |
| FR-012 | Not run | E01/E04 source conflict/reconciliation; whole cohort/authority/ranking acceptance outstanding. |
| FR-013 | Not run | E04 design and independent sign-offs; all professional/building-return variants outstanding. |
| FR-014 | Not run | Existing resident/service controls; full accessible-service/redress fixture outstanding. |
| FR-015 | Not run | E04 denies local release and tests separate supplied receipt/acceptance without clock changes; full awareness/referral/hold matrix outstanding. |
| FR-016 | Not run | E04 capacity/release; whole offered/committed/package/version matrix outstanding. |
| FR-017 | Not run | E04 independent QA, return/fix/reinspection/handover; full measure matrix outstanding. |
| FR-018 | Not run | E04 exact milestones/invoice/payment references; independent line-mismatch inventory outstanding. |
| FR-019 | Not run | E04 distinct application/award/claim/cash and rejected application retry; full unrelated-ledger oracle outstanding. |
| FR-020 | Not run | Existing map preserved; fictional filtered heatmap/table acceptance outstanding. |
| FR-021 | Not run | Existing analytics preserved; complete event-based funnel/reopen reconciliation outstanding. |
| FR-022 | Not run | E04 retained event order; historical durations/pause/reopen range contract outstanding. |
| FR-023 | Not run | E03 exact forecasts/E06 tables; complete authorized scenario UX acceptance outstanding. |
| FR-024 | Not run | Complementary stakeholder suppression; selected-cohort/as-of export contract outstanding. |
| FR-025 | Blocked | E02 registry/manual routing; actual source-linked generative task and evaluation unavailable. |
| FR-026 | Blocked | E04 narrative reject evidence; real suggestion accept/edit/review-effort runs unavailable. |
| FR-027 | Blocked | E02 fake-only and E04 zero-call checks; live scoring/generation unavailable. |
| FR-028 | Not run | E02/E04 manual continuation; whole workflow-only comparator inventory outstanding. |
| FR-029 | Not run | E05 declared literal-text XLSX preview/commit; complete acceptance/load shape outstanding. |
| FR-030 | Not run | E05 role-projected JSON portability; full approval/audit/forecast export comparison outstanding. |
| FR-031 | Not run | Existing strictly-greater-than-five rule preserved; complete exercise counted-event fixture outstanding. |
| FR-032 | Not run | Existing queue scope/reset preserved; exact per-profile default/focus/announcement oracle outstanding. |
| FR-033 | Not run | E04 independent purpose/due/basis/proposed/sent/reassignment commitment history tested; full resident route/browser fixture outstanding. |
| FR-034 | Not run | E04/E06 same-home ownership/blockers; cross-view unknown/reason consistency matrix outstanding. |
| FR-035 | Not run | E03 manifest/E06 orientation; exact defaults and complete eleven/nine scenarios outstanding. |
| FR-036 | Blocked | E02/E04 registry/default denial; live every-workflow/cross-cutting task evaluation unavailable. |
| FR-037 | Blocked | E02 validated fake envelopes; actual Decision 1 contract/probe unavailable. |
| FR-038 | Not run | E01/E04 six schemas/route/version controls; full workspace fixture acceptance outstanding. |
| FR-039 | Not run | E01/E04/E06 readable extraction and candidate lineage; actual selection evaluation unavailable. |
| FR-040 | Not run | E01/E04 individual manual review/source isolation; whole mixed-state UX matrix outstanding. |
| FR-041 | Not run | E01 deterministic validation oracles; complete integrated defect inventory outstanding. |
| FR-042 | Not run | E01/E04 reviewed application/claim packs; complete independent snapshot comparison outstanding. |
| FR-043 | Not run | E01/E04 exact source/input/version invalidation; whole downstream fixture manifest outstanding. |
| FR-044 | Not run | E02/E04 optional/off/manual/protected-field checks; complete throttled/provider-availability UX outstanding. |
| FR-045 | Not run | E04 scheduling-only rejection and existing measure controls; full two-measure fixture outstanding. |
| FR-046 | Not run | E03/E04 withdrawal/sibling isolation; full discretionary gate/choice oracle outstanding. |

## Acceptance Criteria

| Criterion | Full result | Evidence or missing check |
| --- | --- | --- |
| AC-001 | Not run | E04 partial; complete building navigation. |
| AC-002 | Not run | E04 partial; exact shared-package affected scopes. |
| AC-003 | Not run | E04 sibling isolation; building view comparison. |
| AC-004 | Not run | E04/E06 partial; complete perspective/action denial matrix. |
| AC-005 | Not run | E06 orientation only; all profile task endpoints. |
| AC-006 | Not run | Complete queue definition/filter/as-of fixtures. |
| AC-007 | Not run | E04/E05 edit history; complete independent prior/new/source comparison. |
| AC-008 | Not run | E01/E04 invalidation; full reopen matrix. |
| AC-009 | Not run | E05/E12 exact 25-case coordination batch; complete permission/browser selected-case acceptance. |
| AC-010 | Not run | E04/E05 denial tests; all controlled bulk attempts. |
| AC-011 | Not run | E04 blockers; full owner/correction-route matrix. |
| AC-012 | Not run | Complete return/reopen owner/stage/next-step oracle. |
| AC-013 | Not run | E01/E04 exact invalidation subset; full return fixture. |
| AC-014 | Not run | E04 urgency/due/next-action and independent update ownership tested; full cross-role fixture. |
| AC-015 | Not run | E03/E04 missing/conflict handling; full policy/hazard fixture. |
| AC-016 | Not run | E04 sign-offs; full competent-role assignment matrix. |
| AC-017 | Not run | Complete accessible service/redress request fixture. |
| AC-018 | Not run | E04 external authority boundary; full awareness/referral clock oracle. |
| AC-019 | Not run | E04 capacity/work order; full package view/version comparison. |
| AC-020 | Not run | E04 independent QA return/reinspect; all dependent holds. |
| AC-021 | Not run | E04 exact invoice milestones; imported mismatch/line-reference fixture. |
| AC-022 | Not run | E04 distinct events/rejected application; all unrelated-ledger invariants. |
| AC-023 | Not run | Fictional filtered map/table reconciliation. |
| AC-024 | Not run | Full entries/exits/returns/funnel reconciliation. |
| AC-025 | Not run | E04 history; complete duration/return timeline. |
| AC-026 | Not run | E03/E06 forecast subset; complete scenario selection flow. |
| AC-027 | Not run | Selected-cohort stakeholder export/approval comparison. |
| AC-028 | Blocked | Real suggestion task-only accept/edit and prerequisite evidence unavailable. |
| AC-029 | Blocked | E04 rejection subset; real output and paired review effort unavailable. |
| AC-030 | Not run | E02/E04 default/failure/manual subset; complete task matrix. |
| AC-031 | Not run | E05 literal XLSX errors/stale preview; whole frozen workbook acceptance. |
| AC-032 | Not run | E05 cohort JSON; all approval/supersession/audit export comparison. |
| AC-033 | Not run | Complete missed-appointment counted-event/reset/no-hazard-delay fixture. |
| AC-034 | Not run | Exact default IDs/order/focus/reset/zero-matches fixture. |
| AC-035 | Not run | E04 independent purpose/due/basis/proposed/sent/reassignment state tests; whole accepted browser/route fixture unexecuted. |
| AC-036 | Not run | E04 distinct destination/receiver/chase/receipt/acceptance/history tests; full cross-view unknown and consistency oracle unexecuted. |
| AC-037 | Not run | Full two-measure accessible service/redress fixture. |
| AC-038 | Not run | E04 supplied external receipt/acceptance preserves original awareness and hold; full referral/clock fixture. |
| AC-039 | Not run | E04 capacity subset; offered/committed/readiness UI oracle. |
| AC-040 | Not run | E01/E04/E06 EPC conflict; all designated comparison/rationale fixtures. |
| AC-041 | Not run | Complementary suppression subset; filters and illustrative-population comparison. |
| AC-042 | Not run | E04 QA/invoice subset; designated quantity-mismatch and positive-evidence fixture. |
| AC-043 | Not run | E03/E06 manifest/orientation; complete slice and exact default coverage. |
| AC-044 | Blocked | E02 denied task tests; every workflow/cross-cutting registered live task unavailable. |
| AC-045 | Not run | E02 fake response tests; complete designated response fixture matrix not adjudicated. |
| AC-046 | Not run | E01 six-template/version tests; complete integrated form selection fixture. |
| AC-047 | Blocked | E01/E06 actual parser subset; real optional selection evaluation unavailable. |
| AC-048 | Not run | E01/E04 manual review/source isolation; complete accepted/rejected/unknown UX fixture. |
| AC-049 | Not run | E01 deterministic unit/defect tests; independent integrated seeded-defect inventory. |
| AC-050 | Not run | E01/E04 pack export subset; every-field/attachment external-state comparison. |
| AC-051 | Not run | E01/E04 exact stale-set subset; full source/template/rule/downstream oracle. |
| AC-052 | Not run | E02/E04 offline/protected fields; complete disabled/throttled/unavailable browser matrix. |
| AC-053 | Not run | E01/E02/E04 source denial subset; complete cross-scheme/restricted/injection fixture. |
| AC-054 | Blocked | E02/E04 fake/default prohibition subset; actual model-answer authority evaluation unavailable. |
| AC-055 | Not run | E04 scheduling-only denial; exact two-measure design/source fixture. |
| AC-056 | Not run | E03/E04 isolation subset; exact affected discretionary readiness fixture. |

## Non-Functional Requirements

| Requirement | Full result | Evidence or missing gate |
| --- | --- | --- |
| NFR-001 | Not run | E11 actual text resize, CSS zoom, control targets and palette contrast pass; native browser 400% zoom, full contrast/screen-reader and representative human tasks not run. |
| NFR-002 | Not run | E15/E16 two 30-minute workloads pass with >=200 samples/op, five/twenty sessions and two writers. E12 exact 500/25 Store probe passes separately; complete prescribed mixed HTTP import/bulk/core shape and exact five-request/s fixture remain unexecuted. |
| NFR-003 | Not run | E04/E05 service denials; all role/record/field/action combinations not run. |
| NFR-004 | Not run | E04/E05 attribution and E07 exact audit head; complete controlled-event/agent-failure reconstruction not run. |
| NFR-005 | Not run | E03/E04 isolated fictional startup; independent full identifier/ingestion release inventory not assessed. |
| NFR-006 | Not run | E07 clean restart/backup and E13 exits before commit/after commit before response pass; mid-commit/background interruption and full RPO/reconciliation drills not run. |
| NFR-007 | Not run | E03/E06 reproducible forecast subset; whole authorized reviewer UX contract not run. |
| NFR-008 | Not run | E01/E05 lineage subset; whole imported/integrated field authority/owner matrix not run. |
| NFR-009 | Blocked | E14 shared cross-process liability evidence passes. Actual Decision 1/generation, human-adjudicated 120-family labels, paired effort, operator reconciliation and verified quota/terms/price unavailable. |
| NFR-010 | Not run | E05 JSON portability subset; independent audit/forecast/evidence export inventory not run. |
| NFR-011 | Not run | Guard/config/fallback documented; named release owner/monitoring/retention/rollback drills outstanding. |
| NFR-012 | Not run | E03/E06 forecast tables/suppression; full filter/denominator/non-colour/chart integrity inventory outstanding. |
| NFR-013 | Not run | E05 narrow auditable batch outcomes; whole permitted-field/permission/workload contract not run. |

## Blocking Work

Focused financial/handoff/update/return/hazard corrections now pass local
engineering checks; finish their complete role/workflow fixture acceptance
without weakening resident, professional, safety or Finance controls.
Run the exact prescribed workloads and failure/recovery/accessibility shapes
separately. An operator must verify the actual Decision 1 deployment/response
contract, processing terms/quota/prices and bounded charge authorization, then
reconcile a shared liability ledger before any billable adapter activation.
Keep the USD 450 monthly cap, USD 360 warning and USD 405 optional-work pause.
No broad new company research is required to finish these engineering gaps.

An explicit deployment/billable authorization and participant request returned
user unavailable. Read-only catalog eligibility (version 1, GlobalStandard)
does not clear that blocker; no cloud changes or actual inference were run.
