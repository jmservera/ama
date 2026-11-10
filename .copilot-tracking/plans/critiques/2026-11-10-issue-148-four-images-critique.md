<!-- markdownlint-disable-file -->
# Critique: issue 148 four-workload image wiring (the one final-candidate critique)

Readback 2026-11-10T01:33Z. Executed once, by the implementing agent without a nested agent (instruction forbids nesting), against the plan and details before any source edit. Verdict: `proceed with direct amendments`. No significant or divergent issue; no user decision needed.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | Treating an `az` failure on `show-tags` as "missing" can hide an auth or network fault. | Applied: report as "missing or unreadable" and keep the az exit status in the message. |
| 2 | Mutable tags: a resume could accept a stale same-tag image. | Accepted residual; digest pinning belongs to the pipeline/contract and is listed out of scope. |
| 3 | Dependency deploy (`deployApplications=false`) still lets deploy.py guess the orchestrator. | Rejected: applications are not deployed and no job image is used at that stage; changing it widens scope. |
| 4 | `_require_images` needs `found['registry']`; direct use before `discover` would KeyError. | Applied: raise `RebuildError("Discovery incomplete")` when absent. |
| 5 | Wrapping `ScriptExit` in `RebuildError` loses `.code`. | Accepted: nothing tolerates a build exit; the cause chain keeps it. |
| 6 | New reserved names could break existing overrides. | Verified: existing tests/parameters use none of them; keep. |
| 7 | Doc drift in shared READMEs. | Out of ownership; reported in the handoff, not edited. |
