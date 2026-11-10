---
title: Issue 135 C3 plan critique
description: One-pass critique of the final candidate plan and first source draft
ms.date: 2026-11-10
---

* Critique executed once, 2026-11-10T03:48Z, by the implementing session on the final candidate plan, details and the uncommitted first draft. It is a self-critique, not an independent review. It is not repeated.

| Id | Item | Severity | Disposition |
| --- | --- | --- | --- |
| K1 | A running JSON-store server holds `data` in memory with no reload, so an external transfer is overwritten on its next save and invisible until restart | Significant | Accepted limit and documented: the served story and README require stopping a JSON-store server before `transfer`; the SQLite store re-reads the document on each lock entry and is the live path. Tested with both |
| K2 | `import_exceptions` would silently vanish on SQL reload if not in `SqlStore.DOCS` | Blocking | Fixed in the draft; a SQLite restart regression must fail without it |
| K3 | The screen does not show `original_source.at`; the time is appended to the displayed reason | Minor | Accepted trade-off to avoid a web edit; time is also kept in `original_source.at` |
| K4 | The static empty-state text on the screen still says failed imports are not connected | Minor | Accepted: conservative and not an all-clear; the Sources list is the accurate line. Recorded as follow-up, no web edit |
| K5 | `EX-nnn` ids are positional and can move when new items appear | Minor | Accepted: the stable identity is `ref`; tests assert the ref, not the id |
| K6 | Transfer trust boundary is whoever can run the CLI against the store; no HTTP route is added | Minor | Accepted: same boundary as other local tools; no new permission or role |
| K7 | Same ref with a different reason keeps the first copy; a later re-refusal is not shown | Minor | Accepted, matches the ledger's first-reason-stays rule |
| K8 | A damaged projection must not look connected | Blocking | Draft already reports unrouted and keeps NOT_CONNECTED; a regression covers it |
| K9 | SQL Server not exercised | Significant | Not claimed; stated in the handoff |

Verdict: proceed with the dispositions above. No conflict with a confirmed decision and no user decision required.
