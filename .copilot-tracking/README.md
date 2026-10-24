---
title: Active Work and Retained Evidence
description: Retention policy and archive-backed historical presentation evidence
ms.date: 2026-10-24
---

## Retention

Follow the [tracking retention policy](../docs/reference/method/tracking-retention-policy.md).
Keep active work, original RPI records, unknown-active tasks and adverse reviews.
Reusable builders and durable evidence belong in `tools/` and `docs/`; new heavy
generated outputs default to explicit external scratch or an approved artifact
store. Original-review and complete publication gates remain required.

The [PR 438 manifest](../docs/reference/resources/tracking-retention-manifest.json)
maps exactly 115 pruned historical files to locally archived member names,
sizes and hashes. Historical preview links to those members are archive-backed,
not live-local. The policy gives archive availability limits and safe isolated
restore commands. All other pre-existing tracking entries remain unchanged,
including the 89 current native-build files. No automatic cleanup is authorized.
