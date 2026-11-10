---
title: Ranking archive ancestor durability 1258 continuation research
description: Research for the two coverage omissions R2/DV-3 and R3/DV-2 left by the original 1258 review
ms.date: 2026-11-08
---

Research disposition: executed. Planning Readiness: Ready. Start head `26b4ea391d6a6000e9be8fc6f78994e52a6d0f6c`, tree `c9c7c239d2b0872425843ad9cff97c74f277a6f8`, main `f548b65f`; ignored-inclusive status clean.

* Prior art: `AncestorDurabilityTests.labelled()` in `test_ranking_publication.py` labels directory fsyncs by stat identity and wraps `os.link`; reusable as is. API class `PublicationWiring` (via `QualityMatrix`) has `self.archive()` and the existing archive-directory fault test, the template for a parent fault by `os.path.samestat`.
* Behavior: `_ancestors()` stops before the first parent failing `os.access(W_OK)`. Test user is uid 1000, so permission bits are effective; under uid 0 `access` is always true, so a permission test must skip and the root-run case is only mockable.
* The API archive is a temp path owned by the test store; its parent is a safe fault target.
* These are coverage omissions, not confirmed defects; tests may pass on unchanged source and no red run is fabricated.
