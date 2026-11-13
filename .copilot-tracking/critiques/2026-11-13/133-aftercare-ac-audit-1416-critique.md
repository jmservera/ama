<!-- markdownlint-disable-file -->
# Plan critique: 133-aftercare-ac-audit-1416

* Reviewer: independent `rubber-duck` sub-agent; execution: executed once, before any test or probe
* Verdict: approve with changes

## Findings and dispositions

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | Blocking | AC4 overclaimed: the API carries outcomes, but the rendered table (`aftercare.js:170`) shows counts, not investigation outcomes | Applied: AC4 `NOT FULLY PROVEN`; API data and rendered view reported separately; the screen is verified in Phase 3 |
| PC-002 | Blocking | AC3 verdict exceeds evidence: code excludes a sensor-only basis but cannot show a person did not rely on a normal reading | Applied: AC3 claim limited to implemented safeguards; operational evidence recorded as unobserved |
| PC-003 | Blocking | FR-036 fields not fully mapped (prompt, thresholds, reviewer) | Applied: Phase 3 maps each FR-036 field against the `ai_registry` entry; served review and model release remain separate gates |
| PC-004 | Blocking | Execution safety: editable installs, inherited `ZF_RESIDENT_MSSQL=1`, broad `/tmp/venv-*` cleanup | Applied: `PYTHONDONTWRITEBYTECODE=1`, `unset ZF_RESIDENT_MSSQL`, `git status` check after install, remove only `/tmp/venv-133-1416` |
| PC-005 | Non-blocking | AC1 must not demand a digital route | Applied: digital absence is reported as a note, not a failed clause; accessibility and operational evidence remain the gap |
| PC-006 | Non-blocking | AC2 needs direct citations to unknown-owner creation and assignment | Applied: cite `aftercare_intake.py:467` and `673-691`; criterion `NOT FULLY PROVEN` |
| PC-007 | Non-blocking | AC5 denylist cannot prove a universal claim; wrong test name in research | Applied: separate inventory of generated and static text with counterexamples; `NOT FULLY PROVEN`; test name corrected |

No conflict with a confirmed user decision; no user decision required.
