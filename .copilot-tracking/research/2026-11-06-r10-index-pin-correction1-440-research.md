---
title: R10 index pin correction 1 research
description: Research for the first correction of the new R10 checkpoint batch, a one-character-class index pin typo
ms.date: 2026-11-06
---

## Identity and method

Task `440-r10-index-pin-correction1`, first correction of the NEW seventeenth (R10 design) checkpoint batch. It is not a further correction of the r58, correction 1, correction 2, post-integration batch or batch correction 1 cycles, and it does not backfill any earlier phase. Start HEAD `d8dd8c74c6fa92a25d5fbd3de3ddd294e8a85d21`, tree `1439b2b8df2118ec2276fa1dd23370376ec31f92`, ignored-inclusive status 0 lines at intake. The `rpi-research` skill body was loaded through the skill tool before this record. Posture focused, three inline waves, no worker. Documentation observation only: no test, SQL, browser, container, install, scanner, model or provider call.

Inputs read: the supplied root assessment `440-r10-root-assessment-r68.md` (coordinator session files) and the existing R10 index paragraph in `docs/reference/README.md`.

## Fresh pins (git fetch exit 0, native shell 14:17:11 to 14:17:12 UTC)

| Item | Identity |
| --- | --- |
| Governance `origin/feat/discovery-assurance-integration-123` | `119828353ccc1d678c1a4e9c1c67b621b0d263a0` (unchanged) |
| Main `origin/main` | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` (unchanged) |
| R10 design commit in `issue-144-queue-recovery` | `1e19209985d93e053dd449e873e792f214dd110c`, object type commit, resolved by `rev-parse` |
| Local `feat/infra-hosting-integration-136` | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` (`show-ref`), equal to main |

## Wave 1, wider

Candidate surfaces that could carry the wrong short pin: the README paragraph, the pack Seventeenth section, the log entry, and the seven new tracking records. Candidate fix shapes: edit the README in place, or additively qualify. Adjacent topics (136 topology, trace citations, state metadata) are in the root assessment as already correct or disclosed.

## Wave 2, deeper

* C1 `docs/reference/README.md:460`: the Seventeenth paragraph prints `1e199209` for the R10 design short pin. The exact pin is `1e19209985d93e053dd449e873e792f214dd110c`, whose first eight characters are `1e192099`.
* C2 `git grep -c "1e199209" HEAD -- docs .copilot-tracking` returns one file, the README, with one line. The pack and log use the exact or twelve-character pin, and none of the seven new tracking records contains the typo.
* C3 The README is a live index, not an append-only record; the owner and root direction is to correct only this index pin and record the correction in the append-only log, with no renumbering and no pack change.
* C4 The R10 state JSON and plan carry pending-style metadata from the original cycle (state `session_status` running as artifact metadata, plan markers). Root says qualify additively; the original records must not be rewritten. The new Changes record will carry this qualification.

## Wave 3, contrarian

* Alternative: leave the typo and rely on the correct pack and log pins. Rejected: the index is the discovery entry point and a wrong pin is a wrong identity in a published document; root classified it Low but publication-blocking for coherence.
* Alternative: also fix the older unresolved log anchor or other index text. Rejected: excluded by the brief as unrelated.
* Alternative: add a new pack section. Rejected: no new checkpoint or renumbering was requested; the log entry is the append-only record.
* Risk that another short-pin typo exists elsewhere: checked by the scoped grep above, which finds only the README line. A different wrong pin form would not be caught by that grep, so the focused checks will also verify the new pin against the exact commit id.
* Not established: any new runtime or design defect. Original High 1 and High 2 findings, R9 Revise, R10 independent status and every approval boundary are unchanged.

## Synthesis

* Accepted: replace `1e199209` with `1e192099` in the README paragraph only; append one focused log entry; add additive qualification of the old R10 state and plan metadata in the new Changes record only.
* Rejected: any pack, requirement, ADR, design or source edit; any renumbering; any rewrite of the 38 existing batch records.
* Deferred: eventual published 136 topology (unresolved, not an owner question); full critique-skill load for the earlier R10 critic (unverified, not invented here).

Research disposition: executed. Planning Readiness: Ready. Output mode: convergence on the one-pin correction.
