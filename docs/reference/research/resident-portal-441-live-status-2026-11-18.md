---
title: Resident Portal Documentation Integration Status (Issue #441)
description: Live-demo assessment of the unticked #441 acceptance criterion, with the evidence checked and why it cannot be proven for the demo
ms.date: 2026-11-18
---

## Evidence limits

The test result below was observed during the run; raw output not retained. The BRD and PRD statements come from repository files read at the cited lines.

## Scope and limits

Documentation-only check of issue #441 on main `76d89fee2`, run under the owner decisions of 2026-11-18 (synthetic desktop demo; live Azure authorised; DPO/Legal approval, billing reconciliation and person-run assistive-technology testing not needed for the demo). No source, Azure resource or credential was touched.

## Criterion status

Eight of nine criteria are ticked in the issue and were not re-assessed. One is unticked.

| Criterion | Status | Basis |
|-----------|--------|-------|
| 5: requirements owner dispositions FR-044/AC-084 wording before publication; human review stays default and any exception inactive; unsigned status, quality findings, OD-52-55 and Not run criteria visible | Unproven | See below |

## Why criterion 5 cannot be proven for the demo

* The criterion is a named human decision, not a runtime behaviour. Browser or Azure evidence cannot satisfy it, so none was gathered.
* Present wording is consistent with the safe default: [BRD FR-044/AC-084](../../brds/agentic-retrofit-programme-brd.md) (line 1602) keep named per-output review normative with a routine exception only under RULE-028/FR-061, and BRD OD-53 (BRD line 2171) and PRD OQ-029 (PRD line 2969) stay OPEN with routine automation OFF.
* The owner direction of 2026-11-02, recorded in [the log](../log.md#2026-11-17-update--record-owner-fr-044ac-084-directions-in-brd-od-53-and-prd-oq-029-refs-441), approves the exception only in principle subject to named Legal/Compliance approval, and states that a synthetic demo display does not satisfy FR-044/AC-084.
* The 2026-11-18 decision that DPO/Legal approval is not needed for the demo does not name FR-044/AC-084, so it is not treated as the disposition. Ticking would require reading it as one, which the earlier direction rules out.
* `tools/test_resident_portal_docs.py` passes (2 tests), confirming the recorded directions are still present. Observed; raw output not retained.

## Smallest next step

The requirements owner confirms in the issue that the integrated wording makes per-message review normative now, with any routine exception inactive and subject to a later OD-53/RULE-020 approval. This is not a request to activate automation.

## Full nine-criterion audit (14:40 UTC recheck)

Commands run from the worktree at main `53282820f`: `python3 tools/test_resident_portal_docs.py` (2 tests, OK; observed, raw output not retained); `grep -c` of FR-053, FR-062, AC-104, AC-111, AC-126, AC-140 and OD-52 to OD-55 in the BRD and PRD (all present except AC-140 in the BRD, which is a PRD-only identifier); `git ls-files docs/adrs` (ADR 0001 to 0007 only); `grep` of PRD line 1358. No Azure, browser or credential action was needed because every criterion concerns document content or a human decision. Criteria 1 to 4 and 6 to 9 are ticked and were checked only for the document facts below; process evidence (worktree, hashes, overlaps, independent review) is historical and not re-run.

| Criterion | Status | Evidence in this recheck |
|-----------|--------|--------------------------|
| 1 genuine RPI loop, isolated worktree | Proven (historical) | `.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441*` records exist in the tree; not re-run |
| 2 identifiers and traceability | Proven | BRD and PRD contain FR-053 to FR-062, AC-104 to AC-126 and AC-111 to AC-140 ranges; the two-test check passes |
| 3 overlap inspection | Unproven today | Historical record only; no fresh PR/issue overlap check was run, none is needed for a docs-only local candidate |
| 4 prospective integration, memory untouched | Proven | BRD, PRD and addendum carry the amendments; `docs/reference/memory.md` unchanged in this run |
| 5 FR-044/AC-084 owner disposition | Unproven | Named human decision; 2026-11-02 direction says demo display does not satisfy it; OD-53 and OQ-029 stay OPEN |
| 6 Option B boundaries | Proven (text) | OD-53/RULE-028 wording keeps per-message review default; not behaviourally tested |
| 7 ADR registry resolved | Proven | `docs/adrs` holds 0001 to 0007 only; PRD line 1358 records the proposal as `id: null`, unregistered, registration UNMET; no guessed ID |
| 8 workload assumptions | Proven (text) | PRD and BRD keep 60,000 as homes, not accounts (BRD line 709, PRD lines 1074, 1598); net -1.594/14.74/94.333 figures present in BRD, PRD and addendum |
| 9 focused checks, no overclaim | Partly proven | Focused test passes; exact-head hosted gates and independent review of a published head do not exist for this unpublished local commit |

Unmet for the demo: criterion 5 (needs the requirements owner), criterion 3 recheck and criterion 9 hosted gates (need publication, which this run must not do).
