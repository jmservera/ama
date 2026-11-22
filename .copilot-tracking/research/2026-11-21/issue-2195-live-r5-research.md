# Issue 2195 r5 research

Date: 2026-11-21. Scope: remaining demo gaps after r4 (axe browser run, 500 recheck, live re-probe).
Disposition: reused r4 evidence (docs/reference/research/issue-2195-chat-routing-live-r4-2026-11-21.md) plus targeted new checks. Planning Readiness: Ready.

## Findings

* Pinned axe-core 4.10.3 (sha256 880970c0...a68bb, npm pack, hash verified) run through `checks.employee_chat_browser_check`: PASS, 3 dialog states, 0 violations.
* Local tests: api accessibility baseline, content standard, resident assistant API 59 OK; core chat routing and chat panel 74 OK.
* Live revision `--0000043` (employee): thread creation returned 500 three times and one ask returned 500; retries then returned 200. Routing lines for funding, stock, tie, general and refused were correct. Resident chat: 3 asks routed correctly.
* Container logs for the same minutes show `ProgrammingError` on `POST /api/chat/threads`, `POST .../ask`, `GET /api/map`, `GET /api/briefing`, each next to concurrent `/healthz` probes. This reverses r4 (500s did not recur): the 500s are a live defect on the demo.
* Hypothesis: the SQL driver connection is shared across request threads and statements overlap. The unmerged fix at commit 193c9aaa90 (per-connection lock, rows read inside it) targets that; the exact driver message is not logged, so the cause stays a hypothesis until redeployed and re-probed.

Planning Readiness: Ready.
