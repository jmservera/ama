---
title: Issue 200 live audit plan (Refs #200)
description: Plan to prove or bound the unticked criterion of issue 200
ms.date: 2026-11-18
---

Tier: FOCUSED (documentation and evidence only; no src, SQL, infra or deployment change). Basis: no source edit, no push to the registry, no Azure write.

* [x] Phase 1: read-only live probes of `ca-cutover-test-demo-api` and `ca-resident-demo` (revisions, images, exec uid, /data, process command)
* [x] Phase 2: local image build from `src/api/Dockerfile` plus `src/check-container.py`
* [x] Phase 3: write research note, index and log entries; per-criterion table in the changes record
* [x] Phase 4: single review, commit

Decision: no registry public window and no new revision. It would change shared registry posture and the demo revision that parallel live checks use; the criterion's "new tag deployed" part is reported as unproven.
