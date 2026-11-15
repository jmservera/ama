# Plan: server refusal lexical guard

* Add `test_server_refusals_in_signoffs_and_workflows_avoid_internal_terms` to `src/api/tests/test_content_standard.py`.
* Parse `signoffs.py` and `workflows.py` with `ast`; collect string constants (including f-string parts) inside `raise` expressions and the sign-off `why` lists; assert none match `BANNED`.
* Guard against vacuous pass: assert a minimum number of literals found.
* No wording changes needed (research: zero hits).
* Validate: test_content_standard, test_workflows, test_finance_signoffs, ruff, mypy.
Details: single test, ~25 lines, no new dependencies.

## Revision after critique (verdict Revise, all three applied directly)

* PC-001: scope also includes returned reasons in `signoffs.missing_items` and `signoffs.technical_gate` (all string constants in those functions).
* PC-002: boundary is literal message text authored in these two files; text built in other modules (for example `gates` verdict reasons) is guarded by existing tests there. Fragments are joined per f-string so a word split across interpolation is judged on rendered literal text.
* PC-003: per-file, per-category minimum counts (raise, why list, returned reasons), plus a mutation test that injects a banned word into each category of the source and expects the extractor and guard to flag it.
