---
title: Issue 107 release admission phase details
description: Phase details for release admission
ms.date: 2026-10-15
---

Binding fields compared at admission: registry, schema, provider, endpoint, deployment, prompt, policy, data, provenance and permission versions. The expected serving model is compared after the call. Routine case edits stale proposals by source signature (existing); any binding change needs a new release. Denials are retained as disabled tasks plus append-only events.

## PR 287 review-fix details (2026-10-15)

* Gate signature becomes `gate(task, deployment=None)`; `Ai.run` and `look_at` pass the deployment they will call and recheck after the call.
* Legacy records bind registry, schema, provider, endpoint, deployment, prompt, policy, data, provenance and permission versions; one record per called deployment.
* Legacy completion recheck discards late text. It does not suspend the release and there is no legacy returned-model check.
