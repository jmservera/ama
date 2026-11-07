# Issue 86 formal-complaints typing correction: details

Scope: jmservera/ama#86 only. Plan: `.copilot-tracking/plans/2026-11-06/issue-86-formal-complaints-typing-plan.md`.

## Edit 1: `src/core/src/zava_forward/core/complaints_route.py`

* Imports: `from collections.abc import Mapping`, `from typing import Any, NoReturn, Protocol`.
* Add `class ComplaintsReceiver(Protocol)` with `def submit(self, envelope: dict[str, Any]) -> object: ...` and a one-line docstring tying it to the README contract.
* `UnconfiguredReceiver.submit(self, envelope: dict[str, Any]) -> NoReturn`.
* `receiver_from_env(env: Mapping[str, str]) -> ComplaintsReceiver`.
* `build_envelope(case_id: str, req: Mapping[str, Any], route_key: str, attempt: int) -> dict[str, Any]`.
* `parse_acknowledgement(value: Any) -> dict[str, Any]`. Bodies unchanged. (Critique finding 1: `object` fails strict mypy at `value.get`; the value is an untrusted receiver reply and the body already validates it at runtime.)

## Edit 2: `src/core/src/zava_forward/core/store.py`

* Import `TYPE_CHECKING` and, under it, `ComplaintsReceiver` from `.complaints_route`.
* In `class Store`, add `if TYPE_CHECKING:` with the annotation-only declaration `complaints_receiver: ComplaintsReceiver | None` and a one-line comment that it is the test and future-approved-receiver injection point. No runtime class attribute is created (critique finding 2: a `= None` default would make `hasattr` true and alter `getattr`/patch semantics).

## Edit 3: `src/core/tests/test_resident_decisions.py`

* `route()`: `found: dict[str, Any] = self.store.cases["ZF-1"]["service_requests"][0].get("formal_route", {})` then return it.
* `request_without_route()`: `req: dict[str, Any] = copy.deepcopy(...)`; pop; return.

## Validation commands (from `src/core`, scratch `/mnt/ama-gates/restart-1106-86-typing/`)

* `python -m mypy` with `MYPY_CACHE_DIR` in scratch.
* `python -m ruff check .` and `python -m ruff format --check .` with `RUFF_CACHE_DIR` in scratch.
* `PYTHONPATH=src:tests python -m unittest test_resident_decisions` and the complaints tests, with `zava_forward.core.__file__` printed to prove worktree origin.
* `git diff --check`; confirm no `type: ignore` or `cast` added.
