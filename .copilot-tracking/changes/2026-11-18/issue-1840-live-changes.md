# Changes: issue 1840 live

Date: 2026-11-18. Source changes: none. Plan: `.copilot-tracking/plans/2026-11-18/issue-1840-live-plan.md`.

## Outcome

Blocked. The target `src/api/checks/old_image_sql_probe.py` and frozen candidate `510fd90f4f8c15bfe4da24b761d29990d3986a85` are not available in this repository, remote or any local worktree (evidence in the research note). Nothing was reconstructed. Divergence from the goal ("implement"): recorded here, caused by a missing dependency the issue itself names.

## Per-criterion table

| Criterion | Status | Reason |
| --- | --- | --- |
| Failing-first regressions for missing mismatch execution result and missing reinvoke state with active MUTATED row | Unproven | Target module absent; no test can be written against it |
| Incomplete or malformed completion evidence yields INSUFFICIENT unless trustworthy adverse evidence proves violation | Unproven | `completed()` not available |
| Preserve positive control, late-restoration detection, active-MUTATED rejection, bound release identities, adverse precedence | Unproven | No change made; nothing to preserve or regress against |
| Run affected probe/release/restart tests, strict typing, exact counts and skips | Unproven | No affected tests exist on this base; mypy not run because no source changed. Canonical bare mypy and the two `config()` errors at lines 1255 and 1417 cannot be reproduced without the file |
| Separate RPI loop and independent exact-head review, tier justified | Partly delivered | RPI loop and one review recorded locally; independent exact-head review and hosted CI are pending and not claimed. Tier: focused for this no-source record; the fix itself defaults to full tier because diagnostic evidence correctness is security-sensitive |

Live Azure and Playwright: not applicable. The defect is in an offline fixture diagnostic; the demo apps do not run it. No Azure action, no throwaway resource, no credentials read.

## Validation

* `git status`/diff review: only `.copilot-tracking/` artifacts added.
* No unit tests, mypy or ruff run: no executable change. `rpi-checks.py --all` not run.

## Follow-up

Provide `test/assistant-old-image-sql-107` at `510fd90f`, branch from it and apply the deferred design in the details file. Refs #1840; no closing keyword.
