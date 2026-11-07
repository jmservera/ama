# Issue 86 formal-complaints typing correction: research

Scope: jmservera/ama#86 only (`Refs #86`). First bounded correction of the actual R2 FULL failure in `project-core`. Dated 2026-11-06. Base head `b69afe33267022356da626998d04c42922416cf6`, tree `fb0803feacb07ff5bad76033531e12840e26ab71`. Original research, plan, critique, changes, review, alignment records and the R1/R2 receipts are preserved unchanged.

## Evidence

* R2 gate (`/mnt/ama-gates/g86-r2-1106/0054-project-core.log`, receipt status `failed`, scope `full`) stopped at `python -m mypy` in `src/core` with 14 errors across 267 files. The R2 receipt is not a passing or verified receipt.
* Reproduced RED on the unchanged head with the reviewed gate definition (`tools/rpi-checks.py` line 973: `python -m mypy` in the project directory; `src/core/pyproject.toml` `[tool.mypy] strict = true`, `files = ["src", "tests"]`, mypy `2.4.0`). Read-only use of the R2 core venv `python`; cache in `/mnt/ama-gates/restart-1106-86-typing/cache`; output `/mnt/ama-gates/restart-1106-86-typing/red.txt`. Exit 1, the same 14 errors as the log.
* The R2 venv does not import `zava_forward` outside `src/`; mypy reads sources by `mypy_path`, so the check analyses the worktree files.

## Findings by error

| Error | Cause |
| --- | --- |
| `complaints_route.py:30,34,41,56` no-untyped-def | `submit`, `receiver_from_env`, `build_envelope`, `parse_acknowledgement` were written unannotated. The module is not in any mypy `ignore_errors` override. |
| `test_resident_decisions.py:3237,3242` no-any-return | helpers `route` and `request_without_route` return values read from the untyped `Store.cases` (Any). |
| `test_resident_decisions.py:3262..3380` attr-defined (8) | tests inject `self.store.complaints_receiver`, an attribute `resident_decisions._receiver` reads with `getattr(store, "complaints_receiver", None)` but `Store` never declares. |

## Typing patterns found

* `store.py` declares `class Store(...mixins)`; `SqlStore(Store)` and `MssqlStore(SqlStore)` inherit it. `store.py` and `resident_decisions.py` are in the migrated-module `ignore_errors` override, so annotations there are read by mypy but errors inside are not reported.
* `typing.Protocol` ports exist in `ai_consumption.py` (`LedgerPort`) and `forms.py` (`DocumentReader`, `FormStore`). The README already documents the receiver as "any object with `submit(envelope) -> acknowledgement`".
* `test_resident_decisions` has `disallow_untyped_calls = false`, so tests may call the untyped Store.

## Candidate corrections

1. Declare a `ComplaintsReceiver` Protocol in `complaints_route.py` and annotate its four functions. `submit(envelope: dict[str, Any]) -> object`; `UnconfiguredReceiver.submit` returns `NoReturn`; `receiver_from_env(env: Mapping[str, str]) -> ComplaintsReceiver`; `build_envelope(case_id: str, req: Mapping[str, Any], route_key: str, attempt: int) -> dict[str, Any]`; `parse_acknowledgement(value: object) -> dict[str, Any]`.
2. Declare the injection contract on `Store`: class attribute `complaints_receiver: ComplaintsReceiver | None = None`. Runtime effect: `getattr(store, "complaints_receiver", None)` already treats absent and `None` identically, so `_receiver` behaviour is unchanged and default stays unconfigured. Rejected: `type: ignore`, `cast`, test subclass of Store (would not exercise `SqlStore`), setattr indirection.
3. Test helpers: bind the Any value to a locally annotated `dict[str, Any]` and return that. No behaviour change.

## Risks and unknowns

* Adding a class attribute to `Store` is the only non-test, non-adapter edit. It is a declaration only, default `None`, imports a Protocol from a module with no heavy imports (only `datetime`, plus `typing`), so no import cycle.
* `isinstance(value, dict)` in `parse_acknowledgement` keeps runtime narrowing; typing it `object` is accurate because the receiver is external and untrusted.
* No evidence of a runtime defect; no new runtime logic is proposed. Operational acceptance, any real receiver and external acknowledgement remain unproven.

Planning readiness: Ready.

Superseded by critique (see critique record): `parse_acknowledgement` takes `Any`, and the `Store` declaration is annotation-only under `TYPE_CHECKING` with no runtime attribute.
