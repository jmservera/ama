# Changes: issue 2206 round 2 (2026-11-21)

Tier: focused (tools and docs only; no src change). Files: tools/demo_preflight.py, tools/test_demo_preflight.py, docs/reference/research/issue-2206-demo-preflight-2026-11-21.md, docs/reference/log.md.

Validation: `python3 -m unittest tools/test_demo_preflight.py` (7 pass), ruff check and format clean, two live runs (the second 8 pass, 0 fail, 2 unavailable). rpi-checks --all not run; hosted CI not observed.

Divergence: the tool edits and the live in-network exploration happened before the implement-start witness (it recorded a dirty-source qualification). Live exec used one SELECT only, nothing written, no Azure resource created.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Checks revisions, job statuses, health without printing secrets | Proven | live runs in research note; cold-start false failure fixed and tested |
| Checks cohort and consent counts | Partly proven | in-network read-only SELECT: 20 homes, 10 granted, 10 declined; logic tested with fakes; script run from this host reports UNAVAILABLE (SQL private) |
| Output usable as runbook preflight record | Proven | timestamped Markdown table with summary; runbook not edited |

Unproven: job-live-receiver failure cause (Log Analytics blocked by network perimeter); script-run counts from inside the network. Nothing ticked on the issue.
