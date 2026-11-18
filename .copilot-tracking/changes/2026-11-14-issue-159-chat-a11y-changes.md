# Issue #159 criterion 6 changes

* `chat-widget.js`: log gains `aria-atomic="false"`.
* `chat-widget.css`: widget-scoped `:focus-visible` rule with Fluent focus tokens, including the launcher.
* `tests/test_chat_panel_accessibility.py`: 4 tests (live-region attributes, focus rule, keyboard flow and focus preservation, Send-to-composer focus).

Divergence: the panel remains `role="dialog"` rather than `region`; the dialog is labelled and non-modal.

Validation: the fast formula passed (targeted modules, ruff, mypy). The full discover suite was not run, by instruction.
