---
title: Issue 149 UX parent integration prospective plan (2333)
description: Prospective plan, written before independent critique, for one coherent assembly of independently passed UX inputs into the declared UX parent and one parent to main PR; planning only
ms.date: 2026-11-12
---

## Status and honesty record

Prospective PLAN ONLY, written before the independent critique. No source, publication, cutover pack, ref, PR, issue or tick is changed. The plan binds inputs to exact heads and trees recorded in the research file; any different head amends the plan and is re-critiqued only if a decision changes. Nothing here accepts an unmerged sibling as integrated.

## Objective

Adopt the independently passed inputs 74 (`467a0cf5`), 176 (`da436be3`) and 134 (`cc7e3c3a`) together with the combined 1490 funding correction (`ff40e50c`), plus the later-accepted 215, 233 and 96 UI when ready, as ONE coherent UX integration: one assembly into the declared parent `feat/demo-ux-integration-1112`, one independent final Review, one native #440 checkpoint, one full-tier gate on the final tip, and ONE parent to main PR. No per-input main PR.

## Topology (decision D1)

* Assembly branch `feat/demo-149-ux-assembly-<yyyymmdd>` is created from the parent tip AFTER 1490 is merged. It first merges the freshly fetched `origin/main`, then each input head with `git merge --no-ff`, so original commits, dated RPI artifacts and trailers are preserved (no cherry-pick, no squash, no history rewrite).
* The assembly is published once as a stacked PR into the parent. Preferred merge method is fast-forward of the parent to the gated tip (keeps the receipt SHA and input commit identity); a merge commit is acceptable only with the Phase 8 re-gate; then the parent opens ONE PR to main (owner chooses its merge method; the receipt binds the tip).
* Rejected: a PR to main per input; targeting main with the assembly directly (bypasses the declared parent and its merged children); a parent fast-forward to main (no longer possible, parent has the 1487 squash); rebasing the parent (history rewrite, needs owner approval, none sought).

## Implementation gates (all must hold before ANY assembly code)

* G1 1490 merged into the parent: the coordinator has assessed the exact combined head `ff40e50c8`, published it once (force-with-lease, original head `dc9fb68e0` preserved), hosted checks read as success (pending or absent is not success) and the parent merge is recorded with its SHA. Identity check: if the parent is otherwise unmoved the merged tree equals `2e0bd970693ea2b4f7bab13124e53032a6b13870`; any difference is explained or the plan is amended.
* G2 The coordinator authorises the assembly task, names the cut line (wave A fixed, wave B members), the assembly branch name, the main-sync method (merge into the assembly) and the merge methods, and confirms no new correction pool.
* G3 Re-bind at assembly time: re-fetch main, record its SHA, re-run the read-only merge-tree matrix at the exact SHAs (expected: only 134 against main conflicts), and verify each input head and tree still equals the recorded pins and that its independent acceptance record exists. A head that moved needs its own accepted record first.
* G4 Environment: fresh pip-only venvs outside the repository with editable installs of `src/core`, `src/agents`, `src/api` from the assembly worktree (no uv, no source PYTHONPATH; only the documented test-helper directories `tests`, `../core/tests`, `../agents/tests`); pinned ruff 0.17.1 and mypy 2.4.0; pinned axe 4.10.3 file with recorded hash; heavy lock; disk checked; SQL Server prerequisites PROBED (docker image and daemon) because the full tier needs them and there is no cloud fallback.
* G5 Repo-local noreply identity and Co-authored-by trailer verified for every commit; fresh web-interface-guidelines fetch before any web review.
* G6 For wave B only: 215 coordinator admission (independent Pass exists), 233 independent Pass recorded, 96 backend and UI independently accepted at frozen exact heads, R-UI-1 decided by the root, and the UI repin checklist already completed in its own task.

If any gate fails, stop at that gate, record the blocker and next action; do not substitute a weaker input.

## Phases

* [ ] Phase 0: gates G1 to G6, recorded in the assembly state file; one frozen manifest (details, Section 1 to 3) is re-verified.
* [ ] Phase 1: assembly worktree from the parent tip; merge main (M0); failing-first expectation recorded for each input (its own original red evidence is reused, not re-created).
* [ ] Phase 2: merge wave A in the order 74, 176, 134 (details, Section 4). 134 uses the union resolution rule; every other merge must be conflict-free, otherwise stop and route.
* [ ] Phase 3: merge wave B in the order 215, 233, 96 (the accepted UI head, which contains the backend). The single assembly is gated on ALL of 215, 233 and 96 UI being accepted at frozen heads (critique PC-01). If one is not ready the coordinator must either wait or record an explicit scope change (a reduced assembly, with the remainder in a named later assembly); the plan never silently omits it. No input is added after Phase 6.
* [ ] Phase 4: focused exact-candidate checks on the assembled head (details, Section 6). The browser checks (home case 24 PASS, regulatory 21 states, programme paging, role screens 230, Held download) are REQUIRED publication gates with pinned axe 4.10.3 hash evidence, because the full runner does not run them (PC-04). Failing input behaviour routes to its owning issue and blocks publication; no correction is made inside the assembly beyond conflict resolution.
* [ ] Phase 5: native #440 checkpoint (separate native RPI task, single writer to the pack, README index and log) records the integrated wave at the assembled source head, excluding unmerged siblings.
* [ ] Phase 6: ONE independent final Review of an immutable source candidate (frozen source SHA; evidence-only commits after it are allowed and listed). Scope is the COMPLETE parent-to-main union (`origin/main..candidate`), including the already merged 1487 and 1490c, not only the diff against the parent; it covers original RPI of every input, conflict resolutions, the native 440 checkpoint and fresh web guidelines against changed web files (`chat.js`, `role-screens.js`). The Review attestation is stored externally with the candidate SHA. Material findings BLOCK publication of this candidate and route to the owning input; the Review is not repeated within the task (PC-03).
* [ ] Phase 7: commit dated assembly RPI evidence (research, plan, details, critique, changes, review, state); run the full-tier gate (details, Section 7) with an external output path on the committed tip; verify the receipt; coordinator independent exact-head assessment; publish the assembly PR; read hosted CI.
* [ ] Phase 8: the receipt binds exact HEAD, and a merge-commit into the parent creates a new tip, so after the assembly merges the ACTUAL post-merge parent tip becomes the delivered candidate. Re-fetch main, merge it if moved, then re-run `--all` and `--verify-receipt` on that exact parent tip (required only if the tip tree or base differs from the already gated tip; record the identity comparison, otherwise reuse is not assumed), have the coordinator assess that tip, open the single parent to main PR, read hosted CI for that head, and leave the merge to the owner (PC-02). A fast-forwarded or squash-free assembly merge that keeps the gated SHA is preferred if the coordinator accepts it, since it preserves the receipt.

## Conflict and preservation rules

* 74 versus 82 in `src/api/tests/test_home_case_api.py`: expected clean (hunks at about lines 90 and 122). If a conflict appears, keep BOTH complete methods verbatim, never interleave, and place each as in its own head. The assembled class must contain exactly the method set {existing 3, `test_absent_funding_reads_as_not_confirmed_not_missing_case`, `test_non_finance_staff_get_no_cost_amounts_over_http`, `test_finance_staff_get_building_cost_and_own_home_allocation_over_http`} = 6 tests, all passing; both fixtures stay independent.
* 1487 versus 1490 in `test_mvp.py` and `store.py` is already resolved in 1490c; the assembly asserts both methods exist and the stage check precedes `gate_reasons`.
* Strict funding reader semantics: `funding_ok` is trusted only when `is True` in the gate (`store.py`), `chat_case_answers.py`, `home_case.py` and `taskqueues.py`; `MEMBERSHIP_REVISION` is 3; no input or resolution may weaken them. Detected by the invariant checks in details, Section 5.
* 134 versus main: resolve `cutover-evidence-pack.md` and `docs/reference/README.md` by KEEPING BOTH sides verbatim (main's #1492 section first, then 134's reconciliation section; main's README paragraph then 134's). No wording of the pack is edited; the six partial and four deferred dispositions, "none passes", open #83 wording and the correction history stay exactly as in `cc7e3c3a`. The resolution gets its own independent targeted closure read inside the Phase 6 Review.
* `docs/reference/log.md` is append-only: zero deleted lines; every input's added entries appear once.
* No input is described as integrated, accepted or merged in any record until it is in the assembled head AND its checks ran there. 134 stays partial and deferred; 215, 233, 96, 74, 176 and 1490 are NOT retro-promoted into the 134 rows.
* The assembly does not write cutover pack content, does not duplicate the AI cutover pack writer (#1492 lane and the parent-base preflight 2300 matrix) and adds no new pack section; only the native 440 checkpoint may add one, after assembly, as the sole writer.

## Budget and approvals

Spent history is carried exactly (research file) with NO new correction pool. Human reviews, owner closure of 134, hosted CI, assistive-technology, Finance and legal approvals stay unrecorded; no tick, issue edit, approval or merge is made by the assembly. PRs use `Refs`, never a closing keyword, because whole-issue criteria remain unmet.

## Validation tier

FULL tier, basis: SQL queue membership revision, funding gate on a human approval boundary, Held-copy route and consent-adjacent web code, mssql selected by the canonical selector, and doubt takes the full tier. A mixed change takes the strictest tier. Focused checks (Phase 4) are development aids only and never replace the full receipt. Hosted CI is read separately for the assembly PR head and the parent to main PR head.

## Plan-ready and resume conditions

* Plan-ready: YES for the wave A skeleton and wave B contingent steps. Implementation is BLOCKED until G1 and G2, then G3 to G5 at assembly time.
* Resume at Phase 0 when the coordinator records the 1490 parent merge SHA and the G2 authorisations; resume wave B members individually when each reaches G6.
* If 1490 is not merged, stop: nothing is assembled. If main moves after G3 but before Phase 7, re-run G3 and the affected merge; if an input head changes, it is a new input needing its own acceptance.
