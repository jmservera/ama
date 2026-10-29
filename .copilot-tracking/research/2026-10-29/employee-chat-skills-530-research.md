<!-- markdownlint-disable-file -->
## Research brief

Deliver issue #530 on feat/employee-chat-skills-530. Audience: implementer and
independent reviewer. Focused convergence research for one employee chat with
five repository-defined bounded skills, record-grounding, access enforcement,
minimal audit, workflow fallback and accessible employee UI.

## Parameters and direction controls

Date: 2026-10-29. Source: src only. No push, az, paid inference, deployment,
closing keywords or approval claims. Reuse chat_panel, agents chat and employee
async-action conventions. Full loop explicitly requested; no routine phase
prompts. Preserve manual human acceptance boundaries.

## Extension registry and participation

Repository instructions and RPI phase skills selected. Web Interface Guidelines
selected for the employee web surface; current source retrieved 2026-10-29.
Existing Fluent 2 and accessibility baseline govern over generic styling.
Research inline: tightly coupled code trace does not justify delegation.
Independent plan critique and final Review will use bounded separate contexts.
No interaction required: issue and owner constraints supply the brief.

## Prior knowledge and initial questions

Supplied issue is intent, not evidence of delivery. Initial areas: core
chat_panel, agents chat/regulatory_chat, API authorization/web shell, existing
browser/SQL checks. Questions: which names and boundaries are canonical; which
read model is authorized; how to reuse context and fallback without a router;
which browser and persistence contracts establish acceptance?

## Cycle 1

### Wider

Branch is clean at d70ee60ab3d7346a9991cf64382d9985f4d09f2e, equal to fetched
origin/main. Requested `git pull --rebase` failed because no upstream exists;
explicit pull from origin/feat/employee-chat-skills-530 also failed because
the remote branch does not exist. No history rewritten. PR #529 is merged.
No existing #530 tracking or employee-chat files found.

### Deeper

C1: src/core/src/zava_forward/core/chat_panel.py:263-338 provides typed,
injected single-model turns, permitted citations, lexical refusal, role recheck
and workflow fallback. Legacy no-case chat intentionally abstains.
C2: src/core/src/zava_forward/core/assistants.py:29-45 owns exactly five
capability IDs, purposes, source categories and proposal role limits.
C3: src/core/src/zava_forward/core/chat_isolation.py:56-76 rechecks identity
and uses the employee's projected case; export_fields.py:39-58 adds a closed
external-context allowlist. It must not be replaced by raw store access.
C4: src/api/src/zava_forward/api/server.py:629-744 owns chat routes/privacy
gates. Existing chat thread persistence has owner-filtered JSON/SQLite/MSSQL
implementations and metadata-only audit (chatthreads.py:317-341).
C5: src/api/src/zava_forward/api/web/app.js:269-345 owns route changes;
chat.js supplies the case panel but no global launcher. index.html loads it.
C6: src/api/checks/design_system_browser_check.py:235-285 starts a responsive,
constructed-data, loopback-only process with no inherited model credentials.

### Contrarian

Compared a second router call with explicit native skill selection: no evidence
justifies another inference hop. A selector removes model routing ambiguity and
records the selected skill. A skill is an advisory lens, not permission to
invoke the corresponding proposal operation; all five can explain their public
purpose while record facts remain within the caller's existing projection.
General work help must have trusted workflow sources and explicitly disclose
that no record is visible. Preserve legacy no-case abstention when no skill
argument is supplied. Do not copy raw free text into audit. Privacy references
remain mandatory; absent references must fail visibly, not activate storage.

## Evidence log

C1-C6 above are canonical code evidence. W1: Web Interface Guidelines,
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md,
retrieved 2026-10-29, complete. Native dialog/focus, labels, live updates,
reduced motion, reflow and safe text rendering apply.

## Findings, alternatives and decisions

Default remains one chat agent/five skills, no router unless material evidence
requires owner approval. Do not claim lower measured latency or cost without
measurements.

## Open questions and readiness

Research disposition: executed. Planning Readiness: Ready.
One completed wider/deeper/contrarian cycle; another cycle is not justified by
remaining source uncertainty. No latency/cost benchmark or live access asserted.
Required independent critique, browser/axe, units, typing/lint and actual SQL
remain implementation evidence, not research results.
