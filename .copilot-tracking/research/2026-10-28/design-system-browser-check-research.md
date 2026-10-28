---
title: Design-system browser timeout research
ms.date: 2026-10-28
---

## Brief and controls

Focused convergence research for the full RPI loop explicitly requested by the
owner. Reproduce PR #517's synthetic design-system check on current main;
distinguish app regression from harness or external-network flake. No .env,
private datasets, uv, Docker builds or cloud calls. Keep artifacts brief.
Research root: `.copilot-tracking/research/2026-10-28/`.
Questions: which wait fails; why; what minimal fix retains its behavioral contract?

## Extensions and participation

Repository instructions and rpi-research selected. Browser tooling is relevant;
visual-design skills are not applicable to harness-only investigation.
No independent research lane: this is one continuous trace. Owner's full-loop
request authorizes automatic phase progression and requested branch publication.

## Cycle 1

### Wider

C1: PR #517 run 40669837186 job 122763595736 fails in
`src/api/checks/workbench_browser_check.py:271`, called by the design-system
entry point. All preceding map/design-system assertions pass. The failing wait
looks for the initial held briefing's "Reading your cases..." state.
Evidence: hosted failed-job log retrieved 2026-10-28.

C2: Branch `fix/design-system-browser-check` is clean, has no prior PR, and
starts at origin/main `197e5e3c6d4f7cfb135c9a985af3f13e0f688ac4`.
Candidate merges #514 and #516 affect workspace readiness and briefing scope.

### Deeper

C3: Exact entry point reproduced the same 30-second timeout locally using pip
installed project dev extras and Playwright Chromium. Baseline log:
`/tmp/ama-browser-check-fix-baseline.log`. The check owns its synthetic JSON,
ephemeral port, sanitized environment and server lifecycle.

C4: `src/api/src/zava_forward/api/web/app.js:260` now renders "Reading case
summaries..."; #516 changed that text from "Reading your cases...".
`src/api/checks/workbench_browser_check.py:271` still requires the old text,
and its later disappearance assertion also uses the old text. Its mocked
success payloads also omit the new scope/count fields rendered by #516.

### Contrarian

C5: With every non-loopback request aborted and the briefing response held,
the real app rendered exactly one held request and "Today's briefing /
Reading case summaries...". Releasing a current-contract synthetic payload
rendered successfully. An initial diagnostic used an ambiguous `section.ai`
locator (priority advice is another section); the corrected scoped probe passed.
This rejects cdnjs/axe and shared-script readiness as causes of this timeout:
the failing wait is on stale literal text, not readiness or network progress.

## Parent synthesis and alternatives

Accept C1-C5: fix only the harness, not correct programme-neutral app wording.
Keep cancellation, stale-response rejection, cache and selected-mode retry
assertions; use a heading-scoped visible loading locator and update its
disappearance assertion. Supply complete scope/count response fixtures and
assert them so successful rendering cannot hide undefined/NaN values.
Reject timeout increases, skips, sleeps and accepting either stale/current copy.
No further cycle is needed: exact failure, cause and counter-hypothesis are
covered by hosted logs, source diff and local real-browser reproduction.

## Disposition and readiness

Research disposition: executed. Planning Readiness: Ready.
