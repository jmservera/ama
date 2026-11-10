---
title: Issue 96 diagnostic D1 research
description: Diagnosis of the default configured API mypy failure on the Held download test module
ms.date: 2026-11-10
---

## Scope and disposition

* Research disposition: executed. Parent candidate 02db2362 (artifacts `issue-96-held-download-1110-*` are preserved unchanged). D1 is one bounded validation-harness correction; no D2/D3; the old #96 balance stays UNKNOWN.
* Retained history does not contradict the zero-earlier-diagnostics premise for this consumer: the parent handoff records one baseline invocation error (dotted core module names), a command mistake and not a diagnostic RPI.

## Evidence

Raw logs are external: `ROOT/phase96-diagnostic-d1-evidence-1110/run/`.

* Root reproduced from `src/api`: default `mypy --no-incremental` exit 2, "Source file found twice ... test_form_staging_api and tests.test_form_staging_api" (`96-root-configured-mypy-1110.log`, mypy 2.4.1, unpinned).
* My venv had drifted (mypy 2.4.1, ruff 0.17.3, playwright 1.64.1; `pins-before.txt`). It was restored to the declared `src/api/pyproject.toml` dev pins mypy 2.4.0, ruff 0.17.1, playwright 1.64.0 (`pins-after.txt`). The pinned default run reproduces exit 2 (`mypy-pinned-before.log`). Unpinned (Root) and pinned outputs are both preserved.
* Old claim: the parent state and handoff said mypy passed. The command actually run was `mypy src checks/held_form_download_browser_check.py` with file selectors; it never loaded `tests/`, so it did not prove the configured whole-API check. Ruff then also ran as 0.17.3, not the 0.17.1 pin.
* Cause 1: `tests/test_form_held_download_api.py:12` uses `from tests import test_form_staging_api`. The project convention for sibling test imports is plain `import test_x` / `from test_x import ...` (many examples; `mypy_path` includes `tests`). `tests` has no `__init__.py`, so the namespace import creates the second module name.
* Probe (import line only, then reverted; `research-probe-mypy.log`, 215 source files): exit 1 with 26 errors, all in the new test module. 24 come from borrowing `FormApi.setUp/shutdown/call/working_review` as class attributes (invalid self, missing attributes); 2 are "call to untyped function held_download_enabled" from direct `server.held_download_enabled(...)` asserts.
* `server.held_download_enabled` is unannotated production code. Production edits are out of scope for D1, so the test must not call it directly.

## Options

1. Extract the four fixture methods of `FormApi` into a small base `FormApiFixture(unittest.TestCase)` in the same existing test file (same pattern as `ProcurementApiFixture`). `FormApi` inherits it and keeps its 14 tests; the new module subclasses the fixture. Bounded, typed, no Any or ignore. Selected.
2. Subclass `FormApi` directly: re-runs the 14 base tests in the new module. Rejected as duplication.
3. Dynamic import, ignores, exclusions, `__init__.py`, follow-imports: forbidden by the brief.

Trusted-proxy guard: exercise the real route with the owned test app's provider reporting `trusted-proxy` instead of calling the unannotated function; stronger and typed. Default-OFF flags, profile, attestation guard and exported contract are not changed.

## Planning Readiness

Ready. Residual unknown: whether further type errors appear after the fixes (the probe shows only the above 26).
