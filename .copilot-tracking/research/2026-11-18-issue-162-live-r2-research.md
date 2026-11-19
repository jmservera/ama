---
title: Research for #162 live cross-user isolation proof (r2)
ms.date: 2026-11-18
---

## Opening

* Issue #162: only criterion 6 unticked (admin and break-glass audited with purpose, policy decided). Criteria 1 to 5 ticked.
* Owner request: prove live on the synthetic demo that one user cannot read another's chat or memory, using the staff and resident test sign-ins.
* Prior evidence: docs/reference/research/chat-breakglass-live-proof-2026-11-18.md (criterion 6, partly proven) and a prior run's `issue-162-live-*` artifacts, which this run does not modify.
* Constraints: demo only, desktop, live Azure authorised (rg ama), no drills, no Key Vault rotation, no production change; credentials never printed; tier FOCUSED unless src changes.

## Deviation (honest record)

The brief's state path `.copilot-tracking/rpi-sessions/2026-11-18/issue-162-live-state.json` and `research/2026-11-18-issue-162-live-research.md` already existed from an earlier run. This worker overwrote both by mistake, then restored them with `git checkout`, and uses `-live-r2` names instead. The `research-open` witness record (seq 2, 12:43:17Z) points at the restored original state path, not the r2 state.

## Open questions

* Do the staff and resident identities share one chat store?
* What cross-user probes are possible with real identities?

## Findings

* The demo API (`ca-cutover-test-demo-api`) is the only chat and memory store. Auth is Entra Easy Auth with trusted-proxy; the server derives the owner from the validated principal (`server.py` `_chat`, `user_key(user)`), and thread and memory repo calls take `owner`.
* The resident portal (`ca-resident-demo`) signs in with a demo email and password and has no thread or memory routes (assistant is ephemeral). It cannot hold a second chat identity on the API.
* Only one staff Entra identity exists (`~/.ama-test-user-id`). A genuine "user B reads user A's thread" test with two Entra users on the API is therefore not possible live; thread and memory ids are random (`CT-` plus 16 hex characters), so foreign ids cannot be guessed.
* Feasible live proofs: anonymous denial; resident session replay against the API; forged principal headers and client-supplied owner fields ignored; never-issued ids give 404; own-resource positive control; clean-up of own synthetic records.
* Criterion 6: already partly proven by `chat-breakglass-live-proof-2026-11-18.md`; not re-run beyond a pointer.
* Planning Readiness: Ready.
