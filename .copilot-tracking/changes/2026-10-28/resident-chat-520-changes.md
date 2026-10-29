---
title: Resident chat 520 implementation evidence
description: Changes, validation and publication boundaries
ms.date: 2026-10-28
---

## Scope and Status

Full plan resident-chat-520, task 520. Implementation active, P01 first.
All PC-001..006 direct corrections are part of the current plan; original
critique Revise is preserved. No Azure deployment or model calls authorized.

## Changes and Validation

P01/P02 and P03-T01 implemented. Persistent explicit SQLite callback inventory,
atomic proposals/book/cancel and local assisted-cancel CLI; own-record host
chat routing with data-use checks before lookups, dated regulatory explanation,
preserved bounded Azure advisor; shared global launcher/window with session
generation isolation; automatic appointment search from chat and independent
manual form with explicit booking/cancel confirmation.

Isolated `/tmp/ama-520-venv` pip environment installed
after default Python failed to import the project. No private data was read.

Initial focused units: 43 passed. API Ruff and mypy: passed after correcting
line wrapping; Node syntax: passed. Initial loopback Playwright: passed.
Pinned axe SHA-256 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb
verified; initial rendered chat/callback scan passed with no violations.
External evidence: `/tmp/ama-520-browser-axe/`.
Full API discovery: `PYTHONDONTWRITEBYTECODE=1
PYTHONPATH=tests:../core/tests:../agents/tests /tmp/ama-520-venv/bin/python -m
unittest discover -s tests -q` from src/api: 1160 tests, 425.005 seconds, OK
(314 opt-in/general-discovery skips). These skips are not SQL integration
evidence; the complete exact-head gate must execute required SQL selectors.
Full discovery/browser command exit 0. External stdout:
`/tmp/1793202348707-copilot-tool-output-3976463-fc2d3523-88c8-489b-bd6d-e4dc40c91443.txt`.
After the final confirmation-time refinement, focused five-module rerun:
45 tests, 11.699 seconds, OK, exit 0.
Final browser: `python -m checks.resident_assistant_browser_check
--axe /tmp/ama-520-axe-4.10.3.min.js --out /tmp/ama-520-browser-reviewed`;
Chromium 156.0.8078.4, 16 axe states, zero violations, exit 0. Includes
pointer/touch, keyboard, 200% root text, 400%-equivalent reflow, automatic
search and independent manual book/cancel, delayed responses/session loss,
network/HTTP errors, server UK dates in a New York browser, no external page
requests or script errors. Native browser zoom and actual AT remain Not run.
Final API Ruff check/format, mypy (94 source files), Node syntax for both JS
assets and git diff --check: all exit 0.

The official Safety and Quality Standard page was successfully retrieved at
the corrected URL on 2026-10-28. Selected 2.3.1..2.3.3 provisions match the
local copy; source metadata and API README record that bounded comparison.
This does not validate the currentness/applicability of the wider legal corpus.

Refreshed Web Interface Guidelines fetched before changed-web review.
Existing local ASCII/sentence-case content rules override the external smart
punctuation/title-case preferences. Optional chat text is deliberately transient,
not URL-persisted or saved as a draft. No framework/style overhaul was performed.

## Amendments and Divergences

No material divergence. Synthetic callbacks are not works appointments and
operational appointment/consent records remain unavailable.
Ordinary local judgment: recheck the callback start against the clock after
the fresh authorization check within the reservation transaction; a regression
proves that a slot becoming past during confirmation rolls back.
The pre-existing visible "AI unavailable" and unqualified appointment-change
claims were corrected only on resident_demo, preserving the shared preview.

## Changed-web guideline review

Source refreshed 2026-10-28 before reading all changed web assets.

### src/api/src/zava_forward/api/resident_demo/web/assistant.js

Pass within changed scope. Native controls/labels, transient bounded transcript,
generation guards, status/log semantics, consent error associations, separate
booking/cancel confirmation and Intl UK dates retained.

### src/api/src/zava_forward/api/resident_demo/web/demo.js

Pass within changed scope. One page-level mount, session/error teardown,
manual callback surface and corrected synthetic-only wording.

### src/api/src/zava_forward/api/resident_demo/web/demo.css

Pass within changed scope. Fluent-derived tokens, safe areas, contained scrolling,
native focus, tap handling and reduced motion. Existing unrelated styles were
not audited as a whole-product conformance assessment.

### src/api/src/zava_forward/api/resident_demo/web/index.html

Pass within changed scope. Read-only home/works distinguished from synthetic
callback actions; existing language/zoom/skip-link semantics preserved.

## Acceptance and Remaining Work

Human resident/content and assistive-technology acceptance Not run.
Regulatory currentness unverified (official attempted URL returned 404).
Full gate and independent exact-head assessment remain required before push.
Review readiness: P01/P02 and P03-T01/T02 complete. README/evidence portion of
P03-T03 complete; independent original Review is next. P03-T04 remains pending,
not implied by targeted tests. No source correction after Review is planned.

## Original independent Review and publication handoff

The original Review has completed its source/artifact assessment with execution
Partial and outcome Residual work. No material runtime defect was found.
RV-001 Low identifies the stale remaining-work summary above; it is routed to
later documentation work and intentionally not corrected in this completed
RPI task. The original reviewer did not inspect the external raw browser/stdout
files, so their independent inspection remains required at exact-head assessment.
Original Review: .copilot-tracking/reviews/logs/2026-10-28/resident-chat-520-review.md.
No second original Review or critique will be run.

Publication P03-T04 is still pending. Planned full gate output:
`/tmp/ama-520-rpi-final-20261028-1/receipt.json`, authoritative external evidence,
not a committed receipt. Commit implementation plus original dated evidence,
fetch main, run `python3 tools/rpi-checks.py --all --jobs 3 --lock-timeout 0
--base <fetched-origin-main> --out /tmp/ama-520-rpi-final-20261028-1`.
Then fetch again, verify the full receipt against current origin/main, obtain
the independent external exact-head assessment with access to raw evidence,
verify again immediately before push and create the Refs #520 PR. Missing
prerequisites, lock contention, changed candidate/base/inputs or failed receipt
block publication; no cloud fallback, deployment, force-push or gate bypass.
The pending gate cannot be marked complete in a commit that precedes its run.
