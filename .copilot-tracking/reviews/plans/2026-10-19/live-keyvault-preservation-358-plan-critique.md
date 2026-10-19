---
title: Existing-resource preservation plan critique
description: Original independent final-candidate critique for issue 358
ms.date: 2026-10-19
---

## Metadata

* Task ID: issue-358-live-preservation.
* Slug: live-keyvault-preservation-358.
* Critique date: 2026-10-19.
* Branch: test/live-keyvault-preservation-358.
* Observed HEAD and supplied base: 7f96d9957b28cb174aa759c842376f24087d71a3.
* Plan: .copilot-tracking/plans/2026-10-19/live-keyvault-preservation-358-plan.md.
* Phase details: .copilot-tracking/details/2026-10-19/live-keyvault-preservation-358-phase-details.md.
* Critique execution status: Complete.
* Assessment: one original independent critique of the supplied current plan and details.

## Inputs and Criterion Boundary

The caller requires ordered Research, original critiqued Plan, Implement and
original Review. The authorized branch outcome is a truthful, local,
no-source/no-cloud-change blocked disposition if the literal live preservation
criterion cannot be exercised. Existing ama operations authority does not
authorize Graph changes, new credentials, representative-state preparation,
SQL writes, restarts, traffic/identity/network changes or deletion of ama.
There must be no repeat offline substitute, heavy gate for this blocked
no-change result, or publication without coordinator exact-candidate and
receipt checks.

Inputs read:

* The complete supplied current research, plan and phase details.
* The caller's current requirements and evidence qualifications. No earlier
  main-context conversation or complete original issue/comments were supplied
  directly to this critic; the research's account of those is secondary evidence.
* Sanitized external research-management-summary.json, observed
  2026-10-19T14:19:11.406170+00:00, and profile-summary.json, observed
  2026-10-19T14:20:43.821597+00:00, at the caller-supplied external evidence
  location. No raw payloads, credentials or secret values were inspected.
* infra/scripts/setup-entra.py: Azure.call/rest, require_demo and its
  deployment-contract context, preserve_app_secrets, secret_reference,
  verify_secret_handoff and record_credential_store.
* infra/README.md: existing credential-preservation and recovery section.
* docs/architecture/cutover-evidence-pack.md: original Credential
  Preservation Offline Follow-Up (2026-10-17), including its live criterion.
* Repository case-study, knowledge-base index and memory context. No new
  regulatory or architecture assessment is made.

The independent assessment covers requirements, research conclusions, P01 and
all three tasks, acceptance, dependencies, safety, rollback, privacy, test
ownership and handoff. It assesses the credibility of a no-write disposition,
not successful Azure preservation, a production profile, app-value usability,
policy/provider authorization, a clean implementation candidate or publication
readiness. No Azure calls, tests, child agents or source changes were performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Ordered RPI and original independent stages | Covered | Research exists; P01 depends on this original critique; P01-T03 requires one original Review and immutable original outcomes. |
| Literal acceptance / AC1 / research B1 | Covered | All three primary app GET summaries explicitly report secrets null, zero visible KV pairs and zero listed binding counts. No populated target is demonstrated; AC1 remains Blocked / Not run. |
| C1-C4 / FR2 / P01-T02 | Covered | Pure preserve_app_secrets transforms inventories; Azure.rest supplies the ARM transport. Full secret_reference mutation additionally creates a Graph password and changes handoff/store tags. The plan does not invoke or falsely claim that path. |
| Authority and profile distinction | Covered | Permission metadata is explicitly not successful provider authorization. Actual require_demo refusal concerns unknown/malformed deployment evidence and roster eligibility, not a proved production profile or universal ARM prerequisite. |
| FR1 / P01-T01 / AC3 | Covered | Final production GET metadata comparison is read-only. Secret null/presence, counts, revision/ready state and lock/handoff observations are retained; changes are reported, not restored. |
| Probe limitations | Covered | Research preserves the agents auth request error, API auth observations and unexecuted listSecrets/PATCH. A failed probe is not converted into an empty successful auth inventory. |
| FR3 / AC4 / P01-T02 | Covered | Dated deltas go into existing runbook/evidence/index; log append only; memory and historical offline/adverse evidence remain untouched. |
| FR4 / rollback and cleanup | Covered | Zero writes need no cloud rollback, payload backup or lock. Task-owned cleanup is limited to attributable bytecode; concurrent external state must not be restored or deleted. |
| Privacy / non-functional requirements | Covered | Sanitized metadata only; no raw app payload, resource identifiers, credentials, tokens, private roster or secret values in durable evidence. External summary permission requirements are explicit. |
| Test ownership and candidate lock | Covered | Existing setup suite owns behavior; zero additions and removals, no generated targets, no source defect or test change. Markdown/link/diff checks are not represented as behavioral acceptance. |
| AC2 / P01-T03 | Covered | Durable blocked evidence and original Review are pending implementation, not already claimed complete. Changes record must separate executed reads from unexecuted helper, mutation and gates. |
| Heavy-gate exception and publication | Covered | The explicit caller exception applies only to this local blocked no-source/no-cloud-change result. No receipt or review-ready candidate is invented; a later publication candidate needs the full applicable gate and independent coordinator checks. |
| Future populated-target operation | Covered as deferred | Fresh actual-resource planning/critique, private inventory, concurrency and restart-risk analysis are required before a later operation. This is not current execution authorization. |

## Verdict

* Verdict: Pass.
* Rationale: The plan is credible for its narrowly stated no-write evidence
  disposition. The decisive missing populated target is directly supported by
  the supplied production-GET summaries. It neither substitutes an empty
  rebuild/clone nor treats historical offline tests as live proof. The
  profile and permissions qualifications match the supplied evidence.
* This Pass concerns plan credibility only. It does not pass AC1, complete
  issue 358, approve a mutation, waive later publication gates or establish
  operational readiness.

## Findings

No actionable substantive findings within the supplied assessment boundary.
Severity counts: Critical 0, High 0, Medium 0, Low 0.
No PC identifiers are assigned because no planner correction or unresolved
user decision is required. No discoverable concerns are withheld for another
critique.

## Strengths and Residual Risk

* The plan rejects both overbroad Graph/image prerequisites for the isolated
  ARM/helper boundary and an unauthorized attempt to exercise full setup.
  The latter also has tagging, credential and runtime effects absent from an
  inventory-only component exercise.
* Explicit secrets null and zero visible bindings are observations at the
  stated read window, not proof about every possible hidden value or future
  state. No listSecrets was performed. This limitation does not justify a
  write: there is no demonstrated pre-existing KV pair to preserve.
* The agents auth read is unresolved. This remains a limitation, not an
  additional necessary blocker to the no-write disposition.
* Advisory-lock/handoff absence does not prove exclusive access. The plan
  appropriately performs no write and treats final-read differences as
  external/concurrent changes, never permission to restore state.
* The no-heavy-gate exception is the caller's explicit disposition rule,
  not a claim that documentation changes are generally exempt. Planned
  evidence/documentation changes remain local and non-publishable here.
* A future populated-target plan must establish its exact payload, value
  usability checks, pre-write coordination, versionless-reference risks,
  revision/traffic invariants and rollback inventory against that target.
  Current conditional discussion is not a reusable approved mutation runbook.

## Questions or Blocking Evidence Gaps

No decision-critical gap blocks assessment or execution of this no-write plan.
AC1 itself is blocked by the absence of a demonstrated populated eligible
existing target. Clearing that live criterion requires later target evidence
or separately scoped representative-state preparation; current direction
already requires stopping rather than creating state merely to pass.

## Limitations

* The supplied sanitized primary records were read, not independently
  regenerated. This critique performs no Azure operation or credential access.
* External record permission modes are reported by research and plan, not
  independently verified here. Do not infer a permissions audit.
* Research citations to official schema/secret behavior and issue history
  were assessed as supplied evidence; no external retrieval was repeated.
* Only the current plan/details are graded. The final readback, documentation
  diff, changes record and original Review do not yet exist as completed
  deliverables of P01 and cannot receive acceptance from this critique.
* The starting worktree contains untracked current RPI inputs/state. HEAD
  equals the supplied base; there is no frozen clean publication candidate.
* Plan, details, research, source, historical evidence and state are unchanged
  by this critique. The only authorized output is this critique artifact.

## Recommended Next Action

* Highest-impact finding: none; AC1's populated-target blocker remains explicit.
* Action owner: planning parent, then implementation coordinator.
* Smallest next action: record this Pass without changing original critique
  content; execute only P01's final read-only check and bounded evidence
  updates, then obtain the one original independent Review.
* User response required: no for the current blocked disposition. Any later
  divergent representative-state preparation needs separate scope/authority;
  it must not delay or be implied by this handoff.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-19/live-keyvault-preservation-358-research.md](.copilot-tracking/research/2026-10-19/live-keyvault-preservation-358-research.md) | Current research and sanitized evidence provenance |
| [.copilot-tracking/plans/2026-10-19/live-keyvault-preservation-358-plan.md](.copilot-tracking/plans/2026-10-19/live-keyvault-preservation-358-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-19/live-keyvault-preservation-358-phase-details.md](.copilot-tracking/details/2026-10-19/live-keyvault-preservation-358-phase-details.md) | Assessed execution details |
| [.copilot-tracking/reviews/plans/2026-10-19/live-keyvault-preservation-358-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-19/live-keyvault-preservation-358-plan-critique.md) | This original independent critique |
| [infra/scripts/setup-entra.py](infra/scripts/setup-entra.py) | Unchanged production helper and transport boundaries |
| [infra/README.md](infra/README.md) | Existing credential-preservation runbook |
| [docs/architecture/cutover-evidence-pack.md](docs/architecture/cutover-evidence-pack.md) | Original offline evidence and literal live criterion |

## Next Steps

Return Complete / Pass to the active planning parent. No repeat critique or
user response is required. The parent may continue only the no-write P01
disposition and original Review, retaining AC1 Blocked / Not run and no
publication. Later publication requires the coordinator's independent
exact-frozen-candidate and valid receipt checks; this critique supplies
neither.
