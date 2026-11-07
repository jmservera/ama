# Issue 80 r9 Review: schema download browser regression (final, author-only)

Task `excel-transition-80-r9-schema-download-browser-check`. Reviewed boundary: commits 778484311 (research, plan, details) and 51e0f2386 (test module, README, changes, state) over parent 1e56f443. Changes: [changes](../changes/2026-11-06-excel-transition-80-r9-schema-download-browser-check-changes.md). Plan: [plan](../plans/2026-11-06-excel-transition-80-r9-schema-download-browser-check-plan.md).

Review execution: executed once by the author, not independent. Outcome: Conformant to the bounded scope for what was checked; browser behaviour UNPROVEN. Open work is routed to later tasks, not re-reviewed here.

## Web guidelines

web-design-guidelines loaded; source `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` fetched again before this Review, complete (all rules and output format). No web file (JS, CSS, HTML) changed in r9; production UI is byte-identical to 1e56f443 (`src/api/src` tree 4edd946e..., `src/core/src` tree 0d608464... equal at both). The changed files are a Python browser check and README text, so the page-level rules do not apply to them. Applicable intent, checked in the test: native keyboard reach of a semantic link (Tab then Enter), no gesture-only action, no mocked response. Repository ASCII and owner standards override generic style advice.

## Findings (file:line)

* src/api/checks/schema_download_browser_check.py:65 - Tab loop bounded at 150; a focus order longer than that fails the run (fail-closed, acceptable). Unproven against the real page.
* src/api/checks/schema_download_browser_check.py:85 - reload after registering relies on the screen re-reading form-review; unproven until run.
* src/api/checks/schema_download_browser_check.py:97 - download assertions depend on Chromium honouring the `download` attribute on Enter; unproven until run.
* src/api/checks/schema_download_browser_check.py:129 - denial text assertion couples to the current wording "could not be read"; a wording change fails it loudly.
* src/api/checks/schema_download_browser_check.py:157 - "COMPLETE" wording only means these assertions ran; it states no axe scan. It is not an accessibility result.
* src/api/README.md - added paragraph states no CI wiring and no assistive-technology acceptance. No findings.

No blocking findings. Qualified: the journey has never been executed.

## Completed light checks versus deferred

* Completed: ast parse; CI-style isolated Ruff on the new file (first attempt rc 1, preserved; rc 0 after formatting the new file); component Ruff, format and mypy (187 files) rc 0; nine API modules 120 tests zero skips rc 0; imported identities under the worktree; production byte identity; state JSON valid; links resolve; ignored-inclusive status clean before the Review.
* Deferred and unperformed: the browser, keyboard and download run (`cd src/api && PYTHONDONTWRITEBYTECODE=1 python -m checks.schema_download_browser_check`, selector `a[href="/api/form-schemas.csv"]`; needs Playwright, Chromium, src distributions, root admission while #188 holds the heavy lane); FULL on the final head against fresh main; independent exact-head review; hosted CI; owner acceptance. Publication stays blocked.
* Not claimed: every-list exports, owner thresholds, approvals, accessibility conformance; no issue tick or closure.

## Routed follow-ups

1. Run the check once admitted; fix selectors if it fails and preserve the failing output.
2. FULL gate and independent exact-head assessment on the final stable head.
