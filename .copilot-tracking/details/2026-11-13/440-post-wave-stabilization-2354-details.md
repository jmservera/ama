# Details: #440 post-wave stabilization checkpoint (2354)

## Phase 1: pins

* `git rev-parse HEAD HEAD^{tree}`, `git fetch`, `git diff --stat 839774883 origin/main`.
* Read the last checkpoint section and the coordinator "Stabilization checkpoints" contract.

## Phase 2: ladder

* `python3 -m venv /tmp/venv-440-2354`; `pip install ./src/core ./src/agents ./src/api ./src/orchestrator ./src/importer pytest`.
* Core: manifest, needs inventory, synthetic audit, provenance, coverage, determinism tests.
* Api: accessibility baseline, resident and procurement screen tests, role endpoint inventory, with `PYTHONPATH=../core/tests:../agents/tests` and `ZF_AI_GOLDEN`.
* Infra: `infra/tests/test_bicep_policy.py`.
* Success: exit 0 for each, or a traced environmental cause. Logs kept outside the repository in `/tmp/440-2354-logs`.

## Phase 3: evidence pack

* Append one section at the end of the pack with pins, covered PRs, traceability, commands and exits, classes, findings and recommendation. ASCII only.

## Phase 4: close out

* Change record, review, state file; commit with the repository-local GitHub noreply address and Copilot trailer; no push.
