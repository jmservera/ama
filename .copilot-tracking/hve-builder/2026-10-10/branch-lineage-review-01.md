---
title: "Static review: branch lineage workflow"
date: 2026-10-10
mode: review
stage: static-review
profile: Medium
target: .github/copilot-instructions.md
source_changed: false
---

## Scope and evidence

* Reviewed: .github/copilot-instructions.md, Branch and Pull Request Workflow, with remaining file context only for conflicting instructions.
* Criteria: user-supplied branch-lineage invariants; requirements catalog; review rubric.
* Excluded: author and intake logs, behavior execution, validation, tests, workspace exploration, and unrelated project-fact issues.
* Source artifact: unchanged.

## Applicable dimension results

| Dimension | Result | Evidence |
| --- | --- | --- |
| Workflow contract | Revise | BRANCH-001 and BRANCH-002 |
| Safety and enforcement | Revise | BRANCH-002 |
| Outcome and structure | Pass | Coherent-workstream default, ambiguity stop, and PR lifecycle routing are explicit. |
| Reviewer bounding | Pass | The branch decision table supplies bounded no-change, continuation, child, and fresh-branch cases. |
| Convention conformance | Pass | The target uses the repository's established Markdown structure and preserves owner-controlled checks and merges. |

## Material findings

### BRANCH-001

* Severity: High
* Dimension: Workflow contract
* Location: .github/copilot-instructions.md, Branch and Pull Request Workflow, branch-decision table, final row.
* Finding: The row makes any "explicit owner request" select a fresh branch from latest origin/main. That conflicts with the required exception priority: an owner's explicit safe base direction, such as a dependent unmerged parent topic, must be honoured. It can also contradict the preceding child-branch row.
* Smallest coherent fix: Replace "or an explicit owner request" with language limiting the main-based default to an explicit owner request for a new main-based branch, then add one sentence that an explicit owner branch/base direction takes priority when it preserves the stated safeguards.
* Evidence: .github/copilot-instructions.md; /home/azureuser/.copilot/installed-plugins/hve-core/hve-core-all/skills/hve-core/hve-builder/references/requirements-catalog.md, Instruction-file architecture, "No conflicting layers"; /home/azureuser/.copilot/installed-plugins/hve-core/hve-core-all/skills/hve-core/hve-builder/references/review-rubric.md, Workflow contract.

### BRANCH-002

* Severity: High
* Dimension: Safety and enforcement
* Location: .github/copilot-instructions.md, Branch and Pull Request Workflow, ambiguity paragraph and branch-selection table.
* Finding: The safety stop expressly prohibits several history-changing actions, but it does not prohibit PR reopening, branch deletion, or remote writes solely to choose a branch. The later PR workflow describes normal push/PR actions without distinguishing them from branch selection. The required invariant therefore remains incomplete.
* Smallest coherent fix: Add one compact sentence to the ambiguity/selection safeguard: branch selection must not automatically stash, alter history, reopen a PR, merge, delete a branch, or write to a remote; perform only the minimum read-only inspection and ask when clarification is required.
* Evidence: .github/copilot-instructions.md; /home/azureuser/.copilot/installed-plugins/hve-core/hve-core-all/skills/hve-core/hve-builder/references/requirements-catalog.md, "Emphasis matched to enforcement" and Instruction-file architecture; /home/azureuser/.copilot/installed-plugins/hve-core/hve-core-all/skills/hve-core/hve-builder/references/review-rubric.md, Safety and enforcement.

## Verdict and limits

* Static verdict: Revise.
* Behavior execution: Not run.
* Behavior verdict: Not applicable to this requested static-only stage.
* Validation: Not requested.
* Limits: This log assesses only the named branch workflow against supplied criteria. It does not establish runtime behavior, repository state, PR state, or applicability of unrelated instructions.
