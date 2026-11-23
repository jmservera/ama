# Issue 2237 live review (2026-11-23)

Review executed once, after implementation. Boundary: working tree diff against `b11b8259bd` (4 source/test files, docs and tracking records).

Outcome: conformant for the local scope; no open material finding. Deployment and lock-holder identification are routed to later owner-selected work.

## Checks

* Scope matches the plan: a core helper, one API mapping, tests, evidence and documentation. No web UI file changed, so the web-UI test gates do not apply.
* Behaviour: only an unhandled GET or HEAD failure whose driver error carries the SQL 50002 text, before the response starts, becomes 503 with `Retry-After: 5`. During implementation the self-check found that a POST may follow a committed step, so POST was excluded; that restriction is in the final diff and recorded in the changes record. A POST lock timeout still answers 500 (not separately tested; residual risk recorded below).
* Security and privacy: the log line carries class, path, frame and cause marker only; the test asserts the secret in the exception text appears in neither body nor log.
* Audit control: the audit write still fails closed and is never skipped.
* Tests: the new 503 test fails without the server change (observed 500 and no header); helper tests cover true, chained and negative cases. Targeted suites pass; mypy `src/api` clean; `src/core` mypy shows the 3 pre-existing errors only (verified identical with changes stashed); ruff check and format pass.
* Evidence: log evidence files hold no credentials or e-mail addresses (searched for password, secret, token: none); every research claim cites a file in the evidence folder.
* Process: `implement-done` was witnessed before the final GET/HEAD restriction edit; the restriction was re-tested (10 API tests, mypy, ruff) afterwards.

## Residual risks and routed follow-ups

1. Lock holders unidentified; shorten write transactions or narrow the global lock (design change, later research).
2. The fix is not deployed; a live 503 path cannot be shown without a push and a deployment (owner-gated) and a lock held for over 15 s (no drills).
3. No dedicated test that a POST timeout keeps the 500 path (low value, logic is a single condition).

## Per-criterion outcome

Reproduce: proven historically, test-reproduced locally. Cause: proven (lock timeout), holder unproven. Fix with regression test: proven locally, not deployed. Live 200: proven on revision 0000054 for the Programme Manager account.
