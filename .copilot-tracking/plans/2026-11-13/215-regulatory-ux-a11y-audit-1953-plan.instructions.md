---
applyTo: '.copilot-tracking/changes/2026-11-13/215-regulatory-ux-a11y-audit-1953-changes.md'
---

# Plan: issue 215 accessibility evidence audit

Details: [details](../../details/2026-11-13/215-regulatory-ux-a11y-audit-1953-details.md)

* [ ] Phase 1: run unit tests (`test_regulatory_ux_check`, `test_accessibility_baseline`, `test_content_standard`) in `/tmp/venv-215-1953`; record counts.
* [ ] Phase 2: fetch axe-core 4.10.3 to an external dir, run `checks.regulatory_ux_check --axe`; record PASS line and axe violations/incomplete counts.
* [ ] Phase 3: write the changes record with results and residuals (no assistive technology test, no staff comprehension test, axe incomplete items need human assessment); no source edits.
* [ ] Phase 4: independent code-review, commit, remove own venv, witness.

Critique amendments: Phase 2 uses a fresh empty output directory and records any failure instead of reusing stale JSON; Phase 3 states this is not a WCAG conformance claim and criterion 3 remains unmet.
