---
title: Issue 151 focus not obscured changes
ms.date: 2026-11-04
---

* src/api/src/zava_forward/api/web/style.css: scroll-padding rule
* src/api/tests/test_accessibility_baseline.py: two tests
* docs/reference/research/ux/wcag-conformance-baseline.md: audit row
* docs/reference/log.md: entry

Validation run (src/api, PYTHONPATH=src:../core/src:../agents/src): unittest test_accessibility_baseline, test_design_system, test_content_standard (34 OK); ruff; mypy --cache-dir=/tmp/mypy-151. Not run: gate, browser/axe, full suites, benchmarks, screen reader.
