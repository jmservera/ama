# Research: issue 2244 live re-verification on revision 0000054

Status: complete. Research disposition: executed. Planning Readiness: Ready.

Goal: prove or disprove the live criteria on ca-cutover-test-demo-api--0000054. Parent: issue-2244-live (20261122T141035Z) fixed src (42546c9221) and left the live criterion unproven.

Evidence: [docs/reference/research/issue-2244-live-r54-2026-11-22.md](../../../docs/reference/research/issue-2244-live-r54-2026-11-22.md) and its live-probe.txt. Key facts: rev 0000054 Healthy, replica restartCount 0 for 33 min, fix present in container (4 `startup_retries` matches), second replica started clean, 13/13 healthz 200.

Constraints: held-lock test is a drill (excluded), registry firewalled, Log Analytics unreadable. Unrelated runtime ProgrammingError on POST /api/chat/threads at 23:35:34Z noted for triage.
