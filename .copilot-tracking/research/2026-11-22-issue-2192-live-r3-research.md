---
title: Issue 2192 research (round 3, live redeploy)
date: 2026-11-22
---

Disposition: executed (reuses round 2 findings, adds deploy evidence).

* Round 2 found the resident checkbox wrote consent for the sensor home while the employee view reads the case-id home. PR 2225 (`8a8ac7d3c6`, in origin/main `0696d94464`) fixes that. The live `ca-resident-demo` revision 0000020 predates the fix, so the live employee effect is unproven.
* Registry `crcutovertestrzsrg` is network-locked (public Disabled, Deny). `/tmp/acr-push.sh <ip> <image>` opens a trapped window and restores it on exit.
* Reusable probe: `docs/reference/research/issue-2192-live-r2-2026-11-21/live_probe.py` (credentials read at runtime, never printed).
* Source change: none planned, so tier is focused, not FULL. Deploy is a live Azure change to one revision of one app in resource group `ama`; ACR stays Disabled, no Bicep, hardening off.

Planning Readiness: Ready.
