---
title: Issue 73 current-base refresh - research
ms.date: 2026-11-10
---

## Opening (2026-11-10T06:27Z, before substantive research)

* Third bounded metadata scope after the original integration loop (af7b20a3) and the independent-record loop (27dab9b5). It does not alter either loop, its state or its witness.
* Frozen initial head 27dab9b5e2d3659f42a326ffcd11a432b55e304f, tree 414d9c64dd1aeefa30d749d5a4aa0f932c2acc84, clean. Target base is origin/main 736561ba0cccb9beb69eea3ae0d3a997bd0dd9bd.
* Documentation tier; no runtime, gate, cloud or source change.

## Findings (after the research-open witness event, seq 2)

* Fetched origin/main is 736561ba0cccb9beb69eea3ae0d3a997bd0dd9bd, a descendant of the earlier pin 4244e84e (merge-base of HEAD and main is 4244e84e). `git diff --quiet 4244e84e origin/main -- src infra tools .github` exits 0: the delta is documentation and RPI records only (12 files, 337 insertions, 1 deletion, Discovery checkpoint 440 records, cutover-evidence-pack, reference README, log).
* Published PR 1361 (gh): base 736561ba, head 27dab9b5, mergeable CONFLICTING, state DIRTY. This is the hosted result and is preserved as is.
* Local `git merge-tree --write-tree HEAD origin/main` (git 2.43.0) exits 0 with tree abdc36c2. Root recorded tree a8107ee4 for the same identities; the two trees differ only in docs/reference/log.md ordering (8 lines). The local previews therefore disagree with each other as well as with the host, and neither proves hosted mergeability or CI.
* The likely overlap is the shared append-only region at the end of docs/reference/log.md (main added 9 lines, this branch 8). Treated as a hypothesis until the real merge.
* Source projects CI and rubric workflows are active per the task statement; no check run exists yet for the head. No settings, protection or workflow change is in scope.
* Earlier invocation parser error (unsupported --brief, no event recorded) and ordinary record-evolution notes stay as they are.
* Planning Readiness: Ready. Disposition: executed.
