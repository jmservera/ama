<!-- markdownlint-disable-file -->
# Review: AI consumption economics

## Scope and Evidence

* Task ID: 432
* Review date: 2026-10-31
* Review scope: full source-only task and issue acceptance/gap evidence.
* Assessed source HEAD: 9cce5c23545678d46821613b8df0a53a7c00762c
* Current reviewed main base: 1330869ea675ff019958846330108b4f45e163ce
* Plan: .copilot-tracking/plans/2026-10-31/ai-metering-432-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/ai-metering-432-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-31/ai-metering-432-changes.md
* Research: .copilot-tracking/research/2026-10-31/ai-metering-432-research.md

## Opening Review State

* Interpreted review goal: independently assess source correctness, complete
  planned wiring, critique dispositions and honest issue acceptance evidence.
* Evidence readiness: P01/P02 markers, details and changes reconcile; requested
  discovery passes 1436 tests with 320 opt-in skips, component static checks and
  24 core/six local HTTP tests pass. Original adverse results remain recorded.
* Acceptance basis: issue #432, source-only user boundaries, current plan and
  PC-001 through PC-008 dispositions; no whole-issue closure or live approval.
* First comparison boundary: existing-ledger admission and transport/output/
  review composition against completed P01-T01/P01-T02 and tests.
* Active read-only boundaries: all source, prior artifacts, docs and state;
  only this canonical review record may be written.
* Initial blockers: applicable operational prices/OD-51/billing/held-out
  authority unavailable; final committed full gate and hosted/human approvals
  remain separate post-Review publication/acceptance requirements.
* Base reconciliation: after the source-only implementation commit, current
  main advanced once more only in coordinator agent documentation (#599).
  A non-rewriting topic merge preserves the current-main ancestry, without
  changing cost-ledger code or attributing baseline changes to this issue.

## Execution Status

* Execution status: Complete.
* Review execution evidence: the one original independent post-implementation
  Review completed on 2026-10-31 against the source HEAD and main base above.
  All 29 owned changed files were assessed, including all ten changed runtime
  modules, three test files, the test typing override, component/economics
  documentation and original RPI evidence. The opening state above is preserved.
* Mandatory intake: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md,
  docs/reference/memory.md and
  docs/reference/research/sector/housing-association-primer.md. Exact issue
  acceptance text was read with `gh issue view 432 --repo jmservera/ama --json
  title,body`; no GitHub state was changed.
* Independent execution used only constructed in-memory SQLite data, synthetic
  references and existing test source. No credential files, private datasets,
  ignored answer keys, Azure, deployment, model network call, nested agent,
  source edit or Git write was used. Only this record was written.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Closed consumption events, immutable price/authority/billing, serialized admission and economics | Reconciled as implemented, not accepted | RV-001 to RV-004 expose lifecycle/admission/financial coverage defects despite implemented contracts. |
| P01-T02 | Ai transport, worker contexts, assistant/legacy/chat joins and manager report | Reconciled as implemented, not accepted | Actual review transaction and legacy save ordering conflict with the new attribution semantics; RV-001/RV-004. |
| P02-T01 | Two modules/30 methods, guides, pitch brief and local static/regression/discovery evidence | Reconciled with coverage limitations | No regression removal or UI change. The tests do not cover the verified defect sequences; RV-005 identifies remaining promised composition coverage. |
| Final publication dependency | Original Review, final evidence commit, complete gate and immediate receipt verification | Open by design | No full gate or exact-head receipt exists yet; this Review does not substitute for either. |
| Follow-Up Items | OD-51, applicable prices/billing, authorised batch and resident financial join | Reconciled as distinct follow-up work | RV-006; not added to active implementation or falsely classified as source defects. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/ai_consumption.py | Dedicated ai-consumption-v1 partition in existing assistant_events; no new DDL or database | Full module read; closed event keys, bounded scan, serialized port, exact decimal arithmetic, reservation/settlement/report trace | Existing 24 semantic methods passed with Review-owned memory-only fixtures; independent adverse sequences below | Substantial implementation; RV-001/RV-002/RV-003/RV-004 prevent acceptance. |
| P01-T02 | src/core/src/zava_forward/core/ai.py; src/core/src/zava_forward/core/assistants.py; src/agents/src/zava_forward/agents/dispatch.py | Financial admission before provider, explicit context inside provider threads, cached usage and opaque IDs through shaping | Complete changed-source trace, existing transaction/thread/fence context, new assistant composition test | Implementation reports six loopback tests and affected regressions passing; actual Assistants.review independently reproduced with synthetic SQL rows | Financial settlement is independent of proposal fencing; withdrawal is nevertheless blocked by RV-001 and pre-network hold enforcement is incomplete under RV-002. |
| P01-T02 | src/core/src/zava_forward/core/ai_registry.py; src/core/src/zava_forward/core/ai_tasks.py; src/core/src/zava_forward/core/store.py | Legacy result/output/review provenance | Envelope fields and save/event ordering read in full changed boundary | Memory-only fault injection executed actual ai_tasks.review; existing legacy regressions use nonmetered doubles | RV-004: a committed legacy acceptance can lose its financial review join without report incompleteness. |
| P01-T02 | src/agents/src/zava_forward/agents/chat.py; src/core/src/zava_forward/core/chat_panel.py | Cached tokens and successful meter identities survive chat adapters; chat output deliberately ineligible | Call context, ModelReply, usage normalization and finish/error branches assessed | Existing adapter regressions reported passing; no new metered chat composition assertion | Ineligible chat is not a proposal denominator. Failed/revoked calls retain financial liability but can remain unjoined; that conservative Unknown is not itself a defect. RV-005 remains. |
| P01-T02 | src/api/src/zava_forward/api/server.py | Existing manager-only report gains aggregate consumption, explicit period validation and unavailable-SQL response | Existing role check preserved; unknown/empty/repeated parameters rejected; no UI or HTTP write endpoint | Existing manager-role regression plus new loopback report test, as implementation evidence | Aggregate consumption does not export historical content-bearing events. It inherits RV-004's incomplete review-join detection. |
| P02-T01 | src/core/tests/test_ai_consumption.py; src/api/tests/test_ai_consumption_api.py; src/api/tests/test_assistants.py; src/api/pyproject.toml | 24 core and six API methods; old envelope test gets a mock meter; narrow untyped-call test override | Diff shows zero removed tests, two new modules, 30 additions within maximum 35 | Static/discovery/regression evidence assessed below | Passing doubles do not prove metered withdrawal, fault recovery or every promised adapter composition; RV-005. |
| P02-T01 | src/core/README.md; src/agents/README.md; src/api/README.md; docs/reference/resources/ai-tokenomics.md; docs/capstone/pitch/tokenomics-pitch-brief.md | Component interface, source-only economics and pitch gap documentation | All owned changes read; relative targets and evidence labels reviewed | Documentation/diff review; no repository documentation build exists | Operational caveats are explicit. Engineering assurance claims must be reconciled with RV-001 to RV-005 during correction. |
| P02-T01 | docs/reference/resources/azure-ai-price-source-2026-10-31.json; docs/reference/README.md; docs/reference/log.md; .copilot-tracking/documentation/2026-10-31-session.md | Dated price retrieval availability and maintained knowledge index/log | Null numerical/applicability fields, source/version/hash and append-only new log entry | Source/diff review only; no price retrieval repeated | Retrieval metadata is not a usable numerical price, invoice, owner approval or live cost. |
| P01/P02 evidence | .copilot-tracking/research/2026-10-31/ai-metering-432-research.md; .copilot-tracking/plans/2026-10-31/ai-metering-432-plan.md; .copilot-tracking/details/2026-10-31/ai-metering-432-phase-details.md; .copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-plan-critique.md; .copilot-tracking/changes/2026-10-31/ai-metering-432-changes.md; .copilot-tracking/rpi-sessions/2026-10-31/ai-metering-432-state.json | Original ordered research/critique/implementation evidence and parent state | All read; original Revise retained; current active phase Review | Evidence reconciliation, not another critique or state mutation | Plan markers describe executed work, not defect-free acceptance. Parent owns subsequent state/evidence reconciliation. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01, PC-001/002/004/006/007 | Deterministic identities, closed partition, sticky holds, exact arithmetic and billing/quality formulas | Original critique; confirmed source-only boundaries, not live financial approval | Final-candidate contract addendum appears in details and aligns with plan/changes | Original Revise preserved; direct dispositions, no second critique | Direction is compatible. Implementing the words does not prove the sequences; RV-001 to RV-004. |
| P01-T02, PC-003/005 | Explicit worker contexts, cached usage, eligibility and SQL versus legacy joins | Actual thread/reducer/save boundaries identified by critique | Concrete source files and join limitations included in details/guides | Direct compatible dispositions | SQL review hook is atomic but prevents an existing valid transition. Legacy incomplete review coverage is not actually detectable as claimed. |
| P02-T01, PC-008 | Two modules, 30 methods, per-criterion local/operational matrix | Caller test budget and exact acceptance requirements | Details and Tokenomics matrix preserve all nine operational limitations | Direct disposition recorded | Addition/removal limits are met; promised composed/fault coverage is not fully met, RV-005. |
| P01-T01/P01-T02 hardening | Reject synthetic production prices, post-token expiry/staleness check, currency reuse and 30-decimal arithmetic | Implementation discoveries reported in changes; no expanded spend authority | Relevant source and semantic tests assessed | Compatible hardening of the accepted direction | Synthetic transport/provenance and arithmetic cases are supported. RV-002/RV-003 show incomplete hardening. |
| Base ancestry | Integrate upstream main without rewriting source history | Upstream transport ancestry and later coordinator documentation #599 | Supplied base is merge-base; HEAD remains 9cce5c23545678d46821613b8df0a53a7c00762c | No new planning/critique scope inferred | No unrelated upstream features attributed to this issue. |

## Critique and Material Revision Assessment

* Latest critique dispositions: all PC-001 through PC-008 have directly applied
  contract dispositions in phase details. The original verdict Revise and its
  adverse rationale are retained, not rewritten into a passing critique.
* Material revisions: identity/privacy/admission/billing/quality contracts
  preserve the confirmed source-only direction. Production synthetic-price
  rejection and exact arithmetic are compatible corrections, not permission
  for paid inference or an invented OD-51 decision.
* Dependent-work pause assessment: the supplied ordered evidence puts
  implementation after the critique dispositions and Review after completed
  P01/P02 reconciliation. No contrary early-resumption evidence was found.
* Justification assessment: recording separate resident/historical coverage,
  missing real prices/billing/authority and unchanged deck is justified.
  PC-001/004/005/008 completion claims do not establish correctness where
  RV-001 to RV-005 remain. No second critique or Review was executed.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| OD-51 denominator, quality floors, budgets, alert owners and TCA inventory | Human business/financial decisions cannot be inferred from fixtures | Owner with Finance and accountable programme/quality owners | Open, distinct operational follow-up under RV-006; not a source defect. |
| Applicable actual numerical prices, attributable Azure billing/allocation and tolerance | Public retrieval has placeholder cells; no authorised financial records supplied | Finance and authorised operator supply dated evidence and approve applicability | Open, distinct operational evidence follow-up under RV-006. |
| Owner-authorised held-out measured batch and released effort | No paid inference or actual employee measurement authorised in this task | Owner authorises finite spend and measurement; evaluation/Finance owners retain approvals | Open, distinct operational follow-up under RV-006. |
| Resident/historical financial composition | Existing resident SQL controls and historical calls are expressly unjoined | Core/API accounting owner plans a separate source delivery; deployment owner controls any later activation | Open, distinct follow-up under RV-006; existing resident reservations remain unchanged. |
| Actual slide placement, rebuilt/rehearsed pitch and final challenge | This delivery updates the brief/Q&A draft, not a deck | Owner/presentation owner updates and rehearses actual assets with evidence labels | Open, distinct presentation follow-up under RV-006. |

Unresolved plan follow-up items remain distinct follow-up work. They are not
new active P01/P02 tasks merely because their operational criteria remain open.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Immutable first review prevents withdrawing a metered accepted assistant proposal

* Related scope: P01-T01/P01-T02, PC-005/007; existing human review lifecycle.
* Evidence: src/core/src/zava_forward/core/ai_consumption.py:594-600 rejects
  any changed disposition. src/core/src/zava_forward/core/assistants.py:1067-1068
  calls it inside the authoritative review transaction. Existing
  src/api/tests/test_assistants.py:192-207 explicitly permits edit-accept followed
  by reject, but its ordinary fake provider supplies no meter root.
* Independent observation: actual Assistants.review on a synthetic accepted
  SQL row with existing metered acceptance raised `ValueError: Review
  attribution is immutable.` The transaction rolled back, leaving
  authoritative state/revision `('accepted', 1)`. Direct ledger accept-to-reject
  likewise failed and accepted_proposals stayed 1.
* Impact: adding metering removes an existing human withdrawal path and keeps
  an outcome in the accepted denominator. Immutable evidence should preserve
  prior dispositions, not make the first disposition irrevocable.
* Destination: rpi-implement.
* Smallest useful next action: append later review transitions without rewriting
  earlier events, derive the latest disposition as of the report cutoff, retain
  idempotent replay, and extend the metered assistant composition test through
  accept/edit-accept then reject.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: A reservation awaiting credentials can dispatch after a shared-budget liability hold

* Related scope: P01-T01/P01-T02, PC-001/004; unknown liability stops dispatch.
* Evidence: src/core/src/zava_forward/core/ai_consumption.py:466-495 rechecks
  only price/authority expiry and that reservation's age.
  src/core/src/zava_forward/core/ai.py:91-95 invokes this check after token
  acquisition and immediately before HTTP. Budget holds are checked only
  during reserve, at ai_consumption.py:401-413.
* Independent observation: reserve A and B against the same budgets; while A
  awaits credentials, complete B with absent cached usage. dispatch_check(A)
  returned successfully despite B's sticky hold. A fresh root's reservation
  was correctly denied with `liability-unknown`, proving the intervening hold
  exists but does not govern the pre-network boundary.
* Impact: a caller that has not yet reached the provider can start billable
  work after the system already knows an intersecting budget has unknown
  liability. Serialized admission alone does not enforce the promised stop at
  this later dispatch boundary.
* Destination: rpi-implement.
* Smallest useful next action: re-evaluate durable held/unknown liabilities
  for all budgets of the reservation at dispatch_check, record the owned
  workflow-only denial, and test this token-wait interleaving with zero later
  fake-provider dispatch.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Deferred price registration bypasses the shared-budget currency invariant

* Related scope: P01-T01, PC-001/006; exact currency budgets across authorities.
* Evidence: src/core/src/zava_forward/core/ai_consumption.py:302-308 compares
  currencies only if both referenced prices are already recorded.
  authorize permits missing price references; price registration and reserve
  do not revalidate existing shared-budget currencies.
* Independent observation: create an authority referring to a deterministically
  known but not yet recorded USD price ID; create a GBP authority with another
  configuration sharing the same budget IDs/limits; register the deferred USD
  price. Both authorities then admitted and completed a call. The recorded
  shared-budget currencies were `['GBP', 'USD']`, with two admitted calls.
* Impact: the same durable monetary limit can aggregate different monetary
  units. Report currency Unknown is too late to restore the admission guarantee;
  the normal known-price cross-currency test does not cover this legal ordering.
* Destination: rpi-implement.
* Smallest useful next action: enforce an immutable budget currency binding
  even for deferred prices, or fail closed on unresolved currency when sharing
  a budget, and revalidate at price/admission boundaries. Add the deferred-price
  sequence without resetting existing liability or inventing exchange rates.

<!-- rpi:review id=RV-004 -->
### RV-004 [High]: Lost legacy review joins leave committed acceptance invisible to financial coverage

* Related scope: P01-T01/P01-T02, PC-005/007; explicit incomplete cross-store joins.
* Evidence: src/core/src/zava_forward/core/ai_tasks.py:380-382 and
  src/core/src/zava_forward/core/store.py:940-943 commit authoritative review
  before the financial review event. Already-reviewed records cannot retry
  that operation. ai_consumption.py:674-684 detects missing outputs, not missing
  authoritative review links; lines 705-711 can still publish a money ratio.
* Independent observation: actual ai_tasks.review with an injected ledger-link
  failure saved `Accepted`, then raised `constructed-link-failure`. Retrying
  raised `This AI output has already been reviewed.` With another joined
  accepted root, exact synthetic billing and two output joins, report returned
  coverage `recorded-ledger-only`, unjoined_outputs 0, accepted_proposals 1 and
  cost_per_accepted_proposal `0.000270`, although both authoritative outputs
  were accepted.
* Impact: the documented best-effort alternative does not expose this missing
  review join. The report cannot distinguish genuinely unreviewed work from
  a failed attribution of an already-committed acceptance, so its denominator
  and qualified economics can be wrong while coverage appears complete for
  the recorded ledger.
* Destination: rpi-implement.
* Smallest useful next action: reconcile existing authoritative legacy review
  records or persist recoverable join status so failed links remain visible;
  prohibit financial qualification until authoritative review joins reconcile.
  Preserve the successful human save and support idempotent repair, with
  fault-injected review/output save-order tests for both legacy paths.

<!-- rpi:review id=RV-005 -->
### RV-005 [Medium]: Promised metered adapter composition is not covered by the delivered test boundary

* Related scope: P02-T01, PC-003/005/008.
* Evidence: src/api/tests/test_ai_consumption_api.py has six methods covering
  metered assistant success, low-level admission, image denial, fan-out,
  money denial and manager report. It does not compose successful metered
  legacy text/output/review, employee ChatModel/ChatPanel, or AgentWorker.dispatch.
  Existing test_ai_tasks/test_chat_model/test_dispatch tests retain ordinary
  doubles and do not assert the new financial joins. Core lost-output tests
  are direct ledger tests, not cross-save fault composition.
* Impact: the exact resolving evidence requested by the original critique is
  incomplete. Broad discovery success cannot establish preserved metered
  identities, cached usage and human review across these changed adapters;
  RV-001/RV-004 demonstrate concrete failures concealed by nonmetered doubles.
* Destination: rpi-implement.
* Smallest useful next action: parameterize the existing two new modules
  within their 35-method cap to exercise these actual adapters with local
  synthetic transport and assertions for root/attempt/config/prompt/cached
  provenance, output eligibility and failure/review joins. Update the
  completion matrix to the evidence actually obtained.

<!-- rpi:review id=RV-006 -->
### RV-006 [Low]: Whole-issue financial, coverage and pitch acceptance remains distinct operational work

* Related scope: original issue #432 criteria 1 and 3-9; plan Follow-Up Items.
* Evidence: exact issue acceptance text, phase-details acceptance addendum,
  docs/reference/resources/ai-tokenomics.md source-only matrix,
  docs/reference/resources/azure-ai-price-source-2026-10-31.json null applicable
  rates, and docs/capstone/pitch/tokenomics-pitch-brief.md unchanged-deck boundary.
* Impact: even corrected source cannot prove actual owner-approved OD-51,
  attributable Azure reconciliation/tolerance, authorised paid held-out
  measurements, Finance-booked cash, full historical/resident joins or
  updated/rehearsed actual pitch assets. Declaring any of these delivered
  would exceed evidence and authority.
* Destination: distinct residual-work owners, not active rpi-implement,
  rpi-plan or rpi-research defects.
* Smallest useful next action: Owner/Finance approve and supply the financial/
  measurement inputs; accounting owners separately scope missing joins;
  presentation owner updates/rehearses actual assets. Maintain Refs #432
  with unmet criteria explicitly open, without a closing keyword.

## Defects

* RV-001 through RV-004 are independently verified source defects routed to
  rpi-implement. RV-005 is missing promised implementation validation, also
  routed there. No source fix was made during Review.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Parent/implementer restores append-only review transitions and as-of state | Existing human lifecycle regression within accepted direction. |
| RV-002 | rpi-implement | Parent/implementer enforces shared-budget holds at pre-network check | Concrete dispatch interleaving defect. |
| RV-003 | rpi-implement | Parent/implementer closes deferred-price currency reuse | Concrete monetary identity invariant violation. |
| RV-004 | rpi-implement | Parent/implementer makes legacy review joins recoverable/visibly incomplete | Concrete committed-review/report composition defect. |
| RV-005 | rpi-implement | Parent/implementer completes bounded synthetic adapter/fault tests and evidence matrix | Delivered test coverage falls short of the applied critique contract. |
| RV-006 | Distinct operational/accounting/presentation follow-up | Owner, Finance, accounting and presentation owners | Explicitly deferred live acceptance, not an introduced source defect. |

Later implementation of a routed finding does not require another Review.
Preserve this original outcome, execute corrections and their evidence, and
retain the separate independent exact-head publication assessment.

## Residual Work

* RV-006 remains open with the owners/actions in Plan Follow-Up Assessment.
* No new deployment, paid batch, live authority, financial rule, resident
  stored-procedure change, historical migration or deck rebuild is authorised.

## Blockers and Remaining Work

* Review execution blockers: none; the bounded source/evidence assessment
  completed. Operational items in the preserved opening are whole-issue
  acceptance blockers, not reasons to fabricate a source result.
* Remaining active work: correct RV-001 to RV-005 in the existing P01/P02
  direction, reconcile parent changes/details/state and update related
  engineering assurance claims. Complete markers do not waive these findings.
* Publication blockers: material source/validation findings; final evidence
  commit and fresh complete local gate/receipt verification are still required.
  Actual Chromium, SQL and scanner groups may not be replaced by these
  synthetic tests, skips, cloud execution or historical receipts.
* Hosted and human approval remain separate. No push, PR approval, issue
  completion or merge was performed by this Review.

## Validation Evidence

| Command | Scope | Status | Summary |
| --- | --- | --- | --- |
| `git status --short`; `git branch --show-current`; `git rev-parse HEAD`; `git diff 1330869ea675ff019958846330108b4f45e163ce HEAD`; `git merge-base HEAD 1330869ea675ff019958846330108b4f45e163ce` | Assessed source/base and 29 owned files | Passed | Branch feat/ai-metering-432; supplied HEAD/base confirmed; only existing authorised Review record untracked. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/core/src:src/core/tests python3 -` with in-process MemoryPort setup and existing ConsumptionTests loader | All 24 existing core semantic methods with memory-only fixtures | Passed | 24 methods, 0.041 seconds. No file-backed fixture writes; single shared SQLite connection/RLock does not independently validate multi-connection or actual SQL Server concurrency. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/core/src:src/core/tests:src/agents/src python3 -` with constructed memory-only reproduction | Direct review change, deferred-price currency sequence, split call windows and missing review coverage | Passed as diagnostic execution; adverse product observations | Changed review rejected; USD/GBP admitted against shared budget; split windows each counted the same output; missing review join still gave a numeric ratio. Split-window counts follow the declared per-window call cohort and are not independently classified as a defect. |
| `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/core/src:src/core/tests python3 -` with actual Assistants.review and ai_tasks.review on constructed rows/store | RV-001/RV-002/RV-004 reproductions | Passed as corrected diagnostic execution; adverse product observations | Withdrawal transaction rolled back; waiting reservation passed dispatch_check after shared hold while fresh root was denied; legacy acceptance saved before failed link, retry blocked and ratio remained numeric. |
| Earlier Review-owned memory-only diagnostic attempts | Synthetic harness construction, not source implementation | Failed, then corrected | First minimal Assistants object omitted mssql and raised AttributeError; next synthetic task omitted source_signature and raised KeyError. Both are preserved here as harness failures, not product defects. Corrected fixtures reached the actual reviewed error above. |
| Requested API discovery from src/api: `PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q` | Existing API suite, implementation evidence | Failed initially; passed on rerun, with skips | Original 1374-test run had two missing azure.eventhub import errors and 320 opt-in skips. Manifest-pinned dependencies were restored with pip after actual failures. Rerun: 1436 tests in 574.076 seconds, 320 opt-in skips. Synthetic-provenance correction during discovery means this is not an exact-head receipt. No discovery rerun in Review. |
| Existing component Ruff check/format and strict mypy commands, as recorded in changes | Core 170 files; agents 24; API 124 | Passed as implementation evidence | No static rerun claimed. Static success does not resolve the independently reproduced semantic defects. |
| Existing focused semantic/composition/regression commands, as recorded in changes | 24 core; six loopback API; 106 affected API with one skip; 21 agents dispatch/chat | Passed as implementation evidence | Fresh 24/six checks covered the latest provenance correction; no new fake-HTTP exercise was run in Review. Existing doubles and coverage limitations are stated above. |
| Issue-specific Playwright UI exercise | Changed UI | Skipped, inapplicable | No UI file changed. This does not skip actual existing Chromium groups in the later full gate. |
| Complete local `tools/rpi-checks.py --all` gate and immediate receipt verification, not invoked in Review | Final clean committed source/evidence, actual browser/SQL/scanner groups | Unavailable as final-candidate evidence; not run | Scheduled only after Review, corrections and final evidence commit. No receipt or passing full gate is claimed. Parent selects the actual fresh external destination and freshly fetched main base under applicable policy. |
| Paid held-out batch, actual applicable price, Azure billing and Finance/owner approval | Operational issue acceptance | Unavailable | Not supplied or authorised; no live substitute or invented numerical result. |

### Exact Issue Acceptance Disposition

Criteria below follow the nine checkbox rows read from issue #432 in order.
They are not new approval criteria or assertions that the original issue is done.

| Issue criterion | Assessed source/evidence position | Remaining acceptance |
| --- | --- | --- |
| 1: every model call, versions/usage/retries/failures/output and no raw case telemetry | Metadata-only partition, configuration/prompt hashes and cached usage implemented; source wiring assessed | RV-001/RV-004/RV-005; historical/resident joins and complete actual usage remain partial. |
| 2: per-request calls/depth, loop/fan-out stop and unaffected workflow/clocks | Exact root/depth tests and two-call fake transport stop; existing workflow unchanged in supplied regressions | Local engineering evidence, not live governed activation or whole-system operational acceptance. |
| 3: token/budget/expiry/unknown-price/liability dispatch stop and owned alert | Conservative reservation, expiry, sticky liability and opaque owner alerts implemented | RV-002/RV-003; real named owners and approved budgets remain unavailable. |
| 4: retrieved dated/versioned price; Unknown with none | Official retrieval metadata/version/hash stored; unusable cells and applicability explicitly null | Applicable numerical rate/approval absent; no cost may be inferred from the public metadata. |
| 5: Azure period reconciliation, owner tolerance, billing financial source | Synthetic exact billing/projection/variance distinction implemented | Actual attributable Azure bill/allocation/Finance validation absent; RV-004 affects trustworthy denominator coverage. |
| 6: separate TCA, named accepted denominator, quality rates and worse-quality failure | Exact billed ratio and distinct TCA components; cohort-bound supplied metric counts/floors/baselines; quality regression tests | RV-001/RV-004/RV-005; OD-51, real matched quality/effort and complete TCA approval absent. |
| 7: capacity not cash unless booked Finance destination | Explicit capacity classification and Unknown cash; no cash conversion | Actual measured released time/Finance destination absent. |
| 8: finite authorised held-out measured batch and spread | Recorded usage minimum/maximum/mean is labelled not an authorised held-out batch | Actual held-out batch, accepted results and spend authority absent. |
| 9: pitch slide/Q&A with source/evidence labels | Existing brief updated with prospective source-only slide/Q&A and stated gaps | Actual slide placement/deck rebuild/rehearsal/final challenge remain owner work. |

## Outcome

* Outcome: Defects found.
* Outcome rationale: Review execution is complete, but RV-001 through RV-004
  are reproducible material correctness/composition defects and RV-005 is an
  unresolved planned validation gap. No Conformant outcome is supported.
  RV-006 is separate residual operational work and is not the reason these
  introduced source defects exist. Local static/discovery successes do not
  override adverse semantic evidence or satisfy final publication/human gates.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect/validation gap | rpi-implement | Parent routes RV-001 to RV-005 for corrections and focused composed evidence, preserving this original Review. |
| Decision gap or invalid assumption | None in the active source direction | Deferred OD-51 decisions remain distinct operational owner work; no new source planning revision requested. |
| Material research evidence gap | None newly blocking the source review | Live finance/measurement evidence remains RV-006 follow-up, not authority for new paid/network research here. |
| Non-blocking residual work for source review | Distinct operational/accounting/presentation follow-up | RV-006 owners supply approved evidence, scope missing joins and update actual pitch assets. |

* Execution status: Complete.
* Outcome: Defects found.
* Validation coverage: all owned changed source/evidence assessed; 24 existing
  core methods independently exercised with memory-only fixtures; four defect
  sequences independently reproduced without model/network/file writes.
  Prior API/static/regression successes and adverse results remain explicitly
  attributed implementation evidence, not a fresh complete gate.
* Blockers: RV-001 to RV-005 corrections/evidence and final clean committed
  full-gate/receipt verification block publication. RV-006 and hosted/human
  approvals remain separate whole-issue/live acceptance boundaries.

| Artifact | Evidence |
| --- | --- |
| .copilot-tracking/research/2026-10-31/ai-metering-432-research.md | Original source/operational evidence boundary. |
| .copilot-tracking/plans/2026-10-31/ai-metering-432-plan.md | Completed planned source tasks and follow-ups. |
| .copilot-tracking/details/2026-10-31/ai-metering-432-phase-details.md | Direct PC-001 to PC-008 contract dispositions. |
| .copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-plan-critique.md | Original independent Revise verdict, preserved. |
| .copilot-tracking/changes/2026-10-31/ai-metering-432-changes.md | Original implementation and adverse/passing validation evidence. |
| .copilot-tracking/rpi-sessions/2026-10-31/ai-metering-432-state.json | Parent-owned active lifecycle state, not edited by Review. |
| .copilot-tracking/reviews/logs/2026-10-31/ai-metering-432-review.md | This one original independent Review and routing record. |

## Next Steps

The active parent routes RV-001 to RV-005 to rpi-implement, records correction
evidence without replacing this outcome or repeating Review, and reconciles
the parent-owned artifacts. After corrections and final evidence commit, run
the required fresh complete local gate and immediate receipt verification
against freshly fetched current main before any authorised push and independent
exact-head assessment. Retain Refs #432, the original adverse validation and
RV-006 follow-ups; no whole-issue closure or live approval is supported.
