<!-- markdownlint-disable-file -->
# RPI Plan Critique: Repair Account Photo Blob Rendering

## Metadata

* Task ID: zava-account-photo-rendering-2026-10-12
* Critique date: 2026-10-12
* Plan: .copilot-tracking/plans/2026-10-12/zava-account-photo-rendering-plan.md
* Phase details: .copilot-tracking/details/2026-10-12/zava-account-photo-rendering-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Owner-authorized necessary scoped repair
  of RV-001 (parent zava-workbench-entry-2026-10-12). Permit `blob:` in `img-src`
  only; keep default/script/frame/auth/token policy unchanged; cap at two new
  `test_auth.py` tests (CSP scope, authenticated binary MIME/no-store/no token
  exposure); rebuild/redeploy the API image only, without touching token-store,
  SQL, AI, or roles; repeat the real binary (public-logo) render and anonymous
  boundary checks. Real owner photo/consent acceptance is explicitly out of
  scope and not claimed.
* Research and evidence considered:
  .copilot-tracking/reviews/logs/2026-10-12/zava-workbench-entry-review.md
  (RV-001 finding), mvp/zavaforward_mvp/server.py (CSP construction, line 46;
  photo handler, lines 181-186; `_send`, lines 121-130), mvp/web/app.js
  (`URL.createObjectURL`, lines 83-124), mvp/zavaforward_mvp/profile.py
  (`own_photo`, lines 20-40), mvp/tests/test_auth.py (existing CSP exact-match
  test, lines 221-241), infra/modules/containerapps.bicep (container app image
  update surface).
* Decisions, dependencies, and acceptance criteria considered: Plan's
  Acceptance Criteria section (CSP/auth regression pass, full regression plus
  real image build/deploy, live public-logo Blob render success, anonymous
  200/API 401 boundaries); Test Ownership and Candidate Lock section (parent
  owns tests, no removals, max two additions); Follow-Up Items deferring RV-002
  to a separate owner-acceptance task.
* Assessment boundary: This critique can confirm the defect is real and
  reproducible from source (confirmed below) and assess whether the plan's
  fix scope, test cap, and deployment boundary are internally consistent and
  sufficient to close RV-001. It cannot verify live HTTPS behavior, the actual
  container rollout, or genuine owner photo/consent acceptance; those remain
  implementation-time and RV-002 concerns.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| RV-001 defect reproduction | Covered | server.py:46 `self.csp` has no `blob:` in img-src; app.js:122 uses `URL.createObjectURL`. Defect is real and precisely located. |
| P01-T01 CSP scope change | Partial | Phase details say "Add that source only to img-src," but do not address that `test_auth.py:236` already asserts an **exact** CSP string (`assertIn("img-src 'self' data: https://tiles.example.org;", csp)`) that will silently pass only if `blob:` is placed outside that substring, or will break if placed inside it. This existing-test impact is unaddressed. |
| P01-T01 test cap vs. existing test | Partial | "maximum two additions" is clear for new tests, but the existing exact-match CSP test very likely needs **modification** (not addition/removal) to keep accurately asserting the full img-src value. The Test Ownership/Candidate Lock section does not say modification of this existing assertion is permitted, creating ambiguity about whether an implementer may touch it. |
| P01-T01 token-exposure test | Covered | `_send` (server.py:121-130) applies `SECURITY` headers (Cache-Control: no-store) and the handler passes `kind` (image/png or image/jpeg) as content-type for `/api/account/photo`; verifying MIME/no-store/no-token-payload is a straightforward assertion against existing behavior. |
| P01-T02 rebuild/deploy API-image-only | Covered | infra/modules/containerapps.bicep exposes an image-level update surface consistent with an API-only redeploy that leaves SQL/AI/roles/token-store untouched. |
| P01-T02 live binary re-check | Covered | Plan explicitly repeats the real public-logo Blob load against the deployed CSP, directly closing the RV-001 reproduction loop. |
| Acceptance Criteria "existing self/data/map sources... unchanged" | Partial | True for default-src/frame-ancestors, but the exact ordering/format of the new `img-src` value is not specified (e.g., `blob:` before or after `data:`, before or after the optional tile host). Since one existing test performs exact substring matching on this value, order is not cosmetic here — it determines whether that test needs to change at all. |
| RV-002 exclusion | Covered | Phase details and plan both explicitly defer real owner acceptance; critique agrees this is correctly out of scope for this repair task. |

## Verdict

* Verdict: Revise
* Rationale: The core fix (add `blob:` to `img-src`) is correctly scoped, well-evidenced, and does not touch unrelated policy. However, the plan does not reconcile its fix with the pre-existing exact-match CSP assertion in `test_auth.py`, creating a near-certain regression break or an ambiguous "is this an allowed edit" question at implementation time, and the Test Ownership/Candidate Lock wording does not clearly authorize fixing that existing assertion. This is a small, direct planner correction, not a reason to block the repair.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Existing exact-match CSP test is not reconciled with the `blob:` addition

* Related IDs: P01-T01, Acceptance Criteria ("CSP regression... test pass"), Test Ownership and Candidate Lock.
* Evidence: mvp/tests/test_auth.py:236 — `self.assertIn("img-src 'self' data: https://tiles.example.org;", csp)`. mvp/zavaforward_mvp/server.py:46 builds `self.csp` as a single concatenated string that this test checks by exact substring.
* Concern: Adding `blob:` to `img-src` changes the exact string this existing test checks. Depending on where `blob:` is inserted, the existing assertion either (a) still passes because `blob:` was appended after the asserted substring, which under-tests the real production value, or (b) breaks because `blob:` was inserted before/inside the asserted substring. The phase details discuss only "two additions" and never mention this pre-existing assertion.
* Impact: An implementer following the phase details literally could either leave a stale/incomplete CSP assertion (false confidence) or encounter an unplanned test failure outside the "two addition" budget, with no guidance on whether editing that line is within the Candidate Lock.
* Smallest useful change: Add one sentence to P01-T01 phase details: specify the exact resulting `img-src` value (e.g., confirm `blob:` is appended after the tile host segment, or specify intended order) and explicitly state that updating the existing exact-match assertion in `test_auth.py:236` to include `blob:` is in-scope as a correction, not counted against the two-test addition cap.
* Action owner: Planning parent (direct correction to phase details).
* Exact resolving evidence: Updated P01-T01 phase detail text naming the exact `img-src` target string and explicitly permitting the existing assertion edit.
* Decision route: Direct planner correction — no divergent user decision needed; this is a clarifying detail consistent with the plan's existing intent, not a scope expansion.

## Strengths and Residual Risk

* The defect diagnosis is precise and independently verifiable from source: `self.csp` (server.py:46) omits `blob:`, and `app.js` (lines 83, 122-124) relies on `URL.createObjectURL`, which requires it. The plan's fix targets exactly this line.
* The non-functional boundary ("blob: allowed only for images; other directives unchanged") is consistent with the actual CSP construction, which is a single string with independent `default-src`/`frame-ancestors` segments not touched by an `img-src`-only edit.
* The token-exposure/no-store/MIME test is low-risk to add: it verifies existing `_send`/`own_photo` behavior rather than requiring new application logic.
* Residual risk (explicitly accepted by the plan, not a gap): RV-002 (real owner photo/consent/switch acceptance) remains unresolved and is correctly deferred to a separate follow-up; this critique does not treat that as blocking this repair.

## Questions or Blocking Evidence Gaps

* None. PC-001 is resolvable as a direct phase-detail clarification and does not require a user decision.

## Limitations

* This critique did not execute the test suite or a live HTTPS check; it relies on static reading of server.py, app.js, profile.py, and test_auth.py. Confirmation that the rebuilt image actually renders the public-logo Blob over real HTTPS remains an implementation-time verification step per the plan's own P01-T02 task, not something this critique can pre-validate.
* Container Apps image-update mechanics (infra/modules/containerapps.bicep) were confirmed to exist but were not traced in full to guarantee zero incidental change to SQL/AI/roles/token-store; this is consistent with the plan's stated intent but is an implementation-time check, not a planning gap.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: Planning parent
* Smallest next action: Add one sentence to P01-T01 in the phase details specifying the exact target `img-src` value and explicitly authorizing the existing `test_auth.py:236` assertion edit as in-scope (not counted against the two-addition cap), then proceed directly to rpi-implement.
* User response required: No — this is a direct planner correction fully resolvable from the supplied evidence.

## Related Artifacts

| Artifact | Description |
|---|---|
| [.copilot-tracking/plans/2026-10-12/zava-account-photo-rendering-plan.md](.copilot-tracking/plans/2026-10-12/zava-account-photo-rendering-plan.md) | Plan under critique |
| [.copilot-tracking/details/2026-10-12/zava-account-photo-rendering-phase-details.md](.copilot-tracking/details/2026-10-12/zava-account-photo-rendering-phase-details.md) | Phase details under critique |
| [.copilot-tracking/reviews/logs/2026-10-12/zava-workbench-entry-review.md](.copilot-tracking/reviews/logs/2026-10-12/zava-workbench-entry-review.md) | Parent Review with RV-001 finding driving this repair |
| [mvp/zavaforward_mvp/server.py](mvp/zavaforward_mvp/server.py) | CSP construction (line 46) and photo handler (lines 181-186) |
| [mvp/web/app.js](mvp/web/app.js) | `URL.createObjectURL` usage for the proxied photo (lines 83-124) |
| [mvp/tests/test_auth.py](mvp/tests/test_auth.py) | Existing exact-match CSP test requiring reconciliation (lines 221-241) |

## Next Steps

Planning parent applies the PC-001 direct correction to the phase details, then
proceeds to `/rpi-implement` for P01. No user response is required before
implementation.
