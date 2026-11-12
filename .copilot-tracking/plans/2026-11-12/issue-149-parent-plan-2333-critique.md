---
title: Issue 149 UX parent integration plan critique (2333)
description: One independent read-only critique of the prospective plan with verdict and dispositions
ms.date: 2026-11-12
---

## Execution

One independent read-only rubber-duck critique ran once on commit `ba5b50211` (no writes, no nested agents). Verdict: Revise (five blocking findings). It is not repeated.

## Dispositions

| Id | Finding | Disposition |
| --- | --- | --- |
| PC-01 | Wave B could be silently omitted | Applied: single assembly is gated on all of 215, 233 and 96 UI accepted; an omission needs an explicit coordinator scope change |
| PC-02 | Receipt binds exact HEAD; merge commit changes the parent tip | Applied: fast-forward preferred; otherwise re-gate the actual post-merge parent tip and assess it before the main PR |
| PC-03 | Review scope and timing | Applied: immutable source candidate, full `origin/main..candidate` union including 1487 and 1490c, external attestation, material findings block publication |
| PC-04 | Browser checks not gates | Applied: required publication gates with pinned axe evidence |
| PC-05 | Manifest incomplete | Applied in part: 16 exact 96 backend methods listed, paths frozen from `git diff --name-only` at G3; the 96 UI rows remain unfrozen and are filled only from its accepted head (honest limit, not invented) |

No finding conflicted with a confirmed decision.

## Amendment note (A1)

The verdict and dispositions above are unchanged history. The amended plan has NOT been critiqued; a genuine independent critique must run once before any assembly (see the policy amendment).

## Amended-plan critique (A1, 2353)

Executed once: one independent read-only rubber-duck critique in fresh context on commit `808429e50`, no writes, no nested agents. Verdict: Revise (four blocking, one non-blocking). Not repeated; the original verdict and PC-01..05 above are unchanged history.

| Id | Finding | Disposition |
| --- | --- | --- |
| AC-01 | A1 called the 96 addition a new GET route; main already has the GET and the view flag, and the backend adds the freshness POST | Applied: correction notes in the amendment record the actual interface (verified again against `774a91e5f...94760af7d` and UI `423517a71`); focused classification kept on the corrected basis |
| AC-02 | Escalation rule too narrow for the SQL queue refresh behaviour | Applied: owner-focused classification kept (confirmed policy); actual SQL impact assessed at G3 and escalation on further persisted SQL behaviour change |
| AC-03 | Changed UI regression `test_finance_grants_screens.py` not gated | Applied: added to 96 UI checks with the Held browser check |
| AC-04 | "individually reach G6" permitted silent omission | Applied: all wave B admitted or named in a recorded coordinator deferral |
| AC-05 | Stale admission facts | Applied: 96 UI frozen but unassessed; 233 replay 99 and 70 with queued-lock deviation retained, not a compliant-admission claim |

No finding conflicted with a confirmed decision. No new correction pool. The plan is plan-ready for assembly only after G1, G2, per-member G6 and G3 re-binding; no assembly is authorised by this critique.
