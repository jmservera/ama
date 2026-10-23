<!-- markdownlint-disable-file -->
---
title: Issue 349 current-main continuation research
description: Reconcile the existing local checker history with main and remote intent
ms.date: 2026-10-23
---

## Research Brief

Continue issue349-tenant-readiness-preflight, not a replacement history.
Audience: delivery coordinator for draft PR #437. Output mode: convergence
preparing a bounded reconciliation plan. Research posture: focused, selected
from the owner's explicit current-main reconciliation and local checker scope.
No source/history modification during Research.

## Research Parameters and Direction Controls

Worktree: /home/azureuser/source/ama-wt/issue-349-tenant-preflight.
Branch: feat/tenant-readiness-preflight-349.
Initial local HEAD: 3eebcc3922188f5ddd614bfa5d4583b082f4e1c5.
Freshly fetched main: 140d8f494482c78e84d15f3d46b9223d3c487af0.
Fetched remote topic: 6c284d4547de7c52a360b2ec2406ea2078a98f16.
Retain unique remote intent, original RPI dispositions and all append-only log
entries. Do not overwrite newer main evidence with obsolete generated scores.
Authorized: local rebase after planning, focused validation, dated committed
RPI evidence and exactly one new full local gate. Stop before push.

No Azure/Graph/tenant/resource mutation, deployment, paid calls, private data,
registration/secret/roster access, network/privilege changes, UI edits, issue
acceptance, board writes or PR changes. October headroom Unknown despite the
owner's USD 700 ceiling through 2026-10-25T16:02Z.

## Extension Registry and Participation

Repository instructions and RPI research selected. Reconciliation is one
tightly coupled trace, handled inline; no research delegation needed.
UI/domain expansion skipped as inapplicable. No clarification required:
owner explicitly authorizes ordered phases and local rebase, not publication.

## Questions and Starting Areas

* Q1: What unique local/remote commits and file intents must survive?
* Q2: Where does main conflict, and can intent be resolved without widening?
* Q3: What validation, dependency and exact-head evidence is required now?
* Areas: Git lineage/deltas, correction3 evidence, checker/tests, component
  commands, append-only log and generated rubric evidence where overlapping.

## Prior Knowledge and Intake

Read repository instructions, both case-study introductions, KB index/memory.
Clean initial worktree; fetched exact refs above. PR #437 is open and draft.
Remote is one commit ahead of local, titled generated rubric score 48/100;
commit contents still require investigation.

## Research Cycle Log

### Cycle 1: Wider

Inspected commit/file inventories and original correction3 research, plan,
details, critique, changes, Review and state. Main advanced by one requirements
commit (#433); topic contains five human-authored checker commits and two bot
score commits, the last bot commit being the only remote-only change.
Reflection: there is no independent remote source change to choose between;
the overlapping tracked path is generated latest.json, not checker code.

### Cycle 1: Deeper

Read both bot patches in full. 3b881a65 records 48/100 for 1ad2d5ad;
6c284d45 records 48/100 for 3eebcc39 and updates only latest.json. Main's
55/100 artifact has different BRD/PRD fingerprints and includes pitch evidence
introduced with #433; its timestamp is earlier than the remote score, so
timestamp alone is not a safe precedence rule. Its scope is newer main intent.
Main changes no checker, tests, instructions, gate helper or project manifests.
Read main's exact log delta: two entries are inserted before older entries,
with no topic log delta. Reflection: preserve main documents/log byte-for-byte,
preserve checker and original RPI artifacts byte-for-byte, archive old score
patches as inert history rather than install stale topic scores as latest.

### Cycle 1: Contrarian

Challenged dropping remote work: remote-only 6c284d45 has no registration,
source, test, policy or documentation change beyond the generated score.
Simply rebasing local HEAD would silently omit its assessment provenance.
Accept remote into local ancestry first by rebase, archive both bot patches
with exact parent/commit/run provenance, then explicitly drop their generated
latest.json changes from replay. Reject latest-timestamp-wins and whole-file
ours/theirs conflict shortcuts. Reject fabricating a new score or relabelling
the old receipt current. Reflection: retain both intents, with main latest
and historical topic score provenance clearly separate.

## Evidence Log and Findings

| ID | Finding and question | Source |
| --- | --- | --- |
| C1 | Q1: merge base is b4d467cad84535ed106cffa1ae9aa303db7bfed2; local is ancestor of remote; remote-only commit is 6c284d45 | Git fetch, merge-base, left/right log and full show on 2026-10-23 |
| C2 | Q1/Q2: both bot commits modify only latest.json; remote records correction3 source head and 35-test rationale | .github/rubric/scores/latest.json:1-75 at 3b881a65 and 6c284d45 |
| C3 | Q2: main has 55/100, updated BRD/PRD and pitch fingerprints, and main docs/log intent | .github/rubric/scores/latest.json:1-26 at 140d8f49; docs/reference/log.md:6629-6674 main delta |
| C4 | Q1/Q3: correction3 strict boolean projection, sanitizer/guard and original 35-test contract remain canonical | infra/scripts/tenant-readiness-preflight.py:51-61,359-369; infra/tests/test_tenant_readiness_preflight.py:170-207 |
| C5 | Q3: pip-installed distributions, one complete committed-head gate, external receipt with fresh main verification | src/README.md:35-114; unchanged between old base and fetched main |
| C6 | Q1: original critique Revise with rejected worker-local filesystem findings; original Review Complete/Conformant, with coordinator/hosted/human residuals | correction3 plan Critique Disposition; correction3 Review RV-001/RV-002/RV-003 |

## Selected Recommendation and Dispositions

Accept C1-C6. Plan a local-only rebase: record pre-rebase phase artifacts,
integrate fetched remote ancestry, then replay topic onto freshly fetched main,
explicitly omitting only the two obsolete generated score commits after
archiving their Git patches. Keep all human commits, original evidence and
main-only files unchanged. Any additional conflict or remote/main movement
requires evidence-based reconciliation or an exact blocker, not a force choice.
No source behavior change is needed or justified by the observed delta.

## Source Log and Session Identity

Copilot session: e1bd8fce-e9f4-499c-813e-d25c7a8cede2 (resumed same history).
Current tmux launch: rpi-349-current-main, pane shell PID 3253729.
Source log: /tmp/rpi-349-current-main-20261023.log.
Launch brief: /tmp/brief-349-current-main-20261023.md.
These identify the current launch only, not an authority to mutate other
sessions, gate locks or environments. Neither was edited by this continuation.

## Limits, Alternatives and Self-Check

No external/domain research necessary. No tests or live checker calls run in
Research. Old external receipt is historical and invalid for rebased HEAD/base;
do not clean it or infer current validity. Unresolved issue acceptance remains
blocked. No material research gap; three ordered inline waves complete and all
questions answered. Another research cycle is unnecessary unless fresh refs or
unanticipated conflicts change the known boundary.

## Validation Ownership Intake

Before any validation: inspected processes and lslocks. No full-gate process
or held ama-rpi lock observed. A tmux server/session and Copilot resume process
are the current launch lineage, not assumed to be a competing gate owner.
Recheck live ownership before focused validation and full gate.

## Planning Readiness

Research disposition: executed, complete. Planning Readiness: Ready (C1-C6).
Parent continues to Plan under the owner's explicit ordered-phase request.
