---
title: Plan, #134 criterion 2 AC-034 to AC-043 disposition reconciliation
description: One-pass documentation plan to add a consolidated, document-qualified ten-row disposition to the existing profile review, with one index row and one log entry
ms.date: 2026-11-12
ms.topic: reference
---

## Identity

* task_id and task_slug `ac-dispositions-134-1112`; branch `docs/journey-ac-dispositions-134-1112`; PR target (declared, not opened) `feat/demo-ux-integration-1112`, local only, equal to `origin/main` `43b2187b9`.
* Research: [research](../../research/2026-11-12/ac-dispositions-134-1112-research.md). Planning Readiness Ready.
* Details: [details](../../details/2026-11-12/ac-dispositions-134-1112-details.md).

## Decisions carried from the task

* Documentation only; no source, test, tool or workflow change; the register in `src/core` is not edited and its conservative wording stays authoritative for the code check.
* Every observed Pass stays version and source qualified; no historical test is promoted to current execution; the only executions are the register check and 15 existing Core tests recorded in research.
* Disposition language (critique C-3 applied): each row states the register status as authoritative (partial or deferred), the specific unproven Given/When/Then clause, the work owner and a concrete resume check. The section never claims criterion 2 is met, never relabels `partial` as deferred, and says the engineering record is not owner-approved and does not accept an epic, approve a pivot or tick criterion 2; criterion 2 stays open until the owner decides.
* Added delta only (critique C-2 applied): owner, resume condition, candidate evidence for AC-035 and AC-038 not yet in the register, and the partial-versus-deferred reading. The pack tables already give most register statuses and are linked, not restated.
* No blanket deferral: each row says what is observed, what is unknown or not shown and what would resume it.
* No invented human owner or approval; human acceptance owner is stated as unassigned.

## Phases

| Phase | Work | Output |
| --- | --- | --- |
| 1 | Add one dated section "AC-034 to AC-043 disposition reconciliation (2026-11-12, Refs #134)" at the end of the existing cut-over evidence pack (critique C-1 applied: the pack, not the historical profile review, is the traceability home and already holds the per-checkpoint AC rows). Contents: identities, status key, ten-row table anchored to pack line ranges and file paths, what the section is not, remaining literal #134 criteria. The profile review is not edited. | evidence pack diff |
| 2 | Add one index paragraph in `docs/reference/README.md` after the post-153 checkpoint paragraph, same style, linking the new anchor. | README diff |
| 3 | Append one `update` entry to `docs/reference/log.md`. | log diff |
| 4 | Verify: relative links and anchors, ASCII, no em dash, no bolded-prefix list, diff review, `git diff --stat` only three docs plus tracking, no `src` change; mechanical check that each row's status equals the register output (critique C-8); grep that "approved", "accepted" and "pass" appear only negated or as limitation. | review evidence |

## Section design (phase 1)

* Identities row: PRD blob `c788b917`, version 0.21.0, `in-review`; main `43b2187b9`; register blob; the register check and 15 Core tests are recorded here only as register-integrity observation (critique C-6), never as row evidence.
* Status key: register status authoritative; Class vocabulary already used by the pack (local observed, implemented but unverified, blocked, unknown). No row is Pass.
* Table columns: AC and requirement, register status, qualified observed evidence with file or pack line anchor, unproven Given/When/Then clause, work owner, concrete resume check (critique C-7: name a check or lane per row).
* Candidate evidence for AC-035 and AC-038 is labelled "implemented, unverified", with the clause it relates to and the clause it does not (critique C-5; test at `test_resident_decisions.py:3544` is adjacent, not the rejected-handoff Given). The register is noted as not yet updated for it.
* Every figure carries an anchor or is dropped (critique C-4).
* Closing: remaining literal #134 criteria 1, 2, 5; criteria 3, 4, 6 already ticked and untouched. Updating the register source with owner and resume fields is a separately owner-admitted source slice.

## Risks and mitigations

* Over-claiming from candidate evidence: label implemented, unverified; cite only files and line ranges verified in research.
* Contradicting the register: state that the register is a source-owned conservative status and that updating it is outside this slice; list the delta as a follow-up.
* Duplicate documentation: the section links to the pack sections instead of copying their counts beyond one qualified figure per row.

## Follow-ups (ranked, evidence-grounded)

1. Independent exact-head review of this record.
2. Source slice, separately admitted by the owner, to update the register reasons and add owner and resume fields (needs source change; not admitted here).
3. Execute AC-034 reset and focus checks for all eleven profiles (needs a served browser lane and fresh admission).
