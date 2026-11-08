---
title: Details, final fixture-only validation round r5 (issue 1204)
ms.date: 2026-11-06
---

## Method

* Designer receives the full target, issue criteria, catalog, rubric, design template, the prior design as factual setup material and the three correction requirements as fixture requirements (not oracles for the executor).
* Lead validation gate before execution: recompute every capacity row (hierarchy, PRs, assignments kept separate; seven retained means one free slot, eight means zero); H-03F has a ready issue, full branch, worktree, hash, log facts and a literal launch outcome; H-06 uses only canonical .copilot-tracking paths, phase logs, full pins, tier, receipt, head, base and target facts and includes a positive batched stack publication; F-03 facts all supplied with no ellipsis or truncated hash. If a gap remains, do NOT execute; record Partial and stop.
* Executor reads only the target, its executor state and scenario prompts (requests and supplied facts only, no oracles, hints or criteria names).
* Grader derives expected outcomes from issue criteria and target first, separates target defect, executor error and fixture defect, treats unexercised contracted behavior as a miss.
* Persist verbatim returns with hashes externally and in the sandbox; capture host subagent.completed attribution with no model override.
* Known exception: verbatim traces may contain trailing whitespace and Unicode and are not normalised; git diff --check is reported excluding them explicitly.

## Critique amendments (applied directly)

* Lead gate additionally verifies: H-03F successful launch outcome and post-count of eight; H-06 current head, base, target-check facts and the declared stack; every publication row.
* Executor state is written fresh, inspected for leaked oracles, and states all actions are emulated, including publication.
* A hash manifest binds target, executor state, exact prompts, traces and telemetry before and after dispatch.
* The grader receives the finalized design, prompts, verbatim trace, test log, target, issue criteria, catalog and rubric, and no prior grading conclusions or reports.
