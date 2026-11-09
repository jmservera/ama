# Changes: final-parent integration and validation for #136 (2026-11-09)

Refs #136, Refs #1258. Plan: `.copilot-tracking/plans/2026-11-09-ranking-blob-bicep-136-final-parent-plan.md` (amended by the critique). Native record; not an independent review.

## Identities

* Prospective records commit `616fa5e65efd9d8c332ee563f15b150879820683` (tree `41d45af5842ee3aaa002998583364f2d28c907ac`), made BEFORE the merge and any check. Prior frozen head `3783ea0fc5cd34dd62a0477283a99a15fae818cd` (tree `d2c0034cb6d3fd681e41c051be3889624b756602`); reviewed source `95fcaf561a9f046671d2cdf1bac8a6619f703610`.
* Merge commit `8c83062fb70b30beb4e3bf739354c55cedbe2f98`, tree `b5472c0c76f6adc465c8a53b8a6243be834f8585`, parents `616fa5e65` and frozen parent `9b1e2567c2d0a2173b562103cd27508f75181526` (tree `b88cc90f4a4dd48a51b15e526b734e975fa036c5`). Ordinary `git merge --no-ff`, no conflict, no source resolution, no rebase, reset or force. A first attempt with a wrong `-F -` flag exited 129 and changed nothing.
* Author and committer `8036360+jmservera@users.noreply.github.com` (repository-local config), Copilot trailer.
* `origin/main` fetched: `ef28d4da42d83b111d48f14df9b70e3c4932a477`. The parent carries main `8d6f029cac004506953f36606862168bbe9d9412`; main was NOT merged here (outside the brief). Fetched main is newer than the integrated base.

## Merge result

* #136 delta over the parent is exactly the original 7 infra paths: `infra/README.md`, `main.bicep`, `main.test.bicepparam`, `modules/{containerapps,guard,storage}.bicep`, `tests/test_bicep_policy.py` (+192, -1). `git diff 3783ea0fc HEAD -- infra` is empty (infra byte-identical to the prior frozen head).
* The parent brings 12 src files over the prior head (SQL store, priority order, `store.py`, `server.py`, `app.js`, core README and tests) plus its docs; 31 non-tracking paths differ from `95fcaf561` overall, all parent-owned.
* Both behaviours kept: Blob archive and wiring from the parent and #136 (Bicep container, settings), main-8d `_order_unresolved` and `CommittedReloadError` 409 paths. No production or test source was edited in this task.

## Selected checks (owner demo-targeted tier; external dir kept)

External logs: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/logs-136-final-parent/run-fEkThh/` (`SHA256SUMS` sha256 `faf82b8f0a5b26889caa0d8914073caf16cb720e5fccfaf4ad9b4287f3c323b4`, `exits.tsv`, `run.sh`, `run-stdout.txt`, owned `venv/`). Nothing removed. Env: `ZF_*` and MSSQL unset, `PYTHONDONTWRITEBYTECODE=1`, ruff 0.17.1 pinned in the venv, Python 3.12.3. Imports resolve only inside this worktree (log 05); ambient python resolves to the primary checkout (log 02): invalid, not used.

| Log (sha256 prefix) | Check | Exit / result |
| --- | --- | --- |
| 10 (85a5f7fcda6514f7) | `az bicep build` all `*.bicep modules/*.bicep` | 0 |
| 11 (81d3b1e717d4ae02) | `az bicep lint` all | 0 |
| 12 (e769d985..., 2c250a29..., 81d202bc..., 649a1e51...) | `build-params` main.test, main, main.pilot.example, iot-hub-live | 0 each |
| 20 (f0d00d4b0a17d8d4) | infra policy, identity, secret lifecycle, API ingress, governance, edge (`REQUIRE_AZ_BICEP=1`) | 0, Ran 109 OK, no skips |
| 30 (2a7f101098b4954d) | core Blob, publication, runner, documents | 0, Ran 137 OK |
| 31 (2a985d9075dbeb29) | core priority order, resident decisions | 0, Ran 398 OK, skipped=158: 156 "opt-in owned loopback SQL Server", 1 "Explicit isolated synthetic Azure SQL database required", 1 "JSON file rollback only"; none of the SQL lanes ran, same as the parent |
| 40 (710709f915dcd394) | API wiring, case journey (parent 409 `committed`), ranking scale, ranking policy | 0, Ran 97 OK, no skips |
| 50-53 (878adfac..., 9a009728..., 66e308d2..., 3b4e8210...) | ruff 0.17.1 `--isolated` E,F,I,B,UP py312 line 100 check, and `format --check`, on the three-file infra CI form and the changed infra test | 0 each |
| 90 (4e84374cd39cd373) | final identity | 0; `source-unchanged-since-merge` |

Log 40 prints `Ranking archive could not be written: [Errno 1/95] hard links unsupported` and a 503; it is the output of the passing negative-path test `test_unsupported_hard_links_are_a_storage_failure_not_an_authorization_one`, not a failure. Counts of 12 src files and 31 non-tracking paths were recounted with `git diff --name-only`.

## Adverse diagnostic (retained, not a selected pass criterion)

* Log 60 (63bc33c1f7ba11b6): isolated ruff 0.17.1 check on `src/api/tests/test_ranking_publication_wiring.py`: exit 1, 11 errors (9 E501, 2 I001), 2 auto-fixable. The file is byte-identical to the parent and to `52f9b61b` (`git diff --quiet` verified). The parent handoff reported 10 errors (9 E501, 1 I001) from a command form not recorded there; this run's count differs by one I001, a UNRECONCILED difference in command form or ruff version, not a code difference. Not fixed: parent C5 budget is zero and a fix needs separate owner authorization. Child publication cannot bypass it.
* Inherited, unchanged and not re-run: parent `git diff --check` exit 2 from main's committed log file.
* From earlier records, still open: log 40 first-form harness error and the plain-format claim from `validation-capture` (unreproduced; plain default-88 runs were NOT re-run here, so they are neither confirmed nor cleared), plain RUF100, and the lost raw integration-lane logs (not reconstructed, not claimed to survive). The earlier `run-rhvN6X` set and the coordinator `136-independent-verification-proof.txt` are untouched.

## Not run

`rpi-checks`, full gate, SQL Server (158 core tests skipped), browser, scanners, what-if, deployment, real Azure, model calls, role grants, WORM or retention activation, spend, push, PR, board.

## Correction budget

Productive child review cycles stay 1 of 5 (four remain, no reset). This task made no source correction. Parent cycles: five of five spent.
