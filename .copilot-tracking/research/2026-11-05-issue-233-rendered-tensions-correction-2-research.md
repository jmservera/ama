---
title: "Research: issue 233 tensions correction 2"
description: Bounded checker lint correction
author: Copilot
ms.date: 2026-11-05
ms.topic: reference
---

Disposition: executed (light). The existing owned-browser Ruff profile (`--no-cache --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`) reports six E501 violations in the new checker (lines 50, 60, 68, 125, 352, 506). This profile is stronger than the default Ruff check used earlier; the earlier lint and the passed partial gate (receipt sha256 eb9cb6ff...) are not claimed to have failed. Coordinator process deviation, disclosed: its first stronger probe created a new ignored `src/api/.ruff_cache` in `/tmp/ama-wt-233-gate-final`, so that auxiliary is no longer a clean candidate; it is preserved, as are the six original caches. Original records and the frontmatter-omission disclosure stand.
