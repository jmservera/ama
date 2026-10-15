# Research: M2 core hub move (refs #199)

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue 199 comment, ADR 0006 (Accepted, move-not-copy), parity matrix rows marked M2, merged PR 296 (M1 pattern), `src/README.md`, `.github/copilot-instructions.md`.
* Baseline on `main` (`5c717d9`): `cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests` gives Ran 702, OK (skipped=92). Combined with tests already in `src` the target is at least 742 (matrix baseline 719 at the time of M1).
* The store cluster is cyclic through `assistants`, `ai_registry` and `ledger` (matrix A1). The matrix records that no smaller step leaves a working tree, so M2 stays one pull request.
* `core` may not import `agents` (`tests/test_dependency_rule.py`), so `ai_registry` and `assistants` cannot go to `agents` in M2.

## Findings that shape the plan

* Tests `test_mvp`, `test_assistants`, `test_ranking_scale` use the server or harness, so `test_continuity`, `test_document_controls`, `test_ranking_policy` and `test_mssqlstore` cannot move before M5. Shared fixtures (`case`, `DATA`, `ImproveTests`) must be split out of `test_mvp` into `src/core/tests/dataset.py`.
* Path-sensitive code: `ranking.POLICY_DIR` (policy becomes package data), `factory` default `ZF_DATA`, `test_generated_dataset` generator path, `test_content_standard` ROOT, Dockerfile policy copy, CI `PYTHONPATH`.
* M1 lessons: update `infra/README.md`, test path strings, root-context image build, keep check names.
* Docker and SQL Server are not usable locally (docker socket permission denied); rely on CI.
