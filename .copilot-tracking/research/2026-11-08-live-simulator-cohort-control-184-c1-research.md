---
title: "Research: #184 correction 1 (ee2f review findings)"
ms.date: 2026-11-08
---

Disposition: executed (bounded; source evidence is the independent review
`functional-findings.json` of candidate `ee2f27d1`, tree `d411d02e`).

The original `ee2f` candidate, its adverse review and the C0 merge-before-plan
slip are preserved and not altered. Local `origin/main` is `c50e9f0b`; it differs
from the integrated `ecb28815` only in rubric data, so no merge was made.

## Findings and root causes

* F1 High: `live_simulator.run()` treated `COHORT_NOT_IN_STORE` as a transient
  store error and reused the old home list after the cohort changed.
* F2 High: no runnable receiver job, identity, routing-ready setting, command or
  mounted control path existed.
* F3 Medium: the receiver checked the control file only at window start, and
  rounded a sub-second remaining expiry up to one second.

## Environment finding

The installed editable `zava_forward` packages point at another checkout, so the
SQL check imported stale code (4 import errors at the first attempt, exit 1).
A throwaway venv under /tmp pointing at this worktree fixed the import path.
This is an environment matter, not a source defect.

Planning Readiness: Ready.
