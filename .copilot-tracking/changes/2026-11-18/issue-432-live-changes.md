# Issue 432 live changes

Tier: FOCUSED (documentation and evidence only; no src change; rpi-checks.py --all not run). Refs #432.

## Files
* docs/reference/research/ai-heldout-batch-432-live-2026-11-18.md (new research note)
* docs/reference/research/evaluation/heldout-batch-432-live-2026-11-18/ (authorization, manifest, proposals, live report, preserved stopped attempt 1)
* docs/reference/README.md (index row), docs/reference/log.md (entry)

## Live actions (Azure rg ama, authorised)
* Dry run; live attempt 1 from this host stopped (unmeasured-call, network disabled on aif-cutover-test-rzsrg).
* Temporary role assignment Cognitive Services OpenAI User on aif-cutover-test-rzsrg for this identity: created, ineffective, deleted and verified.
* Attempt 2 run inside ca-cutover-test-demo-api via az containerapp exec: 12 calls, completed. Temp files removed. No resource created, no network or Key Vault change. Credentials files not read.

## Per-criterion table
| # | Criterion | Status |
| --- | --- | --- |
| 1, 2, 7 | Ticked earlier | Not re-proven here |
| 3, 4, 6, 9 | Ticked earlier | Not re-proven; 3 and 4 partly exercised, no cost per accepted proposal stated |
| 5 | Billing reconciliation | Unproven, owner waiver for demo |
| 8 | Measured batch with spend authority | Proven for synthetic demo (12 proposals, 180 to 225 tokens, 2,522 total, USD 0.000744 list price); not for real held-out cases |

## Validation
* Existing tests: test_heldout_batch, test_heldout_aoai, test_heldout_freeze: 69 OK (src/agents).
* Secret scan of new files: clean. Link check of the note: relative targets exist.
* Not run: mypy/ruff (no Python changed), hosted CI, independent review.
