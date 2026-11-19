# Changes

Process note: the test file was drafted before this record existed; the witness `implement-start` reported "source was already dirty". Recorded honestly.

* Added src/core/tests/test_challenge_signed_in_principal_220.py (tests only; FOCUSED tier, no source behaviour change).
* Added docs/reference/research/issue-218-first-unmet-demo-criterion-2026-11-19.md, README index line, log entry.

Validation: 26 targeted core tests OK; ruff format and check clean on the new file; mypy in src/core shows only 22 pre-existing missing opentelemetry stub errors, none in the new file; mutation probe (whole-dict comparison) fails the positive test with the live 403 message.

## Per-criterion table

| Criterion | Result |
| --- | --- |
| #218 stabilization checkpoint (#440) | Unproven |
| #218 children closed or deferred | Unproven |
| #220 no retaliation, inferred refusal, delayed hazard response | Proven offline for live-shaped principal; unproven live (needs redeploy) |
| #221 restart authority per RULE-024 | Not attempted |
| #221 suspension and manual fallback drill | Excluded (no drills) |
| #222 owner approval of cohorts (OQ-018) | Unprovable for demo |
| #223 five criteria | Not attempted |
| #224 four criteria | Deferred to production (#1905) |
