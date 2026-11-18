---
title: Issue 1274 resilient verified release downloads audit (Refs #1274)
description: Per-criterion audit of issue 1274 against merged PR 1275, repo state at 79fed518e, retained CI logs and fresh local installer verification on 2026-11-18
ms.date: 2026-11-18
---

Refs #1274. Scope is the synthetic demo, desktop only. No workflow, source or test file changed; no Azure resource was touched (not relevant to this CI issue). Nothing is ticked in the issue by this note.

## Evidence collected on 2026-11-18

* Repo state: `79fed518e` (origin/main). `tools/install-actionlint.py` last changed by `4bc1e3f33` (PR #1275, merged 2026-11-08T10:51:51Z). `src-ci.yml` runs `python3 tools/install-actionlint.py "$RUNNER_TEMP/actionlint-bin"` then asserts version `1.7.7`.
* Installer design (read from source): official browser URL then official API asset URL, 3 attempts per source with 2 s and 5 s delays, 30 s socket timeout, 8 MiB cap, size and SHA-256 check per asset, retry on 5xx and 429, client errors skip to the next source, token sent only to `api.github.com`, install only after both assets verify.
* Job log read with `gh api repos/jmservera/ama/actions/jobs/128696067639/logs`: job `src-namespace` of run 42469282088 (head `fb7231c788aa`), failing step `Native workflow actionlint`, line `curl: (22) The requested URL returned error: 504` then `exit code 22`. Earlier tool, unit and ruff steps passed, so this is a bootstrap failure, not a fixture failure. Run conclusion is still `failure` (old workflow source; old runs do not consume the fix).
* Fresh local run, unit: `python3 -m unittest discover -s tools -p test_install_actionlint.py` gave `Ran 12 tests ... OK`. `ruff format --isolated --line-length 100 --check` on both files: `2 files already formatted`. `mypy --strict` on both: `Success: no issues found in 2 source files`.
* Fresh local run, real integration: `python3 tools/install-actionlint.py <tmp>/bin` exit 0, logs `actionlint_1.7.7_checksums.txt: verified from github.com on attempt 1` and `actionlint_1.7.7_linux_amd64.tar.gz: verified from github.com on attempt 1`; `actionlint -version` printed `1.7.7`; actionlint with `infra/tests/actionlint.yaml` over the five native workflows exited 0. The temp directory was deleted.
* CI history on main: last 30 `Source projects CI` runs all `success`. Scorer runs (last 300 runs, 2026-11-16 to 2026-11-18): 102 success, 13 failure, 22 cancelled, 2 action_required; causes of the 13 failures were not individually classified here.
* AWF probe, GET only, nothing executed: `github/gh-aw-firewall` v0.28.23 `checksums.txt` and `awf-linux-x64` both returned HTTP 200 today. `rubric-score.lock.yml` line 558 runs `install_awf_binary.sh v0.28.23 --rootless` from the generated gh-aw setup action; no repository-owned retry hook exists, and the lock is compiler output (`gh-aw v0.89.21`, DO NOT EDIT).
* PR 1243, 1271 and 1273 states: 1243 and 1271 are MERGED. 1273 was not found by the title search (not located in this audit).

## Per-criterion table

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Identify failing official endpoints for 1243, 1271, 1273 heads, retained logs, affected installers; separate fixture from bootstrap failures | Partly observed | Observed; raw output not retained: 1243 final run 42469282088 failed at the actionlint 1.7.7 Linux archive download (504, exit 22) after unit and ruff passed; affected installer is the `Native workflow actionlint` step. Unproven here: 1271 attempt 2 and 1273 logs (not retrieved), the exact AWF endpoint in any log, and the 1273 c162 cause (PR 1275 also left it unestablished). Heads 1243 and 1271 are now merged, so "current heads" is moot. |
| 2 | Bounded official retrieval, exact identity, fail-closed checksum, no execution of partial or wrong downloads | Observed for actionlint; raw output not retained | Code reading plus 12 passing tests (run output not retained). Not observed for AWF 0.28.23 bootstrap: it lives in upstream gh-aw generated code. |
| 3 | Focused regressions (504/recovery, invalid/truncated/wrong checksum, exhaustion); WORKFLOW_HASHES updated; tools/test_rpi_checks.py and workflow/lint/compiler checks | Partly proven | 12 installer tests cover all listed cases (test names `test_504_then_recovery_on_same_source`, `test_truncated_body_is_retried_and_never_returned`, `test_wrong_checksum_on_every_source_exhausts`, `test_all_504_exhausts_with_bounded_attempts`). Not re-run in this audit: `tools/test_rpi_checks.py` and the compiler check; WORKFLOW_HASHES consistency was asserted by PR 1275 and by 30 successful main runs, not recomputed. No regression exists for the AWF path. |
| 4 | Real exact-version checksum and artifact verification; local checks, independent exact-head review, hosted CI, then merge | Partly proven | Real verification of both official assets with pinned digests reproduced today (exit 0, 1.7.7, native lint 0). PR 1275 merged after independent review and hosted CI (see PR body). The criterion also covers the whole issue scope, and the AWF half is still open. Ticking should wait for an owner decision on that scope. |
| 5 | Dependent PR resume route (already ticked) | Ticked, consistent | PR 1275 body and changes record state the route: old runs reuse old workflow source, dependents need a base update and fresh run. |

## Remaining work and tier

The issue stays open only for the AWF 0.28.23 scorer bootstrap. A fix needs one of: a gh-aw compiler or action upgrade (pinned action and compiler change, workflow/security-control impact), or an upstream retry. Either changes pinned actions and generated workflow source, so it takes the FULL tier with an external receipt, independent exact-head review and hosted CI. This audit changed no source, so it is FOCUSED docs-only; `rpi-checks.py --all` was not run.
Today's HTTP 200 for both AWF assets is a single observation, not a recovery proof.

## Recommendation

Owner decision: either narrow #1274 to the actionlint scope and tick criteria 1 to 4 after confirming the 1271 and 1273 logs, or keep it open and open a separate FULL-tier issue for the AWF bootstrap.
