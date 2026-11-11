---
title: Issue 80 capacity line-754 diagnosis, critique
description: One native critique of the C3 diagnostic plan and proposed correction (not independent)
ms.date: 2026-11-10
---

Executed once on the final candidate plan, by the author, after the observations. Native, not independent. Verdict: plan acceptable as a proposal with the qualifications below; compatible findings applied directly.

* K1 (applied): the proof rests on one focused observation whose store lacks earlier stages' prior POSTs; the research states this limit and does not claim a replay of run 3.
* K2 (applied): observation 1 was a driver defect run and still counts against the budget; the pinned-main counterfactual is not claimed as run.
* K3 (applied): phases B and C deviated from the checker ordering; they are labelled observation-only and prove only the retry mechanism, not that the rest of the stage passes.
* K4 (applied): the flag must not suppress a genuinely unanswered retry; the plan keeps visible timeout behaviour and forbids timeout increases.
* K5 (accepted risk): a JSON 503 body would also unblock the stage but changes the failure being exercised and is therefore not preferred.
* K6 (accepted): after the correction later stages may fail for independent reasons; the plan requires reporting the actual first failure and does not promise a pass.
* K7 (noted): the research file changed after the `research-open` marker (the observation amendment); the witness verify is expected to record that qualification.
