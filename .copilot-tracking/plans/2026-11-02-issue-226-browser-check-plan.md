---
title: Issue 226 browser check plan
date: 2026-11-02
task_id: issue-226-browser-check
---

## Plan

* [x] Add scenario `226` to `src/api/checks/role_screens_browser_check.py` and run the accessibility checks for it.
* [x] Document the check in `src/api/README.md`; append `docs/reference/log.md`.
* [x] Validate: focused unit tests and the browser check with the pinned axe file. No gate or rpi-checks.

## Critique (one pass, inline)

Compatible. Keep scope small; do not claim WCAG, AT or design-system acceptance. Result: PR uses Refs.

Details: [details](../details/2026-11-02-issue-226-browser-check-details.md)
