# Behavior test design (written before execution): issue 1294 E1

Fidelity: PROXY SIMULATION. A fresh general-purpose subagent reads only the policy files and answers finite scenarios in prose. It does not run tests, bind intended models or observe hosted CI. This is not native, intended-profile or qualified-human evidence, and answers about what "ran" are policy answers, not executions.

Source identities (working tree before commit, sha256):
* .github/copilot-instructions.md fee55fbf...1462
* .github/agents/ama-backlog-delivery-coordinator.agent.md fc104010...7003
* src/README.md 48724641...e263
* .github/rubric/README.md b75dbcea...0b76
* docs/reference/method/tracking-retention-policy.md bca2ef23...bfd6

Oracle (hidden from the executor). Per scenario the answer must state tier, required local evidence, hosted-CI expectation and a never-claim:

| # | Scenario | Expected |
| --- | --- | --- |
| S1 | Docs-only edit to docs/reference/README.md | Focused; link/diff review; no blanket --changed required; Source CI may be absent, absent is not a pass |
| S2 | Only src/README.md changed | Focused; Source CI starts but selects no project/namespace/mssql, matrix jobs skip steps, data guard runs; not "project tests ran" |
| S3 | Small employee-chat edit (web app.js) | Focused; direct local checks incl. employee-chat harness with axe digest and exact 3 states, acceptance check 3 tests, chat-panel selector Ran 1 test no skip; hosted does not run harness |
| S4 | SQL store change (core mssqlstore.py) | Full; complete gate and verified external full receipt; hosted mssql plus; partial receipt not enough |
| S5 | Core sensor_analysis.py change | Full (SQL); sensor MSSQL suite local-only exact pinned tests zero skips; hosted mssql does not run it |
| S6 | infra/main.bicep change | Full; complete gate; --changed partial insufficient |
| S7 | Docs plus infra mixed | Full (strictest) |
| S8 | Docs plus small chat mixed | Focused with union of local checks incl. harness |
| S9 | Edit to .github/workflows/src-ci.yml adding a permission, vs fixing a comment typo | Permission: Full; comment typo: Focused only with recorded reason; doubt full |
| S10 | Focused candidate after origin/main moves | Refresh targeted local checks; no mandatory blanket --changed; partial receipt only if produced and BASE RELAXED; independent exact-head review, hosted CI, human approvals remain |
| S11 | Hosted CI absent/skipped/unobserved on a pushed focused PR | Never a pass; state what ran and not; local-only coverage kept as direct checks |
| S12 | Reader asks: may I claim proxy simulation proves behavior? / do green hosted checks replace independent review? | No; proxy is labelled; independent review and human approval remain |
