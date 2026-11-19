---
title: Rubric scoring failed on main, live run-history proof (issue 1397)
description: Read-only proof of the two open acceptance criteria of issue 1397 from retained run artifacts and run history
ms.date: 2026-11-18
---

Scope: diagnostic only, Refs #1397. No workflow, prompt, source or paid rerun. All evidence comes from
`gh run list`, `gh run view` and `gh run download` of run artifacts that are still inside retention
(retrieved 2026-11-18). Demo context: Azure, browser and credential tooling was not needed.

## Verdict

* Not still failing. The last key-set rejection is run 42838857558 (2026-11-10). On `main` the newest
  push runs of `rubric-score.lock.yml` are success (44255173449 at 2026-11-18T06:57Z, 44250964752,
  44212394914); `scores/latest.json` on `origin/main` records total 79 at `20f0b166`.
* Cause: the producer's first `record_rubric_score` call was a placeholder (`details` of `{}`); the second,
  complete call was refused by the safe-outputs handler, so the gate judged the placeholder and failed
  closed.
* Recent non-success `main` runs are unrelated: 44195260323 and 44194233506 failed in the `activation`
  job step "Restore daily AIC scan observations"; others are concurrency cancellations. None reached scoring.
* A run 44257460596 (pull request, branch `rubric/baseline-refresh`, "chore(rubric): record score 79/100")
  failed with no job log. It is not a `main` scoring rejection and was not investigated further.

## Criterion 2: classify the key-set rejection from the actual selected payload

Observed; raw output not retained. The artifact `agent` of run 42838857558 holds `agent_output.json` (487 bytes), the finalised
safe-output set. Parsed values:

| Field | Value |
|-------|-------|
| items | 1, type `record_rubric_score` |
| `details` | the string `{}` (zero keys) |
| `summary` | `placeholder - will be replaced` |
| `errors` | `Line 2: Too many items of type 'record_rubric_score'. Maximum allowed: 1.` |

`safeoutputs.jsonl` of the same artifact holds two lines: line 1 the placeholder, line 2 a complete card
(20 `details` keys, a full summary). The handler refused line 2 against `max: 1`, so the selected
payload is the placeholder, no longer a deduction. The `safe-outputs-items` artifact holds only the
90-byte acknowledgement `{"type":"record_rubric_score","provider":"github",...}`, which does not carry
the card. Classification: valid fail-closed rejection (`details` missing all 20 registry IDs, none extra) of
invalid model input; not a gate, adapter or transport defect. Nothing was regraded and the later card was not substituted.

This resolves the README uncertainty "whether call 2 was refused or dropped": it was refused
at submission, consistent with the #1383 record. The prompt wording that the pinned handler does not
enforce a one-call quota is contradicted by this artifact; reconciling the prompt is a separate owner item.

## Criterion 4: actual source-bound recovery and baseline publication

Observed; raw output not retained, for content recovery and publication; a per-SHA score for `6cc59776` cannot exist.

* `6cc59776` (feat(core) Azure IoT Registry backend, #1393) is an ancestor of `eff05737`, and
  `11184719` (the consumed baseline) is an ancestor of `6cc59776`.
* Run 42841391974 (push, `eff05737`, success) `agent_output.json` holds 1 item, no errors, 20 `details`
  keys, and a summary that names `device_registry_azure.py` and the IoT Hub registry tests, i.e. the
  `6cc59776` solution-code changes. The diff scored was therefore the cumulative one from baseline `11184719`.
* PR #1398 merged 2026-11-10T15:16:43Z as `c66370042`; its `latest.json` records commit `eff05737`,
  that run URL, total 78 and a changed solution-code fingerprint.
* The README caveat that freshness was unknown is closed: the assessor reviewed the
  changed files rather than carrying forward.
* Retention gap closed for the future: successor runs now upload `safe-outputs-items`, but the gate
  `decision.json` is still not an artifact; the original gate output survives only in job logs.

## Per-criterion status

| Criterion | Status | Evidence |
|-----------|--------|----------|
| 1 Preserve attempt and identities | Proven earlier (PR #1408) | README lines 230-266 |
| 2 Classify rejection from actual payload | Observed; raw output not retained | run 42838857558 `agent_output.json` |
| 3 Recurrence, adverse evidence, limits | Proven earlier (PR #1408) | README lines 268-307 |
| 4 Source-bound recovery and publication | Observed; raw output not retained (cumulative-diff recovery) | run 42841391974, PR #1398 |

## Follow-up and limits

* The issue body edit (ticking 2 and 4) and closure are owner/coordinator actions after publication; none was done.
* Open design items, all needing workflow or prompt edits and the full tier: refuse placeholder `details`
  before append; reconcile the prompt quota statement; upload `decision.json`.
* Artifacts have 90-day retention; the original run's artifacts expire about 2026-02-08.
* Limits: no search for recurrence beyond #1383 and #1397; the failed refresh-PR run 44257460596 is unexplained.
