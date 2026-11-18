---
title: Plan for issue 185 live device identity proof
ms.date: 2026-11-18
---

Refs #185. No source change (focused tier; evidence only).

1. Grant `id-cutover-test-api` IoT Hub Registry Contributor on the demo hub (temporary).
2. Run a throwaway Container Apps job in `cae-cutover-test-demo` that creates N=3 `SYN-` SAS devices with Hub-generated keys, mints per-device SAS tokens in memory, sends one device-to-cloud message each, asserts no key text appears in its own output, deletes the devices and reads back an empty registry.
3. Remove the job and the role assignment; confirm hub settings unchanged.
4. Record per-criterion results in `docs/reference/research/issue-185-live-device-identity-evidence-2026-11-18.md`, the knowledge-base index and log.
