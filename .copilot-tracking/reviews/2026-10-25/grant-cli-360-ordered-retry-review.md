# Review: grant CLI ordered retry (issue 360)

Date: 2026-10-25. One review record for this actual retry. Reviewer: independent code-review agent (read-only), run after execution, over the full requirement, the candidate (`git diff 5d79aaee`, infra/scripts and infra/tests) and the retry phase artifacts plus the original 2026-10-24 artifacts.

## Verdict: PASS-with-findings (no code defect)
Code: correct, minimal and in scope. `--apply` obtains a validated private directory through `private_path` inside the existing `try` and passes it as `body_directory`, matching setup-entra.py:1096; unsafe profiles refuse before any az call; dry run stays read-only; `grant()` is untouched. Tests: `python3 -B -m unittest test_grant_application_admin` gave 11 OK in the reviewer's own run.

## Findings and dispositions
1. Low, candidate diff also contains the rubric score file and 2026-10-24 tracking artifacts. Accepted, not a defect; the source and test change is unchanged in scope.
2. Low, the in-repo assertion checks only `az.calls == []`. Accepted as is; the guard is also covered by the 0755 and symlink cases. No source churn.
3. Low, changes file forward-links this review. Resolved by this file.
4. Low, the critique is recorded only in the plan amendment, so its timing is self-reported. Accepted and stated honestly: the repo cannot prove the critique agent ran. Evidence available: file mtimes (research 02:24:20, plan and details 02:25:21, test edit 02:25:30, changes 02:25:40) and the critique corrected two of the author's own errors.
5. Informational, the original research is dated 2026-10-25 in a 2026-10-24 directory, which its note explains.

## Does the retry resolve the delivery process gap?
Partly. Forward order is real for this retry: research, then plan and details, then an independent critique that changed the plan, then execution, then review. But the retry is not greenfield. The 2-line fix, original tests and their mutation evidence existed first, so "retain" was largely a review of existing work and the only forward-ordered change is one symlink test. The retry reused the original's evidence (for example the "3 tests fail without the fix" claim) rather than redoing it. The original order deviation stays recorded and is not called correct; this retry improves the evidence and does not erase it.

## Limits
Offline doubles only. No live Graph write, so no proof of a fresh assignment or owner login. Coordinator independent assessment, exact-head gate and all hosted checks remain required. PR453 stays DRAFT.
