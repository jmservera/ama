---
title: Details for issue 110 live proof
ms.date: 2026-11-18
---

Pass criteria for C1: 3 distinct devices (distinct generation ids and keys, type sas); 6 distinct reading ids received with schema_version in `live-sim-reading-v1 (v1 observed)`; `message_id == reading_id`; hub-stamped device id equals `SYN-` plus body sensor id; duplicate resend carries the same id; wrong key 401; all devices deleted; no key text in output. Cannot prove: production X.509 receiver, Standard tier consumer group.
