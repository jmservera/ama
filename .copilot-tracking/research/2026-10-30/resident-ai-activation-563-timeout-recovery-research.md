---
title: Resident activation timeout recovery research
ms.date: 2026-10-30
---

## Brief and Boundaries

Task 563-timeout-recovery-20261030, slug resident-ai-activation-563-timeout-recovery.
Focused convergence research for the owner and coordinator. Continue the
existing automatic session on ops/resident-ai-activation-563, PR #576 OPEN
to main. Clean intake HEAD 775bbe4e. Read prior owner-enable changes,
independent Review, state and research before new diagnostics. Prior outcomes
remain historical, not overwritten.

Questions: locate the pre-answer timeout; verify health/revision/configuration,
existing account-scoped MI and resident-mini; identify a reversible verification
strategy that spends no more than four newly authorized sign-in submissions.
Diagnose without login first. No ledger read, SQL public access, employee
mutation, new resources, broad RBAC, private endpoints or RG deletion.
Owner approves activation and monitors cost; existing USD20 ceiling and
exclusive 2026-11-01 expiry remain; redeploy authority ends 2026-11-15.
Exact private current backup precedes mutation; min replicas0 and all jobs
Manual. Failed verification restores effective baseline; success stays enabled.
Local commits only, Refs #563, required Copilot trailer. Heavy lock only for
local gates using flock -w600.

## Extensions and Participation

Repository all-file guidance and RPI phase contracts selected. Independent
plan critique and one post-implementation Review required. Research inline:
one coupled operational trace; no independent research lane. Web design and
accessibility audit skills skipped: no UI change or conformance claim.
User explicitly requests ordered full loop continuing automatic work; no
new manual-to-automatic transition. Four-attempt grant supersedes exhausted
earlier two-attempt allowance prospectively, not retrospectively.
Evidence root .copilot-tracking/. Secrets only inside automation; no recordings,
credential output, private payload commits or SQL queries.

## Prior Knowledge Gate

Prior owner-enable changes and Review establish that activation's two variables
were applied, latest revision was ready, then coarse enabled_live stage timed
out without persisted request/substep proof. Rollback restored effective baseline
in owner-safe-173404. Neither SQL nor model failure was diagnosed.
Earlier local full gate blocked on shared heavy lock after600s, no receipt.
Current API guide accepts only assistant ENABLED/ENDPOINT plus existing SQL MSI
settings; deployment hardcoded resident-mini, default off and fail-closed reserve.
Original specification, addendum, reference-index opening and memory read.

## Research Cycle 1

### Wider

Current resident revision owner-safe-173404 is healthy, Succeeded,100% traffic,
initially ScaledToZero. /healthz warmed it in34.369s and returned200; running
replica then ready with0 restarts. Anonymous Chromium156 loaded assets/session
all200, sign-in visible, content hidden, chat usable,0 sign-ins.
Existing resident-mini deployment Succeeded; account-only OpenAI User role
created2026-10-27T10:42:13Z, over three days before this run. No role propagation
delay is evidenced. Env/secretrefs match README; enable/endpoint absent.
Private console/system logs captured outside git; selected operational messages
show startup and522 synthetic admitted rows, no observed exception.

Reflection: healthy anonymous path makes immediate blind login/model retries
unnecessary. Prior automation held an authenticated session across redeployment;
investigate the process-bound authentication contract before changing infrastructure.

### Deeper

C4: src/core/src/zava_forward/core/resident_showcase.py:393-432 signs both
session and CSRF tokens with a fresh process nonce; restart deliberately ends all.
C5: src/api/src/zava_forward/api/resident_demo/__main__.py:53 creates a new
SessionCodec without a fixed nonce on every process start.
C6: prior protected activate.py:289-296 reloads the pre-rollout browser and waits
only for #content, with no sign-in/error alternative, before dispatching an
enabled assistant question.
C7: src/api/src/zava_forward/api/resident_demo/web/demo.js:345-366 correctly
shows sign-in for an invalidated session, never #content.

Reflection: concrete automation defect explains the earlier timeout without any
model request. Fix verification sequencing, not nonce/security, SQL, RBAC or
resource topology: activate and warm first, then open a fresh context and sign in.
Persist each stage plus request dispatch/status; detect sign-in/error explicitly.

### Contrarian

C8: src/core/tests/test_resident_showcase.py:234 and
src/api/tests/test_resident_demo_api.py:440 explicitly require restart to invalidate
sessions. Retaining authentication across rollout would weaken intended behavior.
Managed-identity role age and health do not prove model/SQL accounting success.
Those are separate live gates, not a basis for declaring activation successful.
Do not bypass a fallback or repeatedly spend inference to hide a reserve/model
failure. Distinct from the cold-start delay, the nonce mismatch cannot be fixed
by longer #content waits alone.

Reflection: accept fresh post-rollout login and state-aware waits. Reject nonce
changes, added deployment env vars, additional roles and SQL/network changes.
One pest question and one out-of-scope question planned, no inference retry.
Four submissions are a maximum, not a target; stop on authentication denial.
Another research cycle is unnecessary: bounded cause and remediation are
supported; actual enabled outcome belongs to Implement verification.

## Evidence and Readiness

C1: .copilot-tracking/changes/2026-10-30/resident-ai-activation-563-owner-enable-changes.md:191:
coarse TimeoutError and verified rollback.
C2: .copilot-tracking/reviews/logs/2026-10-30/resident-ai-activation-563-owner-enable-review.md:90:
activation unmet; independent evidence distinguishes rollback from success.
C3: src/api/README.md:1025: exact four settings, accounting and expiry contract.

C9: Azure management and anonymous HTTP/Chromium observations, retrieved
2026-10-30 approximately18:02-18:09UTC, safe evidence under external private
session files/resident-recovery; no secrets/credential file read.
Research disposition executed/Complete. Planning readiness Ready.
No source or infrastructure mutation during Research.

## Selected Approach and Residuals

Exact fresh private backups, two-variable activation, ready100%-traffic revision,
health warm with240s timeouts/retries, then fresh browser sign-in. Test client
and server no-consent, actual AI pest answer/thin label/collapsed known sources,
source-supported claims and rules out-of-scope. Failed verification restores
backed-up effective configuration in a fresh ready revision. All commands,
dispatch/status and rollback results enter changes evidence. Local gate may
remain blocked independently; coordinator owns push and exact-head publication.

Self-check: brief, explicit constraints, extension provenance, prior gate,
three ordered waves/reflections, C1-C9, alternatives and readiness present.
No specialist delegation needed for this single trace. Raw logs/backups are
private external evidence, not production artifacts or passing gate receipts.
