---
title: Branch Lineage Instruction Behavior Report
description: Independent grade of isolated simulated branch-selection decisions
ms.date: 2026-10-10
ms.topic: reference
---

* Target: .github/copilot-instructions.md.
* Tested profile/model: Medium / gpt-5.6-terra, inferred from semantic
  branch/base decisions; target declares no profile. No proxy used.
* Run type: full.
* Design/scenario: branch-lineage-design-01 / branch-lineage-matrix-01.
* Behavior gate: Executed.
* Fidelity: simulation.
* Execution status: Complete.
* Independent verdict: Pass.
* Findings: zero improvement, adjustment, deletion, correction or miss.
* Sandbox: cleaned up after report persistence.

## Summary

All 15 synthetic Git/PR scenarios were freshly simulated and independently
graded Pass against the final branch workflow. Decisions kept research-to-PRD
and PR corrections together, preserved dependent ancestry, separated
unrelated/merged work, respected safe owner directions, guarded existing
changes and selected independent versus stacked PR bases.

The first attempt returned Partial because its attempted bounded read
exposed grading material. Its answers were excluded. The lead placed the
identical accepted user prompt in a standalone scenario file and used a
fresh executor for all cases. Only that clean replay was independently
graded. No failing evidence was relabelled as clean or reused as a grade.

## Fidelity and Limitations

Observed: reported read-only source/state/scenario reads and lead pre/post
source-hash, HEAD and workspace checks. Simulated: branch/base decisions and
clarifications. Emulated: Git inspections/fetch/create/switch/worktree,
commits/pushes/authentication and all GitHub PR operations.

No native Git/GitHub command reliability, authentication, actual metadata,
enforced branch protection, CI or conflict remediation is established.
Medium-tier simulation may resolve ambiguity a lower-tier model exposes;
this report does not establish lower-tier equivalence. No tool configuration
or target model capability surface was inspected or changed.

## Reuse Eligibility

Not applicable: full run, no prior report, reused decisions or reused grades.
All C01-C15 used fresh final execution and fresh independent grading.

## Coverage and Grade Provenance

Every row below is newly executed simulated evidence, independently graded
from .copilot-tracking/sandbox/2026-10-10-branch-lineage-1/test-log.md,
Final Case Trace, before cleanup. The durable condensed trace is retained
here; sandbox paths are provenance, not links to retained files.

| Case | Supplied situation / requirement | Final simulated decision | Fresh grade |
| --- | --- | --- | --- |
| C01 | Active research followed by its first PRD | Reuse research topic and main-based PR; no branch for a phase change | Pass |
| C02 | Correction requested on open PR | Continue same topic and PR | Pass |
| C03 | Risky dependent implementation needs independent review | Child from unmerged topic; PR to parent; declare dependency | Pass |
| C04 | Unrelated work while another topic is open | Fresh latest-origin/main branch; PR to main | Pass |
| C05 | On main with no matching active topic | Fetch latest origin/main and create conventional topic | Pass |
| C06 | Related revision after previous squash merge | New latest-main branch, not the stale merged topic | Pass |
| C07 | Owner explicitly names unmerged parent | Honour safe named-parent child/base direction | Pass |
| C08 | Owner explicitly requests fresh main | Honour fresh latest-main direction | Pass |
| C09 | Matching active topic exists elsewhere | Reuse it after preservation checks; no duplicate topic | Pass |
| C10 | Coherent unpublished local topic | Continue it; no new branch because PR is absent | Pass |
| C11 | Related PR closed without merge | Clarify lineage; no automatic reopening/resurrection | Pass |
| C12 | Detached HEAD and unknown dependency | Clarify context/dependency; no invented base | Pass |
| C13 | Unclear-owned dirty worktree | Owner chooses carry versus separate worktree; no discard/stash/commit/move/switch | Pass |
| C14 | Explanation only, no file changes | Explain only; no branch/file/PR action | Pass |
| C15 | Stacked child retains parent diff after squash merge | Re-evaluate/retarget as appropriate; obtain direction before history/content reconciliation; no silent rewrite/force-push/merge | Pass |

Scope gaps: actual operations, equally matching active topics, conflict
resolution, authentication, commit identity and CI were intentionally
unexercised. There is no claim those independently governed controls passed
behavior testing.

## Findings

None in the final independent grade. The earlier read-isolation problem was
resolved in the evidence harness, not by changing source or weakening cases.

## Containment

Pre/post HEAD: bf71b69c30e7e494fa673d4e5b0fc54458550154.
Pre/post candidate SHA-256:
86b083ef217752368c7c093dadd26945acfa2ad4e536290bf034c93e59742acf.
The source edit and five pre-existing owned stage logs were unchanged.
Only lead-created sandbox files appeared; no unrelated write or branch/PR
action occurred. Executor was read-only; lead alone wrote sandbox evidence.

## Satisfied-and-Skipped

Not applicable. This Major instruction change can affect model actions and
was executed at simulation fidelity rather than skipped.

## Human Review

* [ ] Reviewed and validated by a qualified human reviewer
