---
title: Issue 344 live research, tenth pass (2026-11-23)
---

Refs #344. Research disposition: executed. Planning Readiness: Ready.

Scope: compare criteria 1, 3, 4 and 5 (unticked) with `main` at `ed9500a188` and live revisions `ca-cutover-test-demo-api--0000054` and `ca-resident-demo--0000026` (both active, 100 percent traffic). `src/` and `infra/` have no drift since the ninth pass.

Method: reran the ninth-pass Playwright and read-only Azure probes. Full findings and the per-criterion table are in [the research note](../../../docs/reference/research/public-browser-access-live-r10-2026-11-23.md); raw evidence is in `.copilot-tracking/evidence/2026-11-23/issue-344-live/`.

Result: all ninth-pass observations reproduce. Criteria 3 and 4 proven; criterion 1 partly proven (browser User-Agent gets 302 under `RedirectToLoginPage`; fix is an owner-gated infrastructure change); criterion 5 unproven (MVP retired, one role walked, Blocked rows #349/#350/#210). `/api/ai/report` 500 has no recoverable cause (no Log Analytics workspace). No code gap is fixable and testable within authority.
