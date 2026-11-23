# Plan 2026-11-23 issue 198 live (b)

Critique (executed once, verdict accept): adding a registry test is small and reversible; a test must read `artifacts.json` only, never alter it; the tier is focused because only a test under `.github/rubric/scripts/` changes (no `src/`, workflow or registry edit). Direct disposition: test checks every include/exclude glob and the rubric workflow source for `mvp/` and `prototype`.

Phases:
1. Add `test_given_registry_when_loaded_then_no_mvp_or_prototype_glob` to `.github/rubric/scripts/test_prepare.py`.
2. Run `test_prepare.py` and `test_safe_output_runtime.py`.
3. Write the research note with per-criterion table; update changes and review records; commit.
