<!-- markdownlint-disable-file -->
---
title: Resident browser check 571 research
description: Focused local reproduction and resident acceptance contract investigation
ms.date: 2026-10-30
---

## Research Brief

Identify the failing resident check, reproduce in a real local browser, and
decide whether the prompt, expectation or product is wrong. Audience: implementer
and independent reviewer. Output mode: convergence, preparing planning.
Acceptance: meaningful resident evidence, plain language and honest AI labels.
No Azure, deployment, live sign-in, credentials or push. Full API units only
under `flock -w 600 /tmp/ama-rpi-heavy.lock`.

## Research Parameters

Focused posture inferred from the bounded issue and supplied RV-003 evidence.
Resolved evidence root: `.copilot-tracking/research/2026-10-30/`.
Prior knowledge: issue #571 and RV-003 are claims to verify against current code.
Questions: which script fails; what is actually rendered; which contract is
current; what regression assertion preserves that contract?

## Extension Registry and Provenance

Repository instructions and RPI phase skills selected. API README supplies
local startup. Content standard and AI rules govern acceptance meaning.
Research performed inline because this is one coupled trace; no independent
research lane warrants delegation. Web guidelines will be loaded before any
web edits. No interaction needed: scope and local-only authority are explicit.

## Direction Controls

User's complete-loop and local-commit direction is authoritative. Do not repair
unrelated failures or weaken consent, human help, evidence grounding or labels.

## Research Cycle Log

### Cycle 1

* Wider: read RV-003, issue #571, API startup/check instructions, content
  standard and current check. Identified the standalone assistant check, not
  the SQL resident demo or generated-answer check. Reflection: investigate
  typed finite grammar, not employee focus or live service settings.
* Deeper: ran the untouched check with actual Chromium, local constructed HTTP
  application, disposable agenda and digest-checked axe. It fails at line 330
  on `documents help`, exactly as reported. Inspected full-match patterns and
  history; the generated-answer change a72cb268 introduced intentional
  complete-message admission. `forms help` and `What does my document warning
  or error mean?` are also unknown. Reflection: fixing only the first string
  would leave subsequent failures.
* Contrarian: challenged the product-regression hypothesis by executing the
  existing own-case document HTTP unit: supported natural questions return
  missing survey, warnings, sources and authority limits; cross-case data is
  absent. It passed. The first invocation used nonexistent `ChatTests`; the
  corrected `ChatApiTests` selector passed. Rejected broadening keyword routing
  because complete-message rejection is deliberate and has negative tests.
  Also found a genuine check-quality risk: whole-history text assertions can
  borrow facts from earlier replies after the shared-widget migration.
* Synthesis: select supported everyday questions in the check, preserve all
  factual expectations, and scope each reply assertion to a newly added
  assistant article. Add explicit obsolete-prompt refusal coverage and
  supported-question facts/labels coverage. No second cycle needed: source,
  actual reproduction and contrarian HTTP evidence agree.

## Evidence Log

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | `.copilot-tracking/reviews/logs/2026-10-30/employee-chat-dismissal-correction-review.md:102-110` | RV-003 already reproduced failure on unchanged 366ca4a2; original record preserved |
| C2 | `src/api/checks/resident_assistant_browser_check.py:321-350` | Appends `help` to document/form topics, uses unsupported warning paraphrase and asserts entire history |
| C3 | `src/api/src/zava_forward/api/resident_demo/chat.py:174-221` | Full-message finite grammar admits `Which documents are missing from my case?`, `How do I fill in my form?`, `What is wrong with my document warning or error?`; rejects three old prompts |
| C4 | `src/api/tests/test_resident_chat_api.py:719-755` | Existing actual HTTP evidence preserves document facts and isolation; targeted test passed |
| C5 | `src/api/tests/test_resident_chat_api.py:470-495` | Complete-message admission intentionally rejects extra actions/combined requests |
| C6 | `src/api/README.md:960-1062` | Actual local fixture startup, no-model default, current bounded-grammar and generated-label contract |
| C7 | `docs/reference/research/ux/content-standard.md:21-48` | Everyday words; rules must not be called AI; no approval/consent/safety authority |
| C8 | `/tmp/ama-571-resident-baseline.log` | Actual unmodified Chromium failure at line 330, `Survey: Missing` versus task-limit refusal |
| W1 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-10-30) | UI semantic/focus/async guidance fetched; no production web change needed |

Dependency recovery: `/tmp/mv` could not import core; created task-owned
`/tmp/ama-571-venv`. Initial build lacked wheel, then runtime lacked Playwright.
Installed missing build/runtime requirements from project manifests. All three
editable source distributions point into this worktree. No shared venv changed.

## Findings Mapped to Questions and Evidence

Q1 answered by C1/C2/C8: `checks.resident_assistant_browser_check`.
Q2 answered by C3/C8: expected refusal for obsolete prompts, not missing facts.
Q3 answered by C3/C5/C6/C7: check input is stale, no product routing change.
Q4 answered by C2/C4: accepted questions plus fresh-reply, facts, isolation,
rules-label and authority assertions; refused obsolete questions remain tested.

## Alternatives and Decision State

Selected: change check prompts to supported plain-language questions, not
application prompts or acceptance facts. Retain `Survey: Missing` and every
document warning/source/manual boundary. Add latest-reply isolation.
Rejected: accepting refusal instead of documents (weakens acceptance); broad
keyword admission (weakens bounded AI authority); changing resident product
copy/routing (not justified by C4). Human comprehension/live acceptance stays
unestablished, as before. No new legal currentness claim.

## Open Questions, Risks, and Residual Uncertainty

No research blockers. Named human resident wording approval, real-model,
screen-reader and live-service acceptance are outside this synthetic correction.

## Planning Readiness

Ready. Research disposition: executed, complete. Evidence C1-C8 sufficient for
focused planning; self-check: questions answered, alternatives dispositioned,
three ordered waves complete, paths and failed baseline retained.
