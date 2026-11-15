---
title: 435 unified post-1542 rebase details
ms.date: 2026-11-13
---

## Details

* Resolve log.md conflicts by keeping every entry from both sides, in order.
* Any TSV conflict: take either side, then regenerate with `--write`.
* Do not edit the verifier. Report freshness as measured.
* Remove only the named venv path.
