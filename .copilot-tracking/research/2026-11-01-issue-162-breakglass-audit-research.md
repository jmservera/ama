# Research: issue 162 administrator and break-glass audit (2026-11-01)

Research disposition: executed (code and docs read). Planning Readiness: Ready.

## Findings

* AC1 to AC5 are ticked and delivered in PR #286 (`src/core/.../chat_isolation.py`, `src/api/tests/test_chat_isolation.py`).
* AC6 is a conjunction: audited with purpose (engineering) and policy decided (human, BRD OD-46, owner with DPO).
* `ChatIsolation.break_glass` is default-deny (needs `CHAT_BREAKGLASS_REF` and a named role), metadata only, and audits granted attempts with purpose, policy ref, target and expiry.
* Gap: refused attempts audit the target and reason but not the (redacted) purpose, so a reviewer cannot see what an unauthorised requester claimed. The issue wording is "audited, with purpose".
* Gap: the policy options are not written down in a decision-ready form; `chat-memory-dpia.md` lists OD-46 only as an open item.
* Constraint: no human policy approval may be inferred, so AC6 stays unticked and the PR must use `Refs #162`.

## Scope for this slice

1. Record the redacted purpose on refused break-glass audit entries.
2. Extend the break-glass test to assert purpose, actor, target and policy ref on every audit entry.
3. Add a decision-ready OD-46 policy proposal (marked proposed, not approved) to the DPIA record, update the log and core README.
