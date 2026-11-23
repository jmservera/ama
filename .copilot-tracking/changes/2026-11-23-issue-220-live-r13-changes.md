# Issue 220 r13 changes (2026-11-23)

Refs #220. Tier: focused; no `src` file changed. No Azure resource created or changed.

## Changes

* Added `docs/reference/research/issue-220-live-r13-key-variants-live-2026-11-23.md`.
* Added index line in `docs/reference/README.md` and a log entry in `docs/reference/log.md`.
* Added evidence `.copilot-tracking/evidence/2026-11-23/issue-220-live-r13/` (probe script, JSON and text output, revision name).

## Per-criterion result

| Criterion | Proven or unproven | Evidence and reason |
| --- | --- | --- |
| Digital and staff-recorded routes work on constructed challenges | Proven live (r11, 0000054); offline tests | Not re-run on 0000058 this run |
| Permitted AI, source and policy explanations, owner, next update and resolution visible | Proven live for owner, next update, route; resolution proven offline | r11; core and api tests |
| Only dependent proposals and reviews become stale | Proven offline only; live `dependent_review_versions` was empty | Tests |
| No consent, refusal, sanction, unrelated closure or hazard-clock change inferred | Proven live (r11); adverse inputs on 0000058 left protected hashes equal | `run1.json` |
| No retaliation, inferred refusal or delayed hazard response | Unproven as a whole. Proven for the constructed case and for five key variants (all HTTP 400). Behaviour over time and real hazard-response timing need production history, unavailable in the synthetic demo | `run1.json`; r11 |

The r12 guard hardening is committed in source but not deployed; the live route rejects the variants through its permitted-field list regardless. Deploying an image stays owner-gated.
