---
title: Issue 441 demo disclaimer details
date: 2026-11-03
task_slug: issue-441-demo-disclaimer
---

Notice text: "Demonstration only: Legal and Data Protection Officer review is still outstanding. Do not use this for real resident data or decisions." It is static HTML inside the existing `role="note"` banner (no new live region, no colour-only signal, plain language, block text for narrow widths). No behaviour, consent, data or AI change. Manual help routes are unchanged.

Validation: unit tests for resident demo API, preview API and demo check; ruff; mypy with --cache-dir=/tmp/mypy-441. Not run: gate, browser checks, full suites.
