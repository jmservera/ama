---
title: Resident Synthetic Showcase Live Check r4 (Issue #462)
description: Fourth live desktop check of the synthetic resident showcase on 2026-11-19, with the code-level proof for the open PR 455 review thread and a per-criterion proven/unproven table
ms.date: 2026-11-19
---

## Scope and limits

Session `rpi-462-live`, 2026-11-19, under the 2026-11-18 owner decisions: synthetic demo, desktop only, live Azure in resource group `ama`. Billing reconciliation, Legal/DPO approval and person-run assistive-technology testing are out of scope for the demo. No source, infrastructure or Azure resource was changed and no throwaway resource was created. This is not a security, identity or accessibility acceptance. It supplements the [r3 check](./resident-showcase-live-r3-2026-11-18.md).

Sign-in values were read at runtime from the owner files and never printed; the script asserts they appear in no retained output. Evidence is in `.copilot-tracking/evidence/2026-11-19-resident-showcase-live/` (`live-checks.json`, `live_r4.py`, five desktop screenshots).

## Results

| Check | Result |
|-------|--------|
| Playwright run (`live_r4.py`) | "ok 36 checks": the same 36 checks as r3 (CSRF and origin denial, generic 401 for wrong password and unknown email, forged cookie, case binding, projection canary terms, cookie flags, write routes by GET, sign-out, rate limit) all passed |
| App state | `ca-resident-demo`, latest revision `ca-resident-demo--0000014` Running; image digest `sha256:65481780...bbbd19` unchanged since r3; `minReplicas` 0 |
| Probes | `/` 200; `/api/cases` and `/workbench` 404; `/demo/view` unsigned 401 |
| Owned resources | `ca-resident-demo`, `id-resident-demo`, `aoai-resident-469` in group `ama` (read-only listing) |
| Fixture-identifier thread | The unresolved PR 455 thread `discussion_r4372517587` asks that missing or null fixture identifiers be rejected. `resident_preview.py` now checks `_usable_id(dataset_marker.get("fixture_id"))` before comparing, and `test_refuses_missing_null_or_blank_fixture_identifiers` exists; `python3 -m unittest discover -s tests -p "test_resident_preview*.py"` in `src/core` ran 37 tests, OK |

## Per-criterion result

| Criterion | Result | Basis |
|-----------|--------|-------|
| 1. RPI artifacts and threat model | Proven for the demo | Dated `.copilot-tracking/` artifacts for this run; [threat model](./resident-demo-threat-model-2026-11-16.md) and [update](./resident-demo-threat-model-update-2026-11-17.md); original October independent review not re-derived |
| 2. #444/#455 resolved, failed rubric resolved without edits | Unmet | Closed and merged (r3); the code fix behind the open review thread is now verified by test, but the thread itself is not marked resolved, no hosted rubric run is possible without a push, and absence of manual score edits is not provable locally |
| 3, 4 (ticked) | Re-observed | Playwright run above |
| 5 (ticked) | Not re-run | No source change |
| 6. Pre-spend record | Proven for the demo | Resources, scale-to-zero and stop plan as in [r3](./resident-showcase-live-r3-2026-11-18.md); cost query not repeated, so no fresh figure; the October USD 50 cap is superseded by the USD 700 owner decision |
| 7. Deployed showcase in a browser | Proven on the demo, desktop only | Playwright run above; "gates passed before deploy" not claimed |
| 8 (ticked) | Unchanged | Source commit behind the digest stays unconfirmed (private registry) |

## Not proven

* Criterion 2 completion: thread resolution, hosted rubric run and manual-edit absence need a push or a maintainer.
* Fresh cost figure, source commit behind the digest, session expiry waited out.

Issue #462 stays open. Refs #462.
