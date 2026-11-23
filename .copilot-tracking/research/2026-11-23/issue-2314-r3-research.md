---
title: Research issue 2314 round 3
ms.date: 2026-11-23
---

Disposition: executed. Planning Readiness: Ready.

Rounds 1 and 2 covered rules, owners, runbook anchors and the literal parse pattern. Not yet covered: whether the saved query still groups correctly when the container console emits the structured JSON line (`StructuredFormatter`, `install_diagnostic_redaction(structured=True)`), where the AI_USAGE text sits inside a `body` field followed by `","attributes"...`. Angle: a behavioural test that applies the KQL `parse` pattern (as a regex) to the real emitter output, plain and structured, and checks Capability, Period, Calls, Tokens and UsageState. Owner-only items (deployment, named appointees) are skipped.
