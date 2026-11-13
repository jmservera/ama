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

## A2 pending critique (2026-11-13)

The A2 amendment (final inputs 96 combined `423517a71` and 233 final `837da4fde`, revised cut line, order and checks) changes decisions and requires a genuine independent read-only critique before any assembly. It has NOT been run here and no verdict is claimed. The scope is listed in the A2 section of the [policy amendment](issue-149-parent-plan-2333-policy-amendment.md). The Revise results above (PC-01 to PC-05, AC-01 to AC-05) are preserved and not repeated.

## A2 critique (2026-11-13, executed once)

The pending note above is now closed by this execution. One independent read-only rubber-duck critique ran in fresh context on commit `4a424b321`, with no writes and no nested implementation agents. Verdict: Revise (four blocking). The critic verified that the pins exist, both ancestry chains and the final-input file scopes hold, and that `837da4fde` with `423517a71` merges cleanly with both web additions present. It could not run the sequential simulation or read the external acceptance evidence. Not repeated; PC-01 to PC-05 and AC-01 to AC-05 above are unchanged history.

| Id | Finding | Disposition |
| --- | --- | --- |
| A2C-01 | "Rubric delta only" and main `774a91e5f` are stale: main is `c58f87135` after #1493 | Applied: truthful rebind note in the amendment; the earlier statement is kept as history and is not claimed to have covered `c58f87135` |
| A2C-02 | Focused tier conflicts with the full-tier rule for SQL and security-sensitive changes | Rejected without re-asking: conflicts with the confirmed A1 owner classification and AC-02; the 1490c persisted queue revision was already assessed there. The G3 escalation to the full tier on any further persisted SQL, security-control or gate change stays |
| A2C-03 | Per-merge two-code check is wrong before M5 and M6, and unconditional if a member is deferred | Applied: check each addition only after its own merge; union after M6 only when both are admitted |
| A2C-04 | G3 cannot inspect an assembled diff before assembly; names alone cannot show control changes | Applied: two-stage inspection of pinned input diffs and hunks at G3, then of the actual candidate before publication |

No finding was left open. Assembly is still not authorised: G1, G2, per-member G6 and the G3 rebinding at the then-current main remain.

## A5 critique (2026-11-13, executed once)

One independent read-only rubber-duck critique ran in fresh context on commit `e2b452946`, no writes, no nested agents. Verdict: Revise (two blocking, one non-blocking). The critic found the sequential simulation clean through M6 with only the known 134 `cutover-evidence-pack.md` conflict at M7, and found no 233 dependency or false 233 delivery claim; no tests were run. Not repeated.

| Id | Finding | Disposition |
| --- | --- | --- |
| A5C-01 | A5 called its scope an admitted-members-only selection while A2 requires admission or a recorded coordinator deferral for every wave B member | Applied: A5 correction notes state that 233 is neither admitted nor deferred, the rule is not satisfied for 233, and the result is a source-frozen subset only |
| A5C-02 | Main may advance and a symbol search cannot prove 233 ancestry is absent | Applied: pre-merge rebinding and final-head `merge-base --is-ancestor` checks, stop with proof on any 233 dependency |
| A5C-03 | Source record lacked merge identities and the M7 resolution evidence | Applied: the record lists ordered merges, parents, tree hashes and the resolution outcome |

No finding conflicted with a confirmed root decision. Assembly (source only) may proceed; no publication is authorised.
