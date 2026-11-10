<!-- markdownlint-disable-file -->
# Issue 189 C3 type applicability research (2026-11-09)

Task `type-applicability-189-c3`; parent `browser-check-189-c2`. Refs #189 only. Research disposition: executed (read-only; scratch probes outside the repository). Base HEAD `795f871f9e23a1f713a86ee12b694b0728a09d22`, tree `3a9ec5362a3044749d9b72826bbb1f53d1eb00ee`; fetched `origin/main` `ef28d4da42d83b111d48f14df9b70e3c4932a477`.

## The maintained CI command

`.github/workflows/src-ci.yml` job `project` (matrix includes `api`), working directory `src/api`, Python 3.12, installs `pip install -e ../core -e ../agents -e ".[dev]"` (pins `mypy==2.4.0`, `ruff==0.17.1`), then runs `mypy` with no arguments at line 94. `src/api/pyproject.toml` `[tool.mypy]` sets `strict = true` and `files = ["src", "tests", "checks"]`, so both `tests/` and `checks/` are in the maintained type check. The check file is NOT excluded by the real CI. (The separate design-system harness step lints only `design_system_browser_check.py` and `regulatory_ux_check.py`; it does not run mypy.) The C2 handoff run used the same command, so it applies.

## Equivalent isolated comparison

* Current main (`ef28d4da4`): fresh isolated worktree and venv under an owned `mktemp` directory, the CI install profile, `mypy` from `src/api`: exit 0, `Success: no issues found in 199 source files`.
* Current project (`795f871f9`), the same command: exit 1, 8 errors in 2 files, `checked 202 source files`.
* The branch differs from main in `src/api` only by #189 additions; `pyproject.toml`, `src/core` and `src/agents` are identical to main, so the configuration, pins and install profile are the same.

## Origin of every diagnostic (all in files added by this workstream)

Both files were added by #189 commit `522adc394` and do not exist on `origin/main`; "unchanged lines" in C2 only meant unchanged since that earlier head, which does not establish a main baseline. The errors are therefore introduced by #189, not pre-existing against main.

| Line | Diagnostic | Cause |
|------|------------|-------|
| `checks/simulator_control_browser_check.py:123` | `no-untyped-call` TrustedProxyProvider | strict call of the untyped `auth.TrustedProxyProvider` constructor |
| `checks/simulator_control_browser_check.py:125` | `no-untyped-call` App | untyped `server.App` constructor |
| `tests/test_simulator_admin.py:453` | `unused-ignore` | `# type: ignore[misc]` on `class AdminHttpTests(Base)` is not needed |
| `tests/test_simulator_admin.py:455` | `no-untyped-call` setUp | `super().setUp()` into untyped `test_auth.Base.setUp` |
| `tests/test_simulator_admin.py:484` | `no-untyped-call` principal | untyped `test_auth.principal` |
| `tests/test_simulator_admin.py:638` to `640` | `no-untyped-call` PasswordProvider, authenticate, login | untyped `auth.PasswordProvider` |

The existing `Provider`, `Application` and `handler` module aliases in the test are already typed `Any` by earlier #189 work; they are not diagnostics and are left unchanged.

## Remedy without Any, casts, ignores or config change

A scratch probe (outside the repository, `mypy --strict`) shows that assigning an untyped class or function to a precisely typed `Callable` variable is accepted and calls through that variable are not `no-untyped-call`; a small `Protocol` types the provider surface. A `Callable[[test_auth.Base], None]` alias for `Base.setUp` works (a `TestCase` parameter does not, by contravariance). `server.App` and the provider constructors fall under `server`/`auth` modules whose existing overrides use `ignore_errors` or `follow_imports = skip`; no override is touched.

## Scope and cycle

C3 is explicitly authorised by the coordinator for only proper annotations, typed helpers and guards that remove these eight diagnostics, since they are confirmed introduced by #189 and applicable to the maintained type check. After C3 two of five cycles remain. No `Any`, cast, ignore, mypy configuration weakening, deleted check or unrelated baseline correction. The Stop POST readback synchronisation, file assertion and axe scans in the check are untouched. No product or web file changes, so the web-design-guidelines review is recorded as not applicable to changed web files.

## Planning Readiness

Ready.
