---
title: Redeploy employee chat fix from main 1a644d317, research
ms.date: 2026-11-01
---

Task `redeploy-employee-chat-749`, Research disposition `reused` (prior research [redeploy-chat-research.md](redeploy-chat-research.md) plus live baseline), Planning Readiness `Ready`.

## Scope

Redeploy only the API image to `ca-cutover-test-demo-api` and `ca-cutover-test-api` from origin/main `1a644d317` (merged #752 for #749). Resident app and agents untouched.

## Evidence

* Both API apps ran the same image digest `7aa2a317...`; the resident app and agents need no change because #752 touches only the API stored-chat path.
* Registry `crcutovertestrzsrg` has public access Disabled; publication needs the standing IP-only window with exact restore.
* `ca-cutover-test-api` has no public probe (internal ingress); the agents app has no ingress; all apps use single revision mode, so rollback is revert-and-redeploy, not revision traffic shifting.
