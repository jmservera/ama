---
title: Resident assistant publication phase details
ms.date: 2026-10-27
---

Task ID: 469-publication-2026-10-27. Parent: resident-assistant-aoai.
Interpreted goal: publish only after reproducible local gate and independent
assessment, with no new activation or source edits.

## P01-T01: Preserve and prepare

Candidate starts at 8f51686a3fbc4b1ca9a6e258a921b96f4fdeb8a6.
Fetched main is 49c942b33b89100c084d48a91215989e22de5887, already
an ancestor; do not rewrite history. No head PR exists. Global project
distributions/pyodbc are absent: gate bootstraps isolated pip environments.
Privacy-safe email is derived from `gh api user` (id plus login) and configured
repository-locally. Only task-created files may be staged.

## P02-T01: Preserve cleanup and hand off lock

Enumerate actual ignored/untracked cleanup candidates after task evidence is
committed. Create an external archive of every selected file/directory and
the entire tracking snapshot, retain path/type/size/hash/link identities,
verify readback and restore into new scratch before `git clean -fdxq`.
No broad historical deletion or unknown file selection. Verify protected
tracked bytes before/after. Retain external inventory and cleanup journal.

The initial foreground `flock -w 0` reservation is held while preparing.
Runner's `heavy_lock` reopens the same path and cannot reuse that lock.
Release only our attached reservation immediately before the unchanged
foreground runner with `--lock-timeout 0`; if another owner wins, stop.

## P02-T02: Execute validation

Use Python 3.12 and new external output. Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/rpi-checks.py --changed --jobs 3 \
  --base 49c942b33b89100c084d48a91215989e22de5887 \
  --out /tmp/ama-469-aoai-publication-scoped-NEW --lock-timeout 0
```

Choose a genuinely new generated output path, not the literal example.
Changed workflows may select the full matrix automatically; inspect receipt
selection rather than assuming scope. If full groups are selected, the
runner's default verification already requires full coverage. Otherwise
run a separate `--all` gate before publication. No substitute partial pass. Automatic verification
already chooses the matching scope. If separately inspecting a partial
receipt, use `--verify-receipt ... --required-scope partial`; final publication
verification must retain the default full scope.
Use gate's actual core/API/infra unittest logs to establish the requested
suites; if a suite does not execute, run its existing discovery explicitly
using installed project distributions, not source PYTHONPATH workarounds.
Preserve pre-existing opt-in skips separately from required SQL execution.

## P03-T01: Independent publication Review

Current handoff: P01/P02 complete. First changed-path run on committed
7f1a9f3c passed with full scope/all 17 groups and real accounting SQL
execution. Counts, log identities, cleanup proof and scope are recorded in
the child's changes artifact. Original parent Review stays unchanged.
Only Review and final exact-head publication maintenance remain.

One fresh reviewer activates rpi-review for this child task. Allowed write:
the child's canonical Review artifact only. Assess publication evidence,
original acceptance limitations, plan/change reconciliation and boundaries;
no repeated parent Review or source fixes. Open findings route to follow-up
and block affected publication requirements.

## P03-T02: Exact-head publication

Commit dated original child RPI evidence, then rerun the selected full-covering
gate on the resulting head. No subsequent source/evidence commit before push.
Fetch main immediately before full receipt verification. Changed main must
be integrated without rewriting published history and requires a fresh run.
Independent exact-head publication assessment can be external so its addition
does not invalidate the candidate. PR must be non-draft, base main, no closing
keywords, with `Refs #469`, precise test/gate evidence, USD20 within USD30,
and explicit private-migration/authenticated-MI unmet items. Never deploy or
merge. Hosted and human approvals remain pending.

The final candidate will name the pending publication action in committed
state; actual push/PR metadata and the authoritative final receipt stay
external to avoid a self-referential evidence commit and invalidated gate.
Do not mark unobserved remote actions complete in committed evidence.
