# Plan: #215 unblock and visit grounding regression suite (Refs #215)

Details: [../../details/2026-11-14/215-unblock-visit-grounding-0508-details.md](../../details/2026-11-14/215-unblock-visit-grounding-0508-details.md)
Critique: [../../critiques/2026-11-14/215-unblock-visit-grounding-0508-critique.md](../../critiques/2026-11-14/215-unblock-visit-grounding-0508-critique.md)
Tier: focused (unit and focused API checks; no `rpi-checks.py --all`, Docker or cloud).

* [x] 1. Add `src/api/tests/test_alert_chat_unblock_visit_grounding_215.py` locking API payload, deterministic text and rendered-copy contracts.
* [x] 2. Fix source only if a bug reproduces (none reproduced, no source change).
* [x] 3. Run unittest, ruff check, ruff format --check, mypy.
* [x] 4. Write changes and review records; one commit, no push.
