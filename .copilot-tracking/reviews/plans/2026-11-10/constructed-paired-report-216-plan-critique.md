---
title: Plan critique - constructed paired observations in the regulatory gate report (Refs #216, #208)
description: Single critique pass of the final plan candidate; findings and direct dispositions
ms.date: 2026-11-10
---

## Execution

Executed once, by the implementing agent against the plan and details of the same task (no nested agent). It is a self-critique and so weaker than an independent critique; independent review remains with the coordinator. No user decision conflicts with any finding.

## Findings and dispositions

| # | Finding | Severity | Disposition |
| --- | --- | --- | --- |
| 1 | The scorer would echo `participant` and `task` into `unpaired` and `failed_case_ids`. Free text could carry names or emails into a report that may be recorded. | Significant | Applied: participant and task must match `^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$` (pseudonymous identifier shape, no spaces or `@`). README tells callers to supply pseudonyms. The pattern cannot prove pseudonymity; the qualification says so. |
| 2 | `Path.open` on a FIFO or device could block or stream. The bounded read protects memory but not blocking. | Moderate | Applied: refuse anything that is not a regular file before reading; keep the `MAX_BYTES + 1` bounded read. |
| 3 | Qualification wording must not claim synthetic origin either; the brief says provenance is caller-declared, not proof of human or synthetic origin. | Moderate | Applied: wording says caller-declared constructed data, independent human participation and synthetic origin both unverified. |
| 4 | `runpy` isolation test patching `subprocess.Popen` may break if the fixture legitimately uses it. | Low | Kept; if the unpatched run already depends on it the test will fail visibly and the finding is recorded, not hidden. |
| 5 | Invalid rows would otherwise land in the scorer's `invalid_observations` as a success-shaped result. | Moderate | Already planned (validate and refuse first). Noted in README that `invalid_observations` is therefore always empty for this command. |
| 6 | `--record` could overwrite the canonical results with constructed content. | Moderate | Kept as documented, owner-approved semantics (no new write rule); tests use temporary destinations only. Residual risk recorded for Review. |
| 7 | Scope drift risk: a new helper module or shared validator. | Low | Rejected; logic stays in the one existing script. |

## Verdict

Proceed. Findings 1 to 3 are compatible with the confirmed brief and applied directly to the plan and details; no re-critique. Verdict recorded as `proceed-with-amendments`.
