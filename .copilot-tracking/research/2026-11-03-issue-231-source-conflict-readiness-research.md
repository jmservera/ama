# Research: issue #231 slice 3, unresolved source conflicts and readiness

Disposition: executed (re-read issue, closure audit comment, screens, tests). Planning Readiness: Ready.

## Evidence

* The Technical queue and Quality queue exist (PR #656) with unit tests (`src/api/tests/test_technical_quality_screens.py`) and browser stories `231` and `231q` (PR #769). The closure audit comment on #231 predates and does not see them.
* Reading `technical-queue` in `src/api/src/zava_forward/api/web/role-screens.js`: the readiness reasons covered a missing design, missing references, and sign-offs not valid. A source-fact conflict with no recorded resolution (status "Unresolved" from `assetStatus`) was shown in the Source facts table but did not block "Recorded evidence is complete". The existing test `test_complete_evidence_shows_ready_text_and_no_controls` used an unresolved conflict and asserted readiness, so the gap was masked.
* Acceptance criterion 1 says missing or stale evidence cannot show readiness. An unresolved conflict between sources is unreconciled evidence.
* `docs/reference/research/ux/design-system.md` states Fluent runtime adoption is not complete, so criterion 5 cannot be proven.

## Scope

Make an unresolved source conflict a readiness blocker naming its owner; fix the test fixture to resolve the conflict by default; add a blocking test; extend browser story `231` and scroll panels into view so long text is read in full.

## Limits

Desk-based hypothesis, not observed behaviour. No staleness age threshold exists in the repository, so none is invented; "stale" is evidenced only by the reassessment state. No AT or WCAG conformance claim (#151, #155).
