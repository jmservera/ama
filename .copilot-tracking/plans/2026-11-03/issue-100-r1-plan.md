# Plan: issue 100 r1 AI usage and alerts panel

Details: .copilot-tracking/details/2026-11-03/issue-100-r1-details.md

* [x] Add `assetUsage` panel to the asset-board screen in role-screens.js.
* [x] Tests in test_asset_board_screen.py: values, alerts, Unknown not zero, no token cost, no controls, report unavailable.
* [x] Update atlas-screen-trace.md row and append log.md.
* [x] ruff, ruff format, mypy (--cache-dir=/tmp/mypy-100) and focused unittest.

Stacked slices after this one: per-capability breakdown once the API exposes it; limit values after OD-51; stabilization checkpoint #440 owned separately.

Critique (executed once, inline): compatible. Keep read-only (no approval or consent action), reuse existing helpers and Fluent classes, state AI-unavailable behaviour and manual path, never show tokens as cost, avoid inventing limits. Verdict: proceed. Not security, infrastructure, SQL or deployment: focused tier.
