---
title: Issue 107 R1 agents dispatch review
ms.date: 2026-10-15
---

Review executed once after implementation. Outcome: conformant with open follow-ups.

## Checked

* Plan phases match the changes artifact. Extraction is behaviour preserving: the 110 contract tests pass unchanged. Dependency rule holds (agents imports only agents and core; no new dependency; no SQL or blob in the agents image). Messages carry only the allow-listed task keys and the inert snapshot; failure envelopes keep no raw text or exception text. Human review, fencing and release admission remain in the API.

## Findings routed to follow-up

* Medium: model call still runs in the API process until the queue transport and result post-back exist (#144); complete needs API caller authentication (owner decision).
* Medium: `ResultMessage` is not yet consumed by an API `complete` endpoint; the API re-validation path is the existing `Assistants.complete`.
* Low: `shape_result` and `build_request` live in core by the dependency rule; revisit when #144 settles.
* Low: image and `mssql` jobs unverified locally; wait for CI.
* Owner decisions: approvers, retention, break-glass.
