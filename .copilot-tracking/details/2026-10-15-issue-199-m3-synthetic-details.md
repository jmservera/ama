# Details: M3 synthetic tools and data governance

Plan: [plan](../plans/2026-10-15-issue-199-m3-synthetic-plan.md).

## Moves (all `git mv`)

| From | To |
| --- | --- |
| `mvp/zavaforward_mvp/{scale_fixture,sensor_backfill,loadcheck}.py` | `src/core/src/zava_forward/core/synthetic/` |
| `mvp/zavaforward_mvp/chat_fixture.py` | `src/agents/tests/chat_fixture.py` |
| `mvp/evals/document_control_fixtures.json` | `src/core/evals/` |
| `mvp/evals/document_form_fixtures.json` | `src/importer/evals/` |
| `mvp/evals/registry.json` | `src/agents/evals/` |
| `test_needs_inventory`, `test_sensor_backfill`, `test_sensor_plausibility`, `test_synthetic_provenance` | `src/core/tests/` |
| `test_chat_fixture`, `test_eval_registry` | `src/agents/tests/` |
| `test_document_form_fixtures` | `src/importer/tests/` |

## Edits

* New `core/synthetic/__init__.py` with `output_dir(name, env)`; new test `test_synthetic_output_dir`.
* New `mvp/tests/test_chat_fixture_roles.py` (role names equal `auth.DEFAULT_ROLE_MAP`).
* Repointed `test_recovery`, `test_chat_isolation`, `test_document_controls`.
* CI paths and `PYTHONPATH` in `mvp-ci`, `mvp-validation`; `src-ci` paths add the docs pack and generator folder its tests read.
* Exemptions in `core`, `agents`, `importer` `pyproject.toml`.
* Docs: matrix, reference index and log, `src/README`, `mvp/README`, `copilot-instructions`, retrofit-synthetic-data pack, generator usage strings.
