<!-- markdownlint-disable-file -->
# Phase details: post-fix-wave checkpoint for #440 (2026-11-12)

## Phase 1: preflight

* Run from `/home/azureuser/source/ama-demo-wt/issue-440-post-fix-wave-1112` with `/home/azureuser/.venvs/postwave-440-1112/bin/python` (`--system-site-packages`; `pip install --no-deps -e src/core -e src/agents -e src/api -e src/orchestrator`, exit 0).
* Prove origin: for `paired_equity`, `form_export`, `digest_blob`, `server`, print module `__file__` and compare `git hash-object` with `git rev-parse HEAD:<path>`.
* Record `git status --short`, `pip list` versions for ruff, mypy, zava-forward distributions.

## Phase 2: ladder (raw output outside the repository under `/home/azureuser/.copilot/session-state/f9385f39-ed8d-41ab-b9b0-67f1574db2fe/files/checkpoint-440-postwave-1112/`)

* L1 `src/core`: `python -m unittest discover -s tests -p <file> -q` with `PYTHONPATH=../../src/core/tests:../agents/tests` as needed; files `test_paired_equity.py`, `test_journey_register.py`, `test_form_export.py`, `test_form_dependencies.py`.
* L1 `src/orchestrator`: `PYTHONPATH=../core/tests python -m unittest discover -s tests -p test_digest_blob.py -q`.
* Static: `ruff check` and configured `mypy` per project (`src/core`, `src/orchestrator`), no writes.
* L2 infra: `python -m unittest tests.test_bicep_policy -q` from `infra`; API: `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_form_held_download_api.py -q` from `src/api`.
* Read exit codes directly; record skips; keep failed attempts.

## Phase 3: documents

* Append the dated section at the end of the pack (after the post-153 accuracy note); append the index paragraph after the post-153 paragraph; append a log entry. Plain ASCII, `*` lists, no em dashes.

## Phase 4: review and commit

* Independent read-only reviewer over the unstaged diff and artifacts; commit locally; `git status` clean; record commit and tree.
