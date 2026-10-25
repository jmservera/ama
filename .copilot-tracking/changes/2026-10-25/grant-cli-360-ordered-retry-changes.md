# Changes: grant CLI ordered retry (issue 360)

Date: 2026-10-25. Executed after the research, plan, details and critique in this folder set.

## Actual ordering
1. Research artifact written (02:2x Z).
2. Plan and details written; independent critique (rubber-duck) returned "proceed with changes"; plan and details amended with the critique section before any edit.
3. Execution (below). 4. Independent review (`reviews/2026-10-25/grant-cli-360-ordered-retry-review.md`). 5. Gate.

## Changes
* Source `infra/scripts/grant-application-admin.py`: unchanged in this retry. The candidate from 67366d5b is retained, justified by the research and confirmed by the critique.
* Test `infra/tests/test_grant_application_admin.py`: added `import shutil` and `test_apply_refuses_a_symlinked_profile_before_any_az_call` (target and symlink outside the repository; asserts exit 1, "symbolic link" error, zero az calls, no body file).
* The in-repo test and scratch-copy mutation check from the first plan were dropped after critique (in-repo was already covered).

## Validation
* `python3 -B -m unittest test_grant_application_admin` in `infra/tests`: 11 tests OK.
* Sensitivity check (not committed): with `setup.private_path` patched to return the path unchecked, the new test fails as expected.
* No Azure, m365 or Graph call; no live action.

## Correction to earlier text
The PR453 body said an "unsafe or in-repo profile" was refused; that was true for in-repo and for non-0700 profiles. Symlink refusal was untested until this change.
