<!-- markdownlint-disable-file -->

# Task Research: issue444-resident-feedback-preview

| Field | Value |
|-------|-------|
| Date | 2026-10-24 |
| Researcher / agent | rpi-research, run inline by the RPI Agent (no worker dispatched) |
| Status | Complete, Planning Readiness Ready |
| Research disposition | executed |
| Artifact path | .copilot-tracking/research/2026-10-24/issue444-resident-feedback-preview-research.md |
| Task | `task_id` issue-444, `task_slug` issue444-resident-feedback-preview, mode automatic |

## Research Brief

* What to research: the actual text and acceptance criteria of [#444](https://github.com/jmservera/ama/issues/444) (read through `gh issue view` and the brief at `/home/azureuser/.copilot/session-state/008a3969-.../files/resident-preview-issue.md`, see [creation record](../../github-issues/issue-444.md)), plus the repository code that a read-only synthetic resident preview must reuse or avoid.
* Why it matters: the owner (2026-10-24) wants both employee and resident sites inspectable ASAP, with at most eight parallel work items.
* Scope: `src/core` (case store, appointments, representative authority, projection), `src/api` (server, tests, browser checks, packaging), UX standards (design system, WCAG baseline, content standard), PR #442 as unsigned input.
* Non-goals: live service, real data, external exposure, uploads/messaging/consent/AI, new cloud identity, password database, staff-route changes.

## Safety reading of the issue

The issue is a specification, not authority to relax safeguards. Resolved conflicts:

| Issue or brief text | Repository rule that governs | Resolution |
|---|---|---|
| "explicitly granted synthetic case" | Resident consent, authority and privacy boundaries in the repository instructions; no real resident data | Grants are server-side fixture records; default deny; nothing reads normal `ZF_DATA`, `.env`, rosters or secrets |
| "representative sees only current, case/task-scoped information" | Representative authority is a human-confirmed domain record (`resident_decisions.authority_for`) | A grant reference alone grants nothing; the existing domain check must also pass per task |
| "Fixture identity refuses production/cloud configuration" | Branch/cloud safeguards in the brief | Startup refuses cloud/store/AI environment variables and non-loopback hosts |
| "Case identifiers do not convey authority" | Existing staff `GET /api/case/{id}` is staff-only | Resident routes take no case id; the grant selects the case |
| Existing `/api/cases/{id}/resident` | It is staff recording | Not exposed, not reused by the resident server |

## Evidence

Main at `f1e2d830` has no resident site, principal or subject-to-case grant (a case-insensitive search of `src/` for resident principal, resident/subject grant and `ZF_RESIDENT` finds only opt-in test environment names in `test_resident_decisions.py` and `test_resident_api.py`; the only resident write surface is staff recording).

| Finding | Source | Consequence |
|---|---|---|
| Staff API authenticates with `provider.authenticate(headers)` and an `allowed()` role allow-list; `STAFF_GET` is the default-deny list | `src/api/src/zava_forward/api/server.py`, `core/projection.py` | Do not extend. A separate resident handler and entrypoint avoid editing `server.py`/`auth.py` |
| `projection.py` already hides staff free text per role by deny-by-list | `core/projection.py` lines 1-40 | A resident view must be a positive allowlist built from named fields, not a filtered staff payload |
| `Store(data_path, live_path, audit_path)` loads the dataset into memory; constructor creates directories next to `live_path`, a document store and AI object | `core/store.py` 45-70 | Open the dataset by copying into a fresh private temp state directory; never write beside the dataset; refuse AI/cloud environment |
| `data_file()` defaults to `~/.zava-forward/data/zavaforward.json` | `core/data_paths.py` | The preview must require an explicit path and refuse the normal path/directory |
| Appointments: `appointment_status(w)` returns `Committed`, `Offer`, `Unknown`, or `Ended` from work order evidence | `core/appointments.py` 150-210 | Offer text and confirmed text map directly from this authoritative status; unknown stays unknown |
| Representative authority: `authority_for(c, ref, task, measure, context, version)` requires a `Confirmed` current record, task, measure, context revision, safe-contact revision and dates | `core/resident_decisions.py` 487-500 | Reuse unchanged for the representative checks |
| `STAGE_ORDER` is the 25 authoritative stages; `waiting_on`, `reason`, `history`, `contacts` are staff free text | `core/insights.py`, case shape in `core/tests/dataset.py` | Map stage to fixed plain-language text; unknown stage text says unknown; never pass free text through |
| Test and fixture helpers (`supplied_contract_fixture`, `supplied_appointment_fixture`, resident scope/decision fixtures) live in `src/core/tests/dataset.py` and cannot be imported from `src` | `core/tests/dataset.py` | A src-side synthetic builder reproduces the minimum through public Store operations |
| `api` package-data lists `web/*`, `web/vendor/*` only (not recursive) | `src/api/pyproject.toml` | Resident assets need one additive package-data line; no other shared runtime file changes |
| Existing browser checks are manual Playwright scripts under `src/api/checks/` run by the gate (`design_system_browser_check`, etc.) | `src/api/checks`, `tools/rpi-checks.py` | A new check script for the resident site follows this convention; the gate's current set is not changed |
| Design system: Fluent 2 token foundation, tokens documented, status needs non-colour cue, 40px native buttons, two-tone focus; `test_design_system` tests only `style.css` | `docs/reference/research/ux/design-system.md`, `tests/test_design_system.py` | Resident CSS reuses the same Fluent token names in its own file; no edit to `style.css` (documented tokens test unaffected) |
| Content standard: plain language, blocked message with reason, owner, next action; no resident wording is human-reviewed yet | `docs/reference/research/ux/content-standard.md` | Resident copy is provisional; the page states that wording is unreviewed |
| #350 worktree changes only tools/check-demo-feedback.py, tests and tracking, no runtime product files | `git diff --stat` of that worktree (2026-10-24 13:35 UTC) | No overlap with `src/`; no reservation conflict. Shared-path reservations recorded below |
| PR #442 is unsigned design input | owner brief | Read as input only; nothing depends on it. (`gh pr view 442 --repo jmservera/ama` shows it OPEN on `docs/resident-portal-requirements-441`, docs and tracking files only; its content is not required and is not a dependency) |

Web interface guidelines were fetched on 2026-10-24 from `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` (retrieved in full). The `accessibility` skill was loaded; its runtime probe harness needs `uv`/`npx`/system Chrome and the owner prohibits uv, so it is not run. Disclosed as unperformed. `redesign-existing-projects` is not applicable: this is a new separate page, not a redesign of an existing screen. `design-taste-frontend` targets public marketing pages, not applied; Fluent 2 baseline governs.

## Options considered

| Option | Summary | Decision |
|---|---|---|
| A | Add resident routes and a role to the staff `server.py`/`auth.py` | Rejected: edits shared staff authorization, risks staff behavior, needs #350 coordination |
| B | Separate resident package with its own loopback handler, grant registry and projection, reusing the Store read-only | Selected |
| C | Static/screenshot-only mock | Rejected: the issue requires real server/store path |

Identity options: browser role selector, URL subject, header claim, password, staff impersonation all rejected by the issue. Selected: the server process is started for one fixture subject by the server-owned harness (`--subject`), so identity is process configuration. Two residents are inspected through two loopback listeners or two server instances; no browser input chooses identity. Revocation and expiry are evaluated from the grant file on every protected request.

## Reservations

Shared paths this task will edit, all additive: `src/api/pyproject.toml` (package-data line, per-file Ruff/mypy exceptions not expected), `docs/reference/README.md` and `docs/reference/log.md` (index row and appended entry), `src/api/README.md` and `src/core/README.md` (resident preview section). No coordinator channel name was provided, so the reservation is recorded here and in the final report; conflicts would be textual and additive. `server.py`, `auth.py`, `projection.py`, `store.py` are not edited.

## Risks and unknowns

* Appointment helper fixtures depend on contract and capacity setup; the builder must call public Store operations and must pass in a disposable directory.
* Authority date checks use the real clock; fixtures use far-future review dates.
* No resident-reviewed wording, no accessibility conformance claim, no user testing.

## Planning Readiness

Ready. All gates: disposition recorded, acceptance criteria mapped (see plan), evidence cited, unknowns bounded, safety conflicts resolved.
