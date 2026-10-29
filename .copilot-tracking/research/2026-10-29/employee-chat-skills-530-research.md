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

## PR #541 correction pass intake

User explicitly requests a short Research/Plan/Implement/Review pass for three
review threads and sibling cases, reusing this task and its artifacts. Original
critique and Review remain historical evidence, not rewritten outcomes.
Focused convergence; scope is employee-chat denial/disposal, deterministic
late-success proof and post-redaction question bounds. No push or az; local
commit with required trailer. Required checks: API/core Ruff, format, mypy,
core units, API chat/workspace units, local browser where feasible.
No new UX design or broad audit. Web guidelines selected and fully retrieved
2026-10-29. Independent critique and Review are scoped to this correction pass.
Prior-knowledge gate: current state routes RV-001/RV-002 to later correction;
the user now explicitly selects that work and adds the length regression.
Research is inline because the code trace is tightly coupled.

## Correction cycle 2

### Wider

C7: src/api/src/zava_forward/api/web/chat.js:61-129 has three initialization/
submit awaits: skills metadata, thread creation and ask. Submit denials already
reset the modal but do not explicitly restore focus; metadata denials only
change its status. All completions share the current-dialog/session guard.
Sibling audit includes all three awaits and 401/403/404.

### Deeper

C8: src/api/checks/employee_chat_browser_check.py:112-133 waits for aria-busy,
which AsyncAction sets before request arrival. Optional held-route handling
and permitted cancellation cannot prove a successful late application result.
app.js:49-79 also checks abort after fetch, so even successful transport cannot
prove the dialog's own stale-completion guard. Use separate transport-arrival
and controlled API-promise proofs, with explicit settlement awaited.

C9: src/core/src/zava_forward/core/chat_panel.py:314-316 now writes masked
content directly; chatthreads.py:322 rejects content beyond 8,000 characters.
The prior ChatIsolation -> privacy.add_message route performed a second
pre-redaction truncation. For already masked questions that bounded the final
write. Reapply the bound to ChatPanel's masked question before storage/prompt.
Core and HTTP regressions must assert masked stored text and actual question
sequence. Legacy/explicit skill modes share this write. Regulatory chat has a
separate 1,000-character input contract; assistant-output bounds and privacy's
first-pass general API are pre-existing, not changed by this correction.

### Contrarian

Relying only on fetch interception still lets AbortSignal rejection substitute
for success; controlled API promises intentionally ignore abort and settle
after disposal/session replacement. Assert old and replacement transcript/
status plus active element, not merely absence of an answer in a new modal.
Keep real transport cancellation as a separate check requiring arrival.
Do not refactor all chat/privacy services or change allowed input lengths.
Denial cleanup belongs in one modal-local helper used by both catches; keep
401 login handling in api() and do not steal focus from the login screen.

### Synthesis and readiness

Research disposition: executed. Planning Readiness: Ready. Selected surgical
corrections cover all three supplied threads; no evidence justifies another
cycle or broad UI change. Current source/PR threads confirmed on the named open
branch. Existing installed dependencies and Chromium are available; the heavy
lock was unoccupied on initial inspection, not a reservation or test result.
Historical SQL/full-publication/human gates remain distinct from this pass.
