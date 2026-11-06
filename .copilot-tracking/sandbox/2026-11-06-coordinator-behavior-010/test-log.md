---
title: Test log, run 010 (issue 1204)
ms.date: 2026-11-06
---

* Target blob d471fc61041f9fc73a43564f7bf390a7c7d10cf5 at HEAD 72cfd55e0662f819b98ab7e075e68897611c9711 (tree 39d5f274c51e6f4a19af049e3f5edb1cfcdcdcbe), unchanged through execution and grading.
* Design return sha256 f41b73b13bccbf7c351df22d8cb5a33f7d70d03f6e63c10e109e518d55ae6c9f (test-design.md). Static review return sha256 67a6daf8dcf7ac2e22d9f92764ac61da9a1f31c247cda2475a93f3c035714720 (static-review-return.md, bound to blob aa175c95; F1 to F3 then applied in the final blob).
* scenario-prompts.md sha256 d15e4cf30709e6b341c1a362122ff333df23bfcf86afc66f55d8c181a1a717da; executor-state.md sha256 20dfae8a3b84300aeda5668dcd254a3aff1cd5458e030799151452389abb09d9.
* Lead prompt edits: removed two oracle hint sentences (see run-state.md). Mapped requirements and signals withheld from the executor.
* Executor: hve-core-all:hve-artifact-tester, toolu_01CNFpnMB61eSnfpJ8dRYXCU, claude-sonnet-5.5, session_inheritance, no override, 109301 ms. Trace executor-trace.md sha256 dfb4db602c67feb8701d8e761954723cbad313e1763ca25a53c4dd6bd3d7fad7 (host-saved pointer file copied unchanged). Status Complete.
* Grader: general-purpose, toolu_01Cpk8E6ZrADWtA1WGU5Lf7V, claude-sonnet-5.5, session_inheritance, no override, 49423 ms. grader-return.md sha256 34821b07d3960962730678c677d32561f4f59583f9a2be3aa46b74d9d733d09b (extracted from the event record).
* Designer and static reviewer: general-purpose, harness default; per-agent telemetry not separately captured before later dispatches, so attribution for them is the harness default only.
* External verbatim copies: /mnt/ama-gates/g1204-r6-design/.
