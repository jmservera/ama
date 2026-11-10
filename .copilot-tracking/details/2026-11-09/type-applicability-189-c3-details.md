<!-- markdownlint-disable-file -->
# Issue 189 C3 type applicability phase details (2026-11-09)

Plan: [plan](../../plans/2026-11-09/type-applicability-189-c3-plan.md).

## P2 Edit (from `src/api`)

`tests/test_simulator_admin.py`:

* Import `Callable`, `Mapping` and `Protocol`; add `class SessionProvider(Protocol)` with `login(email: str, password: str) -> str` and `authenticate(headers: Mapping[str, str]) -> Mapping[str, object] | None`.
* Typed aliases: `make_password_provider: Callable[[object, str], SessionProvider] = auth.PasswordProvider`; `principal_header: Callable[..., str] = principal`; `base_set_up: Callable[[Base], None] = Base.setUp`.
* `class AdminHttpTests(Base):` without the unneeded `# type: ignore[misc]`; `setUp` calls `base_set_up(self)`; the principal call uses `principal_header`; the password provider test uses the typed factory. If `simulator_admin.handle` needs a narrower user type, narrow with an `assertIsNotNone` guard already present, not a cast.

`checks/simulator_control_browser_check.py`: typed factory aliases `make_provider: Callable[[object, Mapping[str, str]], auth.TrustedProxyProvider-like Protocol]` and `make_app` with a small `Protocol` or `object`-returning callable accepted by `server.make_handler`; use them at lines 123 and 125. The Stop wait, file assertion and axe scan lines are not touched.

If the exact alias shapes differ after the first mypy run, adjust within the same constraints (no `Any`, cast or ignore, no config change).

## P3 Validation (CI profile, owned `mktemp` capture directory outside the repository, raw cmd/stdout/stderr/exit files)

* Main baseline (already captured in research): isolated worktree and venv, `mypy` exit 0, 199 files.
* Project: `ruff check .`, `ruff format --check .`, `mypy` from `src/api` in the project venv, same pins (ruff 0.17.1, mypy 2.4.0).
* Unit: `test_simulator_admin`, `test_live_control` with `PYTHONPATH=../core/tests:../agents/tests`.
* Browser/axe: the check with the pinned axe file, repeated, plus the retained delayed-write regression (old wait fails, new wait passes) to prove synchronisation is intact. Diff proof that the Stop wait, file assertion and axe lines are unchanged.
* `git diff --stat` shows only the two files; `grep` proves no new `Any`, `cast` or `type: ignore` and no `pyproject.toml` change.

## P4 Records

Raw outputs and `hashes.sha256` stay outside the repository; concise records and the manifest hash go in the changes and review records. Web-design-guidelines review: not applicable, no web UI file changes.
