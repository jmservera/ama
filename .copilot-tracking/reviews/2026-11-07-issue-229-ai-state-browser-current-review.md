# Review (current author review): issue #229 AI state browser check

Date 2026-11-07. Successor to `2026-11-07-issue-229-ai-state-browser-review.md`, which is preserved unchanged as the original review of the unexecuted-selector source. This record covers the corrected source at 68e43c448 (tree 9116515a2e528d479e4d769702045411aa854872), authored by the implementing agent. It is not an independent exact-head assessment.

## Assessed boundary

Child diff against declared parent 660716929: `data_operator_browser_check.py`, new `data_operator_ai_state.py`, new `test_data_operator_ai_state.py`, README paragraph, RPI records.

## Evidence read

* Original first browser run failed after 48 PASS lines on `exactly the two failed AI rows are listed` (preserved: `.copilot-tracking/evidence/2026-11-07-issue-229-ai-state-browser-run1-adverse.log`). Diagnosis: the running app legitimately records its own "AI is not configured" fallback (EX-004) when the landing view loads, so an exact count of two was a checker bug, not a product defect.
* Correction: each synthetic row (quarantined, fallback) must still appear exactly once (`row_text` asserts count 1); the workflow-only record must be absent; every failed AI row must say Quarantined or Fell back and carry the not-a-model-result phrase. No assertion was weakened for the keyboard, no-write, reflow or network-window checks; no retry or sleep was added.
* Corrected run passed: `.copilot-tracking/evidence/2026-11-07-issue-229-ai-state-browser-run2-pass.log` (100 PASS, `RESULT PASS (axe scan ran)`, axe incomplete empty).
* Refused parent-base gate: `tools/rpi-checks.py --changed --base 660716929...` was refused before any output or receipt because the runner requires current origin/main. A mistaken gate plan, preserved; superseded by the manual FOCUSED plan.
* web-design-guidelines: earlier 3000 character fetch was partial (historical); a complete fetch was later retrieved. No web file changed in this child, so there is no web surface to review against it.

## Outcome

No open material finding in the corrected checker. Meanings covered: explicit opening, Quarantined distinct from fallback, failed versus workflow-only versus unknown, unavailable result not all-clear, owner not an appointment, recovery a read-only placeholder with no operational audit-history claim, keyboard/text state meaning, bounded reflow, zero unexpected write/model requests (browser-observed).

## Acceptance gaps

* The "How it failed is Unknown" row is unreachable from real feeds; only the Node VM regression covers it.
* Request checks are browser-observed only, not a server-side audit.
* Constructed fixtures do not prove a serving model, employee effectiveness, accessibility acceptance, resident consent or named approval.
* No receipt: a deliberate manual FOCUSED selection (see the manual plan). Independent exact-head assessment, published parent target, hosted checks, and whole #229 criterion 4 (WCAG, AT, human) remain pending and unticked.
* Final selected-test results against the final head are recorded externally under `/tmp/zf229-scratch/final/`, not in this commit.
