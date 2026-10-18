---
title: Issue 126 authorized integration-only receipt
ms.date: 2026-10-18
---

Task ID: 126. Slug: issue-126-rai-evidence-register. Same completed RPI task.
Status: authorized rebase, exact patch/protected-byte checks, fresh validation
and first lease publication complete; final handoff metadata.
Correction count: 0. No new critique or original Review.

## Authorization and exact boundaries

Coordinator explicitly authorized rebase of only
`feat/rai-evidence-register-126`, PR #409, from original base
`ab0613f3336109ff9b96560a16758ee842232715` and expected local/remote head
`4a23f750f1ea943bb4aaf989256e7bd019a57d12` onto exact
`9403dc6a8f52f1f04c5ad910faab11a57c29ee78` (PR #389 consultation merge).
Fetched first and verified clean worktree, exact branch, both expected heads and
target commit. No other branch/worktree or source correction is authorized.
Only the explicit old-head remote lease is permitted for first publication;
all later receipt pushes must be normal. Later main movement is reported,
never grounds for another implicit rebase.

Executed:

```bash
git rebase --onto 9403dc6a8f52f1f04c5ad910faab11a57c29ee78 \
  ab0613f3336109ff9b96560a16758ee842232715 feat/rai-evidence-register-126
```

Replayed source commit as `c3c8ce2e` and original handoff commit as `93b7450c`.
Exact rebased source/handoff head: `93b7450c823d80765d869e533788662f3c61f94a`.
Only conflict: `docs/reference/log.md`, obvious additive append.
Resolution retained exact upstream log prefix followed by the byte-identical
original issue-126 addition. No log entry was edited or discarded.
README/index/server merges were automatic, then checked by exact patch parity.
No persistence/source conflict, intent change, feature, policy or authority change.

## Before/after integrity and full inventories

Original 30-path scope is retained in `original-30-paths.txt` and the original
inventory itself remains unchanged. Full tree inventories include path, Git mode,
blob ID, byte length and SHA256 for old base, original topic, exact target and
rebased tree. `parity.json` records the full assertions and exact protected paths.
Full-tree JSON files are losslessly gzip-compressed with deterministic timestamps.
`full-changed-inventory.txt` lists every original and separate integration path;
`full-changed-path-hashes.json` binds their exact bytes/modes, excluding only its
own recursive hash (bound instead by the final published Git blob).
`capture.py` and `verify-manifest.py` preserve the exact capture/verification logic.
The latter also verifies final bookkeeping changes are limited to the four
declared current metadata files, with Markdown history retained as an exact prefix.

Normalization removes only diff index object IDs and hunk position/header lines
from a zero-context Git diff, retaining every exact added/removed byte, path and
mode. Before/after normalized patches match for:

* All original 30 paths:
  `bb16f170463c1b3fffc075262db4b33e6f2ac8bdf63cf423792694af4e9c6548`.
* All six owned source/config/test paths:
  `2c94988bd6b03e082cd553038beb677855bf1a3b46c1bb4f91ed6ffecbe48026`.

All 2599 target paths outside the owned scope are byte/mode/blob-identical,
including upstream procurement, consultation controls/API tests and UX synthesis.
The combined server is exactly the original issue-126 server plus the two-line
upstream consultation route, with every own governance map/read/action hunk intact.
Both additive README sections and upstream KB index/UX links are retained.
All 20 original tracking/baseline/original-case/memory files checked before
bookkeeping are byte/mode-identical. Research, critique, original Review and
all prior logs remain immutable after bookkeeping as well.

Original critique SHA256:
`4e24e7e0cc8cf21081c4e5823cbbfbd8fbf0d1d0a8e904220ecd5b0e3235c8bb`.
Original Review SHA256:
`12788d8f7f81279012b54ba3902255f2eabe436d61d97fda3a0ae701bb6b6c24`.
Original Review remains Complete / Conformant for its bounded original source
assessment; that is not a new assessment of this integration.

## Complete actual original execution log

Read all 846 lines / 39413 bytes of `/tmp/rpi-126-register.log`, not just a
summary or artifact list. Byte-identical copy in the authorized resumed session:
`/home/azureuser/.copilot/session-state/10f40604-edc8-40bb-9368-73353faf82a1/files/issue126-original-complete-execution.log`.
Both SHA256:
`918e07c62d006a4c4034ca16a036f540710149ad5f5af453651a6a11aa8e0072`.
The log records actual research, planning, fresh sole critique worker, direct
dispositions, failing-first implementation and validation, and fresh sole original
Review worker. It records intermediate HTTP/lint/type failures as well as later
results. Some tool output is summarized/truncated in the CLI log; prior retained
raw receipts provide the detailed test results. Artifact presence alone is not
claimed as phase-execution evidence.

## Fresh validation

Raw commands, complete stdout/stderr and exit statuses are retained separately
from original logs. No dependencies installed; existing editable src distributions
remain installed. No unrelated formatting or source changes.

| Receipt | Actual result |
| --- | --- |
| focused-tests.log | Governance, ten actual HTTP cases, assistant release: 107 run, 91 passes, 16 MSSQL opt-in skips, exit 0 |
| consultation-tests.log | Consultation controls and JSON/SQLite procurement API: 64 run, 51 passes, 13 explicit skips, exit 0 |
| core-quality.log | Configured Ruff and mypy pass, 125 source files, exit 0 |
| api-quality.log | Configured Ruff and mypy pass, 57 source files, exit 0 |
| formatter.log | Configured format checks pass, core72/API25 files, both exit 0 |
| excluded-format-diagnostic.log | Four existing excluded files would reformat, exit 1 at both original/integrated source heads; no file changed |

Expected injected SQL recovery/HTTP response-encoding error traces remain in the
successful focused receipt. These are asserted synthetic adverse paths, not hidden
suite failures. Fresh suites execute 171 tests, 142 passes and 29 explicit skips;
these figures are not a unique-test claim across historical suites.

Formatter checks use the existing component pyproject configuration, not an
assumption that every source file is formatted. Existing migrated governance,
sqlstore, test_governance and server files are excluded by those configurations.
Explicit stdin diagnostics bypassing exclusions return 1 for all four at both
original and integrated source heads. No bulk formatting, new exception or
post-Review correction. New typed governance HTTP harness is included in the
successful configured API formatter check.

Historical only, not repeated: actual disposable SQL 16/16 and hardened image
107 executions with 16 explicit SQL opt-in skips. Exact production patch parity,
no persistence conflict and no packaging change do not require a broad rerun
under this integration-only authorization. No Azure/model/live acceptance follows.

## Publication and final inventory

Authenticated id8036360/login jmservera was rechecked before commit. Author and
committer use repository-local `8036360+jmservera@users.noreply.github.com`;
both replayed commits and integration commits retain the required Copilot trailer.
First integration metadata commit and verified remote publication:
`b38067293741c5667dd07f5e15e8b2ee39abd823`.
The sole authorized exact old-head lease succeeded; its actual output is retained
in `publication.log`. Initial immediate PR cache still showed the old head;
subsequent actual remote and PR queries agree on the new first-publication head.
PR #409 remains open with empty `closingIssuesReferences`; exact main/base observed
at publication remains `9403dc6a8f52f1f04c5ad910faab11a57c29ee78`.
No additional rebase, merge or source correction.

Final inventory: 57 paths, comprising the original 30 plus 27 separately scoped
integration artifacts, not an expanded production change. Only four original
current metadata files receive additive/descriptive reconciliation. Original
research, both assessments, inventory and all prior raw logs remain unchanged.
The final receipt commit uses a normal push. Its exact resulting head and PR body
are verified externally to avoid a self-referential commit identifier in this file;
complete final publication output is retained at
`/home/azureuser/.copilot/session-state/10f40604-edc8-40bb-9368-73353faf82a1/files/issue126-integration-final-publication.log`.
The PR body supplies exact final head/base, fresh versus historical results,
full inventories, original phase evidence and all unmet human/live gates.

First final-manifest rerun stopped before commit/push on its path-set assertion:
Python's absolute `__file__` mixed absolute new-artifact paths with Git-relative
paths once those artifacts were tracked. The integration-only manifest utility
now normalizes its root to the working directory; inventories are consistently
workspace-relative. Original source, persistence intent and assessments are
unchanged. The failed attempt and successful rerun are retained in the final
session publication log; this is an evidence-generation repair, not a production
source correction or a replacement assessment.

## Acceptance and stop boundary

All 22 baseline findings remain Open; claims never establish human acceptance.
Qualified current-source RAI/inline verifier evidence, competent owner decisions,
privacy/legal and operational approval, witnessed restore/erasure, held-out real
model evidence, current PRD owner acceptance and version-linked actual AI/SQL/Azure
application acceptance remain unmet. No issue/board/merge, automatic signature,
deployment, real contract/spend or paid inference action.
Stop after publication for coordinator independent full exact-head source,
artifact and log inspection. No second original Review or critique.
