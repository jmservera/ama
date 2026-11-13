---
title: Independent exact-head assessment at cbb5d01a4 (issue 1204)
date: 2026-11-13
source: external root assessment, copied unmodified below
reviewed_head: cbb5d01a40f0c8b812574510b0f805cf9889832a
---

# Independent exact-head assessment: permanent completion/refill (issue 1204)

Verdict: **Pass with conditions** (no blocking source finding; publication is NOT yet cleared).
Review only. No GitHub writes, source edits, commits, pushes or cleanup were made. Worktree left clean (`git status --short` empty).

## Identity

* Head: `cbb5d01a40f0c8b812574510b0f805cf9889832a` (matched `git rev-parse HEAD`)
* Target `origin/main`: `6ef00864dac370809ecf034de668b33b3e62252f` (matched)
* Merge base: `347962dace94171724cc8db4044c8d783335fecf` (supplied; diff taken against it)
* Commits: `ab5b10c25`, `cbb5d01a4`. 12 files, +377/-35.

## Coverage (whole diff read)

* Full 578-line PR reference read, including every hunk of `.github/agents/ama-backlog-delivery-coordinator.agent.md` (lines 84-133, 255-260, 582-715, 890-895), `tools/ama-worker-watch.py` (121 lines) and `tools/test_ama_worker_watch.py` (73 lines).
* All 9 `.copilot-tracking` research/plan/critique/changes/review files (original and c2) read.
* Agent-file frontmatter not inspected or changed (user-managed). Held 1296 correction-policy paragraphs not reviewed.
* Independently re-ran: 6 watcher tests pass. Did not re-run ruff, tmux or the launcher (Root evidence relied on, not re-observed).

## Behavior assessment

* Watcher (`ama-worker-watch.py`): read-only, argument-array subprocess, no shell. Absent-at-start returns exit 2, never a completion (lines 74-79); bounded timeout is distinct (exit 3); no-server is empty set, other tmux errors are exit 1; finite positive timeout/poll validated. Completion ordering is sound: poll after pause, finished set computed before the timeout check, so a finish in the last interval is not lost. Met.
* Missing-at-start guard: agent text (lines 709-716) treats exit 2 as "inspect each session's log and exit status, classify, refill, re-arm, never end the run, never a completion". Met; the earlier ambiguous "exit at once" is removed.
* Completion/refill ordering: finished session gets exit/head/evidence read, recount, refill to cap, then re-arm, before optional PR prose. Zero live with ready work is a defect; "fully blocked" requires evidenced per-item dispositions. Met.
* Eight-session accounting (lines 100-133): cap is live useful `rpi-*` tmux sessions; finished session frees its slot; issue stays in ledger; recount from `tmux list-sessions` plus ledger and open PRs; open-PR 20/15 thresholds and drain are retained and separate. Met and internally consistent (default 3 removed at 258). An explicit lower owner limit still governs.
* Permission-qualified continuations (lines 86-89, 103-110): continuation is `ready` only with dependencies met, finite permission, defined selected validation and run-owned source; otherwise `human-blocked`/`dependency-blocked`; unknown is bounded investigation. No approval, finite-authority, model, cloud or force-push boundary is relaxed; watcher is stated as notify-only (text near 735). Met.
* Launcher (lines 606-628): quoted heredoc, positional args, append-only per-session log, `PIPESTATUS[0]` immediately after `tee`, exit appended and returned, run via `bash` so tmux's shell does not matter. Missing `exit=` for the current attempt is unknown. Met per Root's outer-`/bin/sh` extracted run; not re-executed here.

## Findings

* F1, Low (evidence, not source): the c2 plan file `...-c2-plan.md:5-8` leaves all four phase checkboxes `[ ]` while `...-c2-changes.md` records the work done. Reconcile plan markers before publication per the Implement-to-Review rule (evidence-only commit would change head).
* F2, Low (evidence): c2 has no separate post-implementation review artifact. `...-c2-changes.md` records two targeted passes and discloses the final edit was reviewed only by a three-site grep. The original `...-review.md` (approve, three-file boundary) predates c2 and its boundary no longer matches the diff. This is disclosed, not hidden; treat as historical and cover the final head by this assessment plus HVE.
* F3, Low (watcher semantics): a session name reused between arming and the first poll could mask a finish. Admission text says names are reused only after the old session is gone, so impact is bounded. No change required.
* F4, Info (reliability bound): full tmux one-liner interpolation with arbitrary spaced paths is unexercised; the unquoted `{brief-path}` inside the tmux string assumes space-free generated paths (stated by Root). The c2 changes file's "brief path with a space" test refers to the script argument, not the tmux string. No broader native reliability is claimed.
* F5, Info: hosted CI is path-filtered and does not cover `tools/ama-worker-watch.py` (original review note); local tests are the only coverage.

No Critical/High/Medium findings.

## RPI preservation

* Original critique (`Fail`, retrospective, first batch authored before critique) is preserved unchanged and labelled non-prospective. Original review `approve` is preserved as originally recorded. c2 prospective critique (Revise, PC-001..PC-005, written before source edits) is preserved separately with compatible dispositions applied. Original/adverse and later prospective recovery evidence are coherent and distinguishable. Met.

## Conditions before publication

* HVE independent simulation/grade: **PENDING** (running in parallel). It is not a Pass and must not be recorded as one. The canonical-model behavior gate remains Deferred per the c2 changes; no intended-profile Pass exists in this diff.
* If F1 is reconciled or any evidence is added, it must be an evidence-only commit at a new head; this assessment then covers `cbb5d01` only and the final head needs an exact-head confirmation that the delta is evidence-only (no source/tool/agent change).
* Focused tier assumed (agent prose, non-gate tool, docs/evidence): record classification and basis. If the owner treats agent-instruction edits as gate semantics, the full tier and external receipt apply (unresolved here; doubt takes the full tier).
* Applicable hosted CI for the exact head, owner approval and merge decision remain outstanding; not observed here.

## Limits

Evidence-bounded: static whole-diff read plus the six watcher tests re-run. No native agent execution, real tmux, ruff or launcher re-run by this reviewer. No correction authority is requested or assumed.
