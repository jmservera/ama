# Research: issue #219 RAI release record bound to task activation (2026-11-01)

Disposition: executed. Planning Readiness: Ready.

## Findings (repository evidence)

* The release-record mechanism is already delivered in `src/` (merged PRs #315, #504, #646, #658, #667): `src/core/src/zava_forward/core/rai_release.py` (pure contract, selection, `changed_triggers`), `assistant_release.py` (SQL admission, revocation on material change, audit event, denial with owner and manual route) and `assistants.py` (admission before every reactive, proactive and queued dispatch).
* Tests exist: `src/core/tests/test_rai_release.py`, `test_rai_release_invalidation.py`, `src/api/tests/test_assistant_release.py` (zero-call denials, proposal-only matching constructed renewal, every binding mismatch for reactive and proactive dispatch).
* AC1, AC2, AC4 are proven by constructed-fixture tests. AC3 is proven for constructed exercise records only; no actual approved evaluation evidence exists.
* AC5 (OQ-017): `OWNER` text and `AUTHORITY_GAP` state the gap generically in one sentence. The four authorities (release, residual-risk acceptance, suspension, restart) are not itemised, so a reader cannot see which role is unfilled.
* Issue status comment (2026-10-27) names remaining work: actual approved evidence and named OQ-017 holders. Both are owner/human decisions and cannot be supplied by code.

## Gap selected (tight scope)

Make the OQ-017 gap explicit per authority: add a pure, additive structure listing the four authority roles, each `holder: None`, status `gap`, with the OQ-017 reference, and attach it to denials. No new holders are invented.

## Constraints

* Source in `src/core`, tests in `src/core/tests`; no `mvp/` or `prototype/` code; pip only; no secrets.
* Additive denial key only, so existing consumers are unaffected.

## Not provable by this work

* Actual approved evaluation evidence and named live holders (human decisions). The PR must use `Refs #219`.

## Correction cycle evidence

`assistants.py:626` builds `release_denial` with `missing` only, so the universal claim was invalid; scoped in README.
