# Details: #215 doubt route and no-source held-state parity (2026-11-14)

* Harness: `regulatory_fixture.Fixture(sql=True)` plus `App` and `RegulatoryChat` wired with the fixture env; role set by updating the staff body, as in `test_role_change_blocks_direct_and_generic_history`.
* Static checks read `chat.js` and `style.css`; runtime checks call `RegulatoryChat.ask` and `.doubt` directly. No network, no provider calls.
