---
title: "#184 C4 research amendment: full local gate required"
ms.date: 2026-11-08
---

Amends, does not replace, the C4 research and plan (86e0ba5b). Written prospectively for the gate; no gate has started.

* Candidate: commit f28e278df16cda54c614e5958cf57d9fdf94c501, tree ee0abad5f2938f50a36a9b169b26b81f7b7dbe40. The merge commit 242009f47 (tree 5191b3cedd9d3f781a6e4884701a2df67442b2ff) is a different identity and an ancestor.
* Finding: the diff from origin/main fa7ae0c9 touches 25 src, infra and workflow paths, including infra/live-receiver-job.bicep and SQL source. Repository and coordinator policy require the complete local gate, a new external receipt, and verification against freshly resolved origin/main before publication and independent exact-head assessment.
* The original C4 CI-first/focused plan was insufficient for these changes. It is preserved unchanged, with the adverse history.
* The heavy lock is owned or being acquired by #1292. This continuation does not touch it.
