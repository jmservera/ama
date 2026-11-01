# Changes: issue 143 callback consistency guard (2026-11-01)

* `infra/tests/test_edge_module.py`: added `test_entra_callback_path_and_host_are_single_sourced` (edge output path equals `callbackPath` in `infra/entra/app-registration.json`; host derives from custom domain or default endpoint; `main.bicep` surfaces it only with the edge enabled and passes `edgeCustomDomain`); sorted imports.
* No Bicep or runtime change.

Validation: `python3 -m unittest infra/tests/test_edge_module.py` OK (9 tests). `ruff check` reports 5 pre-existing findings in untouched lines of this file (infra/tests is not in a ruff-gated project; not fixed to keep scope tight). `mypy` reports pre-existing Optional `.group` findings in untouched helpers.
