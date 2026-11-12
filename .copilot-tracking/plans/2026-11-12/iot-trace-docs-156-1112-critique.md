<!-- markdownlint-disable-file -->
# Critique: iot-trace-docs-156-1112 (single independent critique)

* Executed once by a separate read-only agent (rubber-duck, fresh context) before any edit. Verdict: Revise. Not repeated.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | High | Five homes is the owner-selected target cohort, not an enforced limit; the control cap is 100 (`live_control.py:28`, runbook rows 55-60) | Applied: wording says target cohort and unenforced; plan and row 5 corrected |
| PC-002 | Medium | "No pause control" overlooks the library pacer pause state (`sensor_stream.py:321`) | Applied: library pause acknowledged; gap limited to an operator-facing pause or replay surface not found in the bounded trace |
| PC-003 | Medium | "No accessibility evidence" conflicts with historical synthetic browser/axe runs (cutover pack ~5744) | Applied: distinguishes recorded automated synthetic evidence from missing human, assistive-technology and design acceptance; no acceptance claimed |
| PC-004 | Medium | "No IoT-to-UI flow specification" exceeds what was inspected | Applied: states only that the cited design note supplies none |
| PC-005 | Medium | Changes and review records exceed the three-file deliverable | Rejected: conflicts with the confirmed user direction to commit original dated RPI evidence (research, plan, details, critique, changes, review); no re-ask |
| PC-006 | Low | The gate parses reference definitions globally | Applied: the new section adds no link reference definitions, only inline links |

Unverified by the critic: live 2026-11-12 issue states and historical browser witness files. The section states issue states as read on that date and treats "no deployed job started" as a dated source-record statement.
