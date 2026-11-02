---
title: Redeploy employee chat fix from main 1a644d317, plan
ms.date: 2026-11-01
---

Critique: one final-candidate critique executed inline by the parent; verdict Proceed. Compatible finding applied: state plainly that only the focused gate runs and give a revert-and-redeploy rollback.

## Phases

1. [x] Back up the full config of all four apps and eight jobs (0600, session folder) plus a sanitized copy.
2. [x] Build the API image from a `git archive` of origin/main under `flock /tmp/ama-rpi-heavy.lock`.
3. [x] Push in one IP-only registry window; restore and compare the full registry configuration.
4. [x] `az containerapp update --image <digest>` on both API apps; five `CHAT_*` variables already present and preserved.
5. [x] Health and sanitized diff.
6. [x] Live Playwright: employee case chat, capacity page, resident chat.
7. [x] Remove own image by exact tag; commit evidence; push topic branch; open PR with Refs only.

## Constraints kept

Min replicas 0, eight jobs Manual, no RG deletion, no private endpoint, public network or RBAC change on the apps (registry restored), resident and agents untouched.
