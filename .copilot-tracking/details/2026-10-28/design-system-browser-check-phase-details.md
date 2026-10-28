---
title: Design-system browser fix phase details
ms.date: 2026-10-28
---

Task: design-system-browser-check. Research C1-C5 is sufficient; no open choice.

<!-- rpi:phase id=P01 -->
## P01: Harness correction

<!-- rpi:task id=P01-T01 -->
### P01-T01

Replace obsolete `.ai` text polling with a visible, heading-scoped locator for
"Reading case summaries...". Update disappearance check to the same current text.
Use scope_label, case_count and summary_count for each mocked success; verify
the current response renders the assigned scope and two-case count accurately.
Do not change app wording or remove request/cancellation/cache/retry assertions.

<!-- rpi:task id=P01-T02 -->
### P01-T02

Explain deterministic #516 copy mismatch in the existing browser-check README.
Run `python -m checks.design_system_browser_check` twice from src/api.
Run API discovery with core/agents fixture paths, core discovery, both projects'
existing Ruff and mypy commands. Retain external output and disclose skips.
Core discovery exposed the public scenario manifest's recipe SHA-256 dependency;
refresh only that source binding plus required index/log, then rerun the failing
selectors and full core suite. Preserve fixture/inventory/version/coverage claims.

<!-- rpi:phase id=P02 -->
## P02: Review and publication

<!-- rpi:task id=P02-T01 -->
### P02-T01

Fresh independent worker owns one Review artifact. Preserve findings and route
later work without repeating Review. Resolve GitHub account to privacy-safe local
author/committer email; commit implementation plus original dated evidence.
Use focused small-issue gate consistent with no-Docker owner scope; fetch main
and verify final head/base/clean state before publication, not a full receipt.

<!-- rpi:task id=P02-T02 -->
### P02-T02

Push fix/design-system-browser-check without force. PR targets main, describes
Refs #517, #516 and #514 and actual validation, never closes issues or merges.
Hosted/human approval remains distinct and required.
