<!-- markdownlint-disable-file -->
# Changes: resident-showcase-azure-deploy-462 (2026-11-17)

Plan: .copilot-tracking/plans/2026-11-17/resident-showcase-azure-deploy-462-plan.md

## Admission (P01)

* RG `ama` ActualCost month-to-date USD 85.39 at about 18:05Z (RG-only, pre-tax, billing may lag). Cap USD 700.
* SQL `retrofit` Standard capacity 10 Online. Registry Premium, public Disabled, default Deny, exports disabled.
* Live app `--0000010`, min 0/max 1, 0.25 CPU/0.5 GiB, image digest 24a9cbe3.
* Finite plan: no new resource; one image-only revision; incremental estimate below USD 1; test window at most 30 minutes.
* Stop: registry state not restored, unexpected resource, min above 0, any SQL/secret/role/employee-app change.

## Execution log

* P02: local build `zava-resident-demo:488c5a0c8` (uid 10001), digest `sha256:f6ce2bde...ad28`. ACR window trapped; the trap
  removed rules via the wrong JSON field, reported RESTORE_MISMATCH, rule removed by hand, readback equal to prior state.
* P03: `az containerapp update` image-only; `--0000010` to `--0000011`; metadata diff showed only the image.
* P04: real-HTTPS Playwright run passed (login, correct synthetic home, generic denials, CSRF 403, forged 401, staff 404,
  sign-out 401). A first run exhausted the in-memory limiter (5 per source per 600 s) and was repeated after the window.
  Evidence: `.copilot-tracking/evidence/2026-11-17-resident-showcase-live/`. The account-menu screenshot showed the fake
  email and was deleted.
* P05: expiry `2028-01-01T00:00:00Z`; ingress external as before; min 0. Docs: infra/README.md, docs/reference/log.md.
* Validation tier FULL: not run here (coordinator runs `rpi-checks --all`). Documentation-only repository diff.
* Unmet: all-in cost forecast, whole-WCAG/human approval, mobile, #444/#455 rubric dependency criterion.
