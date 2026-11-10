---
title: "#184 post-policy validation author review"
ms.date: 2026-11-09
---

Author review of [changes](../changes/2026-11-09-live-simulator-postpolicy-184-changes.md), executed once, not independent. It does not replace the independent exact-head functional assessment that follows. Review findings route to later work; no second review runs in this task.

## Outcome

* Execution: executed once. Outcome: conditionally conformant for the demo-targeted tier, with open items below. No finding is hidden: two defects of the earlier recovery pass (format, project typing) were found by this validation and fixed without behavior change; one flaky pre-existing test failed once.
* Ordering: research, plan, details and the single critique were committed (90d3ee293) before the merge and any check. Original diagnosis-before-records disclosure of the earlier recovery pass is untouched and still applies to it.
* Main reconciliation: pinned 76db469b merged cleanly; ancestry confirmed. origin/main has since advanced to 1f28d0913 (unrelated #1222); a later local merge is for the coordinator.
* Actual SQL: default 70 tests and analysis 10 tests, zero skips, exit 0, six selectors and ten pinned names matched. Offline skips (13) are separate and not SQL proof.
* Runner tuple growth: exactly two names; no logic change; no skip-blind escape in the analysis path. The default selector remains exit-status only by design, so zero skips there rests on the parsed log of this run, not on the harness. This is a residual (a future change could add a count/skip check; not made here).
* Guards (cap 100, 14 day expiry, admin cohort, replay, window, dedup, weather exclusion, consumer data-quality) are covered by passing tests mapped in the changes record.

## Open and residual

* Open Low (C5, unchanged, not independently closed): exact-grant live_receiver.main entrypoint and rejected data-quality under receiver grants have no test.
* F1 flaky send-rate test: first failure kept, three isolated reruns and the final run pass; separate fix draft needed; not waived.
* mypy in src/api shows 48 non-parent errors (46 absent playwright stubs in this venv, 2 in unchanged main tests); hosted CI must confirm. Template-specific infra tests for the two live jobs do not exist (build and lint only).
* Not proven: hosted CI, independent exact-head review, browser checks (none applicable), children #185 and #188 acceptance, credential and log lifecycle (AC3 partial), actual Hub-to-SQL-to-UI-to-Quality-model run, human acceptance, #140 and #110. Issue #184 AC1 stays unmet; no closing keyword is justified.
* Permanent higher-risk full tier is not satisfied; the owner's demo-targeted authorization is the only basis for this tier and is not a full-gate or receipt claim.
