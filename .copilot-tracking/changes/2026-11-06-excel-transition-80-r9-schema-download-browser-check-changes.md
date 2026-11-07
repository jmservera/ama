# Issue 80 r9 changes: schema download browser regression (prepared, not run)

Plan: [plan](../plans/2026-11-06-excel-transition-80-r9-schema-download-browser-check-plan.md). Research: [research](../research/2026-11-06-excel-transition-80-r9-schema-download-browser-check-research.md). Details: [details](../details/2026-11-06-excel-transition-80-r9-schema-download-browser-check-details.md).

## Chronology (actual)

* Intake verified at 1e56f443 / tree 1f06403f, ignored-inclusive clean, parent ead177ef unchanged.
* Research, plan and details written, then committed as 778484311, BEFORE the first test file was created.
* Test module, README paragraph, then static checks, then this record.

## Changed paths

* Added `src/api/checks/schema_download_browser_check.py`: real-server Playwright journey. Retrofit Programme Manager registers a synthetic schema via real `POST /api/form-schemas` (expects 201), opens Funding route and claim pack for ZF-1, reaches `a[href="/api/form-schemas.csv"]` by Tab, activates with Enter, checks suggested name `form-schemas.csv`, header (`SCHEMA_EXPORT_FIELDS`), one row naming `SYN-TECH` and `pam@example.test`, no non-safe page requests, no page errors. Programme Support Officer and Grants and Evidence Officer: no link, "could not be read" text, direct export 403, not an attachment, no catalogue tokens. No `page.route`.
* Edited `src/api/README.md`: one paragraph with the command.
* Production UI, API, core and CSS: byte-identical to 1e56f443 (tree hashes of `src/api/src` 4edd946e... and `src/core/src` 0d608464... equal at HEAD and 1e56f443; `git diff --stat 1e56f443 -- src/*/src` empty).

## Light evidence (direct exits, pipefail, caches external, no bytecode; logs under /tmp/80-ui-browser-r9-1106/)

* Tools: Python 3.12.3, ruff 0.17.3, mypy 2.4.1, node v24.21.0.
* `ruff-ci-a1.log` / `fmt-ci-a1.log`: FIRST attempt on the new file with the CI-style isolated rules rc 1 (6 E501 long lines and a formatting difference). Preserved. `fmt-apply-a2.log` formatted the new file only; `ruff-ci-a2.log` rc 0.
* Component `ruff check` rc 0; `ruff format --check` rc 0; mypy rc 0, 187 files (186 plus the new file).
* Nine API modules together (finance screens, role screens conformance, content standard, role screens, procurement screens, loading feedback, list export API, role endpoint inventory, form staging API): rc 0, 120 tests, 37.233s, zero skips.
* Imported identities proven under the worktree `src/api/src` and `src/core/src`.
* Honest r8 qualification: r8's first mypy failure (`var-annotated`, tests line 241) survives only in the original tool event; its raw file was overwritten by r8's second run to the same log. Original raw bytes were not recovered.

## NOT performed

* The browser journey was not run (no Playwright, Chromium, server or SQL; #188 owns the heavy lane). Its correctness against the real page, keyboard focus order, download and denial behaviour is unproven; the first real run may need selector fixes. No axe, assistive-technology or accessibility conformance claim.
* Future command, from `src/api`, with src distributions, Playwright and Chromium, after root admission: `PYTHONDONTWRITEBYTECODE=1 python -m checks.schema_download_browser_check`; selector `a[href="/api/form-schemas.csv"]`.
* FULL on the final stable head against fresh main, independent exact-head review, hosted CI and owner acceptance remain pending. Every-list exports, owner thresholds and approvals remain unproven; nothing ticked or closed.
