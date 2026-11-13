# Research: verify src/orchestrator unit tests at 3b05143179 (Refs #115, #144, #117, #148)

* Task: 115-orchestrator-verify-1143
* Base: 3b05143179f83235c5b4e80e70aad99bdc44d83f, branch test/child-115-orchestrator-1143
* Disposition: executed (local read-only inspection)
* Validation tier: Focused (tracking-only write surface)

## Findings

* Context read: case study original, addendum (size only, not relevant to a test run), docs/reference/README.md index, memory.md.
* `src/orchestrator/pyproject.toml`: python >=3.12; depends on `zava-forward-core[sql,blob]`; setuptools src layout, namespace package.
* README documents run as `PYTHONPATH=../core/tests python3 -m unittest discover -s tests` from `src/orchestrator`.
* Test modules (lines): test_dependency_rule 48, test_digest_blob 479, test_document_rescan_job 361, test_rebuild 388, test_rebuild_azure 606, test_source_monitor 108, test_token_store 55, test_version 23.
* Tests import helpers that live in `src/core/tests` (`source_monitor_fixture`, `test_document_rescan`, `dataset`, `release_support`), so `PYTHONPATH=../core/tests` (not `mvp`) is required and is the README-documented path.
* Editable installs needed: core, agents, importer, orchestrator (`--no-deps --no-build-isolation`) in a `--system-site-packages` venv.

## Planning Readiness

Ready. Risks: missing optional third-party deps (sql/blob extras) in system site-packages may cause import errors or skips; report them verbatim, do not fix src.
