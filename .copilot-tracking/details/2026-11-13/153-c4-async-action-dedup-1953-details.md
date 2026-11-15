<!-- markdownlint-disable-file -->
# Details

## Phase 1

In `finish(error)`: compute `msg = String(error.message).trim()`. If it matches `/Owner:/` and `/Next (action|step):/`, set `status.textContent = \`${label}: ${msg}\`` (unchanged). Otherwise append `Owner: application support. Next action: check the recorded history before repeating anything. Try again if nothing changed; if it continues, contact application support.`

## Phase 2

Add a node-run test in `test_loading_feedback.py` rejecting with (a) a message already holding Owner and Next action, (b) one with Next step, (c) a plain one; assert exact preserved messages for (a)/(b), and exactly one `Owner:` and exactly one Next action/step label for all cases; neutral wording omits "repeating a change".

## Phase 3

Run test_content_standard, test_loading_feedback, test_case_journey, test_workflows, ruff, mypy in `/tmp/venv-153sc4-1953`.

## Critique dispositions

PC-001 and PC-002 applied directly (verdict Revise).
