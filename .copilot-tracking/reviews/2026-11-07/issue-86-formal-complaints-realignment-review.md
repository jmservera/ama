# Issue 86 formal-complaints parent re-alignment: changes and author review

Scope: jmservera/ama#86 only (`Refs #86`). Dated 2026-11-07. Prospective research, plan and critique were committed first (`70f7a5dce`). Original adverse R2 mypy failure, R3 pass (historical, base `56eec736`) and all earlier records are preserved unchanged.

## Wait interruption (honest account)

The first dependency wait in this session used `pgrep -f "resume=1921e4bf"`, which matched its own command, so it could never finish; the coordinator stopped only that run-owned tmux session. Parent #81 had already genuinely finished. This was a tooling error in my wait guard, not a missing approval, a parent dependency or a validation failure. No wait was repeated; readiness was taken from the parent worktree HEAD, ref and cleanliness (ignored-inclusive clean, branch ref equals worktree HEAD).

## Alignment

* Pinned parent `7d390e13a450a5ca096501b1a2ccefcd9a517fd4`, tree `1d639b132ccf8ed3e4d920eb7dfcf2b394a15bee`; `origin/main` `0f420dc9514db22081cb48fa733267d9d33a0d24` is its ancestor. Old boundary `c5edb320…` is not an ancestor of the new parent (history rewritten), so it stayed the onto boundary; replay range was exactly the 7 expected commits.
* Backups before rebase: `issue86-pre-realign-1107` = `70f7a5dce1ef947c4f7c8803e7f052e8c0f392cb`; `issue86-frozen-6ff492a` = `6ff492adf9d897c81ae666e71696f5a10ed1573d`.
* `git rebase --onto 7d390e13a c5edb320` applied with no conflicts, no skipped commits, no source resolution. Parent worktree and branch untouched.
* Equivalence: `git range-diff` shows all 7 commits `=`; slice diff against parent before and after is 22 files, +842/-3 both times; all 22 slice file blobs are identical between the backup and the new head.

## Focused checks at the aligned head (own scratch `/mnt/ama-gates/restart-1107-86-align/`, R3 venv tools read-only, PYTHONDONTWRITEBYTECODE=1)

| Command | Result |
| --- | --- |
| `python -m mypy` (core) | exit 0, 267 files |
| `ruff check .` / `ruff format --check .` (core) | exit 0 / exit 0, 214 formatted |
| core `unittest test_resident_decisions test_resident_documents test_resident_choice_queue` | OK, 290 run, 101 skipped (SQL-backed; no service) |
| api `unittest test_resident_api` | OK, 20 run, 1 skipped |
| import origin | `zava_forward.core.store` loads from this worktree in both |

## Author review

Rebase was patch-equal and conflict-free; the complaints adapter, `service_forward` flow and the TYPE_CHECKING-only typing fix are intact. No runtime, rule, approval, privacy or web change. Limits: focused checks only; SQL, browser, image and scan groups were not run (heavy lane held by #1231). The old R3 receipt is historical and does not cover this head or current main. This Review is by the author, not independent.

## Pending

FULL on the final child stack tip, then FULL on the new parent integration head; independent exact-head assessment, hosted CI, human approval, genuine receiver acknowledgement and whole-issue #86 operational acceptance. PR 1243 and the remote parent are unchanged; nothing pushed; no box ticked.
