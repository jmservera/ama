# Changes: issue 2206 (2026-11-21)

Tier: focused (tools and docs only; no src change). Validation: `python3 -m unittest tools/test_demo_preflight.py` (6 pass), ruff check and format clean, live run recorded. rpi-checks --all not run (coordinator owns gates). Hosted CI not observed.

Files: tools/demo_preflight.py, tools/test_demo_preflight.py, docs/reference/research/issue-2206-demo-preflight-2026-11-21.md, docs/reference/README.md, docs/reference/log.md.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Checks revisions, job statuses, health without printing secrets | Proven | live run in research note; tests |
| Checks cohort and consent counts | Unproven live (logic proven with fakes) | SQL public access disabled; row reports UNAVAILABLE |
| Output usable as runbook preflight record | Proven | timestamped Markdown table with summary |

Nothing ticked on the issue. Divergence: none. Finding: job-live-receiver last four executions Failed.
