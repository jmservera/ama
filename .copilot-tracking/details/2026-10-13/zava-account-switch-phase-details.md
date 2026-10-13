---
title: Account Selection Phase Details
description: Fixed-route switching and safe operational validation
ms.date: 2026-10-13
---

## Initial Direction

Task zava-account-switch-2026-10-13, P01; approved owner intent above.
Evidence in .copilot-tracking/research/2026-10-13/zava-account-switch-research.md.
Plan owns candidate; no source edits before critique disposition.

## P01-T01

Modify only trusted-proxy switch response to local /sign-in?switch=1.
Existing JS assigns window.location to server redirect, so no new client flow.
In /sign-in parse query, only single switch=1 invokes fixed select_account;
default login remains exact existing URL. Password route remains /app.
Use fixed print events with flush for explicit request and successful app
arrival, not generic HTTP logging. Emit no identity/query/URL/header payload.
Existing CSRF/tenant/role/binding checks retain order. Add no trace tokens to
OAuth state; Easy Auth owns state, nonce and session replacement.
PC-001 event checklist: account-switch-requested/sign-out-requested at
authorized CSRF-checked POST; account-picker-started/sign-in-started at their
fixed Microsoft redirects; workbench-entered only after authorized /app.
Test complete constant outputs and no successful markers on rejected requests;
normal/picker markers must be visible live. Keep blank values in parse_qs
so blank duplicates cannot accidentally enable switching.
Update one intentional switch regression; at most three new methods test
fixed chooser/hostile flags, constant events and unchanged password behavior.

## P01-T02

Targeted auth then full MVP suite; JavaScript syntax. Build existing Dockerfile
locally using available sudo Docker; run non-root image with private synthetic
fixture, temporary named container and dynamic or session-local port; verify
health/signin/select_account and no secrets in image. Stop only named container.
Upload tag through existing ACR, update only Container App image, wait ready.
Preserve current image for explicit rollback if failure; never rewrite SQL.
PC-002: store private pre/post configuration and auth baselines without fetching
secret values. Compare template (excluding intended image), env/secret refs,
identity/registry/ingress and complete Easy Auth settings. Record tested image
tag/digest and new ready serving revision/traffic. Restore only prior image
if these comparisons, readiness or required redirect checks fail.
Live no-redirect trace validates local route then platform Microsoft authorize
prompt, tenant and callback without printing state/cookies/codes. Browser
unauthenticated chooser view does not equal real signed-in account replacement.
Collect constant events from console and ContainerAppConsoleLogs in existing
workspace. Routing already uses allLogs; no broad HTTP log enabling needed.
Do not disable logging or privacy safeguards merely to obtain richer evidence.

## P01-T03

Document switch versus sign-out, fixed-event diagnostic query/table, session
scope and owner real-browser boundary. Update routing and append log.
Record workflow provider HTTP 403 and owner attempt 3 success; no secrets or
token rotation. Publish on continuing #65 using privacy-safe Git identity.
Reconcile all markers/evidence before one post-implementation Review.
Owner subsequently requests all learning in appropriate project documentation.
Use PRD review-learning rows for product implications, ADR 0002 identity section
for platform/binding/cache/session mechanics, and addendum exercise evidence for
dated observed scope/value limits. Keep existing historical tables dated;
do not regrade full acceptance or assert company staffing/competence.
Include earlier role-initialization/preservation and welcome/photo learning
where supported by published source/docs. No gratuitous BRD requirement
change, separate new ADR or personal directory roster. Update dates/index/log.
