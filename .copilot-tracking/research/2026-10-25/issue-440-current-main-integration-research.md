<!-- markdownlint-disable-file -->
# Research: Issue 440 current-main integration and final gate

## Metadata

* Task ID: 440 (same task; follow-on integration cycle). Slug: issue-440-current-main-integration.
* Research date: 2026-10-25, prospective: written before any merge, rebase, source or document change.
* Disposition: executed (read-only git, process and file inspection).
* Planning Readiness: Ready.
* Original review (unchanged, not repeated): .copilot-tracking/reviews/logs/2026-10-24/issue-440-stabilization-review.md, execution Partial, outcome Residual work.

## Observed Facts

* Branch test/stabilization-checkpoints-440 at 65c8708db95e5d51304240a953d13b3dcc78221a, tree 90a3cfa15363167e6f727627f5da04bfd5a3c1da, clean.
* Fresh origin/main is ea5577b2ed0e051161a83813daa63d86e4613c7a. It is not an ancestor of HEAD. Merge base is f1e2d830. Main has 11 new commits (#445, #446, #438, #449, #442, #450, #453, #448, #456, #457, #458).
* Branch-only changes against main: the coordinator agent file, src/README.md, docs/architecture/cutover-evidence-pack.md, docs/reference/README.md, docs/reference/log.md and own .copilot-tracking files.
* Main changed docs/reference/README.md (+28/-7) and docs/reference/log.md (+440/-5). A trial git merge-tree reports content conflicts in exactly those two files (both sides appended index text and log entries). The coordinator agent, src/README.md and cutover evidence pack were not touched by main, so they merge cleanly.
* Main also changed runtime and policy surfaces: src/core and src/api (Entra-authoritative access #360, ledger-safe migrations, seed merge), infra, BRD 0.21.0, both PRDs, ADR0001/0002, .github/copilot-instructions.md (tracking-retention pointer) and rubric workflows. None of these is edited by this branch.
* Heavy lock /tmp/ama-rpi-heavy.lock: no holder, and no tools/rpi-checks.py process, at 2026-10-25T15:49Z. Only container observed: ama-350-feedback-sql (protected, not touched).
* The 2026-10-23 first checkpoint pinned main 140d8f49 and BRD 0.19.0 / PRD 0.18.0. Those pins describe that assessment only. Main has since moved, so the checkpoint is historical for current main and must say so.

## Original Findings, Current Disposition (before any action)

| Finding | Current evidence | Disposition |
| --- | --- | --- |
| RV-001 High, final gate not run; PERF-440 17383 ms vs 1500 ms | No final gate exists. External failed-receipt directory is absent (RV-004). | Open. Needs a fresh complete gate. Threshold unwaived. |
| RV-002 High, main moved | Moved again, to ea5577b2. | Open until integrated and gated on the then-current base. |
| RV-003 Medium, transcript lacks coordinator entry | /tmp/ama-440-discovery-20261024.txt has no entry. Coordinator comment 6385349053 reports it. | Record as attested, not independently reproducible. No redo. |
| RV-004 Low, external dirs absent | Still absent. | No recreation or backfill. Repository record only; cause unknown. |
| RV-005 Low, no Conformant before gate pass | Gate has not passed. | Open. |

## Options Considered

* A. Non-nesting merge of origin/main into the branch (existing pattern, as at 65c8708d). Preserves published and local history, needs no force push. The two conflicts are append-only text and resolvable by keeping both sides.
* B. Rebase onto main. Rewrites local commits and needs a lease push if ever pushed. Authorised by the coordinator but unnecessary; the branch has never been pushed.
* Selected: A. It preserves all main and branch intents and every earlier tracking commit.

## Conflict Resolution Rules (for the plan)

* docs/reference/log.md: keep main's bytes in full and keep this branch's #440 entries byte-identical, as appended entries after main's. Verify with a diff that no line from either side is lost.
* docs/reference/README.md: keep every main addition (retention policy paragraph, rows, ms.date 2026-10-25) and this branch's #440 pointer.
* Do not touch docs/reference/memory.md, docs/case_study_48_original.md or any main-owned source.

## Gate Facts

* Runner contract: tools/rpi-checks.py --all --base SHA --out NEW_PATH --lock-timeout N; requires clean committed HEAD with the base as ancestor; local only (disposable SQL Server, Chromium, Docker, scanners), no cloud fallback.
* The coordinator named the output /tmp/ama-440-final-ea557-gate1 and --lock-timeout 14400. That path does not exist now (verify again at launch).
* A later commit, a base change or any dirty input invalidates a receipt. A receipt-only commit is not allowed.
* The 17383 ms benchmark (core test_sqlreads.Scale.test_sql_reads_at_60000) is part of the gate. The threshold is not editable. On a new main, core tests also changed, so the new gate is also the first complete run of main's new core and API code with this branch.

## Evidence Boundaries

* Native discovery was attested by the coordinator and is not independently reproducible. It is not behavioral acceptance and will not be repeated.
* Seven HVE scenarios are simulated proxy evidence; the human checkbox stays unchecked.
* No live AI, Entra, Azure or resident-UX acceptance exists or will be claimed. Azure authority has expired.

## Risks

* Rebase or merge could lose append-only content. Mitigation is a byte-level verification step.
* The gate may fail again on the benchmark or on main-introduced tests. Mitigation: preserve the failure, run focused reproduction of the exact failing check, and fix only a confirmed in-scope defect after a bounded plan; at most two correction cycles, then report the blocker.
* The lock may become busy before launch. Mitigation: use --lock-timeout 14400 with no polling.
* Main may move again. Mitigation: after the gate, fetch; if main moved, report the stale-base outcome and reconcile rather than claim currency.

## Follow-Up Candidates

* Re-run the stabilization checkpoint on new main (BRD 0.21.0, PRD 0.20.0, Entra #360 changes). This is a coordinator-scheduled later checkpoint, not part of this integration.
* Diagnose the benchmark repeatability if it recurs.
