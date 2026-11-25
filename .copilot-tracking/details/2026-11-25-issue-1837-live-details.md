# Issue 1837 phase details, 2026-11-25

Phase 1 reuses the `nomination_payload` and `seed_priority_proposal` helpers. Correction payload follows the standalone form: id, expected_version, channel, account, source, reported_subject_ref, next_update. Challenge payload follows `challenge_targets`. Success: every rejected write leaves `GET /api/cases/ZF-1` unchanged.
