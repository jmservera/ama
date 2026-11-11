---
title: Resident-choice CSV feature-wave checkpoint changes (Refs #440)
description: Changes record for the admitted observation on main e09b21f1d
ms.date: 2026-11-11
---

* Added: admission amendment (committed before merge and tests), one section in `docs/architecture/cutover-evidence-pack.md`, one entry in `docs/reference/log.md`, this record, the author review and the updated state.
* Merged pinned main `e09b21f1d` with no-ff `1b3d178d`; trees of src, docs, infra, tools and .github equal main's.
* Observations: C7, C1 to C6, I1 and B1 all exit 0 with counts equal to the static expectation (111 plus the browser story); no skip. Adverse: missing-import preflight, one `node`-missing PATH error on C2 (rerun once, disclosed), both preserved raw.
* No divergence from the plan beyond the C2 rerun. No source, fixture, role, schema, workflow, manifest or test edit; no index change.
