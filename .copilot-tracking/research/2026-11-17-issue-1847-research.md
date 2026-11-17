---
title: Issue 1847 research
---
# Research: nomination test bootstrap isolation (#1847)

Disposition: executed. Planning Readiness: Ready. Tier: FOCUSED (test-only), per coordinator brief.

## Measurements (native, fresh processes, venv `/tmp/v1847` with noneditable installs of `src/core` and `src/agents`)

* `cd src/core/tests; python -m unittest test_bulk_edits test_nomination_route`: 55 tests, FAILED (failures=1, errors=20). Reproduces the #1840 observation on the original bootstrap.
* Reverse order: 55 tests OK.
* Identity probe after importing `test_bulk_edits` then `test_nomination_route`:
  * `test_bulk_edits.ConflictError` came from `/tmp/v1847/lib/python3.12/site-packages/zava_forward/core/store.py`.
  * `test_nomination_route.ConflictError` came from `src/core/src/zava_forward/core/store.py`.
  * `nomination.ConflictError is bulk.ConflictError`: False; `store` modules differ; `GateError` differs; `sys.modules['zava_forward.core.bulk_edits']` is the src copy while `test_bulk_edits.bulk_edits` is the site-packages copy.
  * Confirmed (measured): the whole-family purge splits exception/patch identities; two copies of the same source coexist.

## Contract (from `src/core/pyproject.toml`, `namespaces = true`, no `zava_forward/__init__.py`)

* `zava_forward` is a namespace package spanning `src/core/src` and `src/agents/src`.
* Supported: every loaded `zava_forward` module resolves under `src/` (editable install, or `PYTHONPATH` of the source roots), distribution metadata supplied by the editable install.
* Unsupported: a noneditable/foreign copy (site-packages) already imported before the nomination module loads. The original bootstrap silently purged it; the fix rejects explicitly with `ImportError` and no `sys.modules`/`sys.path` mutation.
* A noneditable install with the nomination module imported first is still isolated, because source roots are prepended to `sys.path` before any package import.

## Smallest safe fix

Replace the purge with a pre-mutation foreign-module check that raises, plus a post-import provenance check. Add a fresh-process regression in a new test module.
