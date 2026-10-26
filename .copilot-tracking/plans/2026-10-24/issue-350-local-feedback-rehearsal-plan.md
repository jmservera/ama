<!-- markdownlint-disable-file -->
---
title: Issue 350 local feedback rehearsal plan
description: Plan to run the existing app on a synthetic SQL fixture for owner feedback
ms.date: 2026-10-24
---

## Overview

Provide an executable loopback rehearsal of the existing src application, then
record evidence. Details: [phase details](../../details/2026-10-24/issue-350-local-feedback-rehearsal-phase-details.md).
Research: [research](../../research/2026-10-24/issue-350-local-feedback-rehearsal-research.md).

## Phases

* [x] Phase 1: Prepare isolated runtime (external venv, pip installs, disposable labelled SQL container on 127.0.0.1, constructed fixture JSON outside the repository).
* [x] Phase 2: Exercise real behavior (login per role, queue, one case action, reload, SQL restart durability, denials, AI/manual, browser).
* [x] Phase 3: Owner-facing server in tmux `ama-350-feedback`, loopback only, with health evidence; stop test helpers.
* [x] Phase 4: Record changes evidence, run the complete local gate on a clean frozen commit, independent review.

## Constraints

* No model inference, cloud writes, tenant changes, private data, 0.0.0.0 bind, auth weakening, push or PR update.
* No source change unless a genuine defect appears.
* Not deployed sign-in, usability acceptance, operational readiness or #350 closure.
