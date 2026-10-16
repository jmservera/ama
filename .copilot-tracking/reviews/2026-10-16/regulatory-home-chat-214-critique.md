---
title: Final-candidate plan critique for issue 214
description: One bounded assessment of offline synthetic home chat acceptance and isolated handoff
ms.date: 2026-10-16
---

## Metadata

* Task ID: #214 / regulatory-home-chat-214
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/regulatory-home-chat-214-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/regulatory-home-chat-214-phase-details.md
* Research: .copilot-tracking/research/2026-10-16/regulatory-home-chat-214-research.md
* Critique execution status: Complete
* Assessment count: One final-candidate critique; the complete actionable finding set is PC-001 through PC-008.

## Inputs and Criterion Boundary

* Confirmed requirements: bounded offline synthetic development; src-only runtime
  and tests; source-only factual claims; no arbitrary legal prose; existing
  per-user isolation; Juan Manuel Servera as the exercise Legal/Compliance/DPO
  doubt recipient; deterministic evaluation and a card comparator; no live
  Azure, model, human approval or operational acceptance claim.
* Read the supplied plan, phase details and research in full. Read project
  context in docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. Consulted the relevant contracts in
  docs/adrs/0004-per-user-agent-chat-and-memory.md and
  docs/adrs/0005-regulatory-compliance-assistant.md, and the cited src chat,
  privacy, rule-card, eligibility, law-store, API, authentication, persistence
  and existing chat-evaluation implementations.
* Dependencies considered: C1-C6 are reusable building blocks, not proof of the
  new integration. C7 is explicitly rejected. Named owner provisioning, current
  source eligibility, current role/case projection, chat privacy admission and
  durable repository behavior remain prerequisites.
* Acceptance boundary: implementation credibility for this offline slice only.
  The supplied inputs refer to eight issue criteria but do not reproduce or
  individually identify them. No remote issue lookup, legal-currentness check,
  model call, private data access, implementation or execution was performed.
  Findings about new behavior are planning gaps, not claims of implemented
  vulnerabilities or failed tests.
* Existing untracked plan/detail/research/change artifacts were left untouched
  on feat/regulatory-home-chat-214. Only this requested critique is written.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Offline synthetic scope; P02-T01 | Partial | Default-off intent is explicit; a server-enforced dataset/exercise and privacy gate is not specified. PC-001. |
| Atomic doubt copy; C1; P02-T01 | Partial | Existing SQL transactions help, but the JSON transaction only locks and public chat methods commit separately. PC-002. |
| Named owner; C2; P02-T01 | Partial | Juan Manuel Servera and reauthorisation are named; recipient identity, selected-turn binding and stored-envelope access checks are not defined. PC-003. |
| Source-only claims; C3-C7; P01-T01 | Partial | Extractive direction is sound; storage schema, fact provenance and size/failure contracts are missing. PC-004. |
| Question scope and conflicts; P01-T01; P03-T01 | Partial | Tests are named without a deterministic selection, unsupported-question or conflict-routing contract. PC-005. |
| Evaluation/card comparison; P03-T01 | Partial | Comparator and safety categories are promised without fixed expected outcomes, scoring or pass conditions. PC-006. |
| Eight issue criteria; P03-T02 | Missing | No criterion-by-criterion acceptance mapping is supplied. PC-007. |
| Local app validation; P03-T02 | Partial | Health/case/chat responsiveness does not exercise the new panel and handoff. PC-008. |
| Agents data-only; alerts unchanged; src-only | Covered | Plan explicitly excludes agent database/tools, rule-alert suppression and legacy production edits. |
| No live/model/staff-value claim | Covered | Research contrarian section and plan follow-ups preserve these exclusions. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 5 High, 3 Medium, 0 Low.
* The bounded approach is appropriate and requires no new scope decision.
  However, default-off is not yet a credible synthetic-only admission contract,
  and an existing repository transaction is not by itself a portable atomic
  handoff. Concrete source-envelope, selection and acceptance contracts are
  also needed before implementation can be assessed reproducibly.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Synthetic opt-in lacks an enforceable admission boundary

* Related IDs: P01-T01, P02-T01, P03-T01; offline synthetic requirement.
* Evidence: The plan says "fail-closed synthetic opt-in"; phase details say only
  "Synthetic mode is off by default." src/api/src/zava_forward/api/server.py
  composes the ordinary store, chat and agent worker. In
  src/core/src/zava_forward/core/chat_privacy.py, decision/_require gate storage
  on DPIA, lawful-basis and notice references. ADR 0005 distinguishes simulated
  authority from real approval.
* Concern: No admission predicate establishes that the loaded case data and
  owner authority belong to this synthetic exercise. A single feature flag
  could expose the new behavior against ordinary runtime data. Nor is it clear
  how the exercise will satisfy existing privacy admission without bypassing it
  or treating constructed references as real approvals.
* Impact: An implementation could pass a default-off test while violating the
  offline-only scope or weakening existing chat controls.
* Smallest useful change: Specify one server-side gate for every new read,
  turn and referral route: explicit enablement plus validated synthetic
  dataset/exercise binding, a permitted offline execution mode and visibly
  simulated authority/privacy references. Missing, malformed or incompatible
  inputs deny. Define that configured provider credentials cannot cause model
  fallback or outbound calls in this path. Leave ordinary chat gates unchanged.
* Action owner: Planning parent; API implementer owns the resulting guard.
* Exact resolving evidence: Revised P02-T01 admission predicate and P03-T01
  matrix for absent/false/malformed enablement, absent/wrong dataset marker,
  mismatched exercise, production-mode denial, privacy-reference handling and
  enabled synthetic success. Tests must assert no reads/writes through denied
  new routes and zero provider calls, including with a configured provider.
* Decision route: Direct planner correction. The user has already selected
  offline synthetic scope; no actual legal or privacy approval is requested.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Existing transactions do not establish portable atomic handoff

* Related IDs: C1, P02-T01, P03-T01.
* Evidence: P02-T01 requires copying a turn "inside one existing repository
  transaction." In src/core/src/zava_forward/core/chatthreads.py,
  MemoryRepo.txn only acquires a lock, MemoryRepo.commit saves the document,
  SqlRepo.txn explicitly rolls back, and chat_create_thread/chat_add_message
  each open their own transaction and commit. Their audit events occur after
  the transaction. src/core/src/zava_forward/core/store.py save replaces the
  live document and audit writes separately.
* Concern: Calling the public chat methods inside an outer transaction can
  nest SQL transactions or save partial JSON state. Locking alone cannot undo
  an inserted inbox thread, message or referral marker after a later failure.
  Post-commit audit failure also needs an explicit outcome rather than a
  misleading claim that the durable copy was rolled back.
* Impact: A reported failure could leave a partial or duplicate handoff, or the
  sender could receive success without a complete durable selected-turn copy.
* Smallest useful change: Plan a single repository-level handoff operation
  using low-level writes and one commit. Define its atomic records and
  concurrency/version checks. Provide rollback or staging for JSON as well as
  SQL, and distinguish durable commit outcome from metadata-audit failure.
  Define retry/duplicate behavior without adding a delivery service.
* Action owner: Planning parent; core persistence implementer.
* Exact resolving evidence: Revised operation contract plus planned fault
  injection after destination creation, each message write, referral-state
  update and save/commit. Both JSON and SQLite tests compare pre/post in-memory
  and reopened state, verify no partial copy, cover stale/deleted source turns
  and concurrent/retried requests, and exercise the stated post-commit audit
  failure behavior. Preserve SQL-portable statements; do not label SQLite as
  live Azure SQL proof.
* Decision route: Direct planner correction; atomicity is already required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Recipient and stored-turn authorization need explicit contracts

* Related IDs: C1, C2, P02-T01, P03-T01; named doubt-route requirement.
* Evidence: The plan names Juan Manuel Servera and phase details require an
  owner-only inbox and reauthorisation on every read/turn/referral.
  src/core/src/zava_forward/core/chatthreads.py user_key derives ownership
  from email; chat_resume filters the owner but does not apply current case or
  field projection to stored content. In
  src/core/src/zava_forward/core/chat_isolation.py, current_user and
  case_context are separate checks.
* Concern: The plan does not bind the named exercise recipient to a unique
  server-provisioned principal, define receiver case/field eligibility or bind
  a referral to a server-loaded question/answer pair. "Reauthorise" alone does
  not say what happens when historical envelopes contain fields the sender or
  recipient can no longer read.
* Impact: A generic administrator, client-selected owner or stale role could
  receive content outside the intended selected-turn grant; copying a thread
  into an inbox must not grant access to the sender's thread or memory.
* Smallest useful change: Define the synthetic Juan Manuel Servera identity
  binding without inventing a real email or tenant identifier. Derive the
  recipient on the server, reject client owner/content overrides, load the
  selected pair by owned thread/turn identity and revalidate both principals'
  current case/field rights. Deny or safely reproject stored envelopes on
  resume/inbox/referral when rights change. Missing/ambiguous binding denies.
* Action owner: Planning parent; API/core authorization implementer.
* Exact resolving evidence: Revised handoff request/response and inbox access
  contract; negative tests for forged sender/recipient/pair, another user's
  turn, mismatched case, removed/revoked recipient, role downgrade after
  storage and unauthorized historical reads. Positive evidence shows only
  the selected pair and its permitted citations in the named recipient's
  isolated inbox, with no source-thread or memory access.
* Decision route: Direct planner correction. The named owner is already
  decided; real tenant provisioning and operational delegation remain deferred.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Complete immutable envelopes are not mapped to the chat contract

* Related IDs: C1, C3, C7, P01-T01, P03-T01.
* Evidence: The plan requires every factual fragment to carry an immutable
  source/fact ID, status and dates. P01-T01 says to store the full envelope as
  an assistant message with IDs in evidence.
  src/core/src/zava_forward/core/chatthreads.py limits content to 8,000
  characters and evidence to 20 strings of 200 characters; _clean_evidence
  stringifies inputs. ChatIsolation.case_context returns projected values,
  not immutable fact-version records. LawStore.provision does provide
  immutable provision metadata.
* Concern: The serialization, bounded size and immutable fact provenance are
  undefined. Passing citation objects as evidence would stringify them, while
  a fact ID based only on a mutable field path could later resolve to a
  different value. Rendering and referral might reconstruct a past answer
  against changed facts or source status.
* Impact: A cited answer can lose its evidential envelope or fail persistence;
  restart and handoff tests cannot prove the promised historical fidelity.
* Smallest useful change: Specify a versioned envelope, where it is serialized
  under existing storage limits, and what its evidence strings reference.
  Include exact excerpt/fact snapshot, immutable version or hash binding,
  case, source status/dates and explicit unknown metadata rather than invented
  dates. Set input/output bounds and a deterministic overflow failure.
  Historical snapshots must remain distinguishable from fresh eligibility.
* Action owner: Planning parent; core/agents contract implementer.
* Exact resolving evidence: An explicit schema and representative bounded
  payload in phase details; planned round-trip/restart/referral equality tests,
  changed-fact/source tests, citation/fragment integrity tests and boundary/
  oversize tests against both JSON and SQLite chat repositories.
* Decision route: Direct planner correction; no new store or legal prose is
  necessary.

<!-- rpi:critique id=PC-005 -->
### PC-005 [High]: Extraction alone does not define relevance, refusal or conflict behavior

* Related IDs: C3-C7, P01-T01, P03-T01.
* Evidence: P01-T01 selects structured fields "by question purpose" and uses
  shared eligibility; P03-T01 names legal refusals and conflicts. In
  src/core/src/zava_forward/core/rule_engine.py, citation_eligibility returns
  citation metadata and an eligibility state, not question applicability or
  conflict detection. In src/core/src/zava_forward/core/rulecards.py,
  is_active supplies lifecycle/date selection, not question relevance.
* Concern: The supported question purposes, allowed fact fields, matching
  rules, empty/ambiguous behavior and conflict signals are unspecified. Exact
  quotations can still be irrelevant or misleadingly presented as applying
  to the home. "Conflicts show both and route" also leaves unclear whether a
  copy is automatic despite the explicit selected-turn doubt action.
* Impact: An arbitrary question may receive a generic card dump that appears
  grounded, or conflict handling may invent legal interpretation or silently
  share content without the required explicit action.
* Smallest useful change: Define the finite offline question-purpose mapping,
  allowed fields and card/provision selection, stable ordering and budgets.
  Require active simulated approval plus successful citation eligibility.
  Define unsupported/ambiguous/legal-conclusion refusal and deterministic
  conflict fixtures/signals. Show eligible conflicting excerpts without
  choosing a legal winner; offer the named doubt action but copy only after
  explicit user action. Keep unavailable/ineligible evidence clearly separate
  from answer support.
* Action owner: Planning parent; API retrieval and agents renderer implementers.
* Exact resolving evidence: A finite purpose/field/card/refusal table and
  explicit conflict transitions; planned tests for unrelated questions,
  ambiguity, semantically legal requests, missing/ineligible citations,
  held/retired/unapproved cards, relevant conflicting sources, and no referral
  before a click. Tests assert fragment-to-source equality, not merely that
  one valid citation occurs somewhere in the answer.
* Decision route: Direct planner correction. No actual legal interpretation
  or expansion to open-ended language understanding is needed.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Evaluation and card comparison have no falsifiable scoring contract

* Related IDs: P03-T01, acceptance criteria; research contrarian section.
* Evidence: The plan requires deterministic evaluation/card comparison and
  phase details list categories, but neither supplies a fixed question set,
  expected outputs, metrics, denominators or pass conditions.
  src/agents/src/zava_forward/agents/chat_eval.py already distinguishes
  implementer-authored development evaluation from held-out/model/human
  evidence and never returns live enablement approval on that basis.
* Concern: A report could call a run successful merely because it completed,
  or count scripted answer production as lookup benefit without a defined
  baseline. The existing arbitrary-prose panel evaluation is not sufficient
  evidence for this new extractive path.
* Impact: Results would not be reproducible or capable of disproving the
  claimed bounded value.
* Smallest useful change: Freeze the synthetic cases, questions, source/card
  versions and clock. Define expected purpose, fact/provision IDs, refusal/
  conflict outcomes and safety assertions. Set zero-tolerance engineering
  failures for leakage, unsupported fragments, unauthorized writes and
  suppressed alerts. Compare the same inputs with a specified deterministic
  card-with-provision-links path; define lookup/join counts or other explicit
  offline measures, denominators and equal-quality checks. Report neutral or
  negative outcomes honestly.
* Action owner: Planning parent; evaluation implementer.
* Exact resolving evidence: Revised P03-T01 evaluation specification with exact
  runner/report targets under src, expected-output fixtures, thresholds,
  baseline algorithm and report fields. Two identical runs must yield the
  same semantic results; any timings are separately labelled variable.
  AI quality, comprehension, net staff effort and live enablement remain
  explicitly not evaluated.
* Decision route: Direct planner correction; these are synthetic engineering
  thresholds, not a request to approve operational AI thresholds.

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: The eight-criterion acceptance audit is deferred rather than defined

* Related IDs: Plan acceptance criteria, P03-T02.
* Evidence: The plan says "Audit all eight issue criteria" without reproducing
  or identifying them. The supplied research also has no eight-row mapping.
* Concern: There is no supplied contract for deciding which criteria this
  bounded slice can satisfy, partially demonstrate or must leave unmet.
* Impact: Implementation could cover the listed tests yet omit an issue
  criterion or overstate full #214 acceptance.
* Smallest useful change: Have the planning parent insert the authoritative
  eight criteria from its issue context into an acceptance matrix, mapping
  each to the bounded behavior, test/report evidence and explicit limitation.
  Do not invent missing criteria or broaden the user-approved slice.
* Action owner: Planning parent.
* Exact resolving evidence: Eight identifiable criterion rows in the plan or
  phase details, each linked to a planned assertion and a supported offline/
  partial/unmet disposition. Real-model, Azure, staff and operational gates
  must remain unmet where applicable; issue checkboxes remain untouched.
* Decision route: Direct planner correction using existing issue evidence.
  If the parent lacks that evidence, obtain the issue text before finalizing;
  no user scope decision is otherwise needed.

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: Local responsiveness is not an exercise of the new feature

* Related IDs: P02-T01, P03-T02.
* Evidence: P03-T02 defines the local app exercise as a loopback HTTP harness
  checking responsive health/case/chat. P02-T01 adds a separate regulatory
  endpoint, panel controls and owner inbox. Those additions are not identified
  in the HTTP acceptance flow.
* Concern: Existing chat can remain responsive while new route dispatch,
  panel wiring or the selected-turn doubt action is broken.
* Impact: The proposed local validation could pass without demonstrating any
  user-visible #214 behavior.
* Smallest useful change: Extend the explicit loopback flow to the real new
  handlers: disabled denial, enabled synthetic cited turn, persisted resume,
  explicit doubt, recipient inbox read and unauthorized read denial. Exercise
  the new panel's case/home binding and doubt control with existing UI test
  tooling if available; otherwise record that HTTP does not verify browser
  interaction. Include failure display when no unique owner is provisioned.
* Action owner: Planning parent; API/UI validation implementer.
* Exact resolving evidence: Revised P03-T02 named request/assertion sequence
  through the actual server, with synthetic workspace-local data paths and
  provider spies that fail on outbound inference. Record observed new-route
  results separately from static/UI wiring evidence and any untested browser
  behavior. No hosted or live Azure acceptance follows.
* Decision route: Direct planner correction; no deployment or new tooling is
  required merely to improve the HTTP checks.

## Strengths and Residual Risk

* Correctly keeps SQL authority and retrieval in the API and the agents layer
  data-only, rejects C7's any-citation arbitrary-prose validator, preserves
  deterministic alerts and excludes source-monitor candidates.
* Correctly names Juan Manuel Servera for this exercise without claiming actual
  legal/compliance/DPO approval, and distinguishes simulated approvals from
  operational authority.
* Correctly preserves the card-with-links alternative and explicitly excludes
  real-model benefit, human comprehension/net effort, live source approval,
  Azure acceptance and continuing-stock acceptance.
* These deliberate limitations are not findings requiring scope expansion.
  Source-only extraction still requires relevance and access checks; the
  findings above concern making the chosen scope verifiable.

## Questions or Blocking Evidence Gaps

* No new user question is required. The supplied direction resolves scope,
  autonomy, recipient and acceptance limits.
* The eight authoritative issue criteria are absent from the supplied inputs.
  PC-007 routes that bounded evidence gap to the planning parent rather than
  inventing criteria or performing new external research.

## Limitations

* This is a plan assessment, not code validation or a security audit. No tests,
  model calls, browser, SQL server or Azure workload were run.
* Existing contracts were inspected only as necessary for this integration.
  Pre-existing limitations are cited to prevent an unsupported reuse claim,
  not to request unrelated repairs.
* No source currency, actual delegate authority, private identity or production
  data provenance is established.

## Recommended Next Action

* Highest-impact finding: PC-001, followed by PC-002.
* Action owner: Planning parent.
* Smallest next action: Specify the synthetic admission predicate and portable
  atomic handoff contract, then directly disposition PC-003 through PC-008 in
  the plan and phase details.
* User response required: No. All eight findings are direct planner corrections
  within the confirmed scope, not significant or divergent human decisions.
* Final-candidate stop: Return this single complete finding set to the active
  planning parent. Do not run another critique pass.

## Next Steps

No user action is required. The active planning parent should revise and
finalize against PC-001 through PC-008, preserving explicit offline limitations
and leaving operational approvals and issue acceptance checkboxes unchanged.
