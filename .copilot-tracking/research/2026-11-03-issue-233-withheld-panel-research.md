# Research: issue 233 atlas screens, withheld panel slice

Date: 2026-11-03. Disposition: executed. Planning Readiness: Ready.

## Already delivered (merged PRs, Refs 233)

* 671 trace doc and checker; 713 status refresh and drift check; 767 static
  role-screen guardrails; 496 workbench foundation; 785 and 777 added finance
  and resident service issue screens to the trace.
* Thirteen role screens are registered in `role-screens.js`; twelve are traced in the atlas trace.

## Acceptance criteria status before this slice

* Criterion 1 (perspectives and themes traced or deferred): traced in
  `docs/reference/research/ux/atlas-screen-trace.md`; the checker passes.
  Deferral of the rehearsal theme and stage 1 is owner-open, so not closed.
* Criterion 2 (tensions shown where designs resolve them): rule stated in the
  trace, but the "Not shown for this role" text was absent from screens and a
  test guarded only that gap. Smallest unmet slice.
* Criterion 3 (hypothesis labels): done.
* Criterion 4 (same-home walk): design-level walk only; EX-HOME-901 has no
  fixture or screen. Unmet.
* Criterion 5 (WCAG 2.2): static checks only; AT and human review open. Unmet.
* Criterion 6 (design system, no simulator): static class check only. Unmet.

## Selected slice

Add a read-only withheld-items panel to `programme-queue` and `resident-choice`
(the two screens named for the continuity versus disclosure tension). Stacked
later slices: EX-HOME-901 fixture (needs owner decision on synthetic data),
rendered keyboard/AT checks, #155 validation.
