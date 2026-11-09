# Issue 86 formal-complaints typing correction: plan

Scope: jmservera/ama#86 only, `Refs #86`. Research: `.copilot-tracking/research/2026-11-06/issue-86-formal-complaints-typing-research.md`. Details: `.copilot-tracking/details/2026-11-06/issue-86-formal-complaints-typing-details.md`. Dated 2026-11-06.

Validation tier: FULL remains required for publication (adapter persistence and access boundaries; owner decision D4). This turn admits no heavy gate: only core strict mypy, Ruff check and format check, and the affected core tests run, with scratch under `/mnt/ama-gates/restart-1106-86-typing/`. A new R3 FULL receipt, independent exact-head assessment, hosted CI and human gates remain pending. Old R2 is not passing, covered or verified.

Critique: `.copilot-tracking/challenges/2026-11-06/issue-86-formal-complaints-typing-critique.md` (one pass, no repeat).

Phases

* [x] 1. Critique this plan once (independent), apply compatible findings, commit records before any source or test edit.
* [ ] 2. Annotate `complaints_route.py` and add the `ComplaintsReceiver` Protocol.
* [ ] 3. Declare `Store.complaints_receiver` with the Protocol type, default `None`.
* [ ] 4. Fix the two test helper return types with locally annotated variables.
* [ ] 5. Focused validation: strict mypy (core), `ruff check .`, `ruff format --check .`, core resident-decision tests, import-origin proof.
* [ ] 6. Write changes record and a separate honest author Review; commit.

Out of scope: runtime logic, adapter acknowledgement rules, defaults, persistence, authorization, web files, #144 files, other typing debt, any heavy gate.

Success criteria: the 14 recorded errors disappear with no `type: ignore`, no `cast`, no weakened config; focused resident-decision test outcomes equal the pre-change focused run; whole-suite equality is pending the later FULL gate and is not claimed; working tree clean after commit.
