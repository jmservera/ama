---
title: Issue 86 Main 4bc1 CI integration author review
ms.date: 2026-11-08
---

Author review for issue86 (Refs #86). Not an independent exact-head assessment.

## Outcome

Conformant for the bounded scope, with one disclosed qualification.

* Execution: the review ran once after implementation; the one prospective critique (4 findings, all accepted) is unchanged.
* Source preservation: `src/` identical to `fb7231c7`; merge is ordinary and conflict-free; Main tooling blobs equal Main.
* Focused checks passed: 86 / 19 / 12 / 17 tests, ruff check and format, mypy strict. The first CI-selection run failed on a missing PyYAML and is preserved; the rerun used a scratch-only install.
* Qualification (Low): local ruff and mypy versions were not confirmed against CI pins.
* Not run: actionlint download, SQL, browser, FULL. Reason: no application behaviour changed.
* Drift: origin Main is now `9d035ee9`, past the integrated `4bc1e3f3`. The coordinator decides whether to refresh.

## Open

Independent exact-head assessment, hosted CI on the published head, #1238, human, receiver and approver gates, and the fourth criterion all stay unmet. Nothing was pushed.
