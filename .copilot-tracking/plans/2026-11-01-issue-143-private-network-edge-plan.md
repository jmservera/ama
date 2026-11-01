# Plan: issue 143 callback consistency guard (2026-11-01)

* [x] Add `test_entra_callback_path_and_host_are_single_sourced` to `infra/tests/test_edge_module.py`: the edge output path equals `callbackPath` in `infra/entra/app-registration.json`, uses the custom domain or default endpoint host, and `main.bicep` surfaces it only when the edge is enabled.
* [x] Run `python3 -m unittest infra/tests/test_edge_module.py`, `ruff check`, `ruff format --check`, `mypy` on the touched test.
* [x] Commit, push, open PR with `Refs #143` naming criterion 5 and the unproven live portion of criterion 3.

Critique (single pass): scope is minimal; no live claims; no conflicts with confirmed decisions. Outcome: proceed.
