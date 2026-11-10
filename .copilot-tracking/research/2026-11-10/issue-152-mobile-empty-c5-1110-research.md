<!-- markdownlint-disable-file -->

# Research: issue-152-mobile-empty-c5-1110

* Task ID: issue-152-mobile-empty-c5-1110. Parent task: issue-152-mobile-empty-c4-1110. C5 of 5, last default; C1-C4 spent. Refs #152 and 149 only.
* Research disposition: executed (reproduction) plus reused (C4 records, independent finding). Planning Readiness: Ready.
* Branch test/demo-mobile-queue-empty-152-c4-1110 at 093714958f9f6668b06237c0b802d3d5d9097ffd; declared parent 149 remote 7dffb674; no retarget, rebase or main adoption.

## Evidence

* Independent finding (ROOT/independent-152-mobile-empty-c4-1110/functional-findings.json, Medium): `own_queue_empty_failures` checks `is_visible`, positive bounding box, horizontal scroll only, so vertically clipped text passes. Static counterexample, not a product bug.
* Red-before (original, 2026-11-10T11:41:24Z, /tmp/c5-red-probe.py, outputs /tmp/c5-red.out and /tmp/c5-red.err, exit 0): at 320 px, first empty-queue role, baseline failures `[]`; after test-page mutation `height:12px; overflow:hidden` on `li.empty`, geometry `[clientHeight 32, scrollHeight 224, rect height 34]` and the unchanged C4 observer returned `[]`. The probe printed `PASS RED-BEFORE: C4 observer accepts clipped explanation (false pass)`. That PASS line records the false pass, not product health. Probe lives outside the tree.
* Role counts from workbench-manifest.json: 7 non-Contractor roles, 5 with empty own queues, 2 with populated queues. The C4 "21 role-width empty checks" wording is corrected: 21 role-width observations, of which 15 are empty-queue explanation observations and 6 are populated-queue no-explanation observations. Original C4 records stay unchanged.
* Web guidelines refetched 2026-11-10 (HTTP 200, 8055 bytes, identical to prior fetches). No UI change; harness only.

## Selected approach

Extend `own_queue_empty_failures` with vertical-clipping detection: the element's own `scrollHeight <= clientHeight + 1` and, for every ancestor below `body` that clips (overflow-y not `visible`), the element's rect lies within the ancestor's client rect vertically. Page-level vertical scroll stays allowed (no one-viewport requirement). Add a second constructed negative (`height:12px; overflow:hidden`) that must fail with the clipping message, restoring the exact original inline `style` attribute in `finally`. Keep the display:none negative.

## Limits

Constructed test-page mutations only; no product defect reproduced; no device, assistive technology or user evidence.
