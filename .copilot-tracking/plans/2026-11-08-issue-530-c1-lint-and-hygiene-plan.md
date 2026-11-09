---
title: Issue 530 C1 chat checker lint and ignored-input hygiene plan
ms.date: 2026-11-08
---

* Research: `.copilot-tracking/research/2026-11-08-issue-530-c1-lint-and-hygiene-research.md`. Details: `.copilot-tracking/details/2026-11-08-issue-530-c1-lint-and-hygiene-details.md`.

## Phases

* [ ] Phase 1: commit research, plan, details and critique alone before any edit.
* [ ] Phase 2: format and lint `src/api/checks/employee_chat_browser_check.py` with no behaviour, assertion, axe, result schema or string value change.
* [ ] Phase 3: add `employee_chat_browser_check` to both browser lint tuples in `tools/rpi-checks.py` and one focused regression in `tools/test_rpi_checks.py`.
* [ ] Phase 4: LIGHT validation: tools tests, ruff, mypy, checker lint and format, exact diff, byte-identical production source.
* [ ] Phase 5: relocate generated ignored paths to external scratch with hashes and a journal, then assert zero ignored paths and no unintended changes. Full cleanliness (no ignored, untracked or dirty paths) is asserted after the final commit.
* [ ] Phase 6: changes and Review records, state file, local commit with noreply identity.

## Boundaries

* No workflow or native CI edit; hosted CI parity stays residual. No runner, dry run, probe, lock, SQL, Docker, browser, Trivy or live call. Full gate not admitted.
