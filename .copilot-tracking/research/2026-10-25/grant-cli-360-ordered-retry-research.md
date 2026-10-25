# Research: grant CLI ordered retry (issue 360)

Date: 2026-10-25. Task: grant-cli-360-ordered-retry. Candidate: PR453 head 9a0ad8f2 (source commit 67366d5b), base origin/main 5d79aaee. Research disposition: executed (read-only, local). No Azure, m365 or Graph call.

## Actual phase ordering for this retry
1. Research (this file), written before any plan, source or test edit in this retry.
2. Plan, details and critique, written after this file.
3. Execution, then independent review, then the full gate.

## Why this retry exists
The earlier slice (`2026-10-24/grant-cli-360-*`) disclosed that the fix and first tests were written before research, plan and details, and that no pre-implementation critique ran. The coordinator held PR453 (comment 6392208146, issue comment 6392055096). That sequence was not correct and is not relabelled here. Those artifacts, commit 67366d5b and the gate receipts for 67366d5b and 9a0ad8f2 stay as history. The retry does not claim them as evidence of ordered phases.

## Requirement (owner request, issue 360)
`infra/scripts/grant-application-admin.py --apply` must be able to issue the Graph assignment write from the real CLI entrypoint. Keep: dry run default, expected tenant/app/OID checks, supported role check, enabled Member constraint, single-role idempotent assignment, write-permission refusal, confirmation and readback, no secret output. Reuse the existing temporary body mechanism. No live calls.

## Findings from the current code
* `Azure.call` (setup-entra.py ~137-175) raises "Mutation body storage is unavailable in read-only mode." when a body is passed and `body_directory` is None. Otherwise it writes the body to a `NamedTemporaryFile` (mode 0600 by default) in `body_directory` and unlinks it in a `finally`, on success, `AzureError`, timeout and OSError.
* The candidate source change is 2 lines in `main()`: compute `setup.private_path(args.tenant_profile, directory=True)` only when `--apply`, inside the existing `try`, and pass it as `body_directory`.
* `private_path` (setup-entra.py 102-118) refuses symlinks, paths inside the repository, missing paths, and directories that are not mode 0700. Its `SetupError` is already caught by `main()`, which prints `refused:` and returns 1, so an unsafe profile fails before any `az` call.
* Existing precedent: setup-entra.py line 1096 builds its transport the same way, `Azure(..., body_directory=private_path(args.tenant_profile, directory=True))`. The candidate matches an established pattern and adds no new abstraction.
* Dry run passes `None`, so it stays read-only and needs no profile directory check. The default profile `~/.azure/zava-entra-init` is the same private directory setup-entra uses.
* `grant()` and its validation are untouched (`git diff 5d79aaee 9a0ad8f2 -- infra/scripts` is only the `main()` hunk).

## Findings from the current tests
`infra/tests/test_grant_application_admin.py` has `OfflineAz` (patched `setup.subprocess.run`) and `GrantCliTests` driving `main()` with the real `Azure` transport and a mkdtemp 0700 profile outside the repo: apply writes through a temporary body that is removed and a repeat is a no-op; dry run issues no write; missing write permission refuses without a write; a failed write refuses and leaves no body; an unsafe or in-repo profile refuses before any az call; no token in output. Earlier mutation evidence: 3 of these tests fail without the fix.

## Candidate-risk questions asked in this retry
* Does a symlinked or mode-wrong profile reach `az`? By code reading, no: `private_path` raises first.
* Can a body file leak after an error? By code reading, no: the unlink is in `finally`.
* To verify in execution: whether the unsafe-profile test covers each of in-repo, non-0700 and symlink cases. Add only a missing case if one is found.

## Planning readiness
Ready. Open decision for the plan: retain the 2-line source change and existing tests unless the execution re-run or independent review finds a genuine defect.

## Limits
Offline doubles only. No live Graph write was exercised, so this does not prove a fresh live assignment or owner login. A fresh Graph readback returned 403 earlier and was not widened.
