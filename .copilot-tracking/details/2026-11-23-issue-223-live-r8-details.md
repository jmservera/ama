# Details issue-223-live-r8
Step 1: helper `_elapsed_seconds(start_iso, end_iso)` returns max(0, float seconds) or None on parse failure; review() sets `review_seconds=_elapsed_seconds(rec.get("created"), rec["resolved_at"])`.
Step 2: test that accepted review records numeric review_seconds >= 0, and that a mocked later clock yields the expected value.
Step 3-4: commands in changes record.
