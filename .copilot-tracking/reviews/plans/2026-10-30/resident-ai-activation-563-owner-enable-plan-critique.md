---
title: Resident AI 563 owner-enabled activation plan critique
ms.date: 2026-10-30
---

## Metadata

* Task ID: 563-owner-enable-20261030T1710Z
* Slug: resident-ai-activation-563-owner-enable
* Parent: original issue 563, branch ops/resident-ai-activation-563
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/resident-ai-activation-563-owner-enable-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/resident-ai-activation-563-owner-enable-phase-details.md
* Critique execution status: Complete
* Independent final-candidate assessment: one complete finding set; no corrections implemented.

## Inputs and Criterion Boundary

* Read the exact supplied research, plan, phase details and continuation state:
  .copilot-tracking/research/2026-10-30/resident-ai-activation-563-owner-enable-research.md;
  .copilot-tracking/plans/2026-10-30/resident-ai-activation-563-owner-enable-plan.md;
  .copilot-tracking/details/2026-10-30/resident-ai-activation-563-owner-enable-phase-details.md;
  .copilot-tracking/rpi-sessions/2026-10-30/resident-ai-activation-563-owner-enable-state.json.
* Binding owner decision, 2026-10-30T17:10Z, verbatim:
  "Enable AI, I will take care of checking the cost and will warn you if there's a problem".
  A live ledger pre-read is waived. SQL public access, SQL migration and
  bypassing fail-closed runtime accounting remain prohibited. The USD20 cap
  and exclusive 2026-11-01 expiry remain binding.
* Assessed FR1-FR6, AC1-AC6, C1-C10 and all five phase tasks, including
  dependencies, reversible execution, credential handling, bounded model use,
  live evidence, independent Review, local persistence and local-gate outcome.
* Narrow source checks: advisor request/grounding/accounting code, assistant
  host routing, existing browser check, existing credential-safe acceptance
  helper, API documentation and the gate runner's lock declaration. Context
  checks used the original specification, addendum, reference index and
  owner-memory openings. No other session was read.
* Assessment establishes planning credibility, not deployed behavior.
  Management observations C4/C5 are supplied research assertions, not freshly
  reproduced cloud evidence.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner decision; C1, C6; runtime limits | Covered | Waived pre-read is not reinstated; accounting denial still fails verification and triggers restoration. |
| FR1; AC1; C4/C5; P01-T01 | Covered | Fresh private byte-exact backup, hashes, baseline validation and existing identity checks precede mutation. |
| FR2; AC2; C7-C9; P01-T02 | Covered | Disabled baseline, anonymous denial, client no-request and server no-consent checks precede activation. |
| FR3; AC5; C2-C5; P01-T03 | Covered | Exactly two variables, existing account/model/role, preserved image, min0, Manual jobs and employee configuration. |
| FR4; credential controls; P01-T02/T03 | Covered | One intended login, persistent two-submission ceiling, same context, bounded warm-up and no recordings. |
| FR5; AC3; C7/C8; P01-T03 | Partial | Actual model label, pest relevance and host-known sources are required; claim-to-source grounding acceptance is underspecified, PC-001. |
| FR5; AC4; P01-T03 | Covered | Out-of-scope answer must remain rules/manual fallback, without mocked transport. |
| FR6; AC5; C10; P01-T03 | Covered | Mutation-start marker, restoration on verification failure, original revision/traffic and normalized baseline equality are explicit. |
| P02-T01; evidence and limitations | Covered | Failed attempts, original outcomes, uninspected ledger and unmet activation remain distinguishable. |
| AC6; P02-T02; local gate | Partial | Independent Review and local-only commits are explicit; fixed gate lock conflicts with the execution filesystem boundary, PC-002. |
| Continuation state; full-loop boundaries | Covered | Automatic Plan state is not implementation authority until critique disposition; no push, issue closure or repeated critique is authorized. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 0; Medium 2; Low 0.
* Rationale: The activation and rollback sequence is substantially credible,
  and the owner's cost-monitoring decision resolves the former ledger-read
  prerequisite. Two direct planning corrections are needed to prevent an
  unsupported grounding claim and a prohibited local-gate invocation. Neither
  requires a new owner decision or broader Azure authority.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Known source labels do not establish factual grounding

* Related IDs: FR5, AC3, C7/C8, P01-T03, P02-T01.
* Evidence: .copilot-tracking/details/2026-10-30/resident-ai-activation-563-owner-enable-phase-details.md:63-67
  requires pest acknowledgement, uncertainty, a housing-officer route and known
  host sources. src/api/src/zava_forward/api/resident_demo/aoai.py:131-210
  accepts bounded prose with known source IDs, then supplies host-owned source
  descriptions; it does not validate factual entailment.
  src/api/README.md:1051-1055 explicitly distinguishes those structural checks
  from semantic correctness.
* Concern: The listed checks could accept a relevant, cautious response that
  also invents a visit, reporting channel, timing or case fact. Recognized
  source descriptions and collapsed presentation do not prove that the prose
  is supported by those sources. The plan calls the result grounded without
  specifying how that decision is reached.
* Impact: AC3 could be marked met on an unsupported actual-model answer even
  though the user specifically requires grounding.
* Smallest useful change: Add an in-memory claim-to-source comparison for the
  single paid answer. Compare factual/process claims against the actual
  host-supplied guidance and limited own-case projection; reject unsupported
  details or contradictory claims. Retain only safe claim categories,
  source categories and pass/fail reasons, not private records. An unsupported
  or indeterminate grounding result must fail AC3 and trigger FR6 restoration.
  This is a bounded operational content check, not human acceptance or a new
  model-evaluation project.
* Action owner: Planning parent; operations executor performs the check.
* Exact resolving evidence: Revised P01-T03 and AC3 describe the comparison,
  permitted evidence projection and failure-to-rollback rule. Implementation
  evidence later records the actual answer's safe claim/source decisions and
  overall result without an additional inference or raw case export.
* Decision route: Direct planner correction; no user response required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The planned gate invocation has a known filesystem blocker

* Related IDs: AC6, P02-T02, heavy-lock requirement.
* Evidence: .copilot-tracking/plans/2026-10-30/resident-ai-activation-563-owner-enable-plan.md:44
  names the heavy-lock path, and
  .copilot-tracking/details/2026-10-30/resident-ai-activation-563-owner-enable-phase-details.md:104-110
  directs use of the native runner. tools/rpi-checks.py:2243-2244 hardcodes
  /tmp/ama-rpi-heavy.lock; the timeout defaults to 600 at line 2269.
  The current execution filesystem boundary prohibits file operations in
  temporary directories.
* Concern: External gate output and an output-local TMPDIR do not relocate
  this absolute lock path. Invoking the runner as planned would still attempt
  the prohibited operation. The instruction to use an equivalent arrangement
  does not establish an existing compliant, shared serialization mechanism.
* Impact: The executor cannot truthfully promise an attempted complete local
  gate through this command under the current boundary.
* Smallest useful change: Record the known gate prerequisite as blocked before
  invocation. Do not run a command that accesses the prohibited path, move the
  lock unilaterally, substitute an unshared lock, edit gate tooling within this
  operations task or claim a receipt. Preserve the local-only outcome and
  unresolved gate status. Any later compliant gate mechanism must preserve
  shared serialization and 600-second admission under separately established
  authority; no such change is needed to document this blocker accurately.
* Action owner: Planning parent; operations executor preserves the blocker.
* Exact resolving evidence: P02-T02 distinguishes the executable local
  persistence steps from the currently blocked full-gate step and explicitly
  retains the unmet gate/no-publication outcome. A future passing claim would
  additionally require an authorized compliant runner and actual exact-head
  external receipt, not a timeout-only or TMPDIR-only workaround.
* Decision route: Direct planner correction to record and respect a known
  execution blocker; no new user decision is required for this critique.

## Strengths and Residual Risk

* Scope is constrained to ca-resident-demo in RG ama, the two documented
  variables and existing aoai-resident-469/resident-mini account-scoped MI.
  No new resources, roles, secrets, networking or SQL migration are admitted.
* The baseline-first sequence and explicit restoration verification are
  credible. Restoration failure is an urgent blocker, not activation success;
  a restored baseline does not satisfy unmet AC3/AC4.
* Owner monitoring accepts unknown ledger headroom, not unmetered inference.
  Runtime denial may still prevent activation, without reopening the waived
  pre-read requirement.
* Only one paid question is intended; deterministic fallback cannot justify
  repeated paid probing. Login and recording limits are explicitly retained.
* Human content/resident acceptance, whole-WCAG acceptance and whole-issue
  completion remain outside this operational proof.

## Questions or Blocking Evidence Gaps

* No unresolved owner choice is needed to revise the candidate.
* The local-gate execution prerequisite in PC-002 remains blocked; recording
  it does not turn a blocked or unperformed gate into a passing check.
* Fresh backup, actual AI outcome and successful restoration are future
  implementation evidence, not missing pre-critique cloud investigations.

## Limitations

* No Azure, network, browser, model, SQL or credential access was performed.
* No credentials, private configurations or other sessions were read.
* The original continuation inputs were left unchanged. Only this critique
  artifact was written. No implementation corrections, commits or pushes
  were performed.
* The gate source check was limited to the lock declaration and timeout;
  this is not a full runner audit or an executed local gate.

## Recommended Next Action

* Highest-impact finding: PC-001, because the required actual grounding
  acceptance can otherwise be overstated.
* Action owner: Planning parent.
* Smallest next action: Directly revise P01-T03/AC3 for claim-to-source
  acceptance and P02-T02 for the known gate blocker, recording both
  dispositions without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/resident-ai-activation-563-owner-enable-research.md](.copilot-tracking/research/2026-10-30/resident-ai-activation-563-owner-enable-research.md) | Supplied C1-C10 research and owner decision |
| [.copilot-tracking/plans/2026-10-30/resident-ai-activation-563-owner-enable-plan.md](.copilot-tracking/plans/2026-10-30/resident-ai-activation-563-owner-enable-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/resident-ai-activation-563-owner-enable-phase-details.md](.copilot-tracking/details/2026-10-30/resident-ai-activation-563-owner-enable-phase-details.md) | Assessed execution details |
| [.copilot-tracking/rpi-sessions/2026-10-30/resident-ai-activation-563-owner-enable-state.json](.copilot-tracking/rpi-sessions/2026-10-30/resident-ai-activation-563-owner-enable-state.json) | Supplied automatic continuation state |
| [.copilot-tracking/reviews/plans/2026-10-30/resident-ai-activation-563-owner-enable-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/resident-ai-activation-563-owner-enable-plan-critique.md) | Complete independent critique |

## Next Steps

The active planning parent should make the two direct corrections, record
dispositions and finalize without another critique. Preserve the waived
ledger pre-read, runtime safeguards, independent Review, local-only
commits/trailer and Refs #563 boundary. No user action is required.
