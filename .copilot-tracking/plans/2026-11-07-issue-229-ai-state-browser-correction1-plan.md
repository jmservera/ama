# Plan: issue #229 AI state browser check, correction cycle 1 (successor record)

Successor to the original [plan](2026-11-07-issue-229-ai-state-browser-plan.md); original critique, Review and disclosures are unchanged. Date 2026-11-07.

## Adverse output (first actual run, base 4c58448b8, exit 1)

`AssertionError: exactly the two failed AI rows are listed`, after 48 PASS lines. Full log kept externally at /tmp/zf229-scratch/run1.adverse.log.

## Diagnosis (concrete checker/fixture bug)

A diagnostic on the same synthetic server shows three failed-AI rows: the two synthetic ones plus EX-004, ref 628cd4f0cf71, "Fell back to rules or template ... Reason: AI is not configured". The running app's own landing view writes a real fallback task record because no model is configured. My assumption that only the fixture records would appear was wrong; no product bug.

## Bounded correction (checker only, nothing weakened)

Replace the exact count with two checks: both synthetic rows are present exactly once (already asserted) and every listed failed-AI row states either Quarantined or Fell back, and none claims a model result. Workflow-only absence stays asserted by id. Rerun the targeted regression and the actual operator journey. Correction cycle 1 of at most 2.
