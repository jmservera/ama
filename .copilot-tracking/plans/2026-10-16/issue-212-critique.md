---
title: Issue 212 final-candidate plan critique
description: One bounded independent assessment of deterministic checks and scoped alerts
ms.date: 2026-10-16
---

## Metadata

* Task ID: 212 / issue-212
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/issue-212-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/issue-212-phase-details.md
* Research: .copilot-tracking/research/2026-10-16/issue-212-research.md
* Critique execution status: Complete
* Review count: exactly one final-candidate assessment; no implementation or delegation.

## Inputs and Criterion Boundary

* Assessed the three supplied artifacts and the caller's explicit requirements:
  src-only code; approved immutable cards with unapproved seeds; five results;
  missing evidence unknown; no future or consultation activation; code-owned
  clocks and independent holds; actionable cited alerts; breach acknowledgement
  and outcome; no resident messages; home grouping, deadline/harm ranking,
  attention throttling and false-positive measurement; safe engine failure;
  checkpointed idempotency; role-scoped API; portable SQL; tests outside packages.
* Read the required project context in docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. These do not supply operational approvals.
* Used the supplied architecture pointer, docs/adrs/0005-regulatory-compliance-assistant.md,
  architecture sections 3 and 4, to confirm deterministic results, triggers and
  alert obligations. Consulted only core rulecards/lawstore and API server code
  for material feasibility and existing authority boundaries.
* P01 precedes its corresponding P02 validation and delivery. No implementation,
  private dataset, environment file, editor configuration, GitHub-issues tracking
  folder, live service, legal source retrieval or additional research was used.
* The research reports nine issue criteria but does not reproduce them. This
  assessment covers the caller-supplied boundary, not an independently verified
  complete issue-body acceptance audit.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Src-only code; tests outside packages | Partial | Src-only scope is explicit; P02 should name existing external test directories, PC-008 |
| Approved cards; immutable contract; draft seeds, C4, P01-T01 | Covered | New draft binding, retained history and unchanged seeds are credible; no fabricated approval requested |
| Five results; missing evidence; code clocks/holds, P01-T02 | Partial | Safe principles are stated but executable applicability/result and clock semantics are not bounded, PC-002 |
| Exact citations; current source status/version, C5, P01-T02 | Covered | Explicit identifiers, current-version/status/completeness checks and unknown fallback; test these boundaries |
| Three triggers; atomic persistence; checkpoint/replay, P01-T02/T03 | Partial | Time-based key and post-commit dispatch leave retry/recovery ambiguity, PC-003 |
| Safe action/owner/clock; breach acknowledgement/outcome; no messages | Partial | No messaging and no hold mutation are explicit; complete alert/disposition contract is missing, PC-006 |
| Home grouping; deadline/harm ranking; attention limit; false positives | Partial | Requirement list does not define publication versus checks or measurable false-positive rate, PC-006 |
| Engine-down safety, P01-T03 | Partial | Cannot reliably persist or present an ordinary unknown through a failed law adapter, PC-005 |
| Scoped API and named-owner dispositions, C7, P01-T03 | Partial | Existing rule-owner capability is not a case-scope or operational alert-owner assignment, PC-004 |
| Portable SQL and adapter validation, P01-T02, P02-T02 | Partial | Required prohibited constructs and local portability proof omitted, PC-007 |
| Validation tooling and nine-row acceptance audit, P02 | Partial | Forbidden scratch location and unspecified acceptance mapping, PC-001/PC-008 |
| Legal approval, real staff trial, Azure/SQL Server, UI | Covered as limitations | Explicitly unmet; not expanded into acceptance work here |

## Verdict

* Verdict: Revise
* Severity summary: 5 High, 3 Medium; no Critical or Low findings.
* Rationale: The architecture and approval boundary are credible, but replay,
  outage behavior, authorization and executable semantics need planner-owned
  corrections before implementation. All findings below form the complete
  actionable set for this supplied boundary, not a request for serial critiques.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Validation instructions direct tools to a prohibited scratch location

* Related IDs: User Decisions and Requirements; P02-T02.
* Evidence: .copilot-tracking/plans/2026-10-16/issue-212-plan.md specifies
  `/tmp/zf164`; .copilot-tracking/details/2026-10-16/issue-212-phase-details.md,
  P02-T02, repeats it. The current caller environment prohibits all temporary
  directory file operations.
* Concern: Following the plan would violate the active execution boundary.
* Impact: The candidate is not executable as written, regardless of code quality.
* Smallest useful change: Remove that tool-location instruction. Use available
  installed tools or a project-relative environment if dependencies are actually
  missing; retain pip-only installation and the stated dependency-install gate.
* Action owner: Planning parent.
* Exact resolving evidence: Both artifacts contain compliant validation commands
  with no temporary-directory operations. Do not install anything during critique.
* Decision route: Direct planner correction; parent can apply directly. No user
  decision is needed because the current restriction resolves the conflict.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: The bounded execution specification lacks an executable decision contract

* Related IDs: Scope and Non-Goals; Functional Requirements; P01-T01/T02; C4/C8.
* Evidence: .copilot-tracking/plans/2026-10-16/issue-212-plan.md names two
  executable kinds and five states. The phase details specify bounded approved
  hours and unknown for ambiguous evidence, but do not define facts, result
  precedence or clock start/threshold behavior for either kind.
  src/core/src/zava_forward/core/rulecards.py:161-199 currently accepts prose
  fields and requires explicit extension for new executable fields.
* Concern: An implementer must still invent which SQL facts establish
  applicability, attention, breach risk or clear, and which evidence starts
  an approved clock. A missing fact could accidentally become not applicable,
  or a technical default could become an invented legal threshold.
* Impact: Determinism alone would not prevent unsupported clear results or
  unsafe clock behavior.
* Smallest useful change: Add a compact contract/decision table for each kind:
  whitelisted SQL fact fields and types; approved immutable parameters; exact
  five result strings; missing/invalid evidence precedence; explicit
  not-applicable evidence; UTC awareness/start and threshold boundaries;
  behavior for future/invalid timestamps; and the separation from hazard holds.
  Include attention thresholds only as explicit approved exercise parameters,
  never inferred legal policy. State how the proposal API accepts and history
  exposes the contract before approval.
* Action owner: Planning parent.
* Exact resolving evidence: P01 contract tables and P02 test cases for every
  result, missing versus explicitly false applicability, exact clock boundaries,
  unchanged holds and rejection of unsupported fields/parameters. Only test
  fixtures simulate approval; no seed or live approval is added.
* Decision route: Direct planner correction; parent can apply directly within
  the confirmed bounded exercise scope, without legal interpretation.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Current time in the replay key does not define retry or crash recovery

* Related IDs: P01-T02/T03; Non-Functional Requirements; C1/C6.
* Evidence: .copilot-tracking/details/2026-10-16/issue-212-phase-details.md,
  P01-T02, hashes trigger and code-owned UTC time and promises exact replay;
  P01-T03 checks after committed mutations. No stable trigger identifier,
  persisted evaluation time, catch-up cursor or lost-dispatch recovery is defined.
* Concern: A retry with a fresh time becomes a new check. Conversely, a process
  can stop after case commit but before check/checkpoint persistence, leaving
  no durable record that the committed mutation needs evaluation.
* Impact: Duplicate alert publication or missed checks can occur despite
  atomic writes inside the law adapter.
* Smallest useful change: Define stable event identity and evaluation time for
  transition/data triggers, a bounded schedule slot/cursor, a uniqueness key,
  and restart catch-up over committed facts without requiring a cross-store
  transaction. Define lock order and publication/checkpoint rollback together.
  A rescan design is sufficient if its coverage and cursor rules are explicit.
* Action owner: Planning parent.
* Exact resolving evidence: Revised key/cursor/recovery contract and tests for
  later-time retry, duplicate trigger delivery, restart after case commit but
  before evaluation, failure between check/alert/checkpoint writes, bounded
  schedule resume and distinct later clock evaluations.
* Decision route: Direct planner correction; parent can apply directly.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Rule-card owner capabilities do not establish case-scoped alert authority

* Related IDs: Role-scoped API; P01-T02/T03; C7.
* Evidence: .copilot-tracking/details/2026-10-16/issue-212-phase-details.md
  says reuse existing trusted owner capabilities. In
  src/api/src/zava_forward/api/server.py:390-423, those capabilities govern
  rule authors/approvers; the law GET branch at lines 231-251 serves reference
  data, not per-case alert visibility. Neither proves an operational alert's
  named decision owner can read or act on that case.
* Concern: A rule approver and a repairs/decision owner are different
  responsibilities. General law-read permission or caller-supplied case filters
  cannot establish row scope, and legitimate case owners may lack rule-owner
  capability.
* Impact: Case information may leak or breach dispositions may be inaccessible
  to the intended owner.
* Smallest useful change: Identify the existing server-side case visibility
  check and trusted owner mapping to reuse, and apply them to lists, detail,
  grouping and dispositions. Specify behavior for missing/unassigned owner,
  inaccessible cases and authority-field spoofing. If no trusted assignment
  exists, deny disposition and expose the assignment gap to authorized staff;
  do not invent tenant assignments or privileges.
* Action owner: Planning parent.
* Exact resolving evidence: Named authorization integration points and a test
  matrix covering authorized read, other-role/case denial, mixed-case lists,
  guessed alert IDs, named versus unrelated owner, unassigned owner and
  spoofed actor/date/role. Tests use synthetic trusted assignments only.
* Decision route: Direct planner correction; parent can apply directly with
  deny-by-default fallback. Live tenant assignment remains an honest limitation.

<!-- rpi:critique id=PC-005 -->
### PC-005 [High]: Engine-down unknown requires an independent availability path

* Related IDs: Engine-down safety; P01-T03; Validation Ownership.
* Evidence: P01-T03 in
  .copilot-tracking/details/2026-10-16/issue-212-phase-details.md promises
  failures are logged and shown as unknown. All durable checks are assigned
  to the law adapter. src/api/src/zava_forward/api/server.py:235-236 already
  returns 503 when the law store is absent.
* Concern: A failed adapter cannot reliably persist a fresh unknown check.
  Merely logging a post-commit failure does not ensure the caller learns that
  checks did not run, and cached clear results may appear current.
* Impact: Staff may mistake engine absence or stale checks for a completed
  safety assessment, or a handler error may obscure successful safety intake.
* Smallest useful change: Define an explicit availability/freshness envelope
  and safe manual action that can be returned without the law adapter.
  Distinguish unavailable evaluation from a persisted missing-evidence result.
  Preserve successful primary mutation semantics, never release/block existing
  safety work due to the engine, and mark prior results stale/unverified.
* Action owner: Planning parent.
* Exact resolving evidence: Response contracts and tests with the engine
  absent, read failure, evaluation failure and persistence failure. Verify
  primary safety work survives, unavailable/stale status is visible, the safe
  human path is present, and no failed evaluation appears as fresh clear.
* Decision route: Direct planner correction; parent can apply directly without
  adding UI, live deployment or an alternative approval mechanism.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Alert hygiene needs a retained-check and disposition contract

* Related IDs: Functional Requirements; P01-T02; P02-T01; architecture 4.
* Evidence: The plan lists home grouping, deadline/harm sorting and attention
  publication limits. Phase details retain false-positive history and permit
  acknowledgement or outcome, but do not define the alert payload, publication
  window/key, grouped breach visibility, mandatory breach lifecycle or rate
  denominator.
* Concern: Counting false-positive reports is not measuring false-positive
  rate. Throttling or grouping could hide unresolved breach risk, and a bare
  outcome could bypass the required owner acknowledgement.
* Impact: The implementation could satisfy the nouns in the plan while
  failing the actionable-alert and fatigue requirements.
* Smallest useful change: Specify observed fact, exact citation/status,
  safe action, trusted owner and applicable deadline in each alert; stable
  deadline/harm ordering; preservation of unresolved breaches within home
  groups; attention-only publication limits that do not suppress checks or
  breach escalation; and mandatory recorded owner acknowledgement plus outcome.
  Define a reproducible false-positive measure with numerator, denominator,
  population/window and unreviewed state, labeled reported rather than proven
  accuracy. Do not claim a staff precision trial.
* Action owner: Planning parent.
* Exact resolving evidence: A compact payload/lifecycle/measurement contract
  and tests for grouped unresolved breaches, sorting ties, repeat attention,
  throttle expiry, unthrottled breach, acknowledgement/outcome authorization,
  zero denominator and retained false-positive history without risk resolution.
* Decision route: Direct planner correction; parent can apply directly.

<!-- rpi:critique id=PC-007 -->
### PC-007 [Medium]: Portable SQL is a goal without enforceable implementation constraints

* Related IDs: Non-Functional Requirements; P01-T01/T02; P02-T02.
* Evidence: The supplied plan says portable SQL adapters but neither artifact
  states the caller's bans on replace, ignore, autoincrement and pragma.
  src/core/src/zava_forward/core/lawstore.py exposes distinct SQLite and
  SQL Server adapter implementations; ordinary SQLite tests alone do not prove
  new DDL, pagination, parameterization or duplicate-write handling portable.
* Concern: New engine tables and checkpoint inserts can accidentally rely on
  SQLite-only behavior or inherit an inappropriate convenience method.
* Impact: A local pass would not support even the bounded portability claim.
* Smallest useful change: Record the explicit prohibited SQL constructs,
  adapter-owned dialect DDL, explicit portable keys and transaction/error
  handling. Add a local adapter-contract/static SQL assertion for newly added
  statements, alongside real SQLite persistence tests. Leave live SQL Server
  execution explicitly unmet.
* Action owner: Planning parent.
* Exact resolving evidence: P01 SQL constraints and P02 assertions covering new
  schema and operations, duplicate keys, rollback and checkpoint uniqueness;
  the acceptance audit distinguishes local contract proof from live execution.
* Decision route: Direct planner correction; parent can apply directly. Do
  not expand this into rewriting unrelated existing SQL or provisioning Azure.

<!-- rpi:critique id=PC-008 -->
### PC-008 [Medium]: The nine-criterion audit is deferred without a supplied criterion mapping

* Related IDs: Acceptance Criteria; P02-T01/T02; C3.
* Evidence: .copilot-tracking/research/2026-10-16/issue-212-research.md
  reports unchanged GitHub acceptance criteria but contains no criterion text
  or mapping. The plan promises nine audit rows only after implementation.
* Concern: There is no way within the supplied evidence to verify that the
  two executable kinds and planned API cover each of those nine criteria.
  Validation paths also remain ambiguous despite the outside-package rule.
* Impact: Scope omissions may be discovered only at final review, or local
  proof may be mislabeled as complete issue acceptance.
* Smallest useful change: Have the parent reuse its already retrieved issue
  text to place the nine exact criteria or faithful identified excerpts in
  the plan, mapping each to P01 work, external src/core/tests or src/api/tests
  evidence, and remaining limits. Do not fetch new evidence during this critique.
* Action owner: Planning parent, which owns the C3 retrieval.
* Exact resolving evidence: A nine-row criterion-to-task/test/limitation matrix
  based on that retrieval, explicit existing test-directory paths, and
  acceptance language separating implemented local behavior from legal,
  staff-trial and live-platform gates.
* Decision route: Direct planner correction; parent can apply directly using
  the existing retrieval. If it cannot recover the criterion text, record the
  missing mapping rather than asserting all nine are covered.

## Strengths and Residual Risk

* New immutable contracts are attached only to new draft versions, included
  in owner-visible history and never retroactively added to seeds. This
  preserves the existing distinct author/owner lifecycle.
* Exact provision identifiers, current-version/status/completeness checks,
  unknown for unsupported evidence, no messaging, and no alteration of hazard
  holds are appropriate boundaries.
* The plan explicitly disclaims operational legal approval, SQL Server/Azure
  verification, real staff comprehension/precision trials and accessible UI
  acceptance. Those are retained limitations, not new work requested here.
* Simulated exercise approvals can demonstrate lifecycle behavior but cannot
  establish a legal threshold, real delegation or operational compliance.

## Questions or Blocking Evidence Gaps

* No unresolved user decision is required for these corrections.
* The nine exact issue criteria are missing from this supplied evidence.
  The parent should reuse C3 rather than expand research or invent acceptance.
* Trusted case-owner assignment and executable fact fields need explicit
  integration choices with deny/unknown fallback, not fabricated company facts.

## Limitations

* This is a planning credibility assessment, not a code review, test run,
  legal interpretation, live authorization assessment or release acceptance.
* Existing source was consulted only at the identified rule-card, law adapter
  and API extension points. No runtime, private data or operational approval
  evidence was inspected.
* The initial worktree contained untracked parent RPI artifacts. They were
  left in place unchanged; only this requested critique artifact is written.

## Recommended Next Action

* Highest-impact finding: PC-003, because duplicate or lost evaluations defeat
  the checkpointed safety mechanism despite individually atomic writes.
* Action owner: Planning parent.
* Smallest next action: Define the stable event/checkpoint/recovery contract
  in P01-T02/T03, then apply the remaining direct corrections in this complete
  set and finalize the plan without another critique pass.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/issue-212-plan.md](.copilot-tracking/plans/2026-10-16/issue-212-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-16/issue-212-phase-details.md](.copilot-tracking/details/2026-10-16/issue-212-phase-details.md) | Assessed phase implementation boundaries |
| [.copilot-tracking/research/2026-10-16/issue-212-research.md](.copilot-tracking/research/2026-10-16/issue-212-research.md) | Supplied bounded research |
| [.copilot-tracking/plans/2026-10-16/issue-212-critique.md](.copilot-tracking/plans/2026-10-16/issue-212-critique.md) | Complete one-pass critique and correction evidence |

## Next Steps

The active planning parent can directly apply PC-001 through PC-008, record
their disposition, and finalize without another critique. No user response,
additional agent, implementation, legal activation or live acceptance is
requested or performed by this critique.
