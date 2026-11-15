# 215 keyboard, focus and provenance changes

* Added src/api/tests/test_home_chat_regulatory_keyboard_provenance.py (static checks on chat.js and chat-widget.js: native controls, launcher aria-expanded/aria-controls, Escape and Close focus return, live regions, provenance, Sources count, outcome words, cannot-approve warnings).
* src/api/src/zava_forward/api/web/chat-widget.js: `message()` accepts `outcome` and renders a persistent "Outcome: ..." line.
* src/api/src/zava_forward/api/web/chat.js: `outcomeNames` map passed per reply; `statusFor` handles `fallback` explicitly.
* Unchanged: aria-invalid site count (8), test_accessibility_baseline.py, scenario-manifest.json (it does not hash these files).
* Validation (focused, system python3, no uv): ruff check, ruff format --check, mypy (243 files) pass; test_home_chat_regulatory_keyboard_provenance, test_accessibility_baseline, test_regulatory_a11y_cues, test_scenario_manifest, test_needs_inventory pass; also test_chat_panel and test_chat_widget_focus pass.
* Not run: browser check (regulatory_ux_check.py), assistive-technology and comprehension testing; hosted CI unobserved. No push or PR.
