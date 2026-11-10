<!-- markdownlint-disable-file -->

# Research: issue-152-mobile-empty-c4-1110

| Field | Value |
|---|---|
| Task ID | issue-152-mobile-empty-c4-1110 |
| Position | C4 of 5 for #152; C1-C3 spent, one remains afterward; no automatic C5. Launch recorded once by this task (witness seq 1, 2026-11-10T11:22:57Z) after a first invocation stopped on a wrong `--actor` value with no phase work |
| Branch | test/demo-mobile-queue-empty-152-c4-1110 at 7dffb674e15fa74d5f784a82e28ead867b547cec (declared parent 149) |
| Research disposition | executed (read-only) |
| Planning Readiness | Ready |

## Evidence

* `src/api/checks/workbench_browser_check.py` `run_browser` logs in each of the seven non-Contractor roles at a 1280 px viewport and, at one point, asserts `li.empty` presence and text ("unknown", no "declared gap") only at 1280 px. Reflow at 320/390/1280 is checked separately in other sections (queue reflow, issue 77 definitions). So the empty text at narrow widths is unobserved (C3 review RV-002).
* Manifest `src/api/checks/workbench-manifest.json`: roles with `ids: []` are the empty-queue cases (Retrofit Coordinator and others per C3: seven roles asserted).
* Product copy (`queueEmptyExplanation` in app.js) and style are out of scope and unchanged.
* `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json` source `recipe` binds the SHA-256 of the harness; Core `test_scenario_manifest`, `test_needs_inventory` and `test_generator_coverage` check integrity.
* `src/api/README.md` already holds the empty-state paragraph, the minimal home for an RV-002 observation update.

## Approach (chosen)

Add one helper in the existing harness that, for a logged-in page, sets the viewport to 320, 390 then 1280, awaits the `li.empty` locator, and returns failures: for empty-queue roles exactly one visible `li.empty`, contains the "No open cases are assigned to you" lead and "unknown", no "declared gap", bounding box inside the viewport with positive height, element not horizontally overflowing and the page not overflowing; for nonempty roles zero `li.empty`. The existing 1280 assertion is subsumed by the loop (1280 retained as last width, which also restores the original viewport). A constructed negative injects a test-side style that hides `li.empty` at 320 on one empty-queue role page and asserts the helper reports it, then removes it. This mutation is in the test page only; it is not a product bug and does not touch the product or fixture.

Rejected: new checker or CLI; screenshots as proof; sleeps or retries; changing product copy or CSS.

## Scope and limits

Allowed: the harness, the manifest recipe SHA, a dependent integrity fixture only if required, a minimal README observation. Not allowed: app.js, CSS, API, Core logic, roles, data. A reproduced product defect means HOLD. Constructed widths do not prove whole 152 AC1/AC5, device, assistive-technology or user acceptance. `Refs #152`, 149 only.

Validation tier: targeted DEMO: served harness, Core integrity tests, impacted queue tests, pinned Ruff/format/mypy, Node only if relevant (not, since app.js is unchanged).
