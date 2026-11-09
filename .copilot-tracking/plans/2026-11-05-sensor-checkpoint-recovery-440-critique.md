---
title: Sensor checkpoint recovery critique (Refs #440 #184 #110)
description: Single final-candidate critique of the plan and details
ms.date: 2026-11-05
ms.topic: reference
---

* Execution: once, self-critique against the task constraints and the research artifact. Verdict: proceed with applied findings.
* Finding 1 (applied): BRD and PRD share requirement numbers with different meanings (FR-048, FR-050). The record must always document-qualify them and state the collision.
* Finding 2 (applied): "Covered merged PRs" #1209 and #1210 are tooling only; the record must say they do not establish sensor acceptance so the trigger is not read as coverage.
* Finding 3 (applied): the 64 versus 128 UTF-16 home-key asymmetry is documented and deliberate in the main core README; record it as a boundary, not as a new defect.
* Finding 4 (applied): do not attempt `tools/rpi-checks.py --changed` because it acquires the shared heavy lock; list it as unperformed, not passed.
* Finding 5 (compatible, applied): older observations (2026-10-27 to 2026-11-04 research plan and fourth checkpoint) are imported only as dated historical receipts with original heads.
* No finding conflicts with a confirmed owner decision. No significant or divergent issue needs a user decision. The critique is not repeated.
