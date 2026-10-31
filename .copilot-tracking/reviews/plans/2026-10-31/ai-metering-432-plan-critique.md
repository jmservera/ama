<!-- markdownlint-disable-file -->
# RPI Plan Critique: AI consumption economics

## Metadata

* Task ID: 432
* Task slug: ai-metering-432
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/ai-metering-432-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/ai-metering-432-phase-details.md
* Critique execution status: Complete
* Candidate branch: feat/ai-metering-432
* Execution count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: full RPI, source-only metering, no deployment changes,
  pip only, no paid inference, credentials, private data, Azure, main, other
  worktrees or mvp edits. The parent has loop/test/commit/gated-push authority
  for a Refs #432 PR. This critique has only read authority and permission to
  write this artifact; it does not implement, delegate, publish or create state.
* Primary inputs: the exact plan and phase-details paths above and
  .copilot-tracking/research/2026-10-31/ai-metering-432-research.md.
* Evidence considered: research W1-W2 and C1-C8; bounded source reads of
  src/core/src/zava_forward/core/ai.py, assistants.py, ai_tasks.py,
  chat_panel.py and store.py; src/agents/src/zava_forward/agents/dispatch.py
  and chat.py; src/api/src/zava_forward/api/server.py; existing Tokenomics
  synthesis/pitch brief and the local-gate guide. Required project context
  was read from the case-study documents, reference index/memory and sector
  primer. No additional external research or live execution was performed.
* Decisions and dependencies: P01-T01 precedes P01-T02; P02-T01 follows wiring.
  Existing assistant transactions/events are reused. Resident SQL accounting
  stays separate and explicitly unjoined. Missing OD-51, actual applicable
  prices/billing, approved quality floors and held-out spend authority remain
  unmet. Existing human, release, role, continuity, safety and consent controls
  remain authoritative.
* Acceptance boundary: credibility of the engineering plan, including test
  ownership/removals/addition limits, closed metadata, atomic budgets,
  unknown usage/liability, outcome attribution and truthful economics.
  This is not an implementation review, operational approval, paid benchmark
  or assessment of a deployed financial control.
* Supplied evidence limits: research reports all nine issue criteria open but
  does not reproduce their complete numbered text. Exact whole-issue trace
  therefore needs a parent-owned disposition matrix; none is presumed delivered.
  Research Q2/Q3 remain labelled Open despite its completed synthesis; the
  findings below distinguish concrete source risks from missing contracts.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Scope, W1-W2, operational dependencies | Covered with trace gap | Source-only authority and Refs #432 are explicit; exact nine-criterion disposition needs PC-008. |
| P01-T01, C4, atomic admission | Partial | Serializable port exists; scope intersection, replay and policy-version semantics need PC-001. |
| P01-T01, closed metadata/privacy | Partial | Declared prohibition is sound; existing mixed event stream is not metadata-only, PC-002. |
| P01-T02, C5-C6, task identity/cached usage | Partial | Actual adapters discard extra usage/IDs and use positional provider ports, PC-003. |
| P01-T01/P01-T02, uncertain liability | Partial | Retained reservations are planned; sticky holds, overruns and late outcomes need PC-004. |
| P01-T02, C8, output/review joins | Partial | Stable IDs exist in distinct persistence paths; recovery/eligibility need PC-005. |
| P01-T01, billing financial authority | Partial | Decimal strings and period/currency matching are planned; allocation/completeness need PC-006. |
| P01-T01/P02-T01, accepted denominator/quality/TCA | Partial | Unknown and capacity-not-cash are explicit; cohort and quality contracts need PC-007. |
| P02-T01, regression ownership and limits | Partial | Core/API ownership, no removals and two modules/35 methods are explicit; executable coverage needs PC-008. |
| P02-T01, publication and UI boundary | Covered | Independent Review/full gate/fresh receipt are required; no new UI and no live substitute are claimed. |

## Verdict

* Verdict: Revise
* Severity summary: Seven High findings, one Medium finding; no Critical findings.
* Rationale: the selected source-only direction is credible, but the contract is
  not yet precise enough to implement and test the claimed financial bounds or
  cost-per-accepted-proposal safely. These are directly applicable planner
  corrections, not reasons to expand scope or acquire live financial authority.
  Missing live evidence remains explicitly unmet and does not prevent a bounded
  engineering plan once the contracts below are resolved.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Atomic transactions do not define intersecting budgets or replay semantics

* Related IDs: P01-T01, P01-T02, C4; atomic call/depth/token/currency/expiry admission.
* Evidence: phase details P01-T01 requires durable reservations and policy
  matching but does not define budget keys or mutation rules.
  src/core/src/zava_forward/core/assistants.py:792-853 already prevents
  restarting a token authority from increasing its allowance/expiry and uses
  task fence/revision checks. Its transaction port serializes writes, not the
  new financial aggregation semantics by itself.
* Concern: the plan leaves independent task/period/request budget intersection,
  stable parent/root request identity, depth origin and exact limit inclusivity
  unspecified. New policy IDs or config changes could reset apparent spend;
  concurrent callers and acknowledged-but-retried reservations could double
  count or dispatch twice.
* Impact: an implementation may pass a single-budget test while exceeding a
  period cap through fan-out, restarts or policy replacement.
* Smallest useful change: specify stable budget/request/attempt identities;
  intersect all applicable scopes in one transaction using database time;
  state call/depth/token/money boundary arithmetic and a policy replacement
  rule that cannot erase existing liability. Bind each admitted physical
  attempt to one reservation and define retry-after-commit as lookup, never a
  fresh dispatch permission. Reject missing/invalid bounds and scan overflow.
* Action owner: Planning parent, P01-T01/P01-T02 implementer.
* Exact resolving evidence: revised details with a budget-key/identity contract
  and deterministic tests for concurrent last-slot claims, independent task
  plus period caps, sibling fan-out sharing one root, exact depth/call limits,
  restart/policy replacement, duplicate admission and lost acknowledgement.
  Tests assert durable counts/liability and actual fake-provider call counts.
* Decision route: Direct planner correction. Existing scope authorizes finite
  controls; no production budget value or new spend decision is requested.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Closed metadata must be enforced at ingress and on mixed-ledger reads

* Related IDs: P01-T01, P01-T02, C4-C8; metadata-only records and manager JSON.
* Evidence: phase details calls payloads closed without enumerating permitted
  fields or value validators. src/core/src/zava_forward/core/assistants.py:443
  accepts arbitrary event keyword bodies; completed events at 929-932 include
  output and source identifiers, and review events at 1058-1060 include note,
  reviewer email and edited output. The old stream is not metadata-only.
* Concern: merely adding kind/version or allowlisting field names cannot make
  arbitrary provider model strings, owner/source references, nested usage,
  caller IDs or billing metadata safe. Reading/exporting all historical
  assistant_events could also leak legacy content through the new report.
* Impact: the consumption ledger/report could retain resident or prompt/output
  text despite the stated privacy boundary.
* Smallest useful change: enumerate versioned schemas for every new event,
  including bounded types, enums, opaque references and nested-key rejection.
  Reject arbitrary free text/extra fields before persistence; never copy raw
  provider exceptions or billing documents. Define a kind/version-aware
  consumption reader and aggregate-only manager output that do not return old
  content-bearing events. Preserve historical evidence without rewriting it.
* Action owner: Planning parent, core ledger and API report implementers.
* Exact resolving evidence: schema table and tests injecting unexpected keys,
  nested content, provider-controlled strings, email/case text and malformed
  references; inspect only constructed ledger rows/JSON responses for synthetic
  canaries. Include historical completed/review events in the fixture and prove
  their text is absent from the new consumption export.
* Decision route: Direct planner correction; existing privacy instructions
  resolve the choice. No historical deletion or broader privacy migration.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Meter identity and cached usage need an explicit end-to-end port contract

* Related IDs: P01-T02, C5-C6; source wiring and attributable configuration.
* Evidence: src/api/src/zava_forward/api/server.py:76-80 composes assistants
  and chat through positional AgentWorker provider calls;
  src/agents/src/zava_forward/agents/dispatch.py:46-57 strips tasks to
  TASK_KEYS. assistants.py:953-962 dispatches on a separate thread.
  assistants.py:322-338 and chat_panel.py:259-269 retain only three token
  counters; src/agents/src/zava_forward/agents/chat.py:47-82 constructs
  ModelReply without a meter identity. Ai._chat returns text alone.
* Concern: "explicit/scoped per call" does not identify which port transports
  task/root/attempt IDs into the thread and returns meter IDs through these
  reducers. Cached usage or meter IDs can be discarded, or a default shared
  request identity can accidentally merge independent chat/proposal attempts.
  The listed canonical targets do not explicitly name the agents chat/dispatch
  adapters that participate in this trace.
* Impact: individual calls cannot reliably join outputs or share the correct
  financial budget; cached-token pricing becomes Unknown even when available.
* Smallest useful change: list the concrete call-context and result-envelope
  contract across Ai, assistant execution, agents adapters, chat and legacy
  output construction. Include attempt/root/task, selected configuration and
  prompt identifiers, returned model, meter ID and separately validated cached
  token state. Pass immutable context into the model thread; do not rely on
  implicit thread-local inheritance or mutable Ai attributes. Distinguish
  nonbillable doubles from real Ai without trusting a caller-supplied bypass flag.
* Action owner: Planning parent, P01-T02 implementer.
* Exact resolving evidence: bounded wiring table naming every port/reducer and
  a fake-network composed test for assistant, chat, legacy text and document
  fallback paths. Assert preserved cached counts/meter IDs, separate concurrent
  task identities, configuration/prompt provenance and zero HTTP dispatch from
  real Ai without a valid ledger/admission.
* Decision route: Direct planner correction; adapter changes stay source-only.
  Independent resident financial composition remains explicitly excluded.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Unknown usage and overruns need durable holds independent of proposal completion

* Related IDs: P01-T01/P01-T02, C4-C7; unknown cached usage/liability.
* Evidence: assistants.py:875-877 returns before accounting when a lease/fence
  is stale; execute at 986-990 substitutes a timeout envelope while a provider
  thread may still finish. complete at 915-922 retains the reservation for
  unknown/overrun tokens but does not add excess actual tokens to that existing
  allowance. The new plan mentions token-overrun tests and no ambiguous refunds,
  without defining settlement/hold scope or its lifetime.
* Concern: retaining the original reservation alone does not cover a known
  overrun, nor stop retries after uncertain usage. Late usage may never reach
  financial completion when proposal completion is fenced out. Cached tokens
  require absent/null/zero distinctions and 0 <= cached <= input validation.
  Character length alone is not a proved text-token bound either.
* Impact: charged failures/late calls disappear or excess liabilities are
  understated; subsequent dispatch can continue after uncertainty.
* Smallest useful change: define a sticky owned hold on affected budget scopes
  for unknown price/cached usage, malformed usage and liability overrun.
  Financial completion must be append-only/idempotent even for quarantined or
  stale proposals. Record known excess liability and stop, rather than replacing
  it with the smaller reservation. Define evidence-backed settlement/hold
  resolution without automatic timeout refunds. Specify a conservative text
  input bound for the complete serialized request and the policy/model it covers;
  unsupported inputs/images deny dispatch while storage/manual paths continue.
* Action owner: Planning parent, ledger/transport implementer.
* Exact resolving evidence: state-transition table and tests for absent versus
  explicit-zero cached usage, cached > input, invalid totals/types, Unicode
  input bounds, timeout then late completion, stale fence, duplicate completion,
  actual overrun and next-call denial across restart. Assert no automatic release
  of ambiguous liability and no return of quarantined output.
* Decision route: Direct planner correction. The existing Unknown/fail-closed
  requirement settles the policy; no paid tokenizer validation is demanded.

<!-- rpi:critique id=PC-005 -->
### PC-005 [High]: Immutable output/review links need cross-store recovery and eligibility rules

* Related IDs: P01-T01/P01-T02, C8; outcome joining.
* Evidence: ai_tasks.py:229-244 and 337-380 persist recommendations/reviews
  through the store lock/save path. assistants.py:1001-1061 uses SQL revisions
  and verification before accept/edit-accept. These are different persistence
  boundaries and review vocabularies; note/source verification is not acceptance.
* Concern: stable record IDs alone do not guarantee exactly-once meter-to-output
  joins or durable review linkage. A store save can succeed while a ledger event
  fails, or vice versa. Retries, edited outputs, regenerated proposals, templates,
  chat answers and quarantined results require distinct denominator treatment.
* Impact: counts can be duplicated or omit accepted outcomes; a workflow fallback
  or verification-only action can be reported as a human-accepted AI proposal.
* Smallest useful change: specify opaque output/revision identity, its one-to-many
  call/attempt links, and accepted action mappings for each path. Emit SQL review
  links in the authoritative transaction where possible. For the existing legacy
  store boundary, choose idempotent recoverable reconciliation or explicit
  incomplete-join coverage; do not claim cross-store atomicity without a mechanism.
  Missing links must yield Unknown/incomplete coverage, not disappear silently.
* Action owner: Planning parent, P01-T02 implementer.
* Exact resolving evidence: join/eligibility table and fault-injected constructed
  store tests for each save/event ordering, replay, failed review, verify-only,
  edit-accept, reject, fallback, quarantine and regeneration. Each eligible output
  counts once with all its attempts; lost links are visible as unresolved coverage.
* Decision route: Direct planner correction. No store migration or new database
  is required; explicit incomplete attribution is valid within this scope.

<!-- rpi:critique id=PC-006 -->
### PC-006 [High]: Period billing is not automatically attributable cost per accepted proposal

* Related IDs: P01-T01, billing reconciliation, financial authority and C1-C2.
* Evidence: plan functional requirements make imported billing authoritative
  for an exact period/currency with an owner tolerance; details specify Decimal
  strings but no service/model/scope allocation or duplicate/correction contract.
  docs/reference/resources/ai-tokenomics.md distinguishes invoice reconciliation
  from usage estimates and complete TCA.
* Concern: a whole account/model-period bill can include independent resident
  calls or unrelated consumption. Missing rows, overlapping imports, duplicated
  invoices and immutable corrections can yield a plausible but false numerator.
  Matching only period/currency is insufficient to allocate it to joined outputs.
* Impact: a financial label can conceal missing coverage or double counting,
  especially when the resident path is explicitly unjoined.
* Smallest useful change: define closed billing identity/scope, provenance/status,
  exclusive period boundaries, coverage and correction/supersession links.
  Separate supplied-unverified/synthetic billing from owner-validated authority.
  Define attribution/allocation evidence and variance formula/tolerance units;
  missing scope, allocation or tolerance stays Unknown/unreconciled. Keep actual
  billed amounts, modeled charges and outstanding reservations separate and
  never add them as if disjoint. Reject invalid/nonfinite Decimal inputs and
  specify precision/rounding; do not silently mix currencies.
* Action owner: Planning parent and report implementer; Finance supplies actual
  financial evidence later, outside this source-only delivery.
* Exact resolving evidence: revised import/report contract and synthetic tests
  for duplicate/overlapping/corrected imports, boundary timestamps, mixed
  currencies, partial/unjoined billing, invalid decimal values, owner tolerance
  absent/exceeded and allocated versus unallocated costs. Reports disclose
  synthetic authority and do not claim real reconciled financial cost.
* Decision route: Direct planner correction. Live Finance validation is an unmet
  operational dependency, not a request for Azure access or paid execution.

<!-- rpi:critique id=PC-007 -->
### PC-007 [High]: Denominator and quality rules need one matched cohort and explicit Unknown states

* Related IDs: P01-T01/P02-T01; accepted denominator, quality floors,
  overrides/reopened cases, TCA and capacity versus Finance-booked cash.
* Evidence: the plan requires these measures without defining their counting
  windows, eligible outcomes or comparison baseline. ai_tasks.py and assistants.py
  have distinct acceptance events, while the existing pitch brief explicitly
  leaves OD-51 denominator/floor decisions unapproved.
* Concern: dividing successful-call cost by accepted outcomes hides retries,
  rejected/quarantined drafts and ongoing unreviewed work. Mixing review dates
  with billed dates mismatches cohorts. Unknown quality evidence can be mistaken
  for zero critical misses or a passing floor; denominators for overrides and
  reopened cases also differ. Engineering defaults must not become OD-51 approval.
* Impact: cheaper-but-worse AI can appear economically better; real financial
  uncertainty and unmeasured labour can be concealed by an attractive ratio.
* Smallest useful change: define an explicit reporting cohort/as-of contract,
  distinct accepted proposal/output versus home/handover identities, and inclusion
  of all attributed attempt costs, including failures/retries. Show excluded,
  unreviewed and unjoined counts. Separate financial ratio from quality-qualified
  ratio; missing numerator, acceptance evidence, quality baseline/floor or zero
  denominator yields the corresponding Unknown state. Give critical misses,
  unsupported claims, overrides and reopenings their own observed denominators/
  coverage and matched held-out comparison rules. Enumerate token, hosting,
  review/correction/re-review, assurance and support TCA components with missing
  components explicit, and keep capacity separate from Finance-booked cash.
* Action owner: Planning parent/report implementer. OD-51 owner/Finance approval
  remains outstanding and is not supplied by test fixtures.
* Exact resolving evidence: formulas and report-field contract plus synthetic
  matched-cohort tests for retries/rejections, edits counted once, late acceptance,
  zero acceptance, missing effort/quality evidence, unapproved floor, worsening
  critical misses/unsupported claims, reopened outcomes and capacity-not-cash.
  Fixture prices/floors are labelled synthetic and no live-value acceptance follows.
* Decision route: Direct planner correction for engineering semantics. A later
  operational denominator/floor approval is a significant owner decision already
  explicitly deferred, not an unresolved choice blocking this scoped revision.

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: The test budget needs named coverage and an exact acceptance disposition

* Related IDs: P02-T01; all nine issue criteria, regression preservation,
  maximum two new test modules/35 methods.
* Evidence: plan/details correctly assign core ledger semantics and API composed
  fake-network/report tests and specify zero removals. They do not name modules,
  test selectors, parameterized cases or an AC-to-test matrix. "Canonical targets"
  omits the agents adapters identified in PC-003. Research W1 reports nine open
  criteria but the candidate summarizes them without individual dispositions.
* Concern: substantial concurrency/privacy/financial/join failures could be
  omitted to fit the maximum, or covered only through direct ledger calls rather
  than actual composition. Broad discovery success does not establish each
  promised semantic acceptance criterion. Documentation could accidentally
  promote aggregate local success into whole-issue delivery.
* Impact: insufficient or untraceable evidence despite preserved regressions
  and passing existing suites.
* Smallest useful change: name the two new modules, assign methods or
  parameterized/subTest cases to PC-001 through PC-007 and every exact issue
  criterion, and list affected existing core/agents/API tests and exact caller
  API discovery/Ruff commands. Keep zero removals and at most 35 additions;
  do not relax assertions to meet the cap. Map each criterion to local evidence
  versus explicitly unmet authority/live financial/batch evidence. Include
  agents usage/identity preservation in existing or composed regression coverage.
* Action owner: Planning parent and P02-T01 test owner.
* Exact resolving evidence: amended details with named module/method/selector
  matrix whose addition count is <=35 across <=2 new modules and whose removals
  are zero. Original implementation evidence records commands/counts/results,
  synthetic/live labels and unmet criteria. Preserve independent Review and fresh
  full-receipt requirements; actual results are implementation-stage evidence,
  not demanded during this read-only critique.
* Decision route: Direct planner correction. Parameterization can satisfy the
  existing cap without a divergent test-budget decision or paid test run.

## Strengths and Residual Risk

* Reusing the append-only SQL ledger and transaction port avoids a competing
  financial store. Exact-decimal money, bounded scans and manual fallback are
  appropriate design constraints.
* The candidate correctly preserves independent resident accounting rather than
  claiming a deployed financial migration. Whole-call coverage stays unmet.
* OD-51, applicable actual prices/billing, approved quality floors, appointments,
  accepted held-out outcomes and paid spend authority are explicitly unavailable.
  They remain unmet, not assumed from source-only tests or earlier exercises.
* No UI change, deployment setting, deck rebuild or paid exercise is planned.
  Existing browser/full gate and human approval requirements remain in place.
* Independent Review and exact-head/full-receipt publication checks are retained.
  This critique does not satisfy those later gates.

## Questions or Blocking Evidence Gaps

* No user response is required to make the eight directly applicable corrections.
* Live financial authority and measured batch evidence cannot be resolved here.
  Record them against their exact issue criteria and stop short of whole-issue
  acceptance; do not demand Azure or paid inference to clear this plan critique.
* The parent must transcribe the exact criterion identifiers from its existing
  issue evidence for PC-008. This assessment does not invent their wording.

## Limitations

* Only the supplied candidate and bounded actual source were assessed; no
  implementation, tests, network provider, private data, billing records or
  credentials were exercised.
* Source observations identify why a contract is needed, not confirmed bugs in
  an implementation that has not yet been written. Historical content-bearing
  events are not authorized for deletion or rewrite.
* The initial worktree had untracked parent plan/details/research/state artifacts.
  They were left untouched. This execution writes only this critique artifact.
* No second critique or nested delegation was performed; this is the complete
  actionable set for the supplied assessment boundary.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: define stable intersecting budget/attempt identities
  and replay semantics in P01-T01/P01-T02, then resolve the remaining contracts
  and coverage matrix in the same revision.
* User response required: No. All current corrections apply within confirmed
  direction; later live approvals remain explicitly unmet.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/ai-metering-432-plan.md](.copilot-tracking/plans/2026-10-31/ai-metering-432-plan.md) | Final-candidate plan assessed. |
| [.copilot-tracking/details/2026-10-31/ai-metering-432-phase-details.md](.copilot-tracking/details/2026-10-31/ai-metering-432-phase-details.md) | Phase contracts assessed. |
| [.copilot-tracking/research/2026-10-31/ai-metering-432-research.md](.copilot-tracking/research/2026-10-31/ai-metering-432-research.md) | Supplied research and evidence pointers. |
| [.copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-plan-critique.md) | Complete independent critique; Revise. |

## Next Steps

The active planning parent revises directly against PC-001 through PC-008,
records each disposition and finalizes without another critique. No user action
is required. Implementation and independent Review follow the corrected
contracts; publication still requires the unchanged complete local gate and
exact-head receipt verification. Refs #432 and all live financial/quality/
held-out authority gaps remain explicit.
