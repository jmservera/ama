---
title: Issue 115 digest anchor changes
description: Actual ordered RPI source, validation and publication receipts
ms.date: 2026-10-18
---
<!-- markdownlint-disable-file -->

## Metadata

Task ID: 115. Slug: issue-115-digest-anchor. Date: 2026-10-18.
Plan: .copilot-tracking/plans/2026-10-18/issue-115-digest-anchor-plan.md.
Details: .copilot-tracking/details/2026-10-18/issue-115-digest-anchor-phase-details.md.
Exact base: c803614e8ca7c604e509f1c088f8b8f90f3063ef.
Branch: fix/digest-anchor-evidence-115.

## Execution Status

Partial full-plan invocation; source implementation and local checks Complete.
Completed P01-T01/T02, P01 and P02-T01. Remaining P02-T02 (original independent
Review and publication) and its containing P02. No production edits occurred
before failing-first evidence.
Approved writes: digest_blob.py, existing fake suite, narrow orchestrator guide,
and this task's dated artifacts. No runtime services or cloud/private data.

## Ordered Phase Execution

| Order | Phase | Actual execution and disposition |
| --- | --- | --- |
| 1 | Research | rpi-research executed Wider -> Deeper -> Contrarian; Ready, C1-C8/W1 |
| 2 | Plan | rpi-plan executed, candidate plan/details written; one independent rpi-plan-critique Complete / Revise, Medium PC-001 |
| 3 | Implement | rpi-implement executed failing-first -> minimal guard/guide -> passing local gates |
| 4 | Review | Not yet executed; exactly one independent original required |

## Completed Work

### Planning gate and isolated fixture root

PC-001 planner-direct recommendation adopted: subsequent sanitized test processes
set absolute worktree TMPDIR. Fresh process
`tempfile.gettempdir()` returned
`/home/azureuser/source/ama-wt/issue-115-digest/.digest-anchor-tmp`, assertion passed.
Original critique unchanged, frozen SHA-256
`d1add2a5642689cb9a615f3aaa989871a3b405f7f5cab076689fdcc0110314e0`.
The original's claimed blanket system-temp prohibition is not established here;
using a stricter task-owned root is compatible with caller isolation.

### P01-T01 failing-first regression

Added exactly eight methods to existing test_digest_blob.py, no removals or
existing-test edits, using unchanged FakeImmutableContainer. Actual command,
root cwd:

```bash
env -i PATH=/usr/bin:/bin TMPDIR=/home/azureuser/source/ama-wt/issue-115-digest/.digest-anchor-tmp PYTHONPATH=src/core/tests:src/orchestrator/tests /home/azureuser/.copilot/session-state/afd14196-e65e-4c89-b2cb-12c95fe860b4/files/digest-venv/bin/python -m unittest test_digest_blob -v
```

Exit1: 17 tests, four expected behavioral failures, zero setup errors/skips.
Direct only-unrelated, local-only+unrelated and empty-ledger+unrelated got
intact true instead of false; CLI got0 instead of1. All valid head/year,
unrelated-neutrality, mismatching-anchor and existing controls passed.
Full output: .copilot-tracking/changes/2026-10-18/issue-115-digest-anchor-before.log.
Production digest source still SHA-256
`54cadb9a1d688d9a55e92a55018446ba3007e97a33d2f68a67f34de2f570a0b8`,
matching the exact base. P01-T02 may now run.

### P01-T02 recognized-anchor guard and guide

Replaced `if not names` with `if not heads and not years`. Existing report shape
and markers unchanged; missing evidence problem explicitly names absent
recognized head/year anchors. Narrow README ledger paragraph explains unrelated
blob neutrality and missing-anchor failure; no KB file or other guide section
changed. Existing fake and all nine prior test methods remain byte-exact.
Eight new methods cover direct report, CLI exit/markers, local-only evidence,
genuinely empty audit file, explicit empty GENESIS head, nonempty head/year
against empty ledger, valid head/year separately and unrelated mismatch controls.

### P02-T01 local validation

Focused/coupled invocation from root:

```bash
env -i PATH=/usr/bin:/bin TMPDIR=/home/azureuser/source/ama-wt/issue-115-digest/.digest-anchor-tmp PYTHONPATH=src/core/tests:src/orchestrator/tests /home/azureuser/.copilot/session-state/afd14196-e65e-4c89-b2cb-12c95fe860b4/files/digest-venv/bin/python -m unittest test_digest_blob test_recovery.YearLedgerTests -v
```

Exit0: 21 passed, zero skips (17 digest + four existing year-ledger guards).
The coupled class uses local SQLite only, not a service or recovery drill.
Full discovery from src/orchestrator:

```bash
env -i PATH=/usr/bin:/bin TMPDIR=/home/azureuser/source/ama-wt/issue-115-digest/.digest-anchor-tmp PYTHONPATH=../core/tests /home/azureuser/.copilot/session-state/afd14196-e65e-4c89-b2cb-12c95fe860b4/files/digest-venv/bin/python -m unittest discover -s tests -v
```

Exit0: 40 passed, zero skips, including dependency-rule and existing CLI fixtures.
Configured gates from src/orchestrator:
`<venv>/bin/ruff check . && <venv>/bin/ruff format --check . && <venv>/bin/mypy`.
Exit0, Ruff0.17.1 All checks passed, nine files already formatted,
mypy2.4.0 no issues in12 source files. Digest source/test retain existing format
exclusion and mypy ignore_errors; this is not strict type/format coverage there.
`git diff --check` exit0.

Fresh injected CLI probe with only unrelated.json returned:

```json
{"digests": 0, "entries": 3, "intact": false, "problems": [{"check": "digests", "problem": "the container holds no recognized head or year digest anchors to verify against"}], "year_digests": 0}
```

CLI exit1; `LEDGER_DIGEST_ALERT ledger does not match the immutable digests`;
no OK marker. Existing BlobDigestStore used env={} and the fake transport,
never inherited credentials or real network. Generated test temp directories
were cleaned by fixture teardown; workspace root currently empty.

## Implementation-Time Plan and Detail Updates

No scope or user-decision changes. Planned P02-T02 intentionally spans the
original Review and delivery, so remains unchecked at source Review handoff.
This is remaining publication work, not incomplete source implementation.

## Validation Record

Task-local installed venv:
`/home/azureuser/.copilot/session-state/afd14196-e65e-4c89-b2cb-12c95fe860b4/files/digest-venv`.
In commands below, `<venv>` denotes that exact path; `<root>` denotes
`/home/azureuser/source/ama-wt/issue-115-digest`. No credentials inherited:
test commands use `env -i PATH=/usr/bin:/bin TMPDIR=<root>/.digest-anchor-tmp`
and only the listed public-test PYTHONPATH.

Before venv creation, actual chosen baseline failed with `ModuleNotFoundError:
No module named 'zava_forward'`; system Ruff/mypy were also missing.
Only then ran `python3 -m venv <venv>` and
`<venv>/bin/python -m pip install --quiet -e src/core -e 'src/orchestrator[dev]'`
(exit0). Research sanitized baseline (prior to workspace TMPDIR binding):
nine digest tests passed. Research probes reproduced exit0/OK with zero
recognized anchors and tested head/year/empty controls; see research artifact.

| Check | Status | Evidence |
| --- | --- | --- |
| Workspace TMPDIR selection | Passed | fresh process exact gettempdir assertion, exit0 |
| Failing-first behavioral regression | Expected failure observed | 17 tests, four behavioral failures, source unchanged |
| Focused/coupled tests | Passed | 21/21, zero skips; focused.log |
| Full orchestrator discovery | Passed | 40/40, zero skips; orchestrator.log |
| Ruff check / format / mypy | Passed | quality.log; digest migration exemptions disclosed |
| git diff --check | Passed | exit0 before source handoff |
| SQL Server / Docker / Azure / browser | N/A, not run | No changed SQL/image/infra/UI surface; caller offline boundary. Existing coupled SQLite unit coverage is not external SQL acceptance. |

## Pre-Review Reconciliation

Ready for the one original independent Review of the source candidate.
Plan/details mark P01/P01-T01/T02/P02-T01 complete; P02-T02 remains accurately
open for Review/publication. Evidence, summary, boundaries, follow-ups and
validation reconciled. No source or validation blockers; full plan not yet
claimed complete.

## Frozen Source and Evidence Hashes

SHA-256 before original Review:

| File | SHA-256 |
| --- | --- |
| src/orchestrator/src/zava_forward/orchestrator/digest_blob.py | 568e46a8963a274c1ee5a40bb27c6ab1fbe4c076057ea95b7b6068cde3159f1b |
| src/orchestrator/tests/test_digest_blob.py | 9fcf037f7ef46848626c46fefb55b925924fb7d61ceb42bb80f66e44bec246a3 |
| src/orchestrator/README.md | 4b1ceed344046d4ef7be7e4a15fb31ac4a6e3e7ca809f21508513a5c22dcc803 |
| issue-115-digest-anchor-before.log (this directory) | 9608df527dc8635a87e0bdf2a3d19235604b8af507332e746e4bd39b81f06ee8 |
| issue-115-digest-anchor-focused.log | 8121e91006dbeec28a89618d7be950c205eee8640604d05d45e4a6668d2b9ddc |
| issue-115-digest-anchor-orchestrator.log | e0a9a529dbea99d89e8c1bf2c90bcc9270dba1673aada985652e089799ac39da |
| issue-115-digest-anchor-quality.log | ef29fcc39ea5cdd006365ec062fe5406748501ac545ea6f5dad8e7d0245d5e3c |

## Commit and Publication Preparation

`gh api user --jq '{id,login}'` resolved8036360/jmservera freshly.
Construct local author/committer email from those fields:
8036360+jmservera@users.noreply.github.com. No global/private email.
Remote main still exact pinned base at pre-candidate check. Candidate commit
will include all current task artifacts; original Review and actual publication
receipts necessarily follow in delivery-only commits. No rewrite or amend.

Pre-commit staged diff check initially found two unittest progress lines ending
in spaces in before.log (exit2). Removed only trailing spaces; assertions,
counts, verdict and all test output remain unchanged. Original raw capture
hash was9ad204b8854623e7efcc9a22b5fa068c897c6f52be74f6694bfec44f3ad2d4cc;
the committed normalized receipt hash is in the table above. Neither original
critique nor later original Review is normalized or modified.
Commit skill's documented instruction path was unavailable; resolved its
installed rules/hve-core/commit-message.instructions.md and read conventions.
Its get_changed_files tool is unavailable, so staged CLI inspection provides
the evidence instead. Explicit user publication workflow takes precedence
over that skill's isolated no-push scope.

## Blockers, Remaining Work and Follow-Up Items

No bounded-source blocker. Remaining markers above. Coordinator independent
exact-head review after publication; owner retention/lock and actual
scheduler/monitoring/recovery gates remain outside this correction.

## Return-to-Caller State

Active automatic parent; source implementation Complete, full plan Partial
pending P02-T02; Ready for one original independent Review. No additional
critique, schema redesign or operational authority inferred.
