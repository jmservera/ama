# Plan critique: #107 SQL restart and independent-connection proof (0106)

Executed once by `rubber-duck` (independent). Verdict: Revise (2 blocking, 2 non-blocking). Dispositions applied directly.

* C1 blocking, authority change refills the pool (`ZF_ASSIST_AUTHORITY` keys `assistant_allowance`): accepted as a real, unresolved risk. Research claim narrowed to restart, reload and larger-env non-replenishment for an unchanged authority. Not fixed here because binding the pool to a release record is a design and authorisation decision beyond a surgical test-PR change; routed as follow-up 1. #107 criterion 8 is not claimed fully closed.
* C2 blocking, dispatch untested for suspension: accepted. Added `test_suspension_after_claim_stops_a_worker_paused_before_provider_dispatch` (worker paused after claim, suspension from another connection, zero provider calls, late result quarantined).
* C3 mismatch assertions weak: accepted. Each variation now asserts the release is `revoked` after a fresh store.
* C4 export assertion selected the wrong proposal: accepted. Now selected by proposal id.
