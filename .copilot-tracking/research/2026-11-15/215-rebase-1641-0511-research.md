---
title: "Research: Rebase #215 regulatory alerts and home chat suites onto PR #1641"
description: "RPI research artifact for rebasing the unmerged #215 accessibility, role-matrix, consent-boundary, and provenance commits onto origin/feat/demo-164-chat-grounding-provenance-0900 (d8cb35d25)"
ms.date: 2026-11-15
---

## Research Brief

* Topic: Rebase `#215` regulatory alerts and home chat WCAG 2.2 AA, role matrix, consent-boundary, and provenance test commits (`a3a9030be..d273b99d6`) in worktree `/home/azureuser/source/ama-demo-wt/test-215-visit-consent-0600` (branch `test/demo-215-visit-schedule-consent-boundary-0600`) onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`d8cb35d25`, PR #1641).
* Purpose and audience: Prepare a conflict-clean, contract-aligned rebase and run the focused `#215` API/web test suites, `ruff`, and `mypy` without pushing.
* Scope and non-goals: Rebase unmerged `#215` commits onto `d8cb35d25`, align `#215` assertions and module aliases with PR #1641's upstreamed chat provenance/plain-language/consent contracts, validate with `unittest`, `ruff`, and `mypy`, and freeze the worktree with dated RPI artifacts. Non-goals: pushing to `origin`, live Azure OpenAI calls, browser/screen-reader execution, or claiming full `#215` staff comprehension acceptance.
* Output mode: `convergence`.
* Research posture: `focused` (bounded internal rebase with named commits, target SHA `d8cb35d25`, and explicit test suite list; no-interaction rationale: autonomous non-interactive execution with unambiguous caller specification).
* Research disposition: `executed`.
* Planning Readiness: `Ready`.

## Extension Provenance

* Selected: `.github/copilot-instructions.md` (`applyTo: "**"`, repository governance, focused validation tier, commit trailer, no-push constraint) and `rpi-research` skill.
* Skipped: `web-design-guidelines` / frontend taste skills (no web UI layout or styling redesign is performed; `chat.js` and `style.css` remain at upstream `d8cb35d25`); `RPI Researcher` subagent skipped in favour of direct inline git/file inspection (low-volume, tightly coupled commit-ancestry trace).

## Cycle 1 Execution

### Wider Wave

* `C1` (`docs/reference/log.md:1`): Merge-base between `HEAD` (`d273b99d6`) and `origin/feat/demo-164-chat-grounding-provenance-0900` (`d8cb35d25`) is `0578458d4`. There are 22 commits in `0578458d4..d273b99d6`.
* `C2` (`src/api/tests/test_regulatory_a11y_cues.py:1`): The first 10 commits (`a3a9030be..680ca9a87`) are byte-for-byte identical in cumulative tree diff to squash commit `c42fceed7` (`#1576`), which is already an ancestor of `d8cb35d25` alongside follow-on `#215` PRs `#1651` (`1395ec9ed`), `#1690` (`897c91465`), and `#1718` (`315f1e8a7`).
* `C3` (`src/api/tests/test_alert_chat_provenance_audit_contract_215.py:1`): The remaining 12 commits (`680ca9a87..d273b99d6`, i.e., `799909e72` through `d273b99d6`) are unmerged upstream and contain 11 test modules plus one `chat_case_answers.py` wording update (`83957d33e`) and one `mypy` annotation fixup (`dceb6bdf7`).
* `C4` (`src/api/tests/test_epic215_doubt_route_held_state_wcag_parity.py:1`, `src/api/tests/test_epic215_role_alert_owner_clock_safe_action_matrix.py:1`): Commits `fb322c4b8` and `70464f5ff` wrote `test_epic215_doubt_route_held_state_wcag_parity.py` and `test_epic215_role_alert_owner_clock_safe_action_matrix.py`, whereas the caller's validation selector requests `test_alert_chat_doubt_held_parity_215.py` and `test_alert_chat_owner_clock_safe_action_215.py` (mirroring earlier `#215` stable module aliases such as `src/api/tests/test_alert_chat_keyboard_provenance.py:1`).

### Deeper Wave

* `C5` (`src/core/src/zava_forward/core/chat_case_answers.py:20`, `src/core/src/zava_forward/core/chat_case_answers.py:366`): Upstream `d8cb35d25` refactored `_unblock(r)` to emit citable workflow rules `CHAT_BOUNDARY` (`workflow/chat-boundary`), `SAFETY_SEQUENCE` (`workflow/safety-sequence`), and `VISIT_CONSENT` (`workflow/visit-consent`), and placed `"unblock"` in `RULES_FIRST` (`src/core/src/zava_forward/core/chat_case_answers.py:25`, `src/core/src/zava_forward/core/chat_panel.py:874`). Commit `83957d33e` conflicts in `_unblock(r)` because it predated `RULES`; `VISIT_CONSENT` on `d8cb35d25` mentions resident consent recording via the case consent control, and adding explicit resident consent-and-access confirmation wording to `VISIT_CONSENT` preserves both PR #1641's `RULES` contract and `#215` visit-consent-and-access assertions without using banned internal terms (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`).
* `C6` (`src/core/src/zava_forward/core/chat_panel.py:97`, `src/api/src/zava_forward/api/web/chat.js:69`): Upstream `d8cb35d25` standardized provenance labels in `SOURCE_LABELS` (`"Deterministic decision or workflow rule (not generative AI; no record changed)"`, `"Generative model suggestion (unapproved; check cited sources; no record changed)"`, `"Withheld: ..."`) and `chat.js` (`RULE_LABEL`, `MODEL_LABEL`, `WITHHELD_LABEL`). In addition, `chat.js` (`src/api/src/zava_forward/api/web/chat.js:294`, `src/api/src/zava_forward/api/web/chat.js:367`) updated `regulatoryPlainMode` (`<div class="regulatory-mode">` wrapping `<label for={id}>` + polite state span), added `"aria-labelledby"` and `regulatoryStateLabel(alert.result)` on `<article class="regulatory-alert">`, changed `"Inference is disabled"` to `"No AI model is used"`, and passed `plain_language` in `employeeChat` API requests.
* `C7` (`src/core/src/zava_forward/core/chat_panel.py:868`): Because `unblock` is now in `RULES_FIRST`, `"what can I do to unblock this case?"` and `"how can we fix this safety? Should we schedule a visit?"` always execute rules-first (`answer_source == "decision-rules"`, `answer_origin == "decision_rule"`, `model == "workflow-only"`, 0 model calls) and return both `ZF-4/*` and `workflow/*` citations. Non-`RULES_FIRST` case prompts (`"review what is blocking it"` with intent `"blocked"`, and `"Please summarise this case"` with intent `None`) still exercise `generative-grounded`, `decision-rules-fallback` (when `grounded_answer` covers `"blocked"`), and `withheld` (when `grounded_answer` abstains and the generative draft contains an unsupported claim).

### Contrarian Wave

* Alternative A (rejected): Plain `git rebase origin/feat/demo-164-chat-grounding-provenance-0900` from merge-base `0578458d4`. Rejected because `a3a9030be..680ca9a87` were squash-merged as `c42fceed7` (#1576) and subsequently modified by `#1651`, `#1690`, and `#1718`; replaying the 10 pre-squash commits individually causes avoidable patch conflicts against files already merged and evolved upstream. `git rebase --onto origin/feat/demo-164-chat-grounding-provenance-0900 680ca9a87` cleanly skips the squash-merged prefix while preserving every unmerged commit (`799909e72..d273b99d6`).
* Alternative B (rejected): Removing `"unblock"` from `RULES_FIRST` so old `#215` tests keep getting `generative-grounded` on unblock/visit questions. Rejected because PR #1641 (`798cb888c`, `src/api/tests/test_chat_panel.py`) intentionally routes unblock/visit questions rules-first for safety and determinism (`Refs #164, Refs #159`). Instead, `#215` tests should assert `decision-rules` (with `workflow/*` + `ZF-4/*` citations) on `RULES_FIRST` unblock/visit questions and use non-`RULES_FIRST` case questions (`"review what is blocking it"`, `"Please summarise this case"`) to test `generative-grounded`, `decision-rules-fallback`, and `withheld` paths.
* Environment risk identified: `pip list` shows `zava-forward-*` editable installs currently pointing at a removed sibling worktree path (`/home/azureuser/source/ama-demo-wt/feat-164-chat-revocation-0042/src/*`). Installing `-e src/core -e src/agents -e src/api` (`--no-build-isolation --no-deps`) in this worktree is required before running `unittest` and `mypy`.

## Synthesis and Readiness

* Selected approach:
  1. Fetch `origin/feat/demo-164-chat-grounding-provenance-0900` (`d8cb35d25`) and run `git rebase --onto origin/feat/demo-164-chat-grounding-provenance-0900 680ca9a87` on `test/demo-215-visit-schedule-consent-boundary-0600`, resolving `src/core/src/zava_forward/core/chat_case_answers.py` in `83957d33e` by retaining `d8cb35d25`'s `RULES`/`_unblock` implementation with explicit resident consent-and-access confirmation in `RULES[VISIT_CONSENT]`.
  2. Reinstall editable `src/core`, `src/agents`, and `src/api` packages from this worktree.
  3. Reconcile the unmerged `#215` test suites with PR #1641's upstreamed `chat.js` markup/labels, `SOURCE_LABELS`, `RULES_FIRST` routing, and `workflow/*` rule citations, and add stable test module aliases `test_alert_chat_doubt_held_parity_215.py` and `test_alert_chat_owner_clock_safe_action_215.py`.
  4. Validate all 8 requested `#215` suites (plus sibling `#215` web/core/api suites), `ruff check src/api/tests`, and `mypy` in `src/api`, then commit reconciled changes and dated `.copilot-tracking/` artifacts without pushing.
* Validation tier: Focused (test reconciliation plus a single plain-language rule-string refinement in `chat_case_answers.py`; no infrastructure, SQL schema, dependency, workflow, Dockerfile, or security-control weakening).
* Planning Readiness: `Ready`.
