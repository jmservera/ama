# Changes: issue-175 / synthetic-dictionary-175

## Scope and Current State

Full bounded plan authorized by the delivery request. One critique completed;
PC-001/002/003 applied directly to plan/details. No generator-byte changes.
AC2 remains blocked by absent historic official-source metadata.

## P01 Implementation

Implemented typed core validator and CLI, public-only provenance tests and
generated chat integration. Source readiness is a separate nonzero audit.
Updated dictionary/register, project/pack READMEs, knowledge-base index/log.
No private datasets or cloud operations.

## Amendments and Divergences

No material implementation divergence. Critique's unsupported system-temporary
directory prohibition is rejected as a claim about user constraints; compatible
project-local scratch isolation is adopted.
The actual register-backed generator refuses all repository destinations, so its
tests use a disposable outside-repository temporary directory without mocking
the guard. Legitimate all-excluded monitoring output is accepted explicitly.

## P02 Local Evidence

* Combined synthetic acceptance/regression command: 76 tests passed initially
  (core provenance/determinism/sensor/stock/output paths and agents chat/evals).
  Pre-existing sensor tests emitted unclosed-file ResourceWarnings; no failures.
* Core full-project ruff check/format and mypy: passed (100 checked sources).
* Agents full-project ruff check/format and mypy: passed (23 checked sources).
* Loopback API smoke: fresh committed synthetic DATA, explicit isolated
  ZF_DATA/ZF_STATE/ZF_STORE, cleared inherited environment, no model/remote config.
  Threaded server answered /healthz=200 and landing=200; shutdown and scratch
  cleanup completed. No deployment or full HTTP application acceptance implied.
* Public CLI returned zero. Source CLI returns one with the exact three
  historic sources, independently from passing data checks.
* Final rerun after empty-selection regression: 76 tests passed; core/agents
  full-project lint/format/mypy passed. Public CLI has zero findings.
* All 21 newly added Markdown links/anchors resolve. git diff --check passed.
  Diff scope excludes setup-entra.py, all legacy/private/environment paths.

## Acceptance and Remaining Work

AC1/3/4 have local bounded evidence. AC2 unmet.
One post-implementation Review completed: execution Complete, outcome Residual
work. RV-001 routes missing source provenance to a distinct research follow-up.
No second Review or source correction loop. PR delivery remains.

### Reproduction commands

From the repository root, with editable core/agents/API and core dev tools:

```bash
PYTHONPATH="$PWD/src/core/tests:$PWD/src/agents/tests" \
  src/core/.venv/bin/python -m unittest \
  test_synthetic_provenance test_synthetic_determinism test_sensor_stock \
  test_sensor_backfill test_sensor_plausibility test_stock_fabric \
  test_synthetic_output_dir test_chat_provenance test_chat_fixture test_eval_registry -q
src/core/.venv/bin/python -m zava_forward.core.synthetic.privacy --public-root "$PWD"
src/core/.venv/bin/python -m zava_forward.core.synthetic.privacy --public-root "$PWD" --sources
```

The last command is expected to exit 1 (unmet source provenance), not pass.
Within src/core: `.venv/bin/ruff check .`, `.venv/bin/ruff format --check .`,
`.venv/bin/mypy`. Within src/agents use `../core/.venv/bin/` for those same tools.
