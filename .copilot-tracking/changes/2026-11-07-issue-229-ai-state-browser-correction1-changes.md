# Changes: issue #229 AI state browser check, correction 1 and actual browser run (successor record)

Original [changes](2026-11-07-issue-229-ai-state-browser-changes.md), [review](../reviews/2026-11-07-issue-229-ai-state-browser-review.md) and critique are unchanged. Plan: [correction plan](../plans/2026-11-07-issue-229-ai-state-browser-correction1-plan.md).

## Admission and environment

Coordinator admitted the sole bounded browser/FOCUSED run. Own venv /tmp/zf229-scratch/venv (pip, no uv): playwright 1.64.0 (repo pin) from that venv, zava_forward.core and zava_forward.api resolve to this worktree's src (editable), Chromium 1248 from the playwright cache. Pinned axe copied from the 1262 immutable bytes, SHA-256 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb verified before and after copy. Run under `flock -n /tmp/ama-rpi-heavy.lock`, PYTHONDONTWRITEBYTECODE=1, ZF_AXE_REQUIRED=1, TMPDIR external.

## Run 1 (adverse, source 4c58448b8): exit 1

48 PASS then `AssertionError: exactly the two failed AI rows are listed`. Log: [run1 adverse](../evidence/2026-11-07-issue-229-ai-state-browser-run1-adverse.log). Diagnosis: the running app's own landing view records a real fallback "AI is not configured" task (EX-004); the exact-count assumption was wrong. This also shows the real server made no model result. The first run therefore did not prove the original selectors; the earlier "unexecuted selectors" disclosure stands for everything before this run.

## Correction

Only `src/api/checks/data_operator_browser_check.py`: the exact count became "both synthetic rows present once each (unchanged) and every failed-AI row says Quarantined or Fell back, none claims a model result". Workflow-only absence is still asserted by id. No product, API, role, security, schema, SQL or model change; no retry or sleep.

## Run 2: exit 0

`RESULT PASS (axe scan ran)`, 100 PASS lines, `INFO axe incomplete: []` twice, no writes, no model or AI requests after the register interaction (browser-observed), 320px and 1280px reflow, Tab reach. Log: [run2 pass](../evidence/2026-11-07-issue-229-ai-state-browser-run2-pass.log). Also: ruff exit 0, mypy exit 0, test_data_operator* 12 tests exit 0.

## web-design-guidelines refresh

Full source retrieved 2026-11-07 (first 3000 characters plus the remainder; earlier partial fetch remains historical). No web file changed; the changed checker is Python. Checked against the rules: the checker verifies the link is native `<a>` operated by keyboard, empty and unavailable states, reflow and focusable labelled table regions on the existing UI. No findings against changed files. Not whole WCAG or AT evidence: one synthetic home, one role, axe automated only.

## Limits

Constructed synthetic fixtures; no serving model, employee effectiveness, accessibility acceptance, resident consent or named approval shown.
