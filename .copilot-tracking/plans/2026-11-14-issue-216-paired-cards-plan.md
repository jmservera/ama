# Plan: Issue #216 paired comparison

1. Add card_links and missing_card_links per row.
2. Count unmatched paired cases and missing links as reasons forcing cards alone.
3. Emit recommendation (ship_cards_only | ship_chat_beside_cards) and cards_alone.
4. Unit tests; ruff and mypy.
Critique: single pass, no conflicts.
