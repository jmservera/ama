# Research: #184 one-minute / five-home simulator (rpi-184-iot-unblock)

Disposition: executed. Planning Readiness: Ready.

Evidence:
* Candidate e904ba4c0 (merge-base 15bfee2d7) touches 15 files under src/api and src/core (simulator cadence, five-home Quality scope, operator-triggered paid analysis, READMEs, tests).
* `git apply --check` of `git diff 15bfee2d7..e904ba4c0 -- ':!.copilot-tracking'` against dafed6a27 reports no conflicts. Main changed only app.js, importer tests and docs since the merge-base, so #1473/#1489/#1495 behaviour is untouched.
* The c71cdd457 helper (issue-184-sql-runner-repair-0341/runner.py) is an uncommitted-to-source external script under .copilot-tracking, not in e904ba4c0. It is out of scope and not ported.
* Committed verifier sensor_handover_verify.py reads CSV (not JSON); an empty reference yields HANDOVER_SCHEMA_UNSUPPORTED (fail closed). main() trusts result["passed"] without type check; add a guard so a non-dict/None result or non-True passed never exits 0, with a RED test.
* Prior candidate held on 2 Ruff format issues; fix after applying.
Disjointness: no chat_panel/chat_case_answers/chat.js/agents chat/role-screens edits.
