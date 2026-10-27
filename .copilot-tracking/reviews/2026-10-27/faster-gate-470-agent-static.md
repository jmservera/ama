---
title: Issue 470 coordinator agent fresh-context static review
description: Bounded HVE Builder static assessment of the coordinator policy delta against HEAD
ms.date: 2026-10-27
---

## Scope and evidence

* Stage: HVE Builder fresh-context static review only, not issue #470's later RPI Review.
* Target: .github/agents/ama-backlog-delivery-coordinator.agent.md.
* Comparison: working-tree target against HEAD 2fbb42f0ed80b84429fc7962eda1e04e3265e15e, using `git diff HEAD -- .github/agents/ama-backlog-delivery-coordinator.agent.md`.
* Candidate SHA-256: 3f0683ad314f809e40f31131fae59dc0d3ae473347e3764187c49fe2b425ab9a.
* Criteria: supplied owner requirements, HVE Builder requirements-catalog.md and review-rubric.md under /home/azureuser/.copilot/installed-plugins/hve-core/hve-core-all/skills/hve-core/hve-builder/references/.
* Reviewed the complete target for connections to changed rules, without auditing unrelated inherited policy. Did not read the author log or reasoning.
* Write authority: this report only. Existing source and tracking changes remain untouched.

## Requirement assessment

Locations below refer to .github/agents/ama-backlog-delivery-coordinator.agent.md in the reviewed candidate.

| Requirement | Evidence | Assessment |
| --- | --- | --- |
| Parent/sub-issue delivery uses deliberate stacked PRs | Lines 185-190 require child branches and PRs against the integration parent, whose PR targets main. Lines 204-217 distinguish implementation dependencies from parent integration and select the parent SHA for child branches. | Pass |
| Stack lifecycle remains coherent | Lines 26-29 authorize the declared target; lines 350-354 retain needed parent topics and require parent integration validation; lines 363-376 rebase onto the declared target without silently retargeting. | Pass |
| Full gate is limited to the owner-selected categories | Lines 137-149 identify big features, releases, infrastructure, deployment, SQL and security-sensitive changes, with full taking precedence for mixed work. | Pass |
| Small/tooling/documentation work uses planned unit and focused checks | Lines 133-143 require a recorded tier and relevant checks; lines 239-244 carry rationale, test plan and evidence into the brief. Lines 260-283, 317-320, 337-338 and 370-374 keep publication, merge and correction evidence tier-specific rather than unconditionally requiring full receipts. | Pass |
| Required hosted CI and independent review remain mandatory | Lines 145-149 retain hosted CI, complete RPI, exact-head review and human approvals. Lines 311-346 require current evidence and block failing or missing selected-tier checks; local evidence does not replace hosted checks. | Pass |
| Receipt base is main, not the child PR target | Lines 151-160 explicitly keep runner `--base` at current origin/main for a full-tier child and state that its receipt covers the whole stack. Child diff review separately uses the parent topic. No changed rule instructs passing the parent topic to runner `--base`. | Pass |
| Verification images survive until receipt verification | Lines 167-171 preserve failed-run evidence and verification images until `--verify-receipt` succeeds, then defer cleanup to retention policy. | Pass |
| Non-tool frontmatter is preserved | The target's name and description match HEAD; no non-tool capability-bearing frontmatter change is introduced. Tool configuration was excluded entirely. | Pass |

These assessments apply the catalog's Agent architecture: define stage gates and terminal outcomes; Instruction-file architecture: no conflicting layers; Agents and subagents: fresh-context review and bounded reviewer scope; Evaluation and validation: runnable checks and evidence, not assertions; and Safety and enforcement: preserve non-tool capability fields. The applicable rubric dimensions are workflow contract, evaluation hooks, evidence fidelity, safety and enforcement, and convention conformance. Skill packaging and generic output-schema design are not applicable to this delta.

## Findings

None. No actionable Critical, High, Medium or Low findings within the bounded delta.

## Limits and handoff

* Static reading establishes instruction consistency, not observed agent behavior or executable runner correctness. The supplied main-only runner-base contract was sufficient; tools/rpi-checks.py was not read.
* Behavior testing and mechanical validation were not run in this stage. This is not a satisfied-and-skipped behavior gate or an overall HVE Builder lifecycle pass.
* No agents, full gate, Azure operations, commit or push were performed. This report does not replace the issue's later RPI Review, hosted CI or required publication gates.

## Verdict

Pass. The reviewed policy delta meets the supplied requirements without an unconditional full-receipt requirement for focused work or a parent-base claim for the runner. No static correction is required; hand back for subsequent authorized stages.
