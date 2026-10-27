---
title: Resident assistant Azure OpenAI changes
ms.date: 2026-10-27
---

## Scope and State

Full plan, P01-P03. Research executed; one critique Revise, direct corrections
recorded before implementation. Implementation active. Human approvals remain
open. No claim of live activation or full acceptance.

## P01 - Runtime and Accounting

Implemented bounded model advice, stable own-case accounting, atomic SQL
reservation/usage and explicit deterministic fallback. API startup uses
namespaced opt-in configuration and only ManagedIdentityCredential. The HTTP
host binds accounting to SHA256 of the server-resolved case ID and reauthorises
after inference/fallback. Default rules and the legacy adapter remain.
The SQL verifier now admits exactly the two accounting object EXECUTEs, not
schema EXECUTE, role membership, direct table access or grant options.

## P02 - Infrastructure and Documentation

Dedicated default-off template compiled and provisioned successfully with:

* `Microsoft.CognitiveServices/accounts/aoai-resident-469`, swedencentral,
  local auth disabled and dynamic throttling disabled.
* Account deployment `resident-mini`, gpt-4.1-mini 2025-04-14, Standard
  capacity 1, NoAutoUpgrade.
* Account-scoped assignment `59b49580-bbf9-53d5-80eb-a389ac963e52`,
  Cognitive Services OpenAI User, existing resident principal
  `ab308885-7010-41b8-8b70-9ef5eabe40d0`.

All in existing RG ama, deployment `resident-assistant-469`. No other roles,
groups, resources or ingress changes. No temporary Azure resources were
created, so there are no test leftovers to delete. Intended account remains.
Actual successful what-if contained only these three actionable Create rows.
Readback confirmed exact model, SKU, capacity, upgrade policy and role scope.

Resident health HTTP200 on reachable old `ca-resident-demo--0000002`;
anonymous request to new AOAI inference endpoint returned HTTP401. Neither
is evidence of authenticated new-runtime MI inference. Zero model requests
were issued with credentials; no inference spend was incurred by these probes.
No stored secrets, password/verifier or owner session were read.

## P03 - Validation and Review

* Focused API/model/legacy/showcase tests: 72 passed.
* Full API regression: 1108 tests, OK, 314 existing opt-in skips.
* Core assistant: 6 passed; SQL boundary suite 29 tests, 19 opt-in skips.
* New compiled-account policy: 3 passed.
* Existing identity/RBAC inventory: 11 passed.
* Existing resident-deploy contract: 15 passed.
* Existing Bicep policy regression: 50 passed.
* Local gate tooling: 30 passed after preserving the original selector order.
  New accounting integration selector is wired into local and hosted SQL
  suites; workflow identity hashes updated. No check names changed.
* Changed runtime/core strict mypy and component Ruff checks passed.
* Existing resident assistant Chromium check passed keyboard/focus, response
  isolation after logout, retry/error, 320px reflow and reduced motion.
* Node syntax and git diff whitespace checks passed.
* New actual SQL accounting tests: Not run. Both standalone attempts to
  acquire `/tmp/ama-rpi-heavy.lock` with timeout 0 exited 1 before Docker
  startup. No other session's container, process or lock was touched.
* Scoped committed-head gate: pending after original Review/commit; output
  must be external. Do not treat focused checks as a passing gate.

Web guidelines refreshed from the required source and changed assistant.js
reviewed against it. Result: `src/api/src/zava_forward/api/resident_demo/web/assistant.js`
passes for the one explanatory-copy change. Existing native controls, focus,
live regions and CSS remain unchanged. No general WCAG conformance claim.

## Remaining Work and Review Handoff

Independent Review executed once: Complete, outcome Not accepted for whole-task/
live acceptance. No substantive source defect was established. RV-001 (actual
SQL) and RV-002 (new-runtime authenticated inference) are High evidence gaps,
routed to bounded later evidence work; they are not silently closed by mocks.
Local capability is implemented, resource provisioning observed. Actual
SQL accounting execution, private migration, running new image/config,
authenticated MI/resident smoke and publication remain unaccepted.
Private SQL has publicNetworkAccess Disabled and resolves publicly on this
host; do not weaken that boundary. Existing resident access still expires
no later than 2026-11-01 UTC despite the December funding horizon.

## Commit and Publication Handoff

The ordered RPI assessment loop is complete, not whole-task acceptance.
The original Review is preserved unchanged. Commit implementation and dated
evidence, then run the requested `tools/rpi-checks.py --changed --lock-timeout 0`
against current fetched main in a new external output directory. Required
SQL/browser/scanner or shared-lock failure blocks publication; no cloud
fallback, force-push, protective-rule change or unreviewed rollout is allowed.
Current fetched main is 49c942b33b89100c084d48a91215989e22de5887; its sole new
commit is documentation #439, with no executable overlap. No history rewrite.

Implementation and original RPI evidence committed as 7d854c84. Initial scoped
gate preflights blocked on ignored generated caches, then the candidate not
descending from advanced main. All 95 selected cache/bytecode/egg-info files
were archived with the entire tracking snapshot, restored and hash-checked
outside the checkout, then individually removed; source and original evidence
bytes were verified unchanged. Preservation receipt and prune journal are in
the external session files. A normal merge integrates documentation-only #439
without rebasing; the append-only knowledge log retains both additions. This
publication maintenance is not another critique or Review and does not close
RV-001 or RV-002. Run a fresh scoped gate on the resulting committed head.

## Amendments and Divergences

Critique corrections adopted in the plan. No authority extension: the renewed
funding window does not extend the resident-access window.

Live ARM what-if rejected nano Standard as unsupported. Deeper model metadata
shows its advertised Standard SKU is fine-tuned-model only; mini-4o ordinary
Standard is retired. Selected the cheapest current non-reasoning regional
candidate, gpt-4.1-mini 2025-04-14 Standard capacity 1 in Sweden Central.
Verified retail regional input USD0.000484/1K and output USD0.001936/1K:
8192 input + 256 output <=USD0.004460544, still below the one-cent reservation.
No resource was created by the failed preflight. This is a compatible model
selection under the owner's explicit "cheapest available" direction, not a
new funding or deployment-type decision.
