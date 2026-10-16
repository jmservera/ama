---
title: Regulatory security and privacy changes
description: Implementation and validation record for issue 217
ms.date: 2026-10-16
---

## Scope

Full plan for task 217 / regulatory-security-privacy-217. Executable writes are
limited to src/ and infra/; requested documentation and tracking artifacts are
separate evidence. Starting boundary: P01-T01 after plan critique disposition.

## Validation intent

Focused existing and new synthetic suites, project ruff/mypy and loopback HTTP.
No Azure, actual staff processing or paid model calls. DPO/live acceptance gaps
remain outside locally provable completion.

## Plan critique disposition

PC-001 rejected: the existing evaluator requires an evidence reference but not
recorded reasons. The existing test supplies SYN-HUMAN and no reason. Adding
`reasons` changes the contract, justifying ENGINE_VERSION invalidation.
PC-002 applied: clarify unique Entra principal binding versus existing thread
ownership. Implementation is ready; no unresolved policy decision was invented.

## P01-T01: Controls completed

* API auth maps a separate trusted RegulatoryChat capability, uniquely bound
  through existing principal matching. Infra manifest/script and parity checks
  include author, owner and chat capability declarations.
* Direct regulatory and generic read/archive/delete routes enforce capability;
  generic lists omit unauthorized regulatory threads. Claim-derived roles are
  retained across SQL provisioning rereads, including mutation authorization.
* New regulatory_privacy read model exposes own-role thread metadata, including
  archives, and existing simulated chat settings. All other class periods remain
  unknown; there is no disposal or approval path.
* SQL turn/referral metadata audit uses the current repository transaction and
  existing chain append primitive. An injected failure after audit insert rolls
  back messages, receipt, inbox and chain head. JSON retains its documented
  separate-file post-commit boundary.
* Engine version 2 requires explicit reasons, invalidating older checkpoints
  that could be clear with only an evidence identifier.

## P02-T01: Tests completed

Added 10 methods (three retention, three core chat, one auth and three HTTP);
extended the existing significant-decision and infra parity tests. No tests
removed. Retargeted the pre-existing post-commit audit regression to JSON, where
that limitation still exists; SQL now has stronger transaction-failure evidence.
No generated fixture or evaluation report changed.

## P02-T02: Validation and documentation

Observed local results with installed editable distributions and absolute test
PYTHONPATH per project:

* Core: 99 tests across regulatory privacy/chat, rule engine/cards and shared
  chat privacy/storage; another 59 source-monitor/chat-panel/memory regressions.
* API: 44 regulatory HTTP/auth/alerts tests; another 72 isolation/panel/ledger/
  role-matrix regressions. Final seven-test regulatory HTTP rerun passed after
  adding claim-role checks to generic archive/delete.
* Agents: seven exact-quote/injection/refusal/comparator regressions passed.
* Infra: 22 identity/registration and staff-initialization tests passed; shell
  syntax check passed. No Bicep or live tenant operation.
* Full project ruff and mypy passed for core (98 typed files), API (45) and
  agents (19). node --check for chat.js and git diff --check passed.
* Missing ruff/mypy were installed using pip in a session-isolated venv; the
  declared Playwright dependency was restored after API mypy reported it absent.
* Loopback HTTP tests start responsive ephemeral servers, assert health/case
  200 and the real regulatory routes, then stop them. No provider call allowed.

Initial validation caught an insertion indentation error, stale SQL post-commit
test expectation and a missing CSRF test header; all were corrected and the
affected suites rerun. Final direct review caught generic archive/delete using
the register role; corrected to the admitted claim role and exercised with both
positive own-role and negative wider-role operations.

Updated core/API/infra READMEs, knowledge-base index/log and the existing DPIA
draft. No issue checkboxes changed. DPO completion, DPO-set retention, actual
Entra/SQL/Foundry evidence, operational decisions and real-data approval remain
unmet or partial as enumerated in the API acceptance table.

## Pre-Review reconciliation

P01-T01 and P02-T01/T02 complete with evidence above. Publication is separated
as P03-T01 so Review does not prematurely claim commit/push/PR. This is a
tracking clarification, not a scope change. Details and plan agree. Ten new
methods remain below the locked maximum of 20, no removals. No implementation
blocker remains; human/deployed acceptance is routed as distinct follow-up.
