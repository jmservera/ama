# Plan: #154 alternatives and representative view

* [x] Add pure `resident_access.py`: per-step non-digital alternative with stated needs, `capacity_inferred=False`; `representative_view` shows only the latest confirmed version's tasks and denies when expired, not yet effective, revoked, disputed or unclear, with no case detail.
* [x] Add `tests/test_resident_access.py`.
* [x] Ruff check and format (line length 100); run focused tests.
* Critique (one pass): keep module pure, no store or UI changes; compatible, applied. Wiring into web screens deferred to avoid conflicts.

## Cycle 2 plan

* Replace `(versions or [None])[-1]` with `versions[-1] if versions else None`; behaviour unchanged.
* Annotate test helper `authority(**kw: Any) -> dict[str, Any]`.
* Verify with `mypy`, `ruff check`, `ruff format --check` and the unit tests in `src/core`.
* Critique executed once: compatible, no conflicts, no user decision required.
