---
title: Browser asset matcher phase details
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Metadata

Task ID: pr-594-browser-asset-matchers-568. Task slug: browser-asset-matchers-568.
Plan: `.copilot-tracking/plans/2026-10-30/browser-asset-matchers-568-plan.md`.
Research: `.copilot-tracking/research/2026-10-30/browser-asset-matchers-568-research.md` (C1-C7).
Initial direction: repair harness matching, not app asset serving. No unresolved implementation blockers.

## Phase Index

| Phase | Intent | Status |
| --- | --- | --- |
| P01 | Shared matching, tests, guide | Complete; five new regressions passed |
| P02 | Locked browser and engineering validation | Complete; all affected browser modules, 73 units, Ruff and mypy passed |

<!-- rpi:phase id=P01 -->
## P01: Correct asset instrumentation

Context: query-versioned HTML bypasses exact/glob URL instrumentation. A canonical anchored asset suffix also supports version-directory prefixes without broad filename/query overmatch. All code targets and test budget are locked in the plan.
Boundary: seven checks and shared helper/test only; bare GETs still test bare HTTP behavior. No application or UI edits.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Shared matching and all browser surfaces

Use `asset_url(path, base=None)` returning a compiled regex. Candidate structure: optional HTTP(S) origin (or exact escaped base when supplied), zero or more prefix directory segments, escaped canonical root path, optional query and fragment, fully anchored. Bind page routes/unroutes, waits and coverage to the owned base; off-origin lookalikes cannot enter the page asset callback and reach the context-level deny guard. Add existing-pattern local-only guard to shell context. Keep asset-cache context unrouted: Playwright routing disables browser cache and would invalidate its deliberate warm-cache evidence. That fixture serves constructed local bytes only; asset URL classification remains origin-independent for relative server paths. Python response/failure and coverage filters search it. DOM waits and load/error observation use `new RegExp(pattern)` with the same serialized pattern rather than exact `src`.

Targets: workspace recovery/exhaustion/delayed-companion/coverage; all loading shell/law/helper intercepts and failure observations; employee ops/specialist routes and ordering/count comparisons; widget recovery; both case-enhancement fallback checks; cache widget identification.

Preserve CDP origin identity and existing duplicate-evaluation/view counts. Correct Leaflet cache assertion to actual revalidation and SHA-256 ETag while retaining MIME, 147552 bytes and body/length comparison.

Completion: no version-sensitive asset instrumentation remains; existing behavioral assertions remain intact. Dependency: critique disposed.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Regression tests and guide

Test bare/query/segment URLs for main/shared/vendor JS and CSS, absolute/relative root forms, query/fragment handling, filename/path negatives and query spoofing. Native Playwright tests use a synthetic HTML/script response, no server or network, route and wait on the matcher, and exercise the exact DOM pattern. Unit CDP fixture verifies nonzero actual lexical coverage for version variants, same-origin exclusion and duplicate rejection.

Tests stay within six methods and one new file. Fail-closed native test context intercepts synthetic HTML/scripts; a second origin with the same asset suffix must reach the abort guard, never the local asset callback. API guide records the helper's suffix/origin contract, all corrected checks, locked CI reproduction commands and synthetic-only limits. Completion: tests prove actual route/wait and DOM coverage rather than matching a source string.

<!-- rpi:phase id=P02 -->
## P02: Validate correction

Context: CI failed after most journey checks succeeded. The entire original sequence must pass, not just a standalone matcher proxy. Dependency: P01 completed.

<!-- rpi:task id=P02-T01 -->
### P02-T01: CI replay and affected browser checks

From `src/api`, task-owned pip environment on PATH and API/core/agents test fixtures on PYTHONPATH. Hold heavy lock around the full command chain; preserve before/after logs externally.

Concrete permitted parent context: `/home/azureuser/.copilot/session-state/7dc0069c-bd97-46db-8804-627147673f47/files/venv` contains pip-installed src projects; sibling `files/` holds pinned axe, logs and fresh output directories. Caller explicitly requires `/tmp/ama-rpi-heavy.lock`. Existing fixtures own their tempfile directories and sanitized child environments; no parent restriction disallows these paths. The original lock acquisition/browser health checks already demonstrate usable execution. PC-001's worker-context restriction does not apply here.

CI sequence: `python -m checks.design_system_browser_check`; pinned axe download; `python -m checks.regulatory_ux_check --axe <axe> --out <fresh.json>`; `python -m checks.case_journey_browser_check --axe <axe> --out <fresh-directory>`.

Other corrected modules: workspace scripts and employee workspace (no arguments); loading briefing, chat widget and case-view UX (`--axe`, `--out`); asset cache (`--out`). Existing helper harness owns loopback readiness, sanitized server env and cleanup. Segment URL classification remains synthetic because production emits only query versions.

Completion: all listed modules exit zero with recorded assertions. A failure tightly coupled to correction must be addressed during Implement, not hidden through assertion changes.

Observed: original CI sequence, workspace scripts and loading briefing passed in `fixed-validation.log`. Employee initial retry count was corrected to exactly three before reload plus one additional request after reload. Employee workspace, chat widget, case-view UX and asset cache passed in `remaining-validation.log`. The cache fixture retained real warm-cache reuse and release-B/ETag assertions with no Playwright routing.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Unit, Ruff and typing

Use existing API commands and targeted unittest selector list in the plan. Run API `ruff check .`, `ruff format --check .`, strict isolated lint/format for new helper/test and changed strict case-view check, and `mypy`. Record exact command, counts and any baseline issue. New code should remain typed without broad suppression or casts.

Completion: executable evidence and plan/details/changes agree. Human approval remains unperformed. One post-implementation independent Review follows; no review loop or push.

Observed: 73 selected unittest cases passed in 5.980s. API Ruff check/format passed; strict isolated new-code lint/format passed with `src = ["src", "tests"]` (same import classification as API config). Mypy passed 122 source files. Optional whole-case-view isolated lint has ten original diagnostics, independently reproduced from pre-edit HEAD; no new suppression or unrelated lint cleanup.
