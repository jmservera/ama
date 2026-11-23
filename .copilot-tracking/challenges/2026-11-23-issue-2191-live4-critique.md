---
title: Issue 2191 live pass 4 details and critique
ms.date: 2026-11-23
---

Critique (one pass, executed, verdict: proceed). Risk: importing the api package from infra tests couples projects; avoid by parsing `MAX_FAILURE_RATE` from the simulator source text. Risk: test restates implementation; accepted because it guards a cross-file contract that fails the job at start. Disposition: applied the text-parse approach.
