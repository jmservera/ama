---
title: Issue 151 table headers changes
ms.date: 2026-11-04
---

* src/api/src/zava_forward/api/web/app.js, panels.js: captions and th scope
* src/api/tests/test_accessibility_baseline.py: one test
* docs/reference/research/ux/wcag-conformance-baseline.md: Tables row
* docs/reference/log.md: entry

Validation run (src/api, PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests): unittest test_accessibility_baseline, test_design_system, test_content_standard (36 OK); ruff check and format; mypy with --cache-dir=/tmp/mypy-151 (178 files, tests included, no issues). Not run: gate, browser/axe, full suites, benchmarks, screen reader. Tier: focused (no security, infrastructure, SQL or deployment).
