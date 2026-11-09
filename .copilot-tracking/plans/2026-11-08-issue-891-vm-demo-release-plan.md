---
title: Issue 891 VM demo release plan
description: Bounded plan for the owner-authorised VM release and guarded live verification
ms.date: 2026-11-08
---

## Phases

* [ ] Phase 1: CI-first. Dispatch Source projects CI on main (`gh workflow run src-ci.yml --ref main`) only if no run exists for `e2ecee25`; preserve any failure and diagnose.
* [ ] Phase 2: Build `zava-forward-api` from a clean detached checkout of `e2ecee25` under `flock -n /tmp/ama-rpi-heavy.lock` with scratch on root; run `check-container.py`, Trivy gate and report, SPDX; record image id.
* [ ] Phase 3: Snapshot ACR and app (sanitised), open the registry window with a trap that restores and reads back, push tag `e2ecee25c` and record digest.
* [ ] Phase 4: One `az containerapp update --image <digest or tag>` on `ca-cutover-test-demo-api` only; confirm new revision 100 percent, Healthy, env names unchanged by sanitised diff; rollback to `1f465bf5e`.
* [ ] Phase 5: Warm `/healthz` (bounded retries), resolve expected tid/oid from Entra independently, run an in-memory employee and resident read-only smoke; for chat require receipt model source and label.
* [ ] Phase 6: Record outcomes, issue comment (no ticks), Review, commit on the report branch (no push).

## Stop conditions

* Failed Source CI for this head, scan gate failure or startup failure: stop before any registry change.
* Registry restore readback not Disabled/Deny/no rules/exports disabled: fix first, report.
* Identity not independently verifiable, MFA/consent or exhausted admission: stop at health and anonymous 401 evidence; no replay.
* No chat inference counted without an admitted ask, receipt `model_calls=1` and a non-workflow-only model source.

## Boundaries

No Bicep, production or pilot, new resources, role or finance changes, ledger reset, relaxed ACR protection beyond the short window, GitHub publish fallback, runner build, secret output, or push, PR and merge.

## Critique

Executed once (rubber-duck, 2026-11-08). Verdict: revise; all findings compatible with owner decisions and applied directly.

* Require a successful hosted Source CI run whose head SHA is exactly `e2ecee25` and re-check `origin/main` before mutation; stop on drift.
* Revalidate subscription, resource group, app, registry, traffic and rollback image before the registry window; record the rollback digest and revision.
* Deploy by recorded pushed digest, not a mutable tag; restore and read back ACR protections BEFORE the app update, not only via trap.
* Resolve expected tenant/object from Entra before sign-in; if unavailable, stop at anonymous evidence. Fix a bounded attempt budget (one employee sign-in, one chat ask) and no replay of consumed slots.
* The credential-reading sign-in is an uncommitted in-process script; any failure is recorded as a blocker without echoing inputs. Success needs receipt and answer from the same admitted ask.
* Suppress or sanitise az update output, browser errors and evidence; never print file contents or tokens.
