# Issue 107 r13 research (2026-11-25)

Disposition: executed. Goal: real-AI acceptance harness code and tests, no tokens spent.

Planning Readiness: Ready

Opening findings (prior passes r1-r12 in docs/reference/research/issue-107-live-*): two unticked criteria remain, (a) independent SQL worker/race tests with old images, (b) matching approved exercise record plus delivered-build real-AI/SQL/Azure evidence. Existing pattern: src/agents heldout_batch.py (authorization, caps, dry-run vs live). Live deployed build denies all five assistants (no approved release, OQ-017).
