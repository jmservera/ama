---
title: PR 538 citation and helper recovery research
description: Bounded correction research for three Copilot findings, refs 531
ms.date: 2026-10-29
---

## Research Brief

Correct citation ownership across line breaks, preserve abbreviation/title
boundaries, and recover an initially missing async helper before workspace
use. Audience: implementer and independent reviewer of PR #538. Output mode:
convergence preparing planning. Research posture: focused, selected from the
named files and concrete supplied reproductions.

Non-goals: redesign, new sentence-tokenizer dependency, cloud activity,
publication, whole-project acceptance or changing citation verification policy.
The owner requires a complete RPI correction round, local Conventional Commits,
strict core/API checks, units, relevant browser coverage, nonblocking admission
to the shared heavy lock, and no push, az or force-push.

## Research Parameters and Direction Controls

* Trusted evidence root: `.copilot-tracking/research/2026-10-29/`.
* Candidate internal areas: `ai_tasks.statement_sources`, its regressions,
  workspace startup/dependency retry, loading browser checks and manifest pins.
* External area: current Web Interface Guidelines, scoped to modified web code.
* Questions: Q1 how to preserve trailing citation ownership; Q2 how to avoid
  abbreviation fragmentation without losing real sentence boundaries; Q3 how
  to bootstrap the helper without bypassing bounded dependency failure UX.
* No-interaction rationale: explicit scope and failure strings suffice;
  non-interactive execution is required.

## Extension Registry and Participation

Repository instructions, original case study, addendum, reference index and
owner memory were read. Applicable skills: rpi-research and
web-design-guidelines. Current guideline source fetched 2026-10-29.
Design/redesign skills skipped because this is dependency recovery, not visual
design. Research is inline: one tightly coupled code-path trace needs no worker.
Independent plan critique and final Review belong to later phases.

## Prior Knowledge

The previous same-day correction task is completed/stopped and its artifacts
remain unchanged. This round has a distinct task identity and does not
silently rewrite its original outcomes. Initial branch HEAD: `204507d6`.
`git pull --rebase` succeeded before investigation; matching PR is open.

## Research Cycle Log

### Cycle 1: Wider

Initial evidence confirms parser citation shielding but horizontal-only
trailing-reference normalization, punctuation splitting without abbreviation
protection, and unguarded helper-dependent account listeners before `start()`.
Relevant existing browser runners own synthetic loopback servers.

### Cycle 1: Deeper

The loader caches each path's two-attempt retry promise, stops after timeout or
evaluated-without-readiness, and rechecks expected globals. `AsyncAction` is a
lexical const, so duplicate uncertain evaluation must remain forbidden (C6).
The shell loads it before app.js, but a failed download permits app.js to run.
Bootstrap must await helper readiness before attaching account action handlers.
The loader needs to operate before `/api/me`, when `me` is null (C3).
Both supplied parser examples were executed against current source and
reproduced exactly. Venv `/tmp/mv` exists with mypy and Ruff. No selected
source/check is among the scenario manifest's four pinned inputs (C7).

### Cycle 1: Contrarian

Do not flatten every newline: uncited paragraph and bullet boundaries must stay
visible. Normalize only whitespace between terminal punctuation and protected
citation groups. Do not remove all periods: shield recognized abbreviations
while retaining sentence-ending punctuation and explicit newlines. Tests need
multiple citation groups, mixed CRLF whitespace, real uncited sentences and
abbreviated text followed by a separately cited sentence. Broad NLP dependencies
are disproportionate. A no-op async fallback would silently weaken duplicate
suppression and feedback, so reject it in favor of the actual bounded loader.
Retry exhaustion must offer native reload, not reset a cached retry budget.
Existing route/session isolation must remain tested.

## Evidence Log

* C1: `src/core/src/zava_forward/core/ai_tasks.py:135-161` shields citations,
  moves post-punctuation citations using `[ \t]`, then splits periods/newlines.
* C2: `src/core/tests/test_ai_statement_sources.py:8-42` covers whitespace
  after citation groups, not newline before them or abbreviations.
* C3: `src/api/src/zava_forward/api/web/app.js:220-233` omits async helper
  readiness; `app.js:1518-1540` dereferences it before startup.
* C4: `src/api/checks/loading_briefing_browser_check.py:28-65` already tests
  failed app script and service retry using the actual shell.
* C5: `src/README.md:69-112` distinguishes focused correction checks from
  full publication gate; no publication is authorized in this task.
* C6: `src/api/src/zava_forward/api/web/app.js:191-218` owns bounded script
  injection; `web/async-action.js:3` uses a lexical const.
* C7: `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json:48-53`
  pins workbench manifest, workbench browser recipe, dataset and navigation tests,
  none of which need changes.
* C8: `src/api/tests/test_workspace_scripts.py:24-219` executes the shipped
  loader in Node, covering shared recovery, bounds and stale route/session state.
* C9: `src/api/checks/loading_briefing_browser_check.py:28-65` and
  `checks/design_system_browser_check.py:1-34` support actual-loopback synthetic
  startup checks; no private data or cloud activity is needed.
* W1: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md,
  retrieved 2026-10-29, complete current text. Native actions, announced async
  status, keyboard recovery and explicit error next steps guide changed code;
  repository Fluent/plain-language/ASCII conventions take precedence.

## Findings, Alternatives and Decision State

Q1 answered by C1/C2: normalize trailing citations across line breaks, including
between successive citation marks, before splitting. Q2 answered by C1:
shield bounded recognized title/abbreviation periods during segmentation and
restore exact text. Keep explicit newlines as boundaries.
Q3 answered by C3/C6/C8: include helper in required dependencies and run the
existing loader in a pre-session bootstrap before registering helper-dependent
listeners. Capture loader session identity rather than treating null as an
automatic success. Preserve exhaustion/readiness/timeout policy and expose
reload at terminal startup failure. Test actual successful recovery and
terminal reload plus cheap Node contract regressions.

Selected alternatives are supported by the exact reproductions and existing
loader contracts. Rejected: blanket newline flattening (citation bleed),
generic punctuation removal (lost statement boundaries), and no-op helper
fallback (silently lost action protection). Residual uncertainty: English
abbreviation detection is a bounded heuristic, not general linguistic proof.
No new legal, model-grounding or human accessibility acceptance claim.

Cycle synthesis: all three questions are evidence-backed; no new material
in-scope uncertainty warrants a second cycle. Self-check: scoped paths, stable
evidence IDs, alternative dispositions, participation rationale and limitations
recorded; no source changes during Research.

## Planning Readiness

Research disposition: executed, Complete. Planning Readiness: Ready.
Parent next action: Plan the bounded corrections and one independent critique.
