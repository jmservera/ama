<!-- markdownlint-disable-file -->
# Plan critique: five synthetic demo homes (2026-11-12, Refs #134 #184)

Task `five-home-script-134-1112`. Executed once (rubber-duck subagent, not independent of the author's context). Verdict recorded separately from execution.

* Execution: complete, one pass. Verdict: Revise.
* No finding conflicts a confirmed owner decision; no owner decision required. All findings applied directly.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | Blocking | Preflight checks only the simulator cohort; source still scans every open case, so an operator could trigger a broader paid scan | Applied: details and runbook require evidence that the effective AI scope is the five homes before any analysis trigger; otherwise use route E |
| PC-002 | Blocking | Validation lists a second generator replay | Applied: removed from validation. Note: before this critique the author had already run two local replays during research (byte-identical); recorded truthfully in changes, no further replay |
| PC-003 | Non-blocking | Count match (980/443) does not independently verify the five ids; replay script was uncommitted | Applied: ids attributed to the recorded local replay only; replay probe and output preserved in the coordinator folder for the next lane, not committed |
| PC-004 | Non-blocking | Plan overstated owner selection of the homes | Applied: operating mode is owner-selected; the five ids are replay-selected by a stated rule |
