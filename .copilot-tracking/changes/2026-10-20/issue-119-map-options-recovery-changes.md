<!-- markdownlint-disable-file -->

# Changes: issue-119-map-options-recovery

Plan: .copilot-tracking/plans/2026-10-20/issue-119-map-options-recovery-plan.md
Execution: rpi-implement skill actually invoked in the coordinator-intervention continuation. Scope: full plan P01-P02 and P03-T01; P03-T02 (commit and gate) follows.

## P01 options document

* P01-T01: docs/reference/research/ux/map-tile-provider-options.md Option C cost cell now notes a second, inconsistent secondary OS rate (about GBP 0.000525 per leisure view) and that no secondary figure is relied on.
* P01-T02: bounded-options wording re-read; comparative only, no ranking, shortlist or fallback.
* P01-T03: audit of options doc, WCAG baseline and ADR 0002: prices and DPA positions are labelled secondary or unverified; screen-reader record is "Not run"; engineering evidence labelled not a screen-reader run; the DPO personal-data question is left open. No further edit needed.

## P02 clarifications

* P02-T01: appended a dated correction entry to docs/reference/log.md (append-only).
* P02-T02: appended a clarification section to the six original markdown tracking artifacts. Original JSON state untouched; recovery state is a separate file. Draft commit 69fa487a. An earlier full-gate runner (pids 1610738/1610739, out /tmp/ama-119-gate-yy1w/out) was started on that draft and was left running, not killed, as historical and not final evidence.

## Validation (P03-T01)

* git diff --check clean; no non-ASCII added lines.
* src/api tests.test_accessibility_baseline: 7 tests OK (static checks only).
* Procedural note: the log entry was appended with a shell heredoc rather than the edit tool; content is append-only and reviewable in the diff.

## Divergences and follow-ups

* No plan divergence. Follow-ups: human screen-reader run; owner-approved vendor term and price verification; owner provider decision.

## P04 budget wording correction (rpi-implement, 2026-10-20)

* Independent assessor returned Defects on e69a2ed5: the options doc called USD500 a monthly budget and gated only account creation. Corrected in docs/reference/research/ux/map-tile-provider-options.md (total October cap, accrued and forecast, across ama and other scopes, separate finite costed plan before any paid execution, no spend authorised, unknown headroom blocks).
* Appended a dated correction entry to docs/reference/log.md. Index unchanged.
* Original review, critique and adverse receipt preserved. The e69a2ed5 receipt is historical; the full gate is pending a fresh coordinator run on the new head.
* Not claimed: provider selection, purchase, Legal or DPO approval, UI change, screen-reader acceptance (not run); rates, terms and DPA unverified. Refs #119, not closing.
