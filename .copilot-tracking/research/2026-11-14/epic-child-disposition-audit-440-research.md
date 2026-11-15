---
title: Epic child disposition audit research (Refs #104, #149, #165, #440)
ms.date: 2026-11-14
---

## Research disposition: executed. Planning Readiness: Ready

Sources (read-only): `docs/architecture/cutover-evidence-pack.md`, `docs/architecture/mvp-to-src-parity-matrix.md`, `docs/reference/research/**`; child lists from `gh api .../sub_issues` (read once, encoded in the test, not queried at test time).

## Children

* #104: #105, #106 closed in code; #107 in progress (dispatch rebuild open); #108, #432, #435 deferred (live model runs, metering, capstone human gates)
* #149: #150, #151, #152 implemented-unverified (matrix reopen list names #151; AT and contrast open); #153, #156, #225 to #233 in progress; #154, #155 deferred to resident and usability human work
* #165: #166 closed (pack ledger); #167, #175, #177, #190 implemented-unverified; #176 in progress; #184 deferred (live Azure IoT Hub)

## Findings

* The matrix (2026-10-16) is historical and disagrees with live GitHub on #150, #151, #166, #167, #175 open/closed state. The test records the stricter disposition and does not assert live state.
* The pack never records the three epics closed; line 1931 says all dependent epics are open.
* The pack is not edited, so PR 1618 stays conflict-free.
