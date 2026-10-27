---
title: Technical and quality screen 231 evidence
description: Separate professional reviews and positive per-measure QA evidence
ms.date: 2026-10-27
---

Refs #231. P02-T02, task 149. Independent feat/role-screen-231 from 950bf2e6,
target feat/role-screens-149. Parent canonical RPI evidence inherited.

Read-only home/document/design evidence, four separate technical reviews,
current-version mismatch warnings and missing references with competent role/
proposed named reviewer routing (not an appointment). Per-measure positive
quality evidence, version/checklist/source, return reason/defect owner and
correction/reinspection/handover remain distinct. Missing/stale evidence cannot
show readiness. No sign-off, inspection, acceptance or handover write.

## Validation

27 focused API tests passed (test_workbench, test_role_screens, test_workflows).
Chromium selector 231 and existing workbench browser passed; native keyboard,
320/390/1280 reflow, reduced motion, no POST, denied/expired/empty/failed/late
response boundaries passed. JS syntax, Ruff and mypy (three new Python files)
passed. External 231-unit.log, 231-browser-passed.log and 231-workbench.log
under /tmp/ama-role-screens-149-20261027-evidence retain execution evidence.

Initial exact-text checks failed because offscreen content-visibility sections
had not painted; a subsequent case-insensitive locator selected a different
lowercase label. Original failures are retained, not relabelled passes.
The final check scrolls each case-sensitive matching field and waits for its
actual innerText before asserting visibility; no DOM/style changes or hidden
text proxy. Same constructed ZF-1 explicitly has
stale design review, returned loft evidence, photo reference and named defect
owner. This is a declared child-fixture extension, not a lifecycle claim or
changed original. Professional appointment, physical inspection, human/WCAG
and integrated acceptance remain unproven; issue criteria unchanged.
