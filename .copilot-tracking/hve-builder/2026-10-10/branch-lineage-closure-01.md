---
title: "Targeted static closure: branch lineage workflow"
date: 2026-10-10
mode: review
stage: targeted-static-closure
profile: Medium
target: .github/copilot-instructions.md
source_changed: false
original_review: .copilot-tracking/hve-builder/2026-10-10/branch-lineage-review-01.md
finding_ids:
  - BRANCH-001
  - BRANCH-002
scope:
  - Confirm only the original BRANCH-001 acceptance evidence.
  - Confirm only the original BRANCH-002 acceptance evidence.
excluded:
  - Full static review or new finding discovery.
  - Author, intake, and correction reasoning logs.
  - Source edits, Git operations, network access, agents, behavior execution, and mechanical validation.
---

## Scope and decision boundary

* Source assessed: .github/copilot-instructions.md, `Branch and Pull Request Workflow`.
* Original findings assessed: BRANCH-001 and BRANCH-002 from .copilot-tracking/hve-builder/2026-10-10/branch-lineage-review-01.md.
* Criteria applied:
  * requirements-catalog: Instruction-file architecture, `No conflicting layers`; Outcome and structure, `Emphasis matched to enforcement`; Safety and enforcement, `Confirm risky actions`.
  * review-rubric: Workflow contract and Safety and enforcement.
* This is a targeted closure check. It makes no conclusion about any other part of the source artifact.

## Finding closure

### BRANCH-001

* Original result: High, Workflow contract, Revise.
* Status: Closed.
* Acceptance evidence:
  * The introductory decision rule says: "Honour an explicit owner branch/base direction within the safeguards below; otherwise select by coherent workstream".
  * The fresh-branch table row limits the main-based route to "an explicit request for a fresh main-based branch", rather than treating every explicit request as a request to use `main`.
  * The child-branch row preserves unmerged ancestry for independently reviewable, material-risk, or breaking related work.
* Closure reasoning: Explicit owner branch/base direction has stated priority, while a fresh `main`-based branch remains a narrower, explicit case. The two directions no longer conflict.
* Targeted result: Pass.

### BRANCH-002

* Original result: High, Safety and enforcement, Revise.
* Status: Closed.
* Acceptance evidence:
  * The ambiguity/selection safeguard states that branch selection uses read-only inspection.
  * It explicitly says selection does not authorize discarding, stashing, committing, moving existing work, rewriting history, reopening or merging a PR, deleting a branch, or writing to a remote.
  * It separates selection from action: "Create/switch the selected branch only after this decision and the dirty-worktree safeguard below."
  * The dirty-worktree safeguard requires owner confirmation before existing uncommitted work is discarded, stashed, committed, or moved.
* Closure reasoning: Selection is explicitly read-only and does not automatically alter existing work or history, reopen or merge a PR, delete a branch, or write remotely. Branch creation/switching and later publishing remain separate, safeguarded workflow steps.
* Targeted result: Pass.

## Verdict, limitations, and pending gates

* Targeted static-closure verdict: Pass.
* Original finding status: BRANCH-001 closed; BRANCH-002 closed.
* Full static-review verdict: Not assessed. This closure is not a new finding sweep or full approval.
* Behavior gate: Pending. The instruction artifact can affect model actions; no behavior execution or behavior verdict was produced in this static-only closure.
* Mechanical validation: Not requested and not run.
* Downstream gate: Run behavior testing against the final source state before reporting a complete behavior-bearing review outcome. Run mechanical validation only if requested or otherwise required by the applicable lifecycle route.
* Limitations:
  * Evidence is limited to the exact acceptance criteria for BRANCH-001 and BRANCH-002.
  * No source edit, workspace-state inspection, Git operation, remote operation, agent dispatch, or behavior execution occurred.
