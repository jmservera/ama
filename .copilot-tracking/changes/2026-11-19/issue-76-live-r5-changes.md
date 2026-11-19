# Changes: issue-76-live-r5

Files: docs/reference/research/issue-76-live-r5-2026-11-19.md (new), docs/reference/README.md, docs/reference/log.md. No src change; tier FOCUSED (documentation plus read-only checks). mypy/ruff not applicable. No Azure resource created.

Validation: 35 unittest tests OK (src/core, three files named in the note); az revision read-only.

| Criterion | Verdict |
| --- | --- |
| Default view single list, one status, one next action | Already ticked |
| No perspective picker | Already ticked |
| Queue with visible definitions | Already ticked |
| Blocked steps reason, owner, next action | Already ticked |
| Hazard and safeguarding items show clock and named owner | Proven for demo (safeguarding fully; hazard clock and owner shown, times Unknown by design; owner decides if Unknown suffices) |
| Views agree (FR-034) | Already ticked |
| Single reset (FR-032) | Already ticked |
