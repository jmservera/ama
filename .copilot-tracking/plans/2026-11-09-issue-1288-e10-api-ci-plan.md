---
title: Issue 1288 E10 API CI failures plan
ms.date: 2026-11-09
---

# Issue 1288 E10 API CI failures plan (prospective)

* Research: original CI for 581207 (log `ci1331-api-original.log`): 2546 discovered, 547 skipped, 2 failures in the API unit step.
  * `test_case_journey...test_both_chat_submissions_clear_only_successful_unchanged_raw_questions` last asserts the literal `["ai", "AI assistance", [assistantPanel, chatPanel,` in `app.js`. The Quality work intentionally inserted `simulationPanel()` between them (`app.js:1063`). The regression intent (successful-only clearing for both chat submissions) is covered by the preceding behavioral Node script, which is unchanged. The literal is a stale structure pin.
  * `test_content_standard...test_no_internal_terms_in_web_copy`: `assistants.js:26` uses the banned internal term "holds".
* Plan: (1) update the literal pin to include `simulationPanel(),` in order, no assertion removed; (2) change the copy to "still includes" (same meaning). Web guidelines fetched fresh from the owner-specified source before edit; Fluent 2, WCAG and plain-language standards prevail. Reproduce both failures red first.
* Validation: whole `test_case_journey` and `test_content_standard` modules, API ruff/format/mypy, the E9 Quality browser check with axe under one non-queued `flock -n /tmp/ama-rpi-heavy.lock` admission (its copy assertion is checked for dependence). No Core, Agents, full API, SQL, model or cloud runs.
* Counters: E10 is the final productive correction; none remain after it. Real-provider route OFF.
* Arithmetic supersession: the inherited "861" and "761 non-skipped" claims in earlier prose (including E8 and E9 notes) are superseded. `verified-1288-main-integration-counts.json` lists 19 per-log rows: Core 231 + API 471 + infra 59 = 761 discovered, 100 skipped, 661 non-skipped. Agents 303 and E9 browser 30 are separate, not a deduplicated total. Original records are not rewritten.
