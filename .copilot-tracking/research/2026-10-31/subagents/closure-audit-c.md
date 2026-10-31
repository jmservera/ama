---
title: Closure audit lane C - focused deeper evidence
description: Read-only criterion-level closure evidence for issues 147 148 151 152 153 154 155 156 and 159
ms.date: 2026-10-31
---

## Boundary and result

* Parent: `.copilot-tracking/research/2026-10-31/closure-audit-batch1-research.md`.
* Source pin: main/HEAD `84035ae9605f7ab42744a3d6e9f620bb65126d99`.
* Inputs: supplied `issue-N.json` and `pr-N.json` snapshots in the session's `files/closure-audit-inputs`.
* All nine issues are OPEN. No whole closure supported: 17 of 45 criteria proven, 28 unproven. Two currently unchecked design-artifact criteria are supported (#154 criteria 1 and 4); this is not permission for resident use.
* Three existing ticks lack whole-criterion evidence under a literal reading: #147 criterion 3, #152 criterion 3 and #153 criterion 4. Parent owns any checklist interpretation or change.
* High confidence in no whole closure. Medium confidence in the literal own-queue/pilot-enable interpretations and design-only distinctions, because owner acceptance can change their intended reading. No missing approval is inferred.
* Only the two lane artefacts were written. No issue mutation, code changes, tests, live/cloud checks, private datasets, inference, deployment or nested delegation. Untracked parent evidence was preserved.

## Collection and reference qualification

Every assigned snapshot and candidate file inventory was inspected. Full bodies and file lists of substantive referencing PRs were read, including their historical evidence, adverse outcomes and later corrections. Relevant snapshot review states and check results were compared; gigantic unrelated reviewer boilerplate was not treated as closure evidence. None of these candidates has a 100-file capped list (largest assigned candidate: #503, 78 files), so no supplemental pagination is required for this lane.

The JSON `prs` retains every search candidate, in snapshot order. `referencing_prs` identifies exact, contextually substantive references, including negative acceptance evidence or requirement deltas. A title/body numeric match in a future dependency list or integration chronology is not automatically delivery. PR602 is additionally cited as an indirect current-main metering contribution, not added to the supplied candidate set or misrepresented as an exact #159 reference.

| Issue | All candidates | Substantive exact references | Exclusions and context |
| --- | --- | --- | --- |
| #147 | #500, #274, #385, #391 | #500, #274 | #385 image/demo selection and #391 neutral setup/default distinctions are broad matches, not exact #147 delivery references. |
| #148 | #511, #519, #516, #418, #460 | #511 | #519 briefing checker, #516 manager briefing, #418 priority challenge and #460 paper PDF are unrelated to rebuilding the Azure stack. |
| #151 | #427, #291, #244, #460 | #427, #291, #244 | #291 is substantive negative migration/reopen evidence, not an accessibility acceptance PR. #460 paper/PDF is unrelated. |
| #152 | #317, #401, #319, #380, #400, #477, #539, #423 | #317, #401 | #401 manually includes #152 in its trace/gap inventory, not functional completion. #319 mentions preserving merged #152 during resident-decision integration. #380 iteration manifest, #400 broader design gate, #477 paper, #539 map and #423 roster proposal are not exact #152 delivery. Some contribute shared UI/context indirectly, not whole closure. |
| #153 | #501, #242, #402, #502, #486, #403, #503 | #501, #242, #402 | #403 says no new web/#153 edits, an exclusion boundary, not delivery. #502 sensor bounds and #486 sensor backfill are unrelated. #503 chat hardening is indirect; its broad search result does not establish universal copy acceptance. |
| #154 | #501, #39, #357, #485, #484, #483, #482, #481 | #501 | #39 historical gap analysis, #357 source-image release and #481-485 climate/sensor stack are unrelated exact-reference matches. |
| #155 | #508, #501, #448 | None | #501 refers to future #155 testing as a dependency and expressly supplies no programme results/recruitment/approval. #508 IoT and #448 paper are unrelated. |
| #156 | #401, #400, #519, #357, #514, #516, #518, #376, #386, #503, #317, #402, #387, #313 | #401, #400 | #402's #156 mentions concern preserving #401's index/log during integration, not design delivery. The remaining broad matches deliver briefing, release, workspace, queue, grant, chat, IA, quality or Fluent slices; shared gate context is not an exact substantive #156 implementation reference. |
| #159 | #305, #556, #282, #307, #372, #433, #401, #503 | #305, #556, #307, #433, #503 | #282 names the then-future panel as an open dependency. #401 inventories its screen/gap, not chat implementation. #372 scored-SHA workflow is unrelated. #433 changes draft economics requirements, not implemented metering. |

## Reviewed evidence and checks

These are snapshot/committed historical observations, not new execution. A green hosted suite or rubric review never supplies human, AT, legal or deployed acceptance.

| PR | Reviewed evidence and observed check boundary |
| --- | --- |
| #274 | Bicep build/lint and governance tests; 565 historical MVP tests, 84 skipped. Snapshot two validate checks SUCCESS; no formal review entries. Initial body says expiry open, but current EX-001 now has a real date. No subscription deployment/what-if. |
| #500 | 452 infra tests, zero skips, 25 templates compiled, actionlint and compiled/mutation pilot matrix. Independent authoring-only Complete/Conformant; Defender/pilot live gates absent. Snapshot includes historical rubric CHANGES_REQUESTED then APPROVED and SUCCESS rollup; not actual Defender cost/activation approval. |
| #511 | Original 68 tests/22 external methods; latest order correction yields 23 methods and reviewed red/green Front Door trace. Original Review Complete/Not accepted, RV-001 diagnostic/partial-checkpoint loss remains outside refresh/order corrections. Latest review accepts bounded order source, not Azure rebuild. Snapshot source projects and MSSQL SUCCESS; AI/rubric activation jobs SKIPPED. Publication-gate ignored-input caveats remain historical/unresolved acceptance distinctions. |
| #244 | Initial hex-parser failure preserved, then 180 targeted tests pass; static checks rather than product conformance. Hosted test/validate/image/MSSQL SUCCESS. Body's historical `Closes #151` is contradicted by proposed owner target and every manual row Not run. |
| #291 | Documentation/migration inventory review, 703 historical baseline tests/92 skips; validate SUCCESS. Explicitly calls for reopening #151; parity links do not prove accessibility. |
| #427 | Reviewed bounded contrast correction and exact-head full gate claimed; transition negative/positive evidence kept distinct. Snapshot src-api/source projects/MSSQL SUCCESS, activation-related jobs SKIPPED; comments retain exact-head/hosted caveats. Body expressly disclaims whole-product/AT acceptance. |
| #317 | Complete browser suites recorded after briefing-cache RV-001 red/green correction; 498 API tests/98 skips in follow-up. Original Review Complete/Defects found preserved, RV-001 fixed but device/full-manifest/live-human residuals remain. Snapshot source projects/image/MSSQL SUCCESS. Existing eight auth roles/five widths are not all eleven perspectives/nine workflows. |
| #242 | 422 historical tests/73 skips, hosted test/validate/image/MSSQL SUCCESS. No reviewer entries; body `Closes #153` overstates named wording/universal coverage, which it also says remain open. |
| #402 | 100 integration tests/zero skips, historical browser 17 states/149 targets/zero detected violations but eight contrast incompletes, actual local non-root image evidence. Independent bounded Conformant, not universal copy/human acceptance; snapshot source projects/MSSQL/image SUCCESS. |
| #501 | Independent bounded Conformant; 139 targeted tests/51 skips, separately enabled browser test, design/workbench browser passes and constrained synthetic callback. Actual resident wording/usability/AT not run. Snapshot SUCCESS rollup and rubric APPROVED entries do not approve resident communications. |
| #400 | Original finite 15-row Review Complete/Conformant; link/table/pin checks, no executable tests required for docs-only work. Snapshot checks empty, not passed. Recorded design gate remains Blocked. |
| #401 | Exact 184-issue/74-screen reconciliation and 251 link/anchor targets checked; original critique Partial/Blocked preserved, independent inventory Review Complete/Conformant. Snapshot checks empty. All 74 current screen-design versions missing; finite snapshot is not current universal design completion. |
| #305 | Core/agents/API and companion project tests/lint/mypy, real synthetic keyboard-only browser run; 92 API skips. Snapshot source projects/image/MSSQL SUCCESS. Body leaves screen-reader/live-model/resume/streaming boundaries open; controlled proposal success is not inferred from denial-only tests. |
| #307 | Synthetic 21-scenario evaluator, 258 core/62 agents/458 API with92 skips; hosted source projects/image/MSSQL SUCCESS. Explicit known grounding gaps and missing thresholds/reviewer/held-out/live/human evidence; builds on #159, not full acceptance. |
| #433 | Requirements-only Tokenomics proposal. Snapshot SUCCESS rollup, rubric APPROVED entries and comments retaining missing full-gate/exact-head/human review boundaries. No price/budget/target or applied consumption controls approved. |
| #503 | Original Review Complete/Not accepted, development24 scenarios/61 turns fail/disabled, 59 consumption entries, zero actual model calls; normal-process receipts not crash-safe billing. Later correction reviews scoped Conformant without rewriting adverse original. Snapshot source projects/MSSQL SUCCESS; activation/rubric jobs SKIPPED. Later SQL/role/audit corrections and current source checked; initial-role-denial receipt gap remains. |
| #556 | 106 chat tests/one skip, syntax/static and real Playwright checks; focus defects fixed. Snapshot source projects/MSSQL SUCCESS, activation-related jobs SKIPPED, later reviewer comments retain scroll/consent/focus human concerns. Broader case browser has unchanged baseline layout failure. No live/AT acceptance. |
| #602 (indirect) | Body and current chat metering contribution inspected; source/financial attribution now present. Its original adverse parent Review and residual publication/full-gate failures remain distinct from source checks. It does not name #159 or establish every pre-dispatch denied turn receipt. |

## Criterion dispositions

The JSON carries all 45 exact checkbox texts, original checked state and source/test line anchors. Both `-` and `*` checkbox styles were considered; assigned issue snapshots contain 45 criteria, including #159's additional Tokenomics criterion. No additional checkbox in PR review/plan bodies was substituted for an issue criterion.

* #147: 2/4 proven. Bicep/management and exception register meet their authored-record criteria. Defender coverage/cost approval missing; actual pilot locks/tag inventory absent, despite code guards.
* #148: 0/4 proven as an Azure rebuild. Local perform/verify/teardown/seed/dry-run rehearsal is useful partial evidence, not helper integration or a disposable Azure exercise. Original failure-checkpoint evidence gap persists.
* #151: 2/6 proven. CI checks and honest statement draft exist. Owner target/scope, full audit, manual all-role AT/keyboard and accessible-equivalent acceptance remain unproved. Table strings and polite live regions are not screen-reader results.
* #152: 2/5 proven. Defined-width reflow and open-hazard preservation are reviewed engineering checks. Supported-device decision and full AC-034/043 remain missing. Literal own-only navigation conflicts with `All permitted open cases`; no simulator does not resolve that first clause.
* #153: 1/5 proven. Standard/glossary exists. Eight-file lexical audit excludes dynamic messages/visible stored wording; three-part final-check examples do not cover all failures. Latest reviewed audit calls reviewed-draft authority coverage Partial (`content-standard.md:194`). Appointed Juan Manuel Servera has no evidenced exact-version wording review (`content-standard.md:199-206`).
* #154: 2/5 proven at design-artifact level only. J1-J6 cover all task topics; J3 wireframe distinguishes offers/responses/confirmed commitments. Non-digital accessibility/service availability and actual representative-view expiry enforcement remain specified, not observed. No design/use validation is supplied. Parent may choose not to tick any design-only criterion until its intended acceptance interpretation is resolved.
* #155: 0/5 proven. Learning bundles and resident scripts are inputs, not a complete moderated programme plan/results. SA-009 thresholds remain proposals: at least 80 percent of 5-8 Excel users per role, find case/next step/owner under 5 minutes unaided and SUS at least 70. No participant/results denominator, consent/data protocol, staff audit-use agreement, severity-linked user findings or negative/inconclusive moderated outcomes exists.
* #156: 3/4 proven. Decision log, accessibility/content definition of done and KB indexing exist. Complete finite issue classification cannot replace missing current designs/journey-flow gaps; recorded overall gate is Blocked.
* #159: 5/7 proven for structural synthetic engineering. Optional permitted case panel, citation/label/abstention contract, current-context permission checks, no controlled-write/proposal-only boundary and clear workflow fallback are asserted by substantive tests. Semantic grounding is still a separate known failure. Screen-reader acceptance absent. Tokenomics bounds/normal receipts exist, but denied-role checks precede receipt initialization and every-turn coverage is not asserted; Unknown usage/cost is not zero.

## Blocking uncertainties and confidence

* Exact owner decisions must be independently supplied, not reconstructed from merge/rubric state: Defender coverage/cost/activation, pilot enablement, supported devices, WCAG target, resident wording, OD-41/42 services/authority and staff audit-use agreement.
* No local source/test can supply resident consent, actual screen-reader announcements, human comprehension, legal/retention approval or Azure rebuild/lock observations.
* Old `mvp/` acceptance paths were mapped to existing `src/` tests/source; a migration or filename alone was not proof. Static tests were read for actual assertions.
* The #154 design versus implemented-view interpretation and #152 own versus all-permitted scope are deliberately exposed for the parent, not silently resolved. Regardless of those interpretations, both issues retain other explicit blocking criteria.
* No fresh suite was run: passing counts above are reviewed historical evidence. No receipt validity, actual current platform health or human acceptance was independently certified by this lane.

## Final clarification: #154 C1/C4 check coverage

Initial criterion texts, numbering, design-only findings and no-closure result
are retained. The distinction below is important: there is extant independent
document/source assessment, but no evidenced executable test that asserts all
six J headings/topics or the three exact J3 design strings.

The existing independent Review at
`.copilot-tracking/reviews/logs/2026-10-27/resident-content-153-154-review.md:78`
reconciles J1-J6/R1 with plan AC2/AC3/AC4. Its completed-work row at `:94`
records "Each task includes choices/status, receipt, responsibility/recovery
and non-digital equivalent", validation "Requirements and atlas comparison;
links/anchors passed", and assessment "AC2/AC3/AC4 met as design evidence
only". The reviewed plan at
`.copilot-tracking/plans/2026-10-27/resident-content-153-154-plan.md:74-75`
explicitly names the six required topics. These are documented independent
source comparisons, not runtime or human-user acceptance.

| Issue criterion | Exact design source in `docs/reference/research/ux/customer-journeys/residents.md` | Extant check and limitation |
| --- | --- | --- |
| C1: measure choice | `:149-160`, J1; `:159` explicitly offers agree/do not agree/more information/later for this measure | Reviewed plan AC2 topic and independent six-task assessment at Review `:94`; no executable topic assertion |
| C1: pause/withdrawal | `:175-181`, J2; `:180` names pause/withdraw this measure | Same documented requirements/atlas comparison |
| C1: appointment options | `:196-205`, J3; `:202` names suitable option/another time/postpone/support | Same documented requirements/atlas comparison |
| C1: update commitments | `:218-229`, J4; `:223` names owner/due date/basis/channel, `:227-229` describes commitment ownership | Same documented requirements/atlas comparison |
| C1: handover | `:237-249`, J5; `:241-244` separates quality/handover and help/aftercare ownership | Same documented requirements/atlas comparison |
| C1: complaint/remedy status | `:259-272`, J6; `:266-267` separates complaint response/remedy/defect/closure and keeps open remedy visible | Same documented requirements/atlas comparison |
| C4: offer versus response versus confirmation | `:200` says "Offered - not booked"; `:203` says response recorded/"Waiting for confirmation"/not agreement to works; `:204` says "Visit confirmed" only after the three named confirmations | Reviewed phase details `resident-content-153-154-phase-details.md:42-44` require visit offer/confirmation candidate copy; Review `:94` assesses each task's choices/status. No dedicated J3 three-string assertion or comprehension result is recorded |

The independent document integrity result is specifically Review `:422`:
in-memory relative-link/GitHub-style heading-anchor check and Markdown diff
inspection passed for both changed UX documents and new index anchors.
`resident-content-153-154-changes.md:64` reports the same Markdown/local-link
check. Those checks establish structural integrity; neither claims to
automatically assert six-topic completeness or booking-state semantics.

The actual content tests at `src/api/tests/test_content_standard.py:87-89`
assert headings/wording in the **content-standard document**, not J1-J6 in
`residents.md`. Methods at `:91-99` and `:101-110` assert application
draft/representative/proposal copy, not the J3 design wireframe. Review `:97`
and `:420` restrict the three regressions/rendered callback to those changed
literal-copy paths. Their passing counts must not be relabelled as tests of
these two design criteria.

C1/C4 therefore retain support through the reviewed document requirements
comparison at their design-only scope. If the owner additionally requires an
executable semantic document assertion, that validation requirement is not
evidenced by the extant scoped checks. No new test, application execution,
runtime/UI edit or broadened discovery was performed for this clarification.
