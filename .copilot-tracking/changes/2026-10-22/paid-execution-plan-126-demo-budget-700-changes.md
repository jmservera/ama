<!-- markdownlint-disable-file -->
# Changes: paid-execution-plan-126-demo-budget-700

* Task ID: 126-demo-budget-700
* Plan: .copilot-tracking/plans/2026-10-22/paid-execution-plan-126-demo-budget-700-plan.md
* Declared scope: P01 implemented; P02 (gate and publication) is executed after commit and is recorded in the PR and external receipt, not here.

## Preflight (2026-10-22)

* Worktree run-owned; starting tree clean; branch docs/paid-execution-plan-126; PR #422 open, draft, base main, mergeable.
* origin/main fetched: 9e55a392b95c90730c6410b9a4db4ad3a5ae70ce; the branch already contains it (merge-base check passed), so no rebase and no force update were needed.
* Repository-local author email matched the privacy-safe form from the authenticated account lookup.

## Read-only Azure evidence (P01-T01)

* Existing signed-in session; no credentials, account names or raw records printed or stored. One command printed the subscription scope in the terminal only; it is not recorded in any file.
* Cost Management query at resource group `ama`: succeeded after one throttled attempt; subscription scope: authorization denied. Aggregates are in the research artifact.
* Inventory and public price reads only. No resource, role, tag, job, deployment or tenant change.

## Edits (P01-T01, P01-T02)

* docs/case_study_48_addendum.md: ms.date updated; costed subsection intro rewritten; new "Revised owner budget decision (2026-10-22)" with current evidence, envelope and thresholds on 700, B0 to T3 options table, blockers; the 2026-10-20 text relabelled "History ... (superseded)". Heading and anchor kept so the index link still works.
* docs/reference/README.md: existing index row extended for the revision.
* docs/reference/log.md: one appended entry; earlier entries untouched.

## Validation so far

* Arithmetic recomputed in Python: forecast 535.33; headroom 164.67; admissible U 89.67, 84.67, 74.67, 66.67; thresholds 560/630/665.
* Stale-figure sweep: remaining 400/450/475/535.41 mentions occur only in history-labelled text and the log entry describing history.
* Identifier sweep over the new text and artifacts: no GUID, email, subscription path or tenant domain in additions.
* Full tools/rpi-checks.py gate: not yet run at this point; see the PR for its result and receipt.

## Divergences and follow-ups

* No divergence from the plan. Critique findings PC-001 to PC-007 applied as dispositioned.
* Follow-ups: see the plan's Follow-Up Items.
