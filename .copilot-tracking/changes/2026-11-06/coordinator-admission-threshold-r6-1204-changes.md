---
title: Changes, admission threshold correction r6 (issue 1204)
ms.date: 2026-11-06
---

* Task: coordinator-admission-threshold-r6-1204. Owner authority: "fix 1204 and merge" (merge coordinator-only after gates).
* Commits after intake 7ae41593647acc907cfeeaf78450f879e3836c7e: d1aa4a060d27d15011585acfc64eba1090fc3627 (planning, critique Revise with 3 findings applied), 4d1cff620da598d5db72e00b71058810bc4e8c29 (target blob aa175c95), 72cfd55e0662f819b98ab7e075e68897611c9711 (static F1 to F3, final blob d471fc61041f9fc73a43564f7bf390a7c7d10cf5).
* Source change: admission bullet in .github/agents/ama-backlog-delivery-coordinator.agent.md replaced the unconditional 16 to 20 ban with: admit at 20 or fewer unless a drain is recorded; more than 20 enters a recorded drain; drain bars admission at 16 to 20 until a confirmed count of 15 or fewer clears it (recorded); unavailable count means admit none and re-read; unavailable drain record is rebuilt from evidence; gates never relaxed.
* Evidence: sandbox 010, report 011 (Pass at simulation grade, 0 target defects, 5 Low, 2 Info), independent static review (Revise, findings applied).
* Divergence: design bound to intermediate blob, lead rechecked against the final blob; disclosed in report 011.
* Not changed: other policy, frontmatter, historical reports and raw traces.
