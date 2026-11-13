---
title: Issue 215 regulatory UX accessibility audit changes
description: Automated accessibility and plain-language evidence run for issue 215 criterion 3, with honest residuals
ms.date: 2026-11-13
---

## Summary

No source files changed. This record documents a local, focused-tier audit run on 2026-11-13 (branch `docs/demo-215-regulatory-ux-audit-1953`). It is not a WCAG conformance claim. Issue #215 criterion 3 (WCAG 2.2 AA, no colour-only status, keyboard operable, plain-language mode) and criterion 5 (staff comprehension) remain unmet; nothing was ticked and GitHub was not edited.

## Environment

* Venv `/tmp/venv-215-1953` (pip only): `-e src/core -e src/agents -e src/api`, `playwright==1.64.0` (the pin in `src/api/pyproject.toml`), Chromium 1248 from the local Playwright cache.
* The Playwright driver node needed `libatomic.so.1`, absent from the host and not installable without root (`dpkg` interrupted). The `libatomic1` package was downloaded and extracted under `/tmp/ama-215-1953-out/atomic` and supplied through `LD_LIBRARY_PATH` for this run only. The first run with `playwright 1.65.1` failed on that missing library before any check started.
* axe-core 4.10.3 fetched from cdnjs; SHA-256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb` matches the pin asserted by the check.
* Fresh output directory `/tmp/ama-215-1953-out`; JSON `regulatory-ux-results.json` came from this successful run.

## Results

| Check | Result |
| --- | --- |
| `test_regulatory_ux_check` | Ran 8, OK |
| `test_accessibility_baseline` | Ran 13, OK |
| `test_content_standard` | Ran 21, OK |
| All three combined | Ran 42 in 0.730s, OK, no skips |
| `python -m checks.regulatory_ux_check --axe ... --out ...` | `PASS: 21 browser states, target sizes, keyboard, reflow, roles and real local API; axe executed`; JSON outcome `passed` |

Commands ran from `src/api` with `PYTHONPATH=tests:../core/tests:../agents/tests`.

### axe-core 4.10.3 across the 21 scanned states

* Violations: 0 in every state.
* Incomplete (needs human assessment): 0 in every state.
* Rule passes: 379 in total (14 states at 20, `200-percent-text-320px` at 21; four role screens at 15; `disabled-chat` 17; `supplier-human-route` 1).
* States: alert-collapsed-chat, cited-answer, cited-answer-fade 35 and 50 percent, no-source-refused, 320, 390 and 1280 px reflow, 200 percent text at 320 px, source-changed-retained-risk, conflict-auto-referral, conflict-referral-restored, disabled-chat, seven role screens, supplier-human-route.
* The run logged expected `status=503` responses for `GET /api/law/alerts` while exercising the disabled-chat state.

## Residuals (not evidenced by this run)

* The check's own JSON states: scope is synthetic changed surfaces only, not a WCAG conformance certification; `staff_comprehension` is "Not run; unmet"; `resident_wording_review` is "Not supplied; unmet".
* No screen reader, voice control, switch or magnification testing was done. Automated axe coverage detects only a subset of WCAG 2.2 failures.
* Keyboard operation, target size, reflow and no colour-only status were checked only on constructed synthetic loopback fixtures in headless Chromium, not on the live site or in hosted CI.
* Plain-language mode was verified through copy-audit unit tests against the content standard, not by readers.
* Comprehension with repairs, housing and grants staff (criterion 5) is untested and requires real participants and named human approval.
* The `libatomic` workaround is local only; hosted `src-ci` installs browsers with `--with-deps` and was not observed.

## Follow-ups

* Owner decision on criterion 3 once assistive-technology testing is planned.
* Staff comprehension session for criterion 5.
