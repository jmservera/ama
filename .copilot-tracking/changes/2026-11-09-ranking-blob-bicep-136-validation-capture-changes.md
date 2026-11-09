# Changes: validation-only capture for #136 (2026-11-09)

Plan: `.copilot-tracking/plans/2026-11-09-ranking-blob-bicep-136-validation-capture-plan.md`. Refs #136, Refs #1258. No production, test or Bicep source changed; this commit adds only records.

## Identities

* Subject: frozen candidate HEAD `3de2c2f4c8ad64cf22c579dce05eeec6f4f5245f` (tree `da8ef003240f070587bb4c5f2881455674210483`) on reviewed source head `95fcaf561a9f046671d2cdf1bac8a6619f703610`.
* Validation HEAD (records-only prospective commit, made BEFORE any check): `20266cf23f4fafd9e303eb31e6869aa25beae72a`, tree `10e6be6a5dd1a3c140b90c31cd0b9a08ef1b10a1`. At validation start and end every path outside `.copilot-tracking` was byte-identical to both `95fcaf561` and `3de2c2f4c` (`git diff --quiet`; logs 00 and 90, 91). Tracked tree clean throughout.
* Declared parent `52f9b61bb22c5ceaaed0f9bf6a55dab7a7a59cb8` (topic #1258), not main; no main, #1292 or sibling import.
* Tools: Python 3.12.3, azure-cli 2.91.0, Bicep 0.48.1, owned-venv `ruff 0.17.1` (the CI pin), ambient `ruff 0.17.3` (labelled separately). Venv at `run-rhvN6X/venv` with editable installs of this worktree's `src/core`, `src/agents`, `src/api`.
* External retained logs (not committed): `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/logs-136-validation-capture/run-rhvN6X/`. `SHA256SUMS` sha256 `9fe10ef4e2b15c707940438e981ed9cf9c363fb20b7e53a7734f73ff357446d5`; per-log hashes below.

## Actual imported source paths (log 05, exit 0, printed before any unit run)

* `zava_forward.core` `/home/azureuser/source/ama-demo-wt/issue-136-ranking-blob/src/core/src/zava_forward/core`; `ranking_archive_blob` resolves to `.../src/core/src/zava_forward/core/ranking_archive_blob.py`.
* `zava_forward.agents` `.../issue-136-ranking-blob/src/agents/src/zava_forward/agents`; `zava_forward.api` `.../issue-136-ranking-blob/src/api/src/zava_forward/api`. Outside-worktree list empty.
* Ambient python3 (log 06, supplementary, NOT evidence) resolves all three to the primary checkout `/home/azureuser/source/ama/src/{core,agents,api}/...` and is INVALID for this task. Log 02 is an earlier ambient probe whose output printed `None` for namespace `__file__` and is uninformative; kept unchanged.

## Producer exits and results

| Check | Log | Exit | Result |
| --- | --- | --- | --- |
| `az bicep build --file main.bicep --stdout` | 10 | 0 | built |
| `az bicep lint --file main.bicep` | 11 | 0 | only an upgrade-available warning |
| `az bicep build-params --file` `main.test`, `main`, `main.pilot.example`, `iot-hub-live` | 12 x4 | 0 each | built |
| infra `unittest -v` policy, identity, secret-lifecycle, api-ingress, governance, `REQUIRE_AZ_BICEP=1` | 20 | 0 | 100 tests OK, 0 skipped |
| Core `test_ranking_archive_blob.py` | 30 | 0 | 25 OK |
| Core `test_ranking_publication_runner.py` | 31 | 0 | 45 OK |
| API wiring, first form `-m unittest tests.test_ranking_publication_wiring` | 40 | 1 | HARNESS ERROR, ADVERSE, retained: `ModuleNotFoundError: test_role_matrix` because the dotted-module form lacks `tests/` on `sys.path`; no test executed (loader reported `Ran 1 test`, the failed import itself); not a source defect; not counted |
| API wiring, `unittest discover -s tests -p test_ranking_publication_wiring.py -v` (the repository's documented discover form) | 41 | 0 | 35 tests OK, 0 skipped |
| CI ruff check and format `--check`, changed file `infra/tests/test_bicep_policy.py` (`--isolated`, E,F,I,B,UP, py312, 100), ruff 0.17.1 | 51, 52 | 0, 0 | clean |
| CI ruff check and format, the exact three-file CI form | 53, 54 | 0, 0 | clean |
| Ambient ruff 0.17.3, same CI commands (labelled) | 57, 58 | 0, 0 | clean |

## Qualified baseline, not suppressed

* Plain `ruff check` (no `--isolated`, no `--select`) on the changed file exits 1 with one `RUF100` on the untouched line 167 `# noqa: S307` (logs 55, 59). It is outside the CI command and pre-existing; the finding is retained, not fixed or suppressed. Reported only for accuracy: the CI selection does not enable `S307` or `RUF100`.
* Plain `ruff format --check` (defaults, no config exists between the file and the worktree root, line length 88) exits 1 and would reformat pre-existing long lines (logs 56, 59). DISCREPANCY: the integration handoff said plain `ruff format --check` was exit 0 after its fix; that claim is not reproduced here and its raw output is lost. This is nonselected (CI uses `--line-length 100`, exit 0) and is recorded, not resolved.

## Lost records, preserved disclosure

The integration lane's raw temporary logs were removed and are LOST, including the output of its invalid ambient primary-import API wiring run (reported there as exit 1, 11 failures, 13 errors). They are not reconstructed. Logs 02 and 06 are new, separately labelled observations, not that run.

## Side effects

Editable installs created ignored metadata `src/{core,agents,api}/src/zava_forward_*.egg-info/` (reported by `git status --ignored`, untracked by design). The tracked worktree is clean; the venv depends on them and both are left in place.

## External log hashes (sha256)

| Log | sha256 |
| --- | --- |
| `00-identity-git.log` | `56e0ca7d598b127705582304b9c893860016d65862b7fbabb3cbf7c329c8362f` |
| `01-identity-tools.log` | `edf41eedd4f2e9da5e463069c408b37dfacd0b3c5d2ebd74aae06c2f715a8a9a` |
| `02-ambient-import-probe.log` | `1499a68e5f69fb93c2e031a4bdb748f9e4c69c56e93be880dbb1d09414456b1d` |
| `03-venv-create.log` | `17a278a6fbd8114230cd362411a6417a1f33e935ba493f7ba3fffa7e40052819` |
| `04-pip-install-editable.log` | `2483b8aefd5d55da825e7372c287d3823f9cefc0034b1defb4331291d226b4b1` |
| `05-import-paths.log` | `fb7b71cf0b560e6415d084e4466ff5acc5966dc2c84fe7afd590daf073a92ae0` |
| `06-ambient-path-probe.log` | `241d37d8b9648eeebd9667b097a439f1544fa2fe9473b8eebc3004ae17052210` |
| `10-bicep-build.log` | `dd369ee2119678c31ce4f53a6962ab2d163715f820fd43ab6bcb51d9737704ef` |
| `11-bicep-lint.log` | `af839eec48aacb1925caa0a97aad9b5d579dfee30c27899ef4d3aed1223fb2b0` |
| `12-build-params-iot-hub-live.log` | `f4bac03c1dd57d1695906b719ac4c99429ea2b018a6b822584c356dcc67b9287` |
| `12-build-params-main.log` | `d4482097163603ff799f794a64938264162075ec9c8bffae9465bb9f4394061d` |
| `12-build-params-main.pilot.example.log` | `5987adef1d7ce1719034e85beca225b28e1596f5a22f6b48fbbc698af5a561ea` |
| `12-build-params-main.test.log` | `515dd40ce9e98dd2dbe272fa97a4d6c0802af7e3fa28fb6cb08f3cace9ca5165` |
| `20-infra-unittest.log` | `ee2d924a50cc1c808c583566fdc090e5a6a78214c22e87e5cefa9cec74aecf27` |
| `30-core-blob25.log` | `7c15cdde55703c54da7baf2a110aa01ed0e27cf357c714a1b8252cb30c88fea9` |
| `31-core-runner45.log` | `40dc4b1224ec17869b96615adaab6b2d97bc748088160805be0f6d017eb3b802` |
| `40-api-wiring35.log` | `9c956168a0838d74117f547f06eff918e77ac9e0603d314ff3a2aa21466f85bd` |
| `41-api-wiring35-discover.log` | `8f032390b30889886d0b6a6c30bfe6c6ff05d9f5df6d9f81dc3acbb48158c2f2` |
| `50-ci-ruff-version.log` | `0b9160f87a058786d89f7514bc0ea0455f3ad389078698a74ff8a70bcd9f272b` |
| `51-ci-ruff-check-changed-file.log` | `96ba6a48ccbd791253862337db278a7cf23e14476c5235aa486f5bce94281dc1` |
| `52-ci-ruff-format-changed-file.log` | `ed81489962f2b4e2c9c023e6f702cebc853c21f7eab8f3c2cd61a464d667b947` |
| `53-ci-ruff-check-three-file.log` | `7d70579f88bbcf759d41336939e7589300df0cc34c096eec4b2145285ee0759f` |
| `54-ci-ruff-format-three-file.log` | `f9aaaa0e307a682dba8f1b3d3456aefa213684b4029ff27dc8c7e50088b0e91c` |
| `55-baseline-plain-ruff-check.log` | `e41eaaa27a677b4500e03955519a7b8e04bc7ede520a84624a0c8928a4d80d52` |
| `56-baseline-plain-ruff-format.log` | `1ed0e423294e8b32959de170f30eacc8168d0f19f262da4890fd96c467233daf` |
| `57-ambient-ruff-ci-check.log` | `711abac8cf1d19b811ff206e1445bd139859ce8afdd694187c91751c5b266647` |
| `58-ambient-ruff-ci-format.log` | `dca116a9bc220881cb64de7fe6540d1849ec277029b63e3975207deae66d80bf` |
| `59-baseline-plain-ruff-check-cwd-infra.log` | `719dc16128bc19f9e3583d25f1d5fdf234d878b5c563b120ebff80b5780942f8` |
| `59-baseline-plain-ruff-format-cwd-infra.log` | `1f2072173689b1772f2066e408c210bdc0921136398cb8447f82d039d50751e0` |
| `90-identity-after.log` | `847ea108b3bfa259daf2f8119c6f9da2f87a270a1819fd8c04039d4c874c7912` |
| `91-identity-after-final.log` | `919007775b9e2fcf1f5be29cba54dced0eee7666a469fceae7196296b07409d2` |
| `exits.tsv` | `37eb7134c34b51876d066ae96fd62444215a116c323bdfbd7cc94a67d87a60e0` |

Scripts `run.sh`..`run4.sh` and `run-stdout.txt` are in the same external directory and listed in `SHA256SUMS`. `run.sh` produced logs 00-58, 90; `run2.sh` 41 and 91; `run3.sh` 59 (a first flawed pipe-based 59 draft was deleted before the rerun, it never carried a recorded exit); `run4.sh` 06.

## Not run

Full matrix, `rpi-checks`, SQL, browser, scanners, `az what-if`, deployment, real Azure, role grants, emulator, remaining infra tests, runtime.
