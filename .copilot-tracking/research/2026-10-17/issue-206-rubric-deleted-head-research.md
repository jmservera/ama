---
title: Issue 206 rubric deleted-head research
description: Bounded investigation of rubric score recording races
ms.date: 2026-10-17
---

## Research Brief

Investigate issue #206 and run 38694897856 before changing runtime code.
Determine whether the deleted/moved PR-head failure is already repaired;
preserve exact scored-SHA integrity and all existing gates. Audience: PR
reviewers. Output mode: convergence. Status: Complete.

## Parameters and Direction Controls

* Posture: focused, selected from the caller's named failure and bounded scope.
* Evidence root: `.copilot-tracking/`; source edits prohibited during Research.
* Exclusions: live scoring/inference, Azure, role/network changes, private
  datasets, primary environment files, #370 and #176 workstreams.
* Required checks: closed/deleted head, active unchanged head, moved head and
  API failure, using existing local tests and helpers.
* No main fallback, branch recreation, gate bypass, different-SHA publication,
  merges, force-pushes, history rewrites or issue closure.

## Extensions and Participation

Repository instructions and canonical original/addendum/index/memory were
consulted. `rpi-research` governs evidence; later RPI skills own their phases.
No specialist delegation: this is one continuous workflow/code trace.
No intake question is necessary: the caller supplied scope, branch, criteria,
publication authorization and an explicit four-phase sequence.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | What failed and is that failure already fixed? | Answered: not fixed |
| Q2 | How do existing guards preserve scored SHA and distinguish errors? | Answered: partial protection only |
| Q3 | Which local regressions and compiler establish the exact boundary? | Answered |

## Prior Knowledge Gate

Worktree was clean on `fix/rubric-deleted-head-206` at
`4ca6c7318ee4be35cef8c5ea6eee3425bf1421c4`; no existing PR for this branch.
Open #370 and #368 are unrelated and excluded. Existing rubric artifacts and
README are starting points, not proof of a current fix.

## Research Cycle Log

### Cycle 1

#### Wider

Issue/run evidence identifies failure in `record_rubric_score` checkout,
using deleted branch `docs/agent-chat-memory-brd-prd-adr`, not score validation.
Current workflow, gate helpers, tests and history are the candidate sources.
Reflection: distinguish historical workflow from today's implementation before
choosing a repair.

#### Deeper

Current recording checkout still targets `github.head_ref` (C1). Its later
SHA guard cannot run when checkout fails. PR #204 merged at 06:51:46 on
2026-10-15, before the failing checkout at 06:56:25 (W2/W3). The existing guard
does prevent recording a score when checkout observes a moved head, and publish
targets only the event SHA and the bot's resulting score commit (C2).
Reflection: preserve those protections while moving checkout to the immutable
event SHA and checking current PR state before attempting it.

#### Contrarian

Challenge: merely replacing the branch checkout with a SHA removes the
exception but also removes the moved-head signal; blindly retaining the old
push can recreate a branch deleted after checkout. A plain preflight plus
ordinary push is still insufficient if deletion/movement happens after API
verification. Git's pre-push hook receives the advertised remote SHA; require
it to match the scored SHA, then use normal non-force push (receive-pack
compares the advertised old OID atomically). Reject a zero/mismatched OID.
Use a workflow-created isolated hook, not PR-controlled repository hooks.
Do not treat a PR API 404, authorization failure or outage as proof of closure.
Reflection: explicit closed state is the only obsolete-success condition;
API errors fail visibly. Fresh checks are needed before recording/publication.

#### Parent Synthesis and Re-entry

Accept the historical deletion diagnosis and current-code gap (C1/W2/W3).
Reject the "already fixed" alternative because the failing ref is still used.
Reject a SHA-only change because it loses moved-head protection.
Select immutable checkout, explicit PR-state checks, and an exact advertised
head guard on non-force push. Keep gate/scoring semantics untouched.
No second cycle is needed: named failure, current trace, counterexamples,
existing runner and compiler are identified. Planning Readiness: Ready.

## Evidence Log

| ID | Finding | Source | Retrieved |
| --- | --- | --- | --- |
| W1 | Issue remains open; owner explicitly requests deleted/moved-head investigation | https://github.com/jmservera/ama/issues/206 | 2026-10-17 |
| W2 | Checkout failed because branch/tag did not exist; run SHA f839871a16cc05e8a8ea2594f95594ba85a6b996 | https://github.com/jmservera/ama/actions/runs/38694897856 | 2026-10-17 |
| W3 | PR #204 is merged, with the same head SHA; closure predates failure | https://github.com/jmservera/ama/pull/204 | 2026-10-17 |

### Codebase Evidence

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Record checkout uses mutable branch; verification occurs too late | `.github/workflows/rubric-score.md:209-235` | High |
| C2 | Moved guard suppresses record and blocks passing verdict; status uses scored/new SHA | `.github/workflows/rubric-score.md:260-355` | High |
| C3 | Existing pytest suite already extracts compiled steps and runs Node subprocesses | `.github/rubric/scripts/test_safe_output_runtime.py:65-175` | High |
| C4 | README requires compile and both files; installed gh-aw is v0.89.21 | `.github/rubric/README.md:105-113` and `gh extension list` | High |
| C5 | Existing non-force push disables hooks but can create a missing branch | `.github/workflows/rubric-score.md:278` | High |

## Findings, Alternatives and Remaining Uncertainty

Q1 is answered by C1/W2/W3; Q2 by C2/C5 and the counterexamples;
Q3 by C3/C4. The local baseline command is
`python3 -m pytest .github/rubric/scripts -q --tb=short`; its failures are
recorded during implementation and must not be hidden or repaired out of scope.
No live scorer will be dispatched. A concurrent PR closure cannot be made
atomic with a git ref update, but checking before recording/publication plus
atomic advertised-OID matching prevents a deleted or different head from
receiving the score commit. This limitation must remain explicit.

## Decisions, Risks and Readiness

Research disposition: executed, Complete. Planning Readiness: Ready.
Self-check: all three waves completed inline; questions map to evidence;
no source changes or live scoring were performed. No unresolved research blocker.
Next action: parent executes Plan with the selected bounded repair.

## Integration Continuation (2026-10-17)

Research disposition: reused, with bounded verification; Planning Readiness:
Ready. The caller explicitly resumes the same task for rebase/integration only,
superseding the earlier no-rewrite restriction for this run-owned topic branch.
No new repair, critique loop, scorer dispatch or unrelated fixture work.

Wider verification: clean branch and open PR #372 both identify reviewed head
febd357dbe419260916c463b5663927ce8bb7117. Fetched origin/main is
d890e3de29e24cb26c2eff35af9a6e125a3b541e, containing #368/#370/#371.
Deeper verification: Git's three-dot base-change inventory has no overlap with
.github/rubric/ or rubric-score source/lock; replay should preserve their bytes.
Contrarian verification: a successful old-head CI run is not integrated-head
evidence. Source projects CI run 39017650712 completed successfully but targets
febd357, not the forthcoming rebased head. No final-head CI claim is justified.

Accepted: rebase the two existing topic commits and this preflight checkpoint,
compare canonical bytes and rerun local validation. Rejected: infer integration
from disjoint filenames alone or reuse old-head hosted evidence as final CI.
No new research uncertainty requires another cycle or specialist delegation.
Git inventories and the read-only PR/run snapshots were checked on 2026-10-17.
Run evidence: https://github.com/jmservera/ama/actions/runs/39017650712.
