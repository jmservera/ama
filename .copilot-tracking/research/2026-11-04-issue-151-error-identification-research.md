# Research: issue 151 slice 2, error identification inventory

* Disposition: executed. Planning readiness: Ready.
* Merged evidence: #244 baseline, #427 contrast fix, #857 target size, #917 map tile note. Slice 1 review follow-up 2 was the form error audit.
* Finding: seven `setAttribute("aria-invalid", "true")` sites in `src/api/src/zava_forward/api/web/` (app.js, assistants.js, ops.js x3, panels.js, progress.js). Each links to a visible status or alert message through `aria-describedby`, set nearby or at field build time. CSS adds a border and warning glyph, so not colour-only.
* Unmet criteria: C1 owner decision, C2 full audit (reflow, zoom, rendered target size, screen-reader status messages), C4 manual runs, C5 human check of map list (#119).
* Tier: focused; no security, infrastructure, SQL or deployment change.
* Chosen slice: record the inventory, add a guard test, narrow gap G-4. Refs #151.
