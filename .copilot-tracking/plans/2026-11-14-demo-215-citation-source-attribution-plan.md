# Plan: #215 citation and source-origin attribution (2026-11-14)

Refs #215. Branch `test/demo-215-citation-source-attribution-0501` (stacked child). Details: [details](../details/2026-11-14-demo-215-citation-source-attribution-details.md).

* [x] Phase 1: add `src/api/tests/test_alert_chat_citation_source_attribution_215.py`.
* [x] Phase 2: run alert_chat, grounded and regulatory suites, ruff check, ruff format --check, mypy.

Critique (single pass): verdict accepted. Advice applied directly: assert what the source actually exposes (native details, launcher-only ARIA) instead of inventing `aria-expanded` on source lists; no conformance claim.
