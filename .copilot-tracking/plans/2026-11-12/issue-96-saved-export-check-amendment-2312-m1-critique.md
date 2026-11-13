---
title: Issue 96 saved export check M1 correction 2 independent critique
description: Independent critique of the M1 correction 2 plan, run in a separate agent context before any source change
ms.date: 2026-11-12
---

## Execution and verdict

Critique executed once by a separate `rubber-duck` agent context (not the author) against committed plan `6fdbc3c9f`, before any source change. The critic edited nothing and ran no repository writes. Verdict: Revise (two findings, both compatible with the coordinator direction; no user decision needed). The earlier author-only critique and Review of the original task and amendment 2255 are unchanged.

## Findings and dispositions

* CR-1 (Significant): passing `{}` for a malformed copy returns `Invalid` before the core loads the case and draft, so a digest-consistent mixed-id copy aimed at a missing or other-case draft changes from `Unavailable` to `Invalid`. Disposition: accept as a bounded, disclosed divergence. The coordinator direction is that malformed ids receive the existing `Invalid` through core handling. `Invalid` discloses less than `Unavailable` (nothing about the draft or case), the role and switch checks and the 400 draft-id mismatch still run first and the core still runs `forms._actor`, so a forbidden role stays 403. The old `Unavailable` answer for such a copy was incidental, not a documented control. Add tests that a malformed copy aimed at a missing draft and another case answers `Invalid` with no field details and no write, and document the ordering in the README.
* CR-2 (Moderate): the claim that every internal `TypeError` reaches 503 is too broad, because the frozen core catches `TypeError` itself around the digest and saved-row processing (a patched `_digest` raising `TypeError` still returns `Invalid`). Disposition: accept. Narrow the claim to faults that escape the core (such as `draft_export` and the comparison after it); state the core-internal handling as an existing frozen limit in the README, the changes record and the final Review request.

## Verified without a finding

For ordinary JSON bodies the critic found no further client-caused exception escaping the proposed guard (JSON object keys are strings, malformed issue ids are caught by the core, the remaining saved-body comparisons do not hash values). The all-integer control is discriminating, but its unguarded baseline is `Stale` when current fields exist, not `Current`; the test asserts `Invalid` and the plan wording is corrected here.

## Rejected

None.
