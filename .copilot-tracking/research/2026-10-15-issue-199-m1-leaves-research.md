# Research: M1 isolated leaves (issue 199, epic 195)

Disposition: executed. Planning Readiness: Ready.

## Evidence

* ADR 0006 (Accepted): move-not-copy, `git mv`, no shim, imports and CI updated in the same PR.
* Parity matrix rows M1: `ai.py` to `core/ai.py`; `profile.py` to `core/profile.py`; `rulecards.py` to `core/rulecards.py`; `test_profile`, `test_rulecards` to core tests; `test_ai_identity` to agents tests (matrix target `agents-tests`, ai itself in core).
* Importers of the moved modules: `store`, `sqlstore`, `assistants` (`Ai`, `FORBIDDEN`); `server` (`profile`); tests `test_assistant_release`, `test_continuity`, `test_assistants` (`Ai`), `test_ai_eval` (patch target string), `test_auth` (patch target strings). `rulecards` has no importer outside its test.
* The three modules use only the standard library, so `core` gains no dependency and `mvp/requirements.*` need no new pin.
* Skeleton `src/core` and `src/agents` run `ruff` (E,F,I,B,UP, line length 100), `ruff format --check` and `mypy --strict` in `src-ci`.
* `mvp-ci` builds the image with context `mvp`, which cannot see `src/core`.
* Docker is not usable locally (permission denied on the daemon socket).
* Baseline on main (`b50d8a8`), `cd mvp && PYTHONPATH=. python3 -m unittest discover -s tests -q`: 719 tests, OK, skipped=92.

## Findings and decisions

* Formatting the moved files with ruff exploded `ai.py` (157 to 278 lines) and broke rename detection. Decision: keep the moved files byte-identical except import lines, and exempt them in `core`/`agents` `pyproject.toml` (ruff format exclude, per-file ignores, mypy `ignore_errors` overrides) until M6.
* `pip-compile` of `mvp/requirements.in` today drifts only in transitive `pycparser` (3.1 to 3.11), so the lock is not regenerated.
* `rulecards.TRACE` holds strings naming old test paths; left unchanged (behaviour unchanged) and logged as a follow-up.
