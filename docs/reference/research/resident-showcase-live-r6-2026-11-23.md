---
title: Resident Synthetic Showcase Live Check r6 (Issue #462)
description: Sixth live desktop check of the synthetic resident showcase on 2026-11-23 against revisions API 0000054 and resident 0000026, with a per-criterion proven/unproven table
ms.date: 2026-11-23
---

## Scope and limits

Session `rpi-462-live`, 2026-11-23, under the 2026-11-18 owner decisions: synthetic demo, desktop only, live Azure in resource group `ama`. Billing reconciliation, Legal/DPO approval and person-run assistive-technology testing are out of scope for the demo. No source, infrastructure or Azure resource was changed and no throwaway resource was created. This is not a security, identity or accessibility acceptance. It supplements the [r5 check](./resident-showcase-live-r5-2026-11-22.md).

Sign-in values were read at runtime from the owner file and never printed. Evidence is in `.copilot-tracking/evidence/2026-11-23-resident-showcase-live/` (`live_r6.py`, `live-checks.json`, `az-state.txt`, `resources.txt`, `headers.txt`, five desktop screenshots). The AI summary button was not pressed.

## Results

| Check | Result |
|-------|--------|
| Playwright run | "ok 36 checks", the same set as r5: CSRF and origin denial, generic 401 for wrong password and unknown email, forged cookie 401, case override attempts ignored, own-email-only projection, HttpOnly Secure SameSite=Strict cookie, write routes 405, sign-out then 401, rate limit 429 |
| Revisions | `ca-resident-demo--0000026` Running (min 1, max 1), digest `sha256:a71084bd...0445c5b`; `ca-cutover-test-demo-api--0000054` (min 1, max 4), digest `sha256:3f2be664...faf945` |
| Owned resources | `ca-resident-demo` and `id-resident-demo` in group `ama`; no `aoai-resident-*` account |
| HTTPS | Root returns 200 with `no-store`, CSP `default-src 'none'`, `x-frame-options: DENY`; no `Strict-Transport-Security` header |
| Dependencies | #444 closed; PR #455 merged 2026-10-25T21:25:42Z |

## Per-criterion result

| Criterion | Result | Basis |
|-----------|--------|-------|
| 1. RPI artifacts and threat model | Proven for the demo | Dated `.copilot-tracking/` artifacts for this run; [threat model](./resident-demo-threat-model-2026-11-16.md); the original October independent review is not re-derived |
| 2. #444/#455 and failed rubric resolved | Unproven | Dependencies are closed and merged, but the failed rubric run, the absence of manual score edits and unchanged-rerun fishing need hosted run history, unavailable without a push |
| 3, 4 (ticked) | Re-observed live | Playwright run above; domain and unit tests not re-run |
| 5 (ticked) | Not re-run | No source change |
| 6. Pre-spend record | Proven for the demo | Resources and stop plan in [r3](./resident-showcase-live-r3-2026-11-18.md); no fresh cost figure; the USD 700 owner decision supersedes the October cap |
| 7. Deployed showcase in a browser | Proven on the demo, desktop only | Playwright run above; "gates passed before deploy" not claimed |
| 8 (ticked) | Unchanged | Digests recorded; source commit behind them unconfirmed (private registry) |

No owner-gated item remains for the demo except criterion 2's hosted evidence, which needs a maintainer or a push.

## Observations

* No HSTS header on the resident app. The criterion asks for HTTPS-only session cookies, which are met (Secure flag, http redirects to https). Adding the header needs a `src` change and the full tier, so it is left as a follow-up.
* `minReplicas` 1 on both apps is a standing cost, as noted in r5.

No defect needing a source change was found. Issue #462 stays open. Refs #462.
