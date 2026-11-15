# Changes: 435 C1 call-site inventory (2058)

Status: implemented; validated; one review wording fix applied.

## Change

* `src/api/tests/test_ai_call_site_inventory.py`: added `INVENTORY` entry `agents/src/zava_forward/agents/heldout_aoai.py` classified `own-accounting`, note scoped to runner-mediated calls (critique N1) and reworded after review R1 (the runner checks a worst-case reserve before each call, books measured usage, charges the worst case only for an unmeasured reply). No source, workflow, dependency or document change.

## Validation (focused tier, local; hosted CI not yet observed for this head)

* Before the fix: `test_every_provider_call_site_is_classified` failed for `agents/src/zava_forward/agents/heldout_aoai.py` (15 tests, 1 failure).
* After: `src/api` `unittest test_ai_call_site_inventory test_cutover_audit` (PYTHONPATH `../core/tests:../agents/tests:tests`) 15 OK; `src/agents` `unittest test_heldout_batch test_heldout_aoai` 56 OK; `ruff check src/agents src/api` and `ruff format --check` clean; `mypy` in `src/agents` and `src/api` clean. Re-run after the R1 rewording (see below).
* Not run: complete local gate and hosted CI (hosted `src-api` must be read on the exact head after push).

## Divergences

* The first `implement-start` witness was refused (no changes artifact yet); it was recorded after the one-entry edit, so it notes the source was already dirty.

## Baseline

* Rebased branch onto `origin/main` e3a9a28af before state init (head fdd941d60).
* Failing before the fix (scratch venv, pip): `test_every_provider_call_site_is_classified` reports `agents/src/zava_forward/agents/heldout_aoai.py` unclassified (15 tests, 1 failure).
