<!-- markdownlint-disable-file -->
# Changes: #1402 C2 post-parent integration (C2 of 3 used; C3 unadmitted)

Plan: [plan](../../plans/2026-11-11/aftercare-blank-state-1402-c2-integration-1111-plan.md). The prospective C2 records were committed (`977b8c536`, now `5ee5b14f9`) before the tag, rebase and any test run. No source or test was edited in C2. Delivery target is now `main` (owner decision after parent #1456 merged as `a3862eed4a324b13715eeebf0c98053d9079dec1`, tree `ab22886c...`, first parent `ba65039c2`).

## Preservation and mapping (local only, nothing pushed)

* Local tags: `evidence/1402-c1-e8468` = `e8468bcc386dc9eb49763e490c9ae09a7f04e870` (C1 head), `evidence/1402-c2-prerebase-977b8c5` = `977b8c5366a8afdad4fa1b5b552264760b0eb0fa`.
* Rebase `--onto a3862eed4 2f7465c57`, no conflicts. `git range-diff` shows all four `=` (patch-identical):
  * `6ac95f78b` to `154bde940` (C1 research, plan, details)
  * `3d59c1abe` to `37d14b7aa` (C1 fix and tests)
  * `e8468bcc3` to `7180810f3` (C1 review and state)
  * `977b8c536` to `5ee5b14f9` (C2 research, plan, details)

## Identity checks (`evidence/.../identity/identity.txt`)

* Issue files equal e8468 blob SHAs: `aftercare_intake.py` `fb25f9f5de5b...`, `test_aftercare_intake.py` `ed815f6bd3b5...`: EQUAL.
* Numeric restoration (`aftercare.py`, `test_aftercare.py`, `test_aftercare_store.py`) equal `origin/main` blobs: EQUAL.
* `git diff --name-only main HEAD` outside `.copilot-tracking`: exactly the two issue files (+58/-1).

## Fresh requalification (`evidence/2026-11-11/aftercare-blank-state-1402-c2-integration-1111/`, each with stdout, stderr, exit.txt)

* `core-tests`: `tests.test_aftercare_intake tests.test_aftercare` 67 tests, exit 0.
* `api-screen`: `tests.test_aftercare_screen` 13 tests, exit 0.
* `ruff-check` 0, `ruff-format` (two files) 0, `mypy` (source file) 0.
* Imports (`imports.txt`) resolved to this worktree's `aftercare_intake.py`, SHA256 `30ce83d99f45...b4ef`, equal to the C1 green-1 hash. Later C1 attempts remain inferred, not hash-attested; C2 does not retrofit them.

## Preserved adverse C1 evidence (unmodified)

red-1 (author test bugs), red-2 (9 genuine failures), green-3 (exit 5, no tests), lint-1 (long line), original review (non-independent, store import `dataset` error).

## N/A and limits

SQL, store and served suites, browsers, cloud, installs, full gate: N/A; the changed branch is unreachable through `DocumentStateStore` (None or json.dumps), which is not a universal raw-blank or SQL acceptance claim. Restart means service/store recreation; HTTP 503 is the pure handler contract. Hosted CI and human approval not yet observed.
