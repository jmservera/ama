# Changes: #216 regulatory verification (1143)

Status: complete. Base 3b05143179f83235c5b4e80e70aad99bdc44d83f. Write surface: .copilot-tracking only; no src/ or docs/ edits (post-run `git status` showed only tracking files).

Environment: Python 3.12.3, setuptools 84.2.1, venv /tmp/venv-216-1143 (removed), editable installs of src/core, src/agents, src/api with --no-deps --no-build-isolation. Import origins: `src/core/src/zava_forward/core`, `src/agents/src/zava_forward/agents`, `src/api/src/zava_forward/api`, all inside this worktree. Runs used `env -u ZF_DATA -u ZF_TEST_MSSQL python -m unittest -v <modules>`, PYTHONPATH `tests` (core), `tests:../core/tests` (agents), `tests:../core/tests:../agents/tests` (api). No Docker, browser or model calls; two API-side loopback tests are in-process only.

## Results (true producer exit codes saved straight from `$?`)

| Package | Exit | Tests | Skips | Log sha256 |
| --- | --- | --- | --- | --- |
| core | 0 | 167 | 7 | dacbd659db35e9f096dcd15937981a40b57421170b864a9e84c598a44be7f99b |
| agents | 0 | 51 | 0 | 149510056a8dfa4024cf9e1efbb1d5026ad7a9cf3cbb6398909e27f927e3d182 |
| api | 0 | 40 | 0 | c1abb4295c73a2f1c205eda35eb94af4c4d2d1c32089b05c6c77640b3f7b3ac6 |

Per-module counts:

* core: test_ai_statement_sources 11, test_chat_case_funding_sources 4, test_import_refusals 21 (7 skipped), test_regulatory_chat 25, test_regulatory_privacy 18, test_regulatory_usage 6, test_rule_engine 30, test_rulecards 17, test_source_freshness 6, test_source_monitor 29
* agents: test_alert_triage 7, test_candidate_comparison 19, test_regulatory_answers 7, test_regulatory_gates 18
* api: test_regulatory_at_record_check 7, test_regulatory_chat_api 12, test_regulatory_comprehension_score 6, test_regulatory_ux_check 8, test_rule_alerts 7

Explicit skips: 7 in core test_import_refusals.MssqlProjection, reason `opt-in task-owned loopback SQL` (MSSQL not started by design).
Excluded: test_dependency_rule in each package (boundary tests), all browser checks.

## Acceptance boundaries (issue text as read from `gh issue view`, read-only)

#215 unchecked: "WCAG 2.2 AA: no colour-only status, keyboard operable, plain-language mode"; "Comprehension tested with repairs, housing and grants staff before use". Offline unit tests (test_regulatory_comprehension_score, test_regulatory_ux_check) do not satisfy either: no human or browser evidence is claimed.

#216 unchecked: "Citation validity and refusal accuracy gates set with owners and measured on a graded and adversarial set"; "Paired comparison reports value of chat over deterministic cards with links; if no measured value, ship cards alone"; tokenomics "The paired comparison with deterministic rule cards reports AI cost per accepted check ...". These tests pass on fixtures only; no owner-set thresholds, live-model measurement or hosted CI are claimed.

Not run: hosted CI, browser/Chromium, MSSQL, full local gate. Logs held externally at /tmp/216-out (not committed).
