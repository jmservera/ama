---
title: Issue 350 feedback correction4 changes
description: Strict JSON type implementation and truthful local validation evidence
ms.date: 2026-10-22
---

Task ID: issue-350-demo-feedback-correction4.
Execution status: Source work, local validation and one ordered RPI loop complete;
publication blocked. One Review execution Complete, outcome Not accepted.
Plan: .copilot-tracking/plans/2026-10-22/issue-350-demo-feedback-correction4-plan.md.
Details: .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-correction4-phase-details.md.

## Approved Scope and Critique

Only checker, focused test module and correction4 artifacts/state.
One final-candidate independent critique executed preimplementation; original
Revise verdict retained. PC-001 rejected as worker-local restriction conflicting
with explicit owner `/tmp` requirement; PC-002 diagnostic/PASS assertions applied
to the plan. No repeat critique.

## Implementation

P01-T01: added seven lines to `tools/check-demo-feedback.py`, requiring str
name/email, None-or-str tiles and str attribution. Existing provider guard and
deployed trusted-proxy rule are unchanged. Failures identify the field.

P01-T02: six methods added to the existing test module. Wrong-type matrices use
serialized JSON for both roles: None, empty/populated lists/objects, both bools,
int and float (null omitted only for tiles). Negative subtests require field
diagnostics. Positive matrices require `me_contract` PASS for empty/whitespace/
arbitrary strings, plus null tiles/empty attribution and empty contractor email.
Provider content/origin behavior and blocked overall/SQL acceptance remain.
No removals, dependencies, runtime edits or unrelated changes.

## Validation

* Before checker fix, the two new wrong-type regression methods failed with
  70 failing subtests. Output:
  `/tmp/ama-350-correction4-20261022-Qdq0J7/regression-before.log`.
  Existing provider type rejection passed while the four missing guards failed.
* Corrected-source focused suite: 64 tests PASS in 0.158s, using
  `PYTHONDONTWRITEBYTECODE=1 /tmp/fh350-venv/bin/python -B -m unittest tools.test_check_demo_feedback -q`.
  Output: `/tmp/ama-350-correction4-20261022-Qdq0J7/focused-tests.log`.
* Ruff 0.17.1: isolated `check --no-cache --select E,F,W,B,BLE,I --ignore E501`
  and isolated `format --no-cache --check` on both named tool files PASS.
  Formatter changed only the new test code.
* `git diff --check` PASS; ignored-input status empty after tests/lint.
* Exactly one full-gate attempt after waiting on the shared lock:
  `PYTHONDONTWRITEBYTECODE=1 python3 tools/rpi-checks.py --all --base b4d467cad84535ed106cffa1ae9aa303db7bfed2 --out /tmp/ama-350-correction4-20261022-Qdq0J7/full-gate --lock-timeout 86400`.
  Exit 1: `BLOCKED: Candidate has tracked modifications or untracked inputs`.
  No full-gate checks ran. The runner stopped before creating its output
  directory or a receipt. Console preserved at
  `/tmp/ama-350-correction4-20261022-Qdq0J7/full-gate-console.log`
  (SHA-256 447e1c2c4544d9b67cdd60b7bf0e0cda04acd06a952d7b8006ec99bd523fae29).
  No edits during gate; no duplicate gate and no other holder interrupted.
* Receipt verification unavailable: no receipt and no new committed HEAD.
  HEAD remains 05b5b7d2b754ae0e7134df8db1a867861726a821; local origin/main
  remains the required base. No stale receipt substituted.
* Focused log SHA-256:
  c07b273028bc7a82ec94a005c519d35852e263bb23dad9e26399de37eafa0d04.
  Prior 58-test/Ruff result is not correction4 evidence.

## Blockers and Remaining Work

B1: unchanged gate requires committed clean HEAD but owner forbids committing
before gate/receipt pass. Source work and focused validation completed; commit
and publication remain blocked. No hiding inputs, early commit or old-HEAD gate.
P01 and P02 complete as work/attempt markers, not successful full-gate approval.
P03 one Review completed at
`.copilot-tracking/reviews/logs/2026-10-22/issue-350-demo-feedback-correction4-review.md`.
Required full-gate success, exact-new-HEAD receipt,
commit and independent coordinator assessment remain unavailable.
No `gh api user` or local identity configuration: commit prerequisites failed,
so no identity/network action is needed or authorized now.
No commit, push or PR update; original acceptance remains unmet.
Prior correction3 residual findings remain with their original owners and
evidence, outside this task.

## Parent Closeout

After the one Review finished, the RPI parent synchronized P03 completion and
state to Follow-up, task completed (loop execution only), automatic session
running awaiting coordinator action. Publication remains blocked. RV-001 ranks
first because sequencing blocks any authorized commit/gate; RV-002 independent
assessment ranks second and depends on it. No child work selected or started.
No original acceptance checkbox or prior adverse critique/Review changed.

## Owner Decision on Commit and Gate Sequence

The owner selected `authorize_local_commit_then_gate` in response to the
sequencing question. This supersedes the earlier commit-only-after-receipt
constraint for this bounded correction and authorizes one local-only commit,
followed by exactly one fresh full gate against the current base. The initial
dirty-candidate preflight refusal remains historical and is not a passing
result. No push is authorized before exact receipt verification and independent
coordinator assessment both pass. If the fresh gate or receipt verification
fails, stop without another attempt or publication. No source scope or
acceptance criterion changed; the critique and completed self-review remain
historical and are not repeated.

The candidate is on the isolated #350 worktree at HEAD
`05b5b7d2b754ae0e7134df8db1a867861726a821`, whose merge base is the current
`origin/main` `b4d467cad84535ed106cffa1ae9aa303db7bfed2`. The corrected source,
tests, and seven correction4 RPI artifacts are the only pending worktree
changes. The repository-local GitHub noreply email is
`8036360+jmservera@users.noreply.github.com`. Local commit, fresh gate and
receipt verification remain pending.

## Commit Workflow Tool Availability

The required `get_changed_files` tool is not present in the available session
tools or loaded extensions. The active commit workflow requires that tool for
staged-change inspection and explicitly prohibits `git diff`; therefore no
files have been staged or committed. The owner-authorized fresh gate cannot
start until the staged candidate can be inspected under an approved method.
The source correction and RPI artifacts remain preserved in the isolated
worktree; the earlier authorization to commit locally and gate remains valid,
but no fallback inspection method is assumed.

## Owner Approval for Staged Review Fallback

The owner explicitly authorized one `git diff --cached` invocation to inspect
the staged candidate for this isolated #350 commit. This clears B2 for this
single operation only. Stage the known task files, inspect them once, then make
the local-only commit; do not push. No additional diff invocation is
authorized. The one fresh full gate and exact receipt verification remain
pending, followed by the independent coordinator assessment.
