<!-- markdownlint-disable-file -->
---
title: Issue 350 local feedback rehearsal research
description: Existing-runtime local synthetic rehearsal feasibility for owner feedback, distinct from the offline checker history
ms.date: 2026-10-24
---

## Research Brief

Owner request (2026-10-24): an executable local feedback rehearsal of the existing
`src` application using constructed synthetic fixtures, not another offline
checker. This is new maintenance on branch `test/deployed-feedback-harness-350`
(draft PR #436). Earlier dated #350 research, plans, critiques, changes and
reviews (2026-10-21 to 2026-10-23, offline checker and corrections 1-5) are
historical evidence and are not edited.

Research disposition: executed (focused, internal; one tightly coupled trace).
Planning Readiness: Ready.

## Evidence

* Issue #350 ACs remain unmet; they need the deployed app, tenant/staff
  (#349), a 980-case baseline, model deployments and release authority. A local
  rehearsal cannot close any of them.
* Branch state: clean worktree; published head 6ac8e029; stale base 140d8f49;
  `origin/main` f1e2d830. Reconciled by a local merge commit (history
  preserved, one-line `.github/rubric/artifacts.json` change only).
* Runtime: `python -m zava_forward.api` (`src/api/.../server.py:main`) binds
  `ZF_BIND` default 127.0.0.1, port `PORT`. `ZF_AUTH` default is the shared
  `PasswordProvider`; `make_provider` refuses it when `ZF_ENV=production`.
  Sign-in is `POST /api/login` with a staff email plus `ZF_PASSWORD`; role
  selection is therefore the existing choice of staff email. No new auth code.
* Stores: `ZF_STORE=mssql` with `ZF_SQL_AUTH=password` is documented for CI
  containers only; `mssql_python` is the driver (no host ODBC needed). Existing
  tests create task-owned loopback SQL Server containers
  (`mcr.microsoft.com/mssql/server:2022-latest`, present locally).
* Constructed fixtures: `src/core/tests/dataset.py` (`DATA`: staff Sam
  RLO-01, Pam PM-01; five fictional cases ZF-1..ZF-5 with a P1 hazard, a
  funded accepted case) and `test_coordinator.fixture()` (adds contractor and
  coordinator). Fixture data is hand-constructed, `*.example.test`.
* Case action: `POST /api/cases/<id>/call` (`Store.log_call`), also `decision`,
  `advance`; reload is `GET /api/cases/<id>`.
* AI: `POST /api/ai/priority` and `/api/cases/<id>/ai` without a configured
  model must fail closed or show manual behavior; assistants have a
  workflow-only/failure path (`503 ... continue ordinary case work manually`).
  No model endpoint exists in a fresh environment and none is authorized.
* The private stock register generator in `src/api/README.md` ("Run it
  locally") reads private data. It is excluded.
* Deployed URL returns 403 at `/`, `/health`, `/api/me` (owner statement); not
  re-probed here, to avoid duplicating #349.

## Data classes (never conflated)

| Class | Source | Size | Used here |
| --- | --- | --- | --- |
| Continuing generated stock fixture | `core/synthetic/scale_fixture` | 60,000 homes | No |
| Constructed engineering scenario | `core/tests/dataset.py` plus coordinator additions | 5 cases, 4 staff | Yes |
| Representative programme | private 980-case dataset | 980 cases | No, unmet |

## Decision

Run the existing server over an external-directory fixture and a disposable
labelled loopback SQL Server container; no repository code change is planned.
Add a code change only if a genuine defect appears (focused failing test first,
two correction cycles maximum). Keep the owner-facing server in a named tmux
session bound to 127.0.0.1 only.

## Open risks

* Password mode is a synthetic convenience, not Entra proof; the page does not
  label itself test-only. The owner is told in the hand-off; no UI change is
  authorized.
* Forged-header denial is only meaningful for the password provider (headers
  ignored); trusted-proxy mode needs `ZF_TRUSTED_PROXY` and is exercised by
  existing `test_auth.py`.
* Browser usability is a basic existing-DOM check, not user acceptance.
