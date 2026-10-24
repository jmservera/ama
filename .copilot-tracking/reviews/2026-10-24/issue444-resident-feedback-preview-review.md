# Issue 444 post-implementation review

Date: 2026-10-24. Executed once by an independent code-review agent (read-only, did not run tests).

## Outcome

Conformant with follow-ups. Review executed: yes. Assessed boundary: uncommitted working tree on base f1e2d830.

## Findings

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Medium | `appointment_status == "Offer"` also covers ended, paused, deferred, changed-binding and closed-case records, so dead offers were shown as live "Offered times". | Fixed in this task: offers are shown only when every missing item is a pending "confirmation missing"; otherwise the record is counted as unknown. Regression test `test_ended_or_paused_offer_is_not_shown_as_a_live_offer`. Core 31 tests, api 14 tests re-run and pass. |

## Areas found sound

* Server-owned identity; per-request default-deny grant, expiry and revocation.
* Exact loopback Host check and bind guard; env guard.
* Positive-allowlist projection; fixed static asset map; `textContent` only in resident.js.
* Writes 405, unavailable features 403, other routes 404.

## Routed follow-ups (not actioned here)

* Human screen-reader audit and accessibility harness (needs uv/npx).
* Live Azure, SQL and AI acceptance remains separate; issue #444 criteria needing live proof stay open.
