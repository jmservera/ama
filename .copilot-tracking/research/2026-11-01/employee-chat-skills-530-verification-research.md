# Research: employee chat skills local verification (#530)

* Task: `employee-chat-skills-530-verification`; branch `feat/employee-agent-chat-skills`; base `origin/main` cb57c1b7.
* Research disposition: `executed`. Planning Readiness: `Ready`.

## Question

Issue #530 is open with criterion 8 unmet: "Local unit, browser and SQL checks pass; live verification on the employee site is recorded separately." What is already delivered, and what local evidence is still missing?

## Findings

* Delivered on main: PR #541 (feature), PR #579 (verification), PR #545 (redeploy). The one-agent/five-skill design and router comparison is in [src/api/README.md](../../../src/api/README.md#employee-chat-with-bounded-skills-530) and the knowledge-base log entry of 2026-10-29. Criteria 1 to 7 are ticked in the issue.
* Implementation: `core/chat_panel.py` (`chat_skills()` from `assistants.REGISTRY`, skill category filter, labels, workflow-only fallback, audit of thread id, sequence, skill, outcome), `agents/chat.py` (`ChatModel`), `api/server.py` (`/api/chat/skills`, thread ask with `skill`), `api/web/chat.js` and `chat-widget.js` (header launcher, dialog).
* Closure audit batch 2 (2026-10-31) states what is missing for criterion 8: local disposable SQL Server execution, and the full API/browser checks after a lock timeout. Hosted mssql CI is not local SQL execution. Live employee evidence is blocked: #612 employee attestation denied, zero employee sign-ins.
* No source defect is known. No code change is justified by the issue text; the gap is evidence.

## Local tooling findings

* Isolated venv with pip only (`/tmp/ama-530-venv`), editable installs of core, agents, api.
* Playwright chromium and a pinned axe 4.10.3 copy (SHA-256 matches `AXE_SHA256` in `checks/regulatory_ux_check.py`) are available.
* Docker is available. A SQL Server 2022 container can run on a loopback port with a random password held only in the shell. The ODBC Driver 18 for SQL Server package (`msodbcsql18`) was missing and is installed from the configured apt source.
* Test selectors depend on path order: `test_chat_panel` exists in both `core/tests` and `api/tests`; the browser unit test lives in `api/tests`.

## Scope decision

Verification-only slice. Run the focused tier (relevant unit tests, ruff check, ruff format --check, mypy for core, agents, api), the employee chat browser and axe checks, and the SQL contract tests listed in `mvp-ci.yml` against a local disposable SQL Server. Record results. Do not claim live, screen-reader or voice-control acceptance.

## Open items outside scope

* Live employee-site verification (needs an attested employee sign-in, #612).
* Screen-reader and voice-control acceptance.
* Owner confirmation of the five bounded agents' names (issue comment 2026-10-29).
