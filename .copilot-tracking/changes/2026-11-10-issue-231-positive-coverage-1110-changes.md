<!-- markdownlint-disable-file -->
# Issue 231 positive browser coverage changes (2026-11-10)

Task `issue-231-positive-coverage-1110`; Refs #231 and parent #149. FOCUSED tier: test coverage only, no runtime contract change.

## Changed files

* `src/api/checks/role_screens_browser_check.py`: new positive scenarios `231p` (technical complete) and `231qp` (quality accepted), private `positive_technical_quality_data()` wrapper, `STORY_POSITIVE`, `check_positive_state`, `reach_table_regions` (Tab reach at 320 px; 1280 px reach reuses the existing code), case-record equality before and after, dispatch to the private data factory. The negative `231` and `231q` entries, `STORY_231` and the negative `else` branch are unchanged.
* `src/api/README.md`: scenario paragraph for `231p` and `231qp`.
* Not touched: `role_screens_fixtures.py`, `atlas_tensions_browser_check.py`, `test_atlas_tensions_checker.py`, any app, backend, Core, SQL, schema, panel or style file.

## Evidence (external logs under the session `files/evidence231/`)

* Unchanged baseline before edits: `test_technical_quality_screens` 16, `test_role_screens` 8, `test_accessibility_baseline` 12 OK; browser `231` and `231q` exit 0 (36 PASS each), pinned axe 4.10.3 ran, no violations, incomplete `[]`. First invocation error `ModuleNotFoundError: test_role_screens` (modules run without `discover`) kept as `baseline-unit.log`.
* Environment: new owned external venv `/tmp/zf231-venv` (missing-dependency failure of worktree imports first); ruff 0.17.1, mypy 2.4.0, playwright 1.64.0, Chromium 156.0.8078.4; imports of `zava_forward.core.quality`, `zava_forward.api.server` and the checker resolve under this worktree.
* First positive run (`run1-browser-*`): `231p` 47 PASS and `231qp` 46 PASS, exit 0 with the phrases chosen before the first render (none loosened).
* Mutation proof (`mutation-*`): the negative selectors on the positive data fail on `Cannot confirm readiness`; the positive selectors on the negative data fail on the positive phrases. Temporary external script, not committed.
* Final runs on the final bytes (`final2-browser-*`, under the nonqueued `flock -n /tmp/ama-rpi-heavy.lock`, lock free, no skips, pinned axe run): `231` 36, `231q` 36, `231p` 47, `231qp` 46 PASS, all exit 0; no owned server left running. Unit modules final: same three OK. `ruff check` clean; `mypy --cache-dir` no issues; `ruff format --check` still reports the baseline hunk at the pre-existing `place.evaluate` line (not edited, not in scope); no format hunk remains in the added code.
* Recipe: `role_screens_browser_check` is not a registered browser recipe or needs-inventory entry (`git grep` over `.github`, `tools`, `src/core` finds none): SHA and Core manifest updates N/A.
* Positive evidence is on a constructed synthetic home. Synthetic names, sign-offs and acceptance are test inputs, not professional approval. No WCAG, assistive-technology, usability, live or production acceptance is claimed. Whole #231 is not claimed.

## Divergences

None from the plan. One formatting-only edit after the first final run, followed by a re-run of static checks and all four browser scenarios.

