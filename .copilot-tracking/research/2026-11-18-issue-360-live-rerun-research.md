# Research: issue 360 live re-run (2026-11-18)

Task: `issue-360-live`. Disposition: executed. Tier FOCUSED (no src change). Mode automatic.

## Scope

Re-verify direct Container Apps HTTPS ingress with Entra sign-in and no Front Door on the synthetic demo. Criteria c, d and e are unticked on issue 360.

## Existing evidence (read first)

* `docs/reference/research/direct-ingress-live-demo-2026-11-18.md` (08:36 to 08:42 UTC run): c and e unproven, d partly proven (browser-mode 401 fails, second role and restart persistence unproven).
* `docs/reference/research/entra-signin-live-demo-2026-11-18.md` (#349).
* Issue comments: no owner approval of the migration plan (c) or Front Door retirement (e) found by a keyword scan.

## Gap this run targets

1. Fresh live reconfirmation of environment, NSG, private backing services, Front Door absence.
2. Second identity (resident test account) against the staff API: role denial.
3. Per-replica persistence check if reachable without a drill.
4. Browser-mode anonymous denial re-measure.

## Planning Readiness

Ready. Evidence of this run goes to `.copilot-tracking/evidence/2026-11-18/issue-360-live-rerun/` and the research note under `docs/reference/research/`.
