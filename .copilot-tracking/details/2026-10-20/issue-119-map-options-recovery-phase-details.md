<!-- markdownlint-disable-file -->

# Phase Details: issue-119-map-options-recovery

Plan: .copilot-tracking/plans/2026-10-20/issue-119-map-options-recovery-plan.md

## P01 Verify and correct the options document

* P01-T01: In the Option C cost cell of map-tile-provider-options.md, append that the same unverified secondary summary also cites a leisure-scale view rate of about GBP 0.000525, so the secondary figures are inconsistent and none is relied on. Evidence: recovery research W3.
* P01-T02: Re-read "Bounded options for owner review"; confirm no ranking, shortlist or fallback wording. Evidence: draft critique finding 2 already applied.
* P01-T03: grep the three docs for price, free, DPA, processor, screen reader, DPO; each must be labelled unverified/secondary or unmet as applicable.
* Done when: no vendor price or DPA position is presented as fact.

## P02 Append dated process clarifications

* P02-T01: Append a log.md entry dated 2026-10-20 noting the options doc and protocol were first drafted before the RPI skills ran and were then re-verified through recovery research, plan, critique, implement and review. Append-only.
* P02-T02: Append a short "Clarification 2026-10-20" section to each original issue-119-map-options-* markdown tracking artifact (research, plan, details, critique, changes, review), (original state JSON untouched; a separate recovery state file is created), stating they are pre-RPI unverified draft records, that the critique was a rubber-duck pass not rpi-plan-critique, and that the recovery artifacts supersede them for lifecycle evidence. No existing text is edited.
* Done when: originals still contain their prior content.

## P03 Validate and gate

* P03-T01: git diff --check; non-ASCII scan of added lines; `tests.test_accessibility_baseline` from src/api.
* P03-T02: commit with repo-local noreply identity and Co-authored-by trailer; fetch origin main; run tools/rpi-checks.py --all with a new external out directory; verify receipt. No later commits.

## P04 Budget wording correction (2026-10-20)

* P04-T01: replace the "costed plan before paid account" sentence in the cost method with the total-cap, accrued-and-forecast, multi-scope, no-spend and unknown-headroom-blocks wording.
* P04-T02: append a dated log entry; index needs no change (no file added or moved).
* P04-T03: reconcile plan, changes and state. Validation: git diff --check, ASCII scan. No heavy gate run here.
