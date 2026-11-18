<!-- markdownlint-disable-file -->
# Details: Escape and disclosure semantics tests (#215)

## Phase 1

* Chat panel: launcher `aria-controls`/`aria-expanded` sync, root Escape handler, focus return ordering, shared trigger, no trap.
* Regulatory lookup: native `details`, Escape only when open, focus to own summary, no redundant ARIA.
* Alerts and citations: plain content, no disclosure or ARIA state, new-tab links with `noopener`.

## Phase 2

`cd src/api && PYTHONPATH=src:../core/src:../agents/src:../orchestrator/src:../importer/src:../core/tests:../agents/tests:tests python3 -B -m unittest tests.test_alert_chat_escape_disclosure_semantics tests.test_accessibility_baseline -v && ruff check src tests && ruff format --check src tests`
