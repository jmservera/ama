---
title: Resident decisions final-candidate plan critique
description: One independent bounded credibility assessment for issue 86
ms.date: 2026-10-15
---

## Metadata

* Task ID: issue-86 / resident-decisions-86
* Branch inspected: feat/src-resident-decisions-86
* Critique date: 2026-10-15
* Plan: .copilot-tracking/plans/2026-10-15/resident-decisions-86-plan.md
* Phase details: .copilot-tracking/details/2026-10-15/resident-decisions-86-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique; no second critique requested or performed.

## Inputs and Criterion Boundary

* Caller requirements: full RPI followed by implementation; new code and tests
  only in src under accepted ADR 0006; no private data, inferred agent consent,
  mvp implementation, nonportable SQL or non-pip dependency installation.
  Existing enabled AI proposal paths and human approval gates must survive.
* Functional boundary: supplied decisions bound to home/measure/scope/design;
  representative task/source/scope/review/wishes, expiry, dispute and unclear
  authority; safe disclosure; measure-specific pause/withdrawal and dependent
  readiness review; independent human review and formal complaint without
  detriment. Unsupported owner and live evidence must remain unticked.
* Supplied research: .copilot-tracking/research/2026-10-15/resident-decisions-86-research.md,
  especially C1-C9 and W1-W2. Remote issue/PR assertions are supplied research
  evidence, not independently refreshed in this critique.
* Requirements checked: PRD FR-014, FR-043 to FR-047, AC-017, AC-037,
  AC-052, AC-054 to AC-056, AC-060 and AC-064; ADR 0006; original case study,
  addendum and reference index/memory for context.
* Relevant source: core resident_decisions.py, store.py, procurement.py,
  signoffs.py, sqlstore.py, projection.py, controls.py, buildings.py and
  workflows.py; API server.py; assistant source-selection locations.
  All implementation paths below are relative to the workspace root.
* Assessment boundary: credibility of P01-P03, A1-A5 and the bounded synthetic
  slice against current source. This is not implementation acceptance, a
  legal-currentness review, a live integration test or a new research cycle.
  No production code, plan, details or research was edited.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| ADR 0006; caller placement, privacy and pip/SQL constraints | Covered in intent | src-only ownership and unchanged schema/driver boundaries are explicit. |
| A1; C3/C7/C8; P01-T01 | Partial | Exact-scope recording is planned, but technical design changes are not explicitly connected to current resident context: PC-002. |
| A2; C3/C4/C9; P01-T01/P01-T02 | Partial | Strong representative fields and write-time checks; use-time authority invalidation and temporal rules remain undefined: PC-003. |
| A3; C4/C5/C9; P01-T02 | Partial | Guards are named, but operation-to-measure binding and independent dependency isolation are missing: PC-001. |
| A4; P01-T01/P02-T01 | Partial | Distinct route/owners and honest live-evidence limits; independent closure authority and local no-detriment oracle need definition: PC-006. |
| Privacy; C6; AC-037/064; P01-T02/P02-T02 | Partial | Projection intent is sound; nested aliasing and precise permitted-field policy need explicit handling: PC-004. |
| Enabled AI paths; AC-052/054; P01-T02/P02-T02 | Partial | Legacy draft refusal is coupled to existing AI entry points: PC-005. |
| A5; P03-T01/P03-T02 | Covered for bounded evidence | Five suites, configured tooling, actual local HTTP exercise and explicit live/container limits; add the resolving scenarios below to the two assigned modules. |
| Unsupported owner/live acceptance | Covered | Follow-up list and unticked criteria correctly prevent local evidence becoming product acceptance. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 5 High, 1 Medium.
* Rationale: the candidate correctly identifies the principal controls, but
  leaves implementers to invent dependency applicability and freshness rules.
  Current source also exposes concrete projection and AI compatibility hazards.
  These are direct planner corrections under existing user direction, not
  reasons to reopen the architecture, infer consent or seek fictional company
  evidence. The bounded implementation can proceed after the parent resolves
  this complete finding set directly, without another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Release guards lack an operation-to-measure dependency contract

* Related IDs: A3; P01-T01/P01-T02/P02-T02; C5/C9; PRD FR-046, AC-056.
* Evidence: the plan calls for a shared resident_gate and SQL dependent-case
  validation. src/core/src/zava_forward/core/procurement.py issue_work_order()
  accepts free-text scope; versions store scope text and package scope_version,
  but no resident measure/context bindings. Booking/completion receive a work
  order ID. sqlstore.py _validate_safety_clear() tracks whole case IDs.
* Concern: checking every measure for every operation stops unrelated
  discretionary work; checking an unspecified subset can release paused or
  unconsented work. Preserving sibling answer values alone does not establish
  dependent-readiness isolation. A free-text package or work-order scope is
  not evidence of applicability. The plan also lacks a precise rule for
  resolving the human-review flag without silently clearing it.
* Impact: either overbroad holds or consent bypasses, including reissue and
  correction. A case-level SQL dependency set cannot prove exact applicability.
* Smallest useful change: specify explicit operation/work-order-version
  bindings to measure, scope and design contexts in existing JSON bodies,
  including proposed new scope on correction/reissue. Define case-wide advance
  separately from scoped releases. Unknown applicability blocks that release
  pending owned human review; do not infer it from text. Define review flag
  provenance and the authorized, supplied evidence needed to resolve it,
  retaining the fresh-acceptance requirement. Carry the same bindings into
  transactional revalidation, not just a case ID.
* Action owner: planning parent, then core implementer.
* Exact resolving evidence: revised P01-T02 and P02-T02 with an expected
  affected/unaffected dependency manifest. In
  src/core/tests/test_resident_decisions.py, pause measure A while B stays
  accepted: A-only and A+B releases fail, explicitly independent B-only release
  succeeds when other gates pass, unknown bindings fail, changed scope on
  reissue/correction cannot reuse old consent, and review resolution is
  evidenced rather than automatic. Include two-connection SQLite conflict
  coverage showing stale dependent authorization cannot commit and unrelated
  choices remain unchanged.
* Decision route: direct planner correction; no significant user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Registered resident context can remain stale after a technical design change

* Related IDs: A1/A3; P01-T01/P01-T02; C7/C8; PRD FR-045, AC-055.
* Evidence: phase details require decision writes to match registered current
  context, but do not define its relationship to the existing technical design.
  src/core/src/zava_forward/core/signoffs.py _tech_design_change() independently
  increments technical.design_version and marks selected technical sign-offs
  for reassessment. _tech_design_submit() establishes the initial version.
* Concern: an implementer can register version 1, accept it, change the actual
  design to version 2 and still satisfy a resident gate that checks only the
  resident registration. Re-registering an old version or switching contexts
  back can also resurrect historical acceptance unless explicitly prohibited.
  Requiring a positive integer is not currentness validation.
* Impact: works can proceed against a design the resident never accepted.
* Smallest useful change: define the authoritative current design/context
  comparison at registration, decision, readiness and release; explicitly
  include technical design submit/change and relevant scope version changes
  in the invalidation contract. For the existing case-wide design counter,
  state its conservative applicability rather than inventing unrecorded
  per-measure independence. Context revisions must not silently reactivate an
  earlier accepted decision. Missing or mismatched currentness remains unknown.
* Action owner: planning parent, then core implementer.
* Exact resolving evidence: revised P01-T01/P01-T02 plus tests in
  src/core/tests/test_resident_decisions.py that accept a context, call the
  actual technical design-change action without a resident registration call,
  and observe blocked current readiness/release with historical answers
  preserved. Test stale/future registration versions and context switch-back;
  none may restore acceptance without the required supplied new decision.
* Decision route: direct planner correction; no significant user decision.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Write-time representative validation does not establish current authority at release

* Related IDs: A2/A3; P01-T01/P01-T02/P02-T02; C3/C9; PRD AC-064.
* Evidence: P01-T01 binds representative answers to the authority version
  checked at write. Readiness is described as the latest exact-scope answer.
  The candidate does not explicitly require that an existing representative
  answer be revalidated against current authority, resident wishes and safe
  contact when readiness/disclosure/release is evaluated.
* Concern: after a valid acceptance, time may pass, review may become due, or
  authority may be superseded, revoked, disputed or made unclear. A historical
  authority version still exists, so checking only that reference or answer
  allows stale authority to authorize new action. Multiple representatives
  make accidental latest-global-record or any-valid-record fallback unsafe.
  Expiry tests alone do not specify future dates, review-date boundaries or
  invalid date ordering.
* Impact: unauthorized consent reliance or disclosure despite a later hold.
* Smallest useful change: require use-time validation of the exact referenced
  representative and authority lineage for the requested task/context,
  including current wishes/contact and revocation/supersession. Define
  fail-closed missing/future/invalid date handling, review/expiry boundaries
  and the clock used by local and transactional checks. A failed check creates
  or exposes an owned staff-confirmation hold without rewriting history.
  Preserve the explicitly allowed direct resident statement route.
* Action owner: planning parent, then core implementer.
* Exact resolving evidence: revised authority lifecycle rules and fixed-clock
  tests in src/core/tests/test_resident_decisions.py: accept while valid, then
  advance past review/expiry or dispute/revoke/change wishes/contact; readiness,
  disclosure and dependent release must fail without changing history.
  Unrelated representatives and direct resident decisions remain independent.
  A competing SQL authority change must prevent a stale release commit.
* Decision route: direct planner correction; operational legal/retention policy
  remains unapproved, not invented by this correction.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Nested resident projection can mutate authoritative history

* Related IDs: A1/A2; P01-T02/P02-T02; C6; PRD AC-037/064.
* Evidence: src/core/src/zava_forward/core/store.py detail() first deep-copies
  the case, then replaces measure_decisions with measure_decision_view(c).
  resident_decisions.py measure_decision_view() returns original versions
  lists. projection.py hold_notes() recursively edits dictionaries in place.
  Programme Support Officer and Retrofit Coordinator are RESIDENT_ROLES in
  controls.py but are absent from DEFAULT_REASON_ROLES in projection.py.
* Concern: projecting a detail view can replace stored decision notes through
  the alias, outside a controlled resident write; later saving can persist
  that redaction. Extending those lists with source, wishes and authority
  references increases the risk. Merely choosing "resident-workflow roles"
  also fails to specify which authority/source/wishes fields each role needs
  when existing reason permissions differ.
* Impact: append-only evidence can be damaged by a GET, or sensitive fields
  can leak through nested history and inconsistent role policies.
* Smallest useful change: require detached projections throughout the resident
  view and an explicit exercise permitted-field matrix for new top-level and
  nested fields, consistent with existing need-based restrictions. Use
  event/reference metadata rather than private narratives in new audit and
  error/gate output. Retention and operational role ratification stay Unknown.
* Action owner: planning parent, then core/API implementer.
* Exact resolving evidence: revised P01-T02 and role-matrix assertions in the
  two assigned test modules. Compare complete case/audit state before and after
  detail GETs for allowed, restricted, contractor and configured reason roles;
  save an unrelated permitted change and reopen both JSON/SQLite state to prove
  original history survives. Synthetic sentinel source/wishes/note values must
  be absent from denied nested responses, exports/model inputs and new audit
  details, while needed authorized fields remain available.
* Decision route: direct planner correction using a labelled exercise matrix;
  no operational permission approval is implied.

<!-- rpi:critique id=PC-005 -->
### PC-005 [High]: Refusing the legacy draft can disable existing enabled AI proposals

* Related IDs: caller AI-preservation requirement; P01-T02/P02-T02; C4;
  PRD AC-052/054.
* Evidence: src/core/src/zava_forward/core/store.py ai_run() calls
  self.draft(case_id, ...) unconditionally before selecting the message or
  summary task and before invoking ai_tasks.run_text_task(). The candidate
  requires refusal of unchecked representative-addressed legacy templates.
* Concern: implementing that refusal solely by raising from draft() prevents
  both AI message and summary proposals for affected cases, even if their
  enabled task, source permissions and approval controls are otherwise valid.
  An AI-nonmutation test does not catch this loss of functionality.
* Impact: a privacy fix unintentionally disables existing assistance, contrary
  to explicit user direction; bypassing authority just to restore the AI call
  would instead weaken disclosure protection.
* Smallest useful change: explicitly decouple proposal generation from
  representative-addressed fallback construction. Preserve refusal of unsafe
  addressed material while providing a permitted non-addressed staff proposal
  or explicit safe manual state as appropriate; nothing is sent. Summaries
  must not require a resident-addressed template. Preserve existing task
  enablement, source permissions and independent proposal review.
* Action owner: planning parent, then core/API implementer.
* Exact resolving evidence: revised P01-T02/P02-T02 and enabled-path regression
  tests using the existing adapter seam in src-owned tests. With unchecked or
  expired representative authority, authorized enabled summary and safe
  coordination/message proposal paths still reach the permitted proposal
  service where applicable, while unchecked addressed drafts/disclosure fail.
  Outputs remain unapproved; consent/release/appointments do not mutate.
  Include disabled/failing-model manual access controls; synthetic adapter
  evidence must not be called live inference.
* Decision route: direct planner correction; user direction already requires
  preserving enabled paths, not a new AI capability.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Distinct service owners alone do not enforce independent review

* Related IDs: A4; P01-T01/P02-T01/P02-T02; caller independent-review and
  no-detriment requirement; PRD AC-037.
* Evidence: resident_decisions.py _res_service_close() gives only Complaint
  the special redress-owner-only and different-person checks. Other routes
  permit service or redress owner closure. The plan adds Independent review
  and distinct owners without defining its close/update authority or linking
  independence to the decision being reviewed.
* Concern: adding a route enum and distinct owner check can leave its subject
  or service handler able to close their own review. A4 correctly defers real
  human/without-detriment acceptance, but that does not remove the need for a
  local enforced no-detriment invariant.
* Impact: the new route may be nominally independent only; requesting review
  or complaint could inadvertently change works choices, holds or access.
* Smallest useful change: specify the constructed review subject/reference,
  independent reviewer eligibility, authorized update/closure rules and
  refusal of self-review, retaining existing complaint protections. Keep
  complaint, review and remedy outcomes separate from works authorization;
  neither route clears or creates consent, priority sanctions or hazard holds.
  Do not invent a live complaint destination.
* Action owner: planning parent, then core/API implementer.
* Exact resolving evidence: revised P01-T01/P02-T02 and local tests denying
  closure by the contested decision-maker or service handler, allowing the
  distinct authorized reviewer, and comparing choices, holds, priority and
  hazard access before/after review and complaint open/update/closure on paused
  and closed cases. Actual formal-route integration and real independent-human
  acceptance remain explicitly unticked.
* Decision route: direct planner correction for the synthetic contract;
  actual organizational delegations remain owner-dependent follow-up.

## Strengths and Residual Risk

* Reuses the existing resident mixin and JSON case bodies instead of creating
  parallel consent storage or an agent decision tool.
* Explicit unknowns, supplied source, version history, interpreter/scheduling
  restrictions, safe-contact invalidation and direct resident statements are
  strong foundations.
* Existing hazard intake and complaint access are deliberately independent of
  discretionary release. Real sending is not fabricated.
* src-only test ownership, no generator backfill, portable SQL and truthful
  local-versus-live evidence boundaries match current user decisions.
* Operational authority, retention, formal complaint integration, direct human
  accessibility/no-detriment validation and authorized live platform evidence
  remain open. The plan declares these limits; this critique does not treat
  them as approved residual operational risk or as completed acceptance.

## Questions or Blocking Evidence Gaps

* No significant or divergent user decision is necessary for the six bounded
  corrections. Current requirements already determine their direction.
* Unsupported live/owner evidence prevents full issue/product acceptance,
  not this scoped planning assessment. Preserve those gates explicitly.

## Limitations

* Static planning/source inspection only; no implementation, executable tests,
  Docker, model call, Azure or SQL Server validation was performed.
* Git status showed the supplied RPI artifacts untracked on the named branch.
  They were read in place and left unchanged. Only this critique was written.
* Source observations identify planning risks and a tightly coupled existing
  alias hazard; they are not claims that the proposed implementation already
  contains these defects.

## Recommended Next Action

* Highest-impact finding: PC-001, exact dependent release applicability.
* Action owner: planning parent.
* Smallest next action: add explicit release-to-context dependency bindings
  and affected/unaffected test oracles to P01-T02/P02-T02, then disposition all
  six findings directly before implementation.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-15/resident-decisions-86-plan.md](.copilot-tracking/plans/2026-10-15/resident-decisions-86-plan.md) | Candidate plan assessed; unchanged. |
| [.copilot-tracking/details/2026-10-15/resident-decisions-86-phase-details.md](.copilot-tracking/details/2026-10-15/resident-decisions-86-phase-details.md) | Phase details assessed; unchanged. |
| [.copilot-tracking/research/2026-10-15/resident-decisions-86-research.md](.copilot-tracking/research/2026-10-15/resident-decisions-86-research.md) | Supplied research assessed; unchanged. |
| [.copilot-tracking/plans/2026-10-15/resident-decisions-86-critique.md](.copilot-tracking/plans/2026-10-15/resident-decisions-86-critique.md) | Complete single critique and actionable findings. |

## Next Steps

The active RPI planning parent revises and dispositions PC-001 through PC-006
directly, finalizes the corrected plan without another critique, then continues
the authorized implementation and review sequence. No user action is required.
