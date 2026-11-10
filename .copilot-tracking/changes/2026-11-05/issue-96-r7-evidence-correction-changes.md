<!-- markdownlint-disable-file -->
# Changes: issue 96 r7 evidence correction

Refs #96. Added only these dated tracking files:

* `.copilot-tracking/research/2026-11-05/issue-96-r7-evidence-correction-research.md`
* `.copilot-tracking/plans/2026-11-05/issue-96-r7-evidence-correction-plan.md`
* `.copilot-tracking/changes/2026-11-05/issue-96-r7-evidence-correction-changes.md`
* `.copilot-tracking/reviews/2026-11-05/issue-96-r7-evidence-correction-review.md`
* `.copilot-tracking/rpi-sessions/2026-11-05/issue-96-r7-evidence-correction-state.json`

Corrects: the r6 final-return diagnosis ("about 3 MssqlApiTests skips") is superseded by the policy-qualified diagnosis in the research record (one out-of-policy Chromium launch-failure skip among 344 listed skips, 343 of them in `EXPECTED_SKIP_REASONS`), and the retention and process disclosure about `/tmp/ama-96-gate-r6`, scratch deletion, the 60-second interruption and long polling. The r6 research, plan, details, critique, changes, review and state files and the r5 research are unchanged. No application code, tests, policy, tooling or documentation outside `.copilot-tracking/` changed.

Preserved, untouched and not cleaned: `/tmp/ama-96-gate-r7/` (including `receipt.json`), `/tmp/ama-96-gate-r7.log`, `/tmp/ama-96-gate-r6.log`, `/tmp/ama-96-venv`, `/tmp/ama-96-pipcache`.

Validation: JSON parse of the state file and `git diff --check`. The focused code tiers (ruff, mypy, unittest) do not apply because no code changed; no full gate was run and no receipt exists for this candidate.
