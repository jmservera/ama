# Plan: grant CLI ordered retry (issue 360)

Date: 2026-10-25. Written after the retry research (`research/2026-10-25/grant-cli-360-ordered-retry-research.md`) and before any source or test edit in this retry. Candidate head 9a0ad8f2, base 5d79aaee.

## Decision on the candidate
* Source `infra/scripts/grant-application-admin.py`: RETAIN as is. Evidence: matches setup-entra.py line 1096 precedent, reuses the existing temp-body lifecycle, 2-line surface, keeps dry run read-only. No source churn for process reasons.
* Tests: RETAIN, plus ADD one genuine coverage fix. Research found `test_apply_refuses_an_unsafe_profile_before_any_az_call` covers only mode 0755. The earlier PR body said "unsafe or in-repo profile", which the tests do not show. Add cases for a symlinked profile and an in-repo profile so each `private_path` refusal reached from `main()` is tested before any az call.
* REPLACE: nothing.

## Phases
1. Add two offline CLI tests to `infra/tests/test_grant_application_admin.py` (symlink profile, in-repo profile), each asserting exit 1, `refused:` on stderr, zero az calls, no body file.
2. Run focused tests (`python3 -m unittest` on that file), then mutation-check one case by temporarily skipping `private_path` is NOT planned; instead confirm the new tests fail against a variant that passes the profile unchecked, using a throwaway patched copy in a scratch directory outside the repo, not by editing the candidate.
3. Record changes, run an independent review of requirement, candidate and phase evidence, commit, run the full gate in a new external output directory, verify the receipt, push the same branch, keep PR453 draft.

## Out of scope
Any Azure, m365 or Graph call, role writes, deployment, sensor migration, resident edits, other source changes.

## Success criteria
* New tests pass; the candidate is otherwise unchanged.
* Full exact-head gate passes and verifies; PR stays DRAFT with Refs #360 only.

## Independent critique (run after the plan above, before any edit)
Reviewer: rubber-duck agent, read-only. Verdict: proceed with changes.
* Source fix retention: confirmed justified; no candidate defect found.
* Finding 1 (accepted): the in-repo refusal is already tested by `test_apply_refuses_an_unsafe_profile_before_any_az_call` (it uses the existing `REPO/infra` directory). My research and plan statement that only mode 0755 was covered was wrong. The in-repo temp-directory test is DROPPED. Add only the symlink test.
* Finding 2 (accepted): the scratch-copy mutation check as written would be vacuous, since the tests import the script from its repository path. DROPPED. The symlink test directly exercises the `private_path` guard reached from `main()`; a mutation check is replaced by a documented controlled mutant only if cheap (see details amendment).
Dispositions: both findings applied. The original plan text above is preserved unchanged; this section supersedes its test list and Phase 2 mutation step.
