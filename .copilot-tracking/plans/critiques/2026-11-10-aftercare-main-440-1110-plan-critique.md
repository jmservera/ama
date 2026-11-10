# Plan critique: aftercare integration current-main checkpoint (2026-11-10)

Executed once by the author on the final candidate plan and details; self-executed, not independent. Verdict: proceed with the amendments below, applied directly. No finding conflicts with a confirmed decision and no user decision is needed.

## Findings and dispositions

* A1 Evidence attribution: the plan must not let counts read as runs on `64c3f9191`. Applied: every consumed result is labelled with the original author commit `b7e46b3be` and the original environment, and "Local observed" is limited to those runs.
* A2 Tree equality: ancestry or green CI could be mistaken for proof. Applied: the section records the direct `git rev-parse` comparison per subtree and the explicit `.github` difference, and says equality is source identity only.
* A3 Superset wording: 98 paths against 77. Applied: state that 21 main-only documentation paths are not authored deletions and that main-only documents and the 1396 and 1399 sections remain.
* A4 Adverse items: SDK-missing first failure, progress output-directory failure, 13, 132 and 4 opt-in skips and the unrun full discovery must stay visible and not be healed. Applied.
* A5 Requirement trace overreach: draft and in-review documents are not approval; #133 and #134 criteria are not ticked. Applied: each row is class-labelled; no tick, closure or approval.
* A6 Inherited Mediums: do not describe them as fixed, waived or reproduced here; the runtime adapter scope for #1402 is FileStateStore only. Applied.
* A7 Recommendation scope: a walkthrough recommendation must be bounded to the implemented staff-assisted screen, preserve known defects and exclusions and not manufacture permission. Applied.
* A8 Exclusions: #109, #111, PR 1395, #144, #132, real provider, Azure dispatch and human acceptance stay out. Applied.

## Rejected

* None.
