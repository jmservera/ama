---
title: Resident-choice CSV feature-wave checkpoint plan critique (Refs #440)
description: One independent critique pass over the research, plan and details before Root admission
ms.date: 2026-11-11
---

## Execution

One read-only `rubber-duck` subagent pass (model `claude-sonnet-5.5`, launched with the rubric of the plan owner's constraints) over the research, plan and details. It ran no test and edited nothing; it read the pin tree and the saved candidate diff. Verdict: conformant after fixes (no blocking finding). No critique is repeated for this task.

## Findings and dispositions

| Id | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| CW-01 | medium | A second PRD (`proper-warm-retrofit-programme-demonstrator.md`, same `prd_id`, v0.13.0) reuses FR and AC numbers; the bare "PRD" label is ambiguous | Applied: research qualifies every id by path, version, status and blob and names the second PRD as not cited; details require this in the pack |
| CW-02 | medium | PRD FR-048 and AC-065 ask for a named update owner the CSV does not carry; the link is weak | Applied: marked partial, human to confirm, class capped at local observed (partial) |
| CW-03 | medium | Bare `env -i` omits `HOME`, so Chromium cache and `~/.zava-forward` assertions conflict | Applied: explicit allow-list including an owned or proven `HOME`, `PYTHONDONTWRITEBYTECODE=1` |
| CW-04 | low | No stop rule for `timeout` exit 124, crash, lock wait or red or pending hosted check on the merged head | Applied in the plan stop rules |
| CW-05 | low | `test_resident_choice_export` exists only after the merge | Applied: absent module is `not run`, cause recorded |
| CW-06 | low | Tree-equality gate assumes no other `docs` movement | Applied: any `src` or `docs` movement is recorded as main movement before the first test |
| CW-07 | low | Bytecode files may dirty the preflight | Covered by CW-03 |

Checked and found correct by the critique: pin identity; static counts (ResidentChoiceQueue 4, ResidentChoiceScreen 8 plus 1, RoleScreenConformance 11, RoleEndpointInventory 24, ListExportApi 11, CopyAudit 18, candidate export module 30 with 17 and 13); the four intake selectors including `JsonStaffIntakeApi` inheritance and the Mssql class being environment-gated; the story 232 invocation, `ZF_AXE_JS` skip behaviour, `ZF_BROWSER_SCRATCH` rule and absent self-lock; candidate versus main separation; boundaries; no invented marks or approvals.

## Limitations

The critic is the same model family as the author and read the artifacts and source, not a hosted or runtime result. It did not run any selector, so selector resolution and counts are static reads. The critique does not review PR 1435's merge, which has not happened.
