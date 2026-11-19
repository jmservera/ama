---
title: Issue 1204 delivery-idle research
ms.date: 2026-11-18
---

## Scope

Issue #1204 (unsupported idle ticks, stale coordinator handoffs). Base `origin/main` db74557b5273a67117c6e3cb63a4c32f3e180084. Tier: FOCUSED (prompt/instruction change only). Research disposition: executed. Planning Readiness: Ready.

Process disclosure: the opening artifact and the `research-open` witness were written after the first read-only probes and after the in-place agent-file merge had been staged in the working tree, not before. The witness will record dirty source at that point.

## Evidence

* The issue is OPEN with one unticked criterion (every tick has a next action, bounded closure-review progress, approval reconciliation, no global stop from one blocked lane).
* PR #1813 (the #1204 instruction change) merged on 2026-11-15 into `feat/demo-164-chat-grounding-provenance-0900`, not main. Parent PR #1641 reached main on 2026-11-18.
* On main, `tools/check-coordinator-handoff.py`, its tests and the #1813 RPI artifacts are present, but `.github/agents/ama-backlog-delivery-coordinator.agent.md` lacks the #1813 contract text. `git diff 325ef2ba4 origin/main` shows the agent file differs by 456 lines because later main commits (#1511, #1821, #1843) rewrote it from a different lineage.
* Adverse result on base: `python3 tools/check-coordinator-handoff.py` reports 12 violations and `python3 -m unittest tools.test_check_coordinator_handoff` fails 5 of 11 tests (live agent contract, three polarity cases, CLI exit codes). The checker is not wired into CI or `tools/rpi-checks.py`, so hosted checks did not detect it.
* A three-way merge (base `325ef2ba4^`, theirs `325ef2ba4`, ours main) applies cleanly with zero conflicts, so main's later additions are preserved.

## Conclusion

The #1204 instruction content did not reach main. The smallest fix is to port the #1813 agent-file diff onto current main. The runtime-observation part of the unticked criterion cannot be proven by a repository change and stays for owner/coordinator observation.

## Unmet criteria after this change

* Criterion 2 in practice: sustained every-tick liveness is observable only from future tick logs.
