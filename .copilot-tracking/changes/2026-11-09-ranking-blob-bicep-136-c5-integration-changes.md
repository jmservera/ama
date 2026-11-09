# Changes: C5 parent integration and formatting (Refs #136, #1258)

Plan: `.copilot-tracking/plans/2026-11-09-ranking-blob-bicep-136-c5-integration-plan.md`. Date 2026-11-09. Tier: owner-selected DEMO-targeted (no blanket gate, SQL, browser, scanner, deployment).

## Changes

* Merge commit `c245c8782` (`--no-ff`, local) of exact `52f9b61bb22c5ceaaed0f9bf6a55dab7a7a59cb8` (tree `20901b61...`) into child `a23f5d3c6`. Result tree `2e47aa63575590cc49ae2ec85160d5e6b3639a9f`, identical to the pre-merge `git merge-tree` prediction; no conflicts. No rebase, reset, force, main or sibling import. Both README intents kept (`src/core/README.md` from the parent, `infra/README.md` from the child).
* Formatting: `ruff format --isolated --line-length 100` on `infra/tests/test_bicep_policy.py` (the CI command). 4 hunks, 19+/7-, all on lines this child added (`for template, flag`, `rankingArchiveContainer` access, two `assertIs(evaluate(...))`, the `forbidden` tuple). No existing line reformatted; the `# noqa: S307` line is untouched; no suppression added; no other file formatted.
* Critique PC-3 wording: `infra/README.md` flag row and `modules/containerapps.bicep` `rankingArchiveContainer` description now say flag-off leaves the API on the local folder adapter (dev/test, not durable evidence), and only the runner `--blob` mode refuses. No behaviour change.

## Commands and exits (integrated source, DEMO tier)

| Command | Result |
| --- | --- |
| `infra`: `az bicep build --file main.bicep` | exit 0 (generated `main.json` removed) |
| `infra`: `az bicep lint --file main.bicep` | exit 0 |
| `infra`: `az bicep build-params --file X --stdout` for `main.test`, `main`, `main.pilot.example`, `iot-hub-live` | exit 0 each |
| `infra`: `python3 -m unittest tests.test_bicep_policy tests.test_identity_rbac tests.test_secret_lifecycle tests.test_api_ingress_transport tests.test_governance` | exit 0, Ran 100 OK |
| `src/core`: `PYTHONPATH=src python3 -m unittest discover -s tests -p test_ranking_archive_blob.py` (new C5 adapter) | exit 0, Ran 25 OK |
| `src/core`: same with `-p test_ranking_publication_runner.py` | exit 0, Ran 45 OK |
| `src/api` in a fresh venv under `/tmp` with editable installs of this worktree: `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_ranking_publication_wiring.py` | exit 0, Ran 35 OK |
| `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_bicep_policy.py` | exit 0 |
| `ruff format --isolated --line-length 100 --check infra/tests/test_bicep_policy.py` | exit 0 (was exit 1 at child HEAD: retained baseline) |

## Adverse and baseline evidence retained

* Format `--check` FAIL at child HEAD `a23f5d3c6` (plain and CI command) is the baseline; it is fixed for the changed lines only.
* First API wiring run used the ambient environment whose editable installs point at the primary checkout `/home/azureuser/source/ama/src/*` (no `ranking_archive_blob`): exit 1, 11 failures and 13 errors, caused by the wrong installed distribution, not by this source. It is NOT counted as passing; the isolated venv run above is the evidence. The primary checkout was not modified.

## Not run, absent, not claimed

Full `rpi-checks`, SQL, browser, images, scanners, az what-if, deployment, emulator, remaining infra tests, Blob runtime. No WORM or immutability lock, no approved retention duration, no folder-record migration. Existing account-scope Blob Data Contributor still permits delete. No role, key, SAS, public access, permission, capacity or paid resource added; no policy duration invented.
