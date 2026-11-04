---
title: Research - resident callback 503 (#1053)
ms.date: 2026-11-04
---

## Scope

Issue #1053: the signed-in resident page invites callback booking, but live `POST /demo/agenda` returns 503 because no agenda is configured.

## Evidence

* Merged PRs: #1064 recorded the walkthrough only (docs). #1069 (phase 1 redesign) kept the static lede and the always-mounted form. No merged PR addressed #1053.
* `resident_demo/__main__.py` builds an `Agenda` only when `ZF_DEMO_AGENDA_PATH` is set; `app.py` returns 503 when `app.agenda is None` (explicit failure by design, kept).
* `index.html` lede, `demo.js` (optional link, `mountResidentAppointments`, unavailable-list text, nav label) and the chat `appointments` topic all assumed an agenda.

## Options

* A. Connect a synthetic agenda in the cloud composition: infrastructure and deployment change, needs the gate and owner decision. Not in this slice.
* B. Make the page promise only what the app can do: server reports `callbacks_available`, client hides the form and wording, chat stops offering the search. Code-only, small.

## Decision

Slice 1 = option B. Option A remains a follow-up (infra/deployment, gated). Planning readiness: Ready.
