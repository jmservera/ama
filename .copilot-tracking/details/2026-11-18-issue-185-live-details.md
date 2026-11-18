---
title: Details for issue 185 live plan
ms.date: 2026-11-18
---

Driver lives outside the repository (`/tmp`), is passed to the job as a base64 env var, prints device ids and HTTP codes only. Keys are held in memory, never written to disk, env, logs or repository. Device ids use prefix `SYN-` and a `185` run tag. Marker: device `capabilities` untouched; ownership is shown by the run-tagged ids and a final registry listing.
