<!-- markdownlint-disable-file -->

# Implementation Plan: issue-152-mobile-empty-c4-1110

| Field | Value |
|---|---|
| Task ID | issue-152-mobile-empty-c4-1110 |
| Research | .copilot-tracking/research/2026-11-10/issue-152-mobile-empty-c4-1110-research.md |
| Details | .copilot-tracking/details/2026-11-10/issue-152-mobile-empty-c4-1110-phase-details.md |
| Critique | .copilot-tracking/challenges/2026-11-10/issue-152-mobile-empty-c4-1110-critique.md |
| Changes | .copilot-tracking/changes/2026-11-10/issue-152-mobile-empty-c4-1110-changes.md |
| Tier | targeted DEMO |

## Executive Summary

C4 of 5 for #152 (`Refs #152`, 149). Extend the existing own-queue empty-explanation assertions in `workbench_browser_check.py` from 1280 px to 320, 390 and 1280 px on the same seven-role constructed data and routes, asserting real visibility, containment and wrapping, with a constructed negative proving a hidden narrow empty text is caught. Rebind the scenario-manifest recipe SHA and run the Core integrity tests.

## Requirements

* Only `src/api/checks/workbench_browser_check.py`, the manifest `recipe` SHA (existing mechanism: literal-byte digest checked by `scenario_manifest.py`), a dependent integrity fixture only if required, and a minimal README observation.
* No app.js, CSS, API, Core logic, roles, accounts or data; no sleeps, retries, hidden skips or catches; existing assertions, selectors and timeouts preserved.
* A real product defect means HOLD with evidence.

## Acceptance Criteria

* AC1: for each empty-queue role at 320, 390 and 1280 px: exactly one visible `li.empty` with the assigned-queue lead, "unknown", no "declared gap", inside the viewport, positive size, no element or page horizontal overflow; nonempty roles show none.
* AC2: constructed negative (test-page style hiding `li.empty` at 320) is reported by the helper; the helper is not weakened to pass.
* AC3: served harness exits 0 and prints all prior PASS lines plus the new ones.
* AC4: recipe SHA equals the file bytes; Core manifest, needs-inventory and generator-coverage tests pass.
* AC5: Ruff, format, strict mypy for src/api pass; impacted queue tests pass.
* AC6: no whole-152, AT, device or user claim.

## Phase Checklist

<!-- P01 -->
### [ ] P01: Extend, bind, validate

* [ ] P01-T01 Add the width-looped empty-state helper and negative in the harness.
* [ ] P01-T02 Rebind recipe SHA; README observation; log entry if the repository rule needs it.
* [ ] P01-T03 Own venv, pinned tools, run all targeted checks with raw output and exits.
* [ ] P01-T04 Review once, commit, witness, handoff.

## Critique Disposition

Critique executed once, verdict Revise, three findings applied directly.

| ID | Severity | Disposition |
|---|---|---|
| PC-001 | Medium | Applied: the negative restores the DOM and viewport and is asserted before later role checks run. |
| PC-002 | Low | Applied: lead text is asserted as the role-independent product sentence; role specificity comes from the manifest empty-ids roles, not invented copy. |
| PC-003 | Low | Applied: viewport restored to 1280 after the loop so later checks are unchanged. |

## Follow-Up Items

* One correction (C5) remains of five; not authorized or inferred.
* Coordinator: independent review, publication.
