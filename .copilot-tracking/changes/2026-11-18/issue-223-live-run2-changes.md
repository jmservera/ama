# Changes: issue 223 live human-review evidence (2026-11-18)

Tier: FOCUSED (docs and evidence only; no src, infra, SQL or deployment change). Refs #223.

## Files

* docs/reference/research/human-review-live-223-2026-11-18.md (new note)
* docs/reference/research/human-review-live-223-2026-11-18/ (harness report, live probe JSON and script, test logs, screenshot)
* docs/reference/README.md (index row), docs/reference/log.md (entry)
* .copilot-tracking/ research, critique, plan, details, changes, review, state

## Per-criterion table

| Criterion | Result |
| --- | --- |
| Seeded critical defects detected and gated | Proven offline (harness, 4 defect classes, sensitivity runs). Unproven live and with people |
| Reviewer, source and reason retained | Proven (live reject record; harness rows, audit chain verified) |
| Detection, corrections and effort vs workflow-only | Proven in scripted units (23 vs 24). Unproven as measured time |
| Default acceptance and citation validity alone cannot pass | Proven in harness |
| Automation-bias test; reviewer authority and evidence (OQ-017) | Test proven with scripted panel; authority provisional, OQ-017 open |

## Validation

* src/agents tests.test_review_effectiveness: 37 OK. src/core tests.test_human_review_effectiveness_223: 6 OK.
* mypy in src/agents: clean. ruff format check on review_effectiveness.py: clean.
* Live: one rejected review record created on synthetic case ZF-2025-0331. No Azure resource created, nothing to delete. rpi-checks.py not run (no code).
* Credentials read at runtime, not printed or stored.
