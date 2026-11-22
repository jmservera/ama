# Plan: issue 2206 round 2 (2026-11-21)

Tier: focused (tools and docs only; no src change).

1. Retry a timed-out /healthz once with 90 s in tools/demo_preflight.py; add one test.
2. Record live evidence and the per-criterion table in the research note, log entry.
3. Changes and review records; one local commit.

Critique (executed once, accepted): keep the fix minimal and do not add an exec-based count reader, which depends on a pty and is fragile; document the in-network recipe in evidence instead. A second timeout must still fail. No conflict with owner decisions.
