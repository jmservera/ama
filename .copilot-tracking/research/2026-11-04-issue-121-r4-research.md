---
title: Issue 121 round 4 research
ms.date: 2026-11-04
---

Research disposition: reused (merged PR check and issue comments on 2026-11-04).

* Merged: #919 (register, model-dispatch gate, rights clock), #1013 (read-only register route), plus contextual #205 and #281 (chat DPIA record). Open: #1106 (slice 3, fail-closed dispatch hold at the model transport).
* Issue comments: Legal, Compliance and DPO owner for the exercise is the repository owner; the 2026-10-31 closure audit marks C1 to C11 unmet except the constructed-fixture tick.
* Remaining engineering: persisted, answered rights-request log. It needs SQL state in both stores (SQLite and SQL Server) and a staff write route, which is a SQL-sensitive slice that depends on #1106 and on the DPO deciding the extension and identity-verification rules. Not safe to build ahead of that decision.
* Remaining other work: DPO lawful basis and Article 17(3) position; Legal retention period; approved transfer position; derivative or necessity approval for intact documents; whole-system inventory review. All are human or legal steps.
* Planning readiness: no coherent unmet-criterion slice that avoids duplicating #1106 or inventing a legal decision. Docs-only record.
