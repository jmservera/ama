# Changes: issue 144 hosted conflict reconciliation (2026-11-09, Refs #144)

Plan: [plan](../../plans/2026-11-09/issue-144-hosted-conflict-plan.md).

## Actions

* Prospective research, plan, details and critique committed first as bce2c2f70 (parent 10d7caee).
* Re-fetched: origin/main d4d6827fe60be651cd922ab9656688c18c978e1d; origin/feat/slice-144 still 10d7caeed47bd4638dc62b5754db0302466c4aa6.
* Ordinary merge `git merge --no-ff origin/main` on `fix/demo-recovery-144-1109`: merge commit ad73b46ba43cb31469588c63cdee68b69b1e63da, tree 633cc9842cfed97ce58e1474b8b3b5bd2f2b8957, parents bce2c2f70 and d4d6827f. No conflict, no rebase, reset or force. The earlier tree prediction c71557173 was for the pre-record head and is not reused.
* Appended one entry to `docs/reference/log.md` (append only).

## Verified invariants (observed)

* `docs/reference/log.md`: 0 lines removed relative to both the pre-merge head and origin/main; issue 144 entries (lines 10423, 11059, 11063) and main's last entry (11095) both present.
* `git diff 63d7f8c1 HEAD -- src/agents` is empty; `queue_azure.py:124` keeps `x-ms-date`. The source date header is byte-identical to the approved head.
* Delta pre-merge head to merge outside Markdown and tracking: `.github/rubric/scores/latest.json`, `src/core/.../paired_equity.py`, `src/core/tests/test_paired_equity.py`. No change in `infra/`, `tools/`, workflows or dependency manifests.
* No pre-existing `.copilot-tracking` record modified or deleted; main added sandbox and tracking records only.
* `git diff --check origin/main..HEAD` before the log entry: 0 findings. Inherited raw sandbox whitespace from main is untouched and not authored by this lane.

## Owner demo-targeted tier results (venv /tmp/c1venv, no credentials)

| Command (cwd src/agents unless noted) | Result |
| --- | --- |
| `python -m unittest test_queue_azure test_worker test_dispatch test_dependency_rule` | Ran 49, OK, exit 0, 0 skips |
| `ruff check .` (0.17.1) | exit 0 |
| `ruff format --check .` | 43 files already formatted, exit 0 |
| `mypy .` (2.4.0) | no issues, 48 source files |
| core: `python -m unittest test_paired_equity` | Ran 23, OK |

Not run: `rpi-checks --all`, SQL, browser, negative `x-ms-date` repeat (source unchanged, earlier recorded 403 negative proof stands), the 74 coupled core tests cited in main's log (outside this change). Hosted CI for the new head is unobserved.
