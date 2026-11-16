# Review: issue #1828 (single native execution plus one read-only code-review agent)

* Date: 2026-11-16; boundary: working-tree diff against main 18d3de459f20, one source file plus RPI records.
* Execution: done once. Outcome: conformant for the stated focused scope; low findings dispositioned below.
  This is a worker self-review, not the independent exact-head review that the coordinator must still obtain.

## Findings

1. Low: the 400 ms post-key hold is twice Leaflet's 200 ms debounce, so a key-triggered read later than 400 ms would
   be missed. Disposition: accepted limit. Key handlers in the app are synchronous (pan and zoom); the hold is
   recorded as a bounded observation, not proof of absence at any delay. Routed as optional follow-up, not blocking.
2. Low: `check_viewport_change_requests_map` restored the viewport outside `finally`. Fixed (restore in `finally`
   after the expect block, so the resize is observed before restoring); full check rerun: 330 PASS, 0 FAIL.
   The premise check depends on a 40 px width change producing a read; it did in every run (3 of 3 full runs).
3. Observation: the check restores the viewport after each step, and each restore leaves another pending debounced
   read that only the next `settle_map_reads` absorbs. Every later caller settles first; recorded as implicit
   ordering.

## Assessment

* Diagnosis supported by timing evidence: resize 5926 ms, fetch 6126 ms, first key 6135 ms in the failing probe; 3 of 6
  probes failed at base. The single unmodified base full run passed, so the original 131-pass failure was not
  reproduced by that run.
* Assertion text unchanged and strengthened; mutant delayed key read still fails.
* No app, permission, consent, SQL, deployment, dependency, workflow or gate-semantics change: FOCUSED tier holds.
* `style.css` and `case_journey_browser_check.py` untouched; no overlap with #1297.
* Web guidelines: source fetched (first 3000 characters only, truncated), no web source edited; no visual, Fluent 2,
  WCAG, keyboard or reduced-motion behaviour changed. No assistive-technology testing performed.

## Residuals and routing

* Independent exact-head review, hosted CI (does not run this harness), human acceptance: coordinator.
* Follow-up for the owner: the #440 IoT map checkpoint may rerun the map check; this is not live-gated #109 evidence.
* Later possible work: a Leaflet-aware wait hook exposed by the app is rejected here as an app change.
