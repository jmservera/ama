# Changes: issue 2124 live (2026-11-23)

Tier FOCUSED. No src change. Added: docs/reference/research/issue-2124-live-2026-11-23.md, its evidence folder (refusal_live.py, raw run, unit-test outputs), docs/reference/log.md entry and index row.

Validation: live refusal run 10 of 10 refused, 0 model calls, 10 threads deleted; src/core 31 tests OK; src/agents 80 tests OK. rpi-checks.py --all not run. No hosted CI observed (local commit, not pushed).

## Per-criterion table

| Criterion | Proven or unproven | Basis |
| --- | --- | --- |
| Citation validity and refusal accuracy gates set with owners and measured on a graded and adversarial set | Proven for the demo, with limits | Refusals 10 of 10 live 2026-11-23; cited model answers 9 of 9 valid (2026-11-18 pass); gate code and tests; single case, author-graded |
| Named Legal and Compliance owners, independent grader, larger set | Unproven, owner-gated | Waived for demo |
| Regulatory-chat citation against rule cards live | Unproven | Test account role 403 |
