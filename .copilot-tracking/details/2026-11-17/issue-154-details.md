# Issue 154 phase details

Phase 2: in `ResidentHttp`, add `test_representative_expiry_and_revocation_take_effect_on_the_next_request`, mirroring the resident test: edit grant `G-REP-B` in `grants.json` (revoked, then valid_to in the past), assert 403 with `body["error"] == "You cannot see this page."` and no `appointments`/`home` key, restore in `finally`, assert 200 again.
