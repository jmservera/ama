# Research: issue 435 pitch preparation, live demo pass 3 (2026-11-18)

Status: opened. Disposition: executed (earlier passes r1 and r2 reused as input, not as proof). Planning Readiness: pending.

Task: audit the unticked criteria 1, 2 and 4 of #435 (3, 5 and 6 are ticked in the issue) against `docs/capstone`, with retained evidence this time. Synthetic demo, desktop only, no deck change.

Earlier notes in `docs/reference/research/` (`tokenomics-pitch-criteria-435-live-2026-11-18.md` and `capstone-pitch-435-live-2026-11-18.md`) kept their deck and Azure observations without raw output; this pass retains them.

## Findings (retained evidence)

Evidence folder: `docs/reference/research/evaluation/pitch-435-live-r3-2026-11-18/`.

* Deck, `deck-inspection.txt` (python-pptx, sha256 949e2077...fa7fca): 55 slides; slide 22 (S18) carries the USD 0.44 per home planning scenario with its E21 caveat; slide 53 (B25) carries "accepted-outcome TCA unknown"; slide 55 (B27) carries the bounded-call controls. This matches the owner placement decision of 2026-11-13, so criterion 1 needs no rebuild. The deck does not yet show the #432 measured figures.
* Batch, `report-live.json` and `authorization.json` under `evaluation/heldout-batch-432-live-2026-11-18/`: 12 calls, 2,522 tokens (882 input, 1,640 output), per-proposal totals 180 to 225, accrued USD 0.000744, label `measured held-out batch`, spend authority recorded (cap USD 0.50, 12 calls, expiry 2026-11-19). The 2026-11-13 decision authorised up to USD 5.00.
* Live check, `azure-readonly.txt`: `ca-cutover-test-demo-api` revision 0000031 Running, `ca-resident-demo` revision 0000012 Running, `evhns-cutover-test-demo` Active. Read-only; no credentials read; no resource created. No web file changed, so no Playwright proof applies (the criteria concern a PowerPoint deck and an owner/mentor process).
* Criterion 2 (mentor): no mentor record in the repository; only the owner report of 2026-10-22. Cannot be proven for the demo.
* Criterion 3 (ticked in the issue): `tokenomics-rehearsal-notes.md` and the placement draft say no performed timing is recorded. The tick conflicts with repository evidence; flagged, not resolved.

Disposition: executed. Planning Readiness: Ready.
