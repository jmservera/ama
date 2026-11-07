# Issue 1231 r16 plan critique (prospective, one pass)

Date: 2026-11-07. Target: `.copilot-tracking/plans/2026-11-07/issue-1231-r16-87-parent-plan.md` and its details. Critique execution: Complete (author-run, not independent). Written before any implementation. Verdict: Proceed with the amendments below; amendments are applied to the future implementation through the changes record, not by editing the plan.

## Findings

| ID | Severity | Concern | Disposition |
| --- | --- | --- | --- |
| C-01 | High | Private permissions: a clean textual merge cannot regress the 0600 stage, but parent runner/test changes could alter how tests create archives. A passing test under one umask proves little. | Keep the existing 0022/0002 owner-only test and run it at the aligned head. Assert both stage and final inode modes. Static grep for 0o600 and absence of 0o666. State the proof is owner-only on the local filesystem, no cross-UID claim. |
| C-02 | High | Double-failure propagation: parent changed the order of refusals in the runner. The retained-stage name could be lost if the new `policy_invalid` or `archive_unverified` path pre-empts or reshapes `publish_failed`. | Run the runner and manager-route double-failure tests unchanged. Confirm a foreign file is kept and that no path appears in the response or in the 503 text. Add a regression only if a gap appears. |
| C-03 | High | Registry hash guard: `_policy_problem` needs the registry value to be the same object as the policy. Child tests that build policies by copy could silently now be refused, tempting a test rewrite. | Do not rewrite assertions to pass. If a child test fails because it uses an untrusted copy, report it as a real interaction and fix the fixture to use the registered policy object only with the reason recorded; never relax the guard. |
| C-04 | Medium | Future date versus concurrent winner: parent refuses publish when the latest archive date is after the run date; child returns the winner's later date to a racing loser. These could be conflated as a contradiction. | They act at different layers (runner pre-check versus helper link result). Verify both separately. Do not weaken the future refusal, and do not change the loser's truthful already_published/writtenFalse metadata. The sequential follow-up after the race is correctly refused by the parent rule; record this as intended behaviour, not a defect. |
| C-05 | Medium | Blocked CLI exit: parent now exits 2 for `blocked`. Any child test asserting a different exit for schedule would fail. | Run the runner tests as they are; a failure is evidence to report. Do not edit parent expectations. |
| C-06 | Medium | Import origin: tests might import another worktree or an installed copy and give a false pass. | Print `zava_forward.core.__file__` under the same PYTHONPATH and require the worktree path. |
| C-07 | Medium | Merge technique: a normal merge of the parent is straightforward since merge-base is 357e842d, but the planning commit adds files to the child. | Use the researched dry run, then a real two-parent merge. Verify the resulting tree against the dry-run tree plus the four planning files. Abort on any conflict. |
| C-08 | Low | README hunks from both sides could drop a sentence silently. | Read the merged README region and confirm both the parent policy/future/blocked paragraph and the child archive-storage paragraph survive. |
| C-09 | Low | Scope creep through opportunistic fixes or log/index edits. | Forbidden. No edits to docs/reference/log.md, index, memory, parent records. |
| C-10 | Low | Receipts: a new merge commit invalidates every earlier receipt including r14. | Say so in the changes record and handoff; never describe r14 or g79 as current. |

## Residual risks not resolved by planning

* Owner-only permission is not observed across UIDs.
* EPERM/ENOTSUP injection is not a real unsupported mount.
* A post-link directory-sync failure writes no audit entry.
* Author review and this critique are not independent assessment; FULL gate and exact-head review stay open.

## Decision-critical items for the user

None. The plan conflicts with no confirmed decision. A genuine semantic conflict found during implementation stops the work and is reported to the coordinator.
