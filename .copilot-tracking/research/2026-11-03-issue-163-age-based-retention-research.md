---
title: "Issue 163 age-based retention research (2026-11-03)"
ms.date: 2026-11-03
---
* Research disposition: reused. Planning Readiness: Ready.
* Merged work (PRs 281, 649, 727, 735, 745, 844) delivered the data map, rights requests, log exclusion, free-text warning and an idle-based purge (`purge_retention`, #844).
* Owner decision 2026-11-03: expire a fixed time after creation, not after idleness. The purge used `updated_at`; it must use `created_at`.
* Unmet criteria: 2 (lawful basis, staff notice, DPIA decision by DPO and Legal) and 5 (model provider data handling and region position). Both need named human owners.
