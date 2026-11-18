# Plan: chat keyboard and live announcement hardening (Refs #159)

Date: 2026-11-14. Critique: executed once, self-critique; no conflicts with confirmed decisions.

* [x] Set the widget log to `aria-relevant="additions text"`; update the superseded assertion in `test_chat_origin_badge_a11y.py`.
* [x] Add `src/api/tests/test_workbench_chat_keyboard_live_announce.py` (unique name) covering log/status regions, single status invariants, Escape focus return, Enter/Shift+Enter, native controls.
* [x] Run chat, case journey and accessibility baseline suites; mypy and ruff in `src/api` with `/tmp` caches.
* Tier: focused (small web change, no gate, workflow, dependency or security-control edit). Not pushed.
