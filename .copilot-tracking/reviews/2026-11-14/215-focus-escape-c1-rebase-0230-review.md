# 215 focus-escape C1 rebase review

* Execution: once. Outcome: conformant for rebase scope.
* ruff check and ruff format --check pass on test_home_chat_regulatory_keyboard_provenance.py.
* 130 src/api tests OK (1 skipped): keyboard provenance, regulatory a11y cues, accessibility baseline, chat widget focus, chat panel, rule alerts.
* Limits: focused tier only; no hosted CI, push or independent review done.
