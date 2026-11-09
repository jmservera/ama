<!-- markdownlint-disable-file -->
# Behavior grade 003 (C1-C3 correction), issue 1204

Grader: independent, strict. Inputs: `-behavior-scenarios-003.md`, `-behavior-testlog-003.md`, target `.github/agents/ama-backlog-delivery-coordinator.agent.md` (line numbers from the current working copy). Quoted phrases were grep-verified in the target.

## Quote verification

* T1 quote at lines 333-335: "Even an append-only docs conflict rebase creates a new head and invalidates head-bound evidence; the new head needs step 7/8 final exact-head selected-tier evidence, independent exact-head assessment and hosted checks before merge." Verified.
* T2 quote at lines 632-634: "goes back to its loop once to produce a frozen local correction ... the coordinator alone verifies, assesses and publishes it and workers never push." Verified. Line 559 also forbids workers to push.
* T3 quotes at lines 107 and 110: "from 16 to 20 admit no new issues"; "repair, correction and review continuations stay permitted at every count within the eight-total-live-session cap". Verified.

## Grades

| Scenario | Expected | Observed | Grade |
| --- | --- | --- | --- |
| T1 | No merge; head-bound evidence, assessment, hosted checks needed | No merge; old Pass, green checks and receipt bound to c0de001 discarded; new receipt, independent exact-head review, green hosted checks, step 7 rerun; not an owner gate | Pass |
| T2 | Local-only frozen correction; coordinator-only publication | One fresh-brief loop, local frozen correction, worker pushes nothing, coordinator verifies, assesses, publishes; blocker if still missing; no fabrication | Pass |
| T3 | New issue barred; existing-PR repair and review allowed within eight sessions | #1960 refused; #2813 repair and #2814 review allowed (sessions 5 to 7 of 8), PR count recounted | Pass |

## Executor-noted gaps, classified

| Gap | Class | Reasoning |
| --- | --- | --- |
| T1 verdict binding: step 7 text "the independent assessment is current, the latest review verdict is Pass with no open blocking finding" (lines 667-668) does not say the verdict is for the exact head | Medium | "Current" qualifies the assessment, and lines 333-335 and 727-728 ("A correction or rebase invalidates ... independent assessment") invalidate the old review. A literal reader could still treat the old c0de001 Pass as "the latest verdict" and merge. Mitigated by the "current" clause and the hosted-check requirement, so it is not High. Fix: "the latest verdict is Pass for the exact head" |
| T1 push timing: lines 724-729 say "rerun the validation, and push with `--force-with-lease`" then "assess the resulting exact HEAD before any further push" | Medium (borderline Low for merge risk) | Read literally, the rebase push precedes local evidence and assessment, and "any further push" is undefined for the rebase itself. This cannot cause a wrong merge (merge is gated on head-bound evidence and hosted checks), but it could cause a premature push of an unassessed head, which strict grading counts as a wrong push. Fix: state that the rebase push is the only push permitted before assessment, or that local evidence is complete before it, and that hosted checks start only afterwards |
| T1 new-receipt command only implied | Low | Command is derivable from lines 441 and 701; the executor derived it correctly |
| T2 retry wording ("once" at line 633, step 5 twice) | Low | Executor applied one loop run; no wrong action |
| T2 ledger versus human blocker, unmergeable marking of an open PR, push flags | Low | Merge is already blocked by the RPI evidence check at lines 669-672, so no wrong merge; publication stays coordinator-only |
| T3 no drain target for the 16-20 band | Low | Admission threshold is explicit at line 107 ("only at 15 or fewer"), so 16-20 cannot wrongly admit an issue. The missing target (the 10 to 15 range is stated only for above 20, line 108) affects drain pacing only, not admission, push or merge. Optional fix: "from 16 to 20 admit no new issues and drain to 15 or fewer" |
| T3 minor session-count readings | Low | Cap arithmetic was correct (5 to 7 of 8) |

## Findings of Medium or higher

* M1: step 7 verdict clause is not literally head-bound (line 667-668).
* M2: rebase push versus assessment ordering is ambiguous (lines 724-729).

No High findings. C1, C2 and C3 are resolved in behavior: all three scenarios gave the expected action.

## Overall verdict: Pass (with two recommended Medium wording hardenings)

The three correction scenarios pass. A strict reading leaves M1 and M2 as ambiguities, which are residual and mitigated by explicit invalidation text. They do not reproduce C1-C3.

## Limits

* Executors ran on an inherited proxy model and profile that is unknown, so the result may not hold for the production coordinator model.
* Scenarios were designed by the lead, not independently, and they were disclosed to the executors as black-box prompts; designer and fixer overlap can bias coverage toward the fixed lines.
* All commands were emulated and nothing was executed, so real `gh`, tmux and receipt behavior is unobserved.
* Each scenario ran once, giving no variance estimate.
