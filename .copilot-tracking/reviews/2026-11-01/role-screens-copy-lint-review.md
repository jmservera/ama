---
title: Role-screens copy lint review
---

Review executed once. Outcome: conformant, no open findings.

* node --check passed; api unittest: 1563 tests OK (323 skipped); ruff check and mypy pass on the test file.
* `ruff format --check` reports the test file unformatted; this predates the change (long-line style throughout) and was left alone.
* BANNED unchanged; ALLOWED gains identifier-only `h.hold`, `inv.hold`.
