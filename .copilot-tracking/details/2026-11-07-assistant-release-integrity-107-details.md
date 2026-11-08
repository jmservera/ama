# Details: assistant release integrity regression (#107)

Plan: [plan](../plans/2026-11-07-assistant-release-integrity-107-plan.md).

## Phase 1: combined revocation/race/restart regression

File: `src/api/tests/test_assistant_release.py`, class `Release`. Add imports `threading` and `Assistants`.

Steps in the test:

1. Invoke and claim one proposal (consumes one finite call and a token reservation); record the allowance row.
2. Revoke the release through a separate store connection and service.
3. Release three threads together via a barrier; each opens its own SQL store and service (own connection) with a larger allowance and later expiry, then calls `execute` on the claimed proposal and `invoke` for a fresh one.
4. Assert every worker is denied (`False`, `disabled`) and the provider received zero calls.
5. Complete the original in-flight claim; assert it is quarantined with no output.
6. Restart a further service with enlarged configuration; assert denial, zero provider calls, release stays `revoked`, durable allowance caps unchanged (100 calls, 2000000 tokens), used calls unchanged, reserved tokens not above the prior value.

Success: test passes and the existing 45 release tests plus `test_assistants` and `test_continuity` stay green. No production code, schema, workflow or documentation behaviour changes.
