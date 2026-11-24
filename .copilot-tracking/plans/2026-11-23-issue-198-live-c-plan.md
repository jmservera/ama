# Plan 2026-11-23 issue 198 live (c)

Critique (executed once, verdict accept): a read-only test over the real tracked tree is stable because it only asserts non-empty scope for solution-code and infrastructure and no oversize skips; it must not assert exact counts. Tier focused: test file only under `.github/rubric/scripts/`, no `src/`, workflow or registry edit.

Phases:
1. Add `test_given_registry_when_resolved_then_code_artifacts_have_files` to test_prepare.py.
2. Run test_prepare.py and test_safe_output_runtime.py.
3. Research note with per-criterion table, changes, review; commit.
