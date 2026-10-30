---
title: Workspace script retry 524 research
description: Current-main verification of issue scope and remaining local work
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Research Brief

* Target: issue #524, bounded automatic recovery of missing workspace scripts.
* Purpose: establish current implementation and acceptance gaps before making changes.
* Audience: coordinator and independent reviewer.
* Scope: workspace bootstrap, local static serving, existing regression coverage.
* Non-goals: Azure, deployment, live sign-in, credentials, private data, push.
* Output mode: convergence, preparing the requested full RPI loop.
* Criteria: each issue acceptance criterion mapped to observed evidence or an explicit gap.

## Research Parameters

* Posture: focused, selected for a bounded issue with named code paths.
* Evidence root: `.copilot-tracking/`.
* Candidate internal areas: API web bootstrap, API tests, prior #524 artifacts, API guide.
* Candidate external areas: current Web Interface Guidelines only.
* Explicit boundaries: caller-provided branch and base; local-only execution.
* Research source edits: prohibited.

## Extension Registry and Provenance

| Extension | Selection and authority |
| --- | --- |
| `.github/copilot-instructions.md` | Selected: repository paths, evidence, local gate and web standards |
| `rpi-research` | Selected: three-wave research and evidence/readiness |
| `web-design-guidelines` | Selected: current rules for any changed web files |
| Research specialist | Skipped: a single connected trace is best investigated inline |
| Public-page design skills | Skipped: this is app boot reliability, not design or restyling |

## Participation and Direction Controls

The user explicitly requests research, plan, implement and review in order. This
is automatic continuation consent at intake, not a manual-to-automatic switch.
No interaction is needed or available. Existing merged work must be verified,
not duplicated or undone. The branch is clean at the specified base; historical
PR #527 with the same branch name is merged, but the caller explicitly selects
this new local branch from current main.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | What has already landed and what remains in #524? | Answered, C1/C3-C6 |
| Q2 | What local evidence supports recovery and terminal failure? | Answered, C4/C5; fresh execution belongs to Implement |
| Q3 | Is any source change needed within the exact issue scope? | Answered: no known missing behavior |

## Prior Knowledge Gate

`gh issue view 524 --comments` reports #527 merged and live deployment/owner
verification pending. Historical artifacts exist under 2026-10-28. These are
starting evidence, not proof of the current candidate.

## Research Cycle Log

### Cycle 1

#### Wider

Inspect current bootstrap, existing issue artifacts and local test/runtime
contracts before deciding whether implementation is missing.

Inline findings: current main contains both merged recovery and later bootstrap/
session refinements. Existing unit and actual-browser owners already cover the
named issue. Reflection: prioritize verifying contracts, not adding another
loader or redundant regression owner.

#### Deeper

Inspected the actual loader, missing-global predicates, route guard, test VM,
browser fault injection and local HTTP assertion. C3-C5 show two shared attempts
with 250/500ms delay and 5s timeout, current-global readiness checks and terminal
plain-language error. Browser coverage uses real scripts and verifies one
document request, exactly bounded requests, native keyboard reload and stale
route/session protection. C6 shows full-byte static reads and explicit response
headers. Reflection: the local test already checks status, size, MIME, length
and cache policy; no source evidence establishes the historical live cause.

#### Contrarian

Challenged the premise that new recovery code is needed: #527 is merged and
current code/tests prove the requested design is present (C1/C3-C5). Challenged
retry-on-timeout: a late classic script can install lexical declarations, so
another injection could redeclare them; the existing stop-on-uncertainty policy
is intentional and tested. Rejected speculative cache/auth/infrastructure fixes.
The existing browser suite has no axe scan, so fresh scoped axe checks can
supplement evidence without changing production or existing test ownership.
Reflection: verification plus an API guide reconciliation is the smallest
complete in-scope implementation for this already delivered issue.

### Parent Synthesis and Disposition

Accept verification-only runtime disposition and a dated guide update. Reject
duplicate loaders/tests and changing retry policy without a demonstrated defect.
Defer live diagnostics/acceptance to the owner. One full focused cycle is
sufficient: another source sweep cannot establish prohibited live evidence.

## Evidence Log

| ID | Finding | Source |
| --- | --- | --- |
| C1 | Issue remains open only for live deploy/owner check per its comment | `gh issue view 524 --comments`, retrieved 2026-10-30 |
| C2 | Clean caller-selected branch starts at exact supplied base | `git status --short`, `git branch --show-current`, `git log -1`, 2026-10-30 |
| C3 | Bounded shared recovery, readiness and stale-session protection already exist | `src/api/src/zava_forward/api/web/app.js:220-281`, `:294-360` |
| C4 | Existing regression covers initial absence, error then readiness, exhaustion, timeout, concurrency and session guards | `src/api/tests/test_workspace_scripts.py:151-410` |
| C5 | Actual Chromium fault injection covers initial delivery failure, one/two failed requests, lexical companions, exhaustion and local HTTP contracts | `src/api/checks/workspace_scripts_browser_check.py:59-164`, `:325-361` |
| C6 | Local server emits no-store, exact length and reads whole asset bytes | `src/api/src/zava_forward/api/server.py:39-43`, `:203`, `:255` |
| C7 | Guide already documents recovery and live uncertainty | `src/api/README.md:627-662` |
| C8 | System Python lacks Ruff, mypy and Playwright | prerequisite probe 2026-10-30; isolated pip environment needed |
| W1 | Current Web Interface Guidelines fetched in full | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md, retrieved 2026-10-30 |

## Findings, Alternatives and Readiness

Q1: the only recorded unmet operational criterion is live verification. Q2:
existing tests directly measure issue behavior; rerun them and the caller's
full API/static checks. Q3: do not modify working runtime code just to produce
a source diff. Update the existing API recovery guide with fresh evidence and
the explicit acceptance boundary after successful execution.

Selected recommendation: preserve current implementation and test owners;
implement a current-main evidence reconciliation. Alternative rejected:
unconditional reinjection or a second loader, which increases duplicate lexical
execution risk and scope without addressing a proven defect.

Cause status: unresolved. Source/header checks cannot identify historical
truncation, cold-start behavior or authenticated transport. No live probes,
telemetry, deployment, sign-in or credential access is authorized.

## Self-check

All three waves executed inline; evidence and rejected alternatives recorded.
No research source changes. Earlier adverse Review evidence remains immutable.
Fresh execution is required before claiming current-candidate success.

## Current Decisions

Verify landed behavior before choosing any change. Never infer cold-start or
cache causation from a missing global alone. Live verification remains owner
work because the caller prohibits Azure/deployment/live sign-in.

## Planning Readiness

Ready. Research disposition: executed. Runtime requirements already implemented;
plan a verification/evidence reconciliation, not duplicated recovery code.
