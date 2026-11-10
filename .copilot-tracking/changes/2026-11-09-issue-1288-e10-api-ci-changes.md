---
title: Issue 1288 E10 API CI failures changes and review
ms.date: 2026-11-09
---

# Issue 1288 E10 changes and review

## Changes

* `src/api/tests/test_case_journey.py`: the structure pin now reads `[assistantPanel, simulationPanel(), chatPanel,` (matches `app.js:1063`; the Quality simulation panel is intentional). The behavioral Node script proving successful-only clearing of unchanged raw questions for both chat submissions is untouched and passes. Line wrapped by `ruff format`.
* `src/api/src/zava_forward/api/web/assistants.js:26`: "still holds" becomes "still includes"; meaning, states, controls and manual guidance unchanged. `checks/quality_sensors_browser_check.py` asserts the same phrase and was updated identically.
* `src/api/tests/test_content_standard.py`: after the first fix a second pre-existing masked violation set appeared. CI stopped at the first violating file (assistants.js), so ops.js lines 48, 54, 83 were hidden. They use the JSON key `v.provenance` as an identifier, not visible copy, and are candidate-introduced (`ops.js` Quality sensor panel). `v.provenance` is added to the exact-identifier `ALLOWED` list, following the `p.provenance` and `earlier.provenance` precedent, and to the adjacent-bad-copy identifier test so bad copy beside it is still caught. No visible text change. Reviewer to confirm this allowlist extension is acceptable versus renaming the key.

## Evidence (existing `.venv-1288`, from `src/api`)

* Red before edit: both named tests failed (`logs-1288-e10/red.log`).
* Green after: `test_case_journey` 31 OK, `test_content_standard` 18 OK, `ruff check .` 0, `ruff format --check .` 0, `mypy` 0 (211 files), `node --check assistants.js` 0.
* Browser: E9-corrected Quality check with local axe 4.10.3, one non-queued `flock -n` admission acquired, exit 0, 30 checks passed (same 30 as E9).
* Not run: Core, Agents, full API, SQL, model, cloud.

## Web Guidelines review (fresh fetch of the owner-specified command.md)

* `assistants.js:26` pass: copy-only change in an existing aria-live status region, active plain wording, no markup, control, motion or focus change.
* No claim of AT or conformance acceptance.

## Arithmetic supersession

Inherited "861" and "761 non-skipped" claims (E8, E9 prose included) are superseded without rewriting originals: `verified-1288-main-integration-counts.json` has 19 per-log rows, Core 231 + API 471 + infra 59 = 761 discovered, 100 skipped, 661 non-skipped. Agents 303 and E9/E10 browser 30 are separate counts, not a deduplicated total.

## Counters

E1-E10 spent; authorization exhausted. Real-provider route OFF; ordinary post-fence, local-only cancellation and final-head SQL audit limits unchanged. Whole #1288 open.
