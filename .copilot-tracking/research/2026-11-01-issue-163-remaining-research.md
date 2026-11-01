# Issue 163 remaining criteria research (2026-11-01)

Task: issue-163-remaining. Disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue #163 comments (closure audit batch 2, 2026-10-31): criteria 2 and 5 unmet.
* Merged PRs: #281 (DPIA working record, chat_privacy.py), #503 (hardening), #649 (provider position and DPO decision pack), #423 (private Blob transport, unrelated to provider handling). Open: #727 (DPIA record drift guard, tests only).
* `docs/reference/research/chat-memory-dpia.md`: lawful basis, staff notice, DPIA decision, retention references empty and owned by DPO and Legal; provider terms documented but acceptance, deployment type, abuse-monitoring choice and transfer position open.
* Local verification on this branch: `test_chat_*.py` in src/core, 74 tests OK; ruff check, ruff format --check and mypy clean for src/core.

## Criteria status

| # | Criterion | Status | Deliverable without owner approval |
| --- | --- | --- | --- |
| 1 | Data map | Proven (#281) | n/a |
| 2 | Lawful basis, notice, DPIA decision by DPO and Legal | Unmet, human decision | No |
| 3 | Rights requests locate and delete | Proven (#281, #503) | n/a |
| 4 | Logs and performance exclusion | Proven (#281, RULE-026) | n/a |
| 5 | Provider data handling and region position recorded | Unmet, needs DPO and Legal acceptance and live-resource confirmation | No |
| 6 | Free-text warning and redaction | Proven (chat_privacy.py, tests) | n/a |

## Conclusion

No further criterion is deliverable without owner or live-Azure approval. Recording a decision on behalf of the DPO would fabricate approval.
