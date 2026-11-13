# Review: #435 held-out batch live adapter (1953)

Executed once after implementation: independent `code-review` and `hve-core-all:code-review-security` on the uncommitted diff. Outcome: approve with conditions; all material findings resolved in this task, none left open.

| ID | Finding | Disposition |
| --- | --- | --- |
| R1 (Medium, both) | Served-model `startswith` could pass a pricier model name | Fixed: exact name or `-YYYY-MM-DD` suffix; tests for `m-10`, `m-1-pro` |
| R2 (Medium, security) | Token could go to any Azure OpenAI resource | Fixed: authorization must carry `endpoint` and `deployment` equal to the CLI arguments, checked before the token fetch; tests |
| R3 (Low) | `$` regex accepted a trailing newline | Fixed: `fullmatch`; tests |
| R4 (Low) | Proxy env vars alter egress; token fetched before manifest/proposal gate | Proxy pinned off via `ProxyHandler({})`; token ordering accepted (no model call without gate) |
| R5 (Low) | Per-operation timeout, not wall-clock | Accepted residual: sequential calls, bounded by `max_calls` |
| R6 | `_load(authorization)` now precedes the not-configured exit | Accepted: unreadable authorization is an error either way |

Re-validation after fixes: 56 tests in `test_heldout_aoai` and `test_heldout_batch` OK, `heldout_aoai.py` 100% coverage, `ruff` and `mypy` clean, agents suite 430 OK before the fixes. Deferred follow-ups: durable spend ledger (P4), proposal content bound to freeze digest (P6).
