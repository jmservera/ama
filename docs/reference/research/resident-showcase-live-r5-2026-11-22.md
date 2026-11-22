---
title: Resident Synthetic Showcase Live Check r5 (Issue #462)
description: Fifth live desktop check of the synthetic resident showcase on 2026-11-22 with a per-criterion proven/unproven table
ms.date: 2026-11-22
---

## Scope and limits

Session `rpi-462-live`, 2026-11-22, under the 2026-11-18 owner decisions: synthetic demo, desktop only, live Azure in resource group `ama`. Billing reconciliation, Legal/DPO approval and person-run assistive-technology testing are out of scope for the demo. No source, infrastructure or Azure resource was changed and no throwaway resource was created. This is not a security, identity or accessibility acceptance. It supplements the [r4 check](./resident-showcase-live-r4-2026-11-19.md).

Sign-in values were read at runtime from the owner file and never printed; the script asserts they appear in no retained output. Evidence is in `.copilot-tracking/evidence/2026-11-22-resident-showcase-live/` (`live-checks.json`, `live_r5.py`, five desktop screenshots). The AI summary button visible on the signed-in page was not pressed, to avoid an AI call.

## Results

| Check | Result |
|-------|--------|
| Playwright run (`live_r5.py`) | "ok 36 checks": CSRF and origin denial (403), identical generic 401 for wrong password and unknown email with no cookie set, forged cookie 401, case-override attempts via query and headers ignored, own-email-only projection, HttpOnly Secure SameSite=Strict session cookie (lifetime 1797 s), write routes 405 on GET, UI sign-out then 401, rate limit 401 x3 then 429 x5 |
| HTTPS | `http://` returns 301 to `https`; no `Strict-Transport-Security` header observed on `/demo/session` (the same as r4) |
| Staff routes | `/api/cases`, `/workbench`, `/api/staff`, `/admin`, `/demo/staff`, `/.env` all 404 |
| App state | `ca-resident-demo`, revision `--0000025` Running; image digest `sha256:e6b50684...906618` (changed since r4, r4 digest `65481780...`); `minReplicas` now 1 (was 0), so the cold start measured 0.1 s |
| Owned resources | `ca-resident-demo`, `id-resident-demo` in group `ama`; the `aoai-resident-469` account listed in r4 no longer appears in a read-only name search |
| Content | Banner and title state the showcase is synthetic and not live; signed-in page shows the matched synthetic home, timeline, documents, funding, help, sensors and "Not available in this showcase" |

## Per-criterion result

| Criterion | Result | Basis |
|-----------|--------|-------|
| 1. RPI artifacts and threat model | Proven for the demo | Dated `.copilot-tracking/` artifacts for this run; [threat model](./resident-demo-threat-model-2026-11-16.md); original October independent review not re-derived |
| 2. #444/#455 resolved, failed rubric resolved without edits | Unproven | Needs a hosted rubric run, thread state and proof that no manual score edit was made; none is available without a push |
| 3 (ticked) | Re-observed | Playwright run above; domain and unit tests not re-run |
| 4 (ticked) | Re-observed | Cookie flags, generic errors, rate limit and CSRF observed live; HSTS header absent |
| 5 (ticked) | Not re-run | No source change |
| 6. Pre-spend record | Proven for the demo | Resources and stop plan as in [r3](./resident-showcase-live-r3-2026-11-18.md); no fresh cost figure was queried; USD 700 owner decision supersedes the October cap |
| 7. Deployed showcase in a browser | Proven on the demo, desktop only | Playwright run above; "gates passed before deploy" not claimed |
| 8 (ticked) | Unchanged | Source commit behind the new digest not confirmed (private registry) |

## Not proven

* Criterion 2 completion needs a push or a maintainer.
* Fresh cost figure, source commit behind the digest, session expiry waited out, HSTS header, and the fate of `aoai-resident-469`.
* Scale change to `minReplicas` 1 means a standing cost; flagged for the owner, not changed.

No defect needing a source change was found. Issue #462 stays open. Refs #462.
