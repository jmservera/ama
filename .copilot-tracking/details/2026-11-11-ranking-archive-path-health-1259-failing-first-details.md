---
title: Issue 1259 failing-first verification details
description: Phase details for the source-unchanged replay of the unusable-archive-path regressions
ms.date: 2026-11-11
---

## Phase 1 Prepare scratch exports

* Create `$S` and the three exports. Verify each source blob equals the declared blob with `git hash-object` on the exported file. Verify the old export tests equal the current-main test blobs.
* Success: every declared blob matches; export trees contain no `.git` and no `.env`.

## Phase 2 Current-source run

* Command: `cd $S/cur/src/core && env -i HOME=$S/home PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests ZF_DATA=$S/data/zavaforward.json TMPDIR=$S/tmp python3 -S -m unittest -v <selectors>`.
* Preceded by an origin print of the three imported modules. Success: exit 0, the subtests for regular file, dangling link, dangling ancestor and stat failure pass, the two absent-directory controls pass.

## Phase 3 Old-source replay

* Same command against `$S/oldA`. Candidate B only on a compatibility or import limitation.
* Genuine red is the defect assertions (unknown-versus-empty status, exit code, path in text, `('problem', None, True) != ('problem', None, None)` shape). Absent-directory controls are expected green on the old source.

## Phase 4 Static checks and diff hygiene

* `ruff check`, `ruff format --check`, `py_compile`, `git diff --check` as in the plan. Report exits and counts as observed.

## Phase 5 Record

* Copy raw logs and `manifest.txt` into `.copilot-tracking/evidence/2026-11-11-1259-failing-first/`.
* Write changes, one review and state. Label every result as executed 2026-11-11, after the implementation, never as prospective historical red then green.
* Commit with the privacy noreply identity for author and committer and the Copilot trailer. Write the handoff outside the repository.

## Superseded in part (2026-11-11 documentary C3)

Qualified additively by [the C3 changes record](../changes/2026-11-11-ranking-archive-path-health-1259-doc-c3-changes.md) and [the C3 review](../reviews/2026-11-11-ranking-archive-path-health-1259-doc-c3-review.md). The text above is preserved as originally written; where it differs, the C3 record governs (old-red reach, run counts, run.sh and manifest, process conformance).
