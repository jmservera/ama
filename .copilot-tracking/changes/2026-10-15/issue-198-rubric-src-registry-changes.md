# Changes: issue 198

* `.github/rubric/artifacts.json`: added `src/**/web/vendor/**`, `src/**/data/**`, `**/*.egg-info/**`, `**/build/**` to `solution-code` excludes.
* `.github/rubric/scripts/test_prepare.py`: 10 new cases (5 counted, 5 excluded).
* `.github/rubric/README.md`, `docs/reference/log.md`, `docs/reference/README.md`: documented.
* Before/after on the current tree: every artifact has the same file set (solution-code 120 to 120, no `src/` exists yet); no score change is expected from this PR.
* Validation: 124 passed, 19 failed (same 19 as before the change), 7 skipped.
