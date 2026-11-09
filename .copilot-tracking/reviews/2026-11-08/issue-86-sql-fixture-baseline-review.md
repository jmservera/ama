---
title: Issue 86 resident SQL fixture baseline author review
description: Author review of the baseline execution; not an independent assessment
ms.date: 2026-11-08
---

Scope: issue #86 only. Author review, one pass.

Outcome: baseline executed as planned (plan steps 1-3 only). Plan criteria met: owned container under the non-blocking canonical lock, unskipped single-method runs, origin and hash proof, observations kept apart from diagnosis, cleanup verified. The 4 != 40 failure remains open and still blocks publication; Main reproduction does not waive it. Routing: test-only correction needs separate admission; its fix is proven only by a later unskipped regression. Pending: independent exact-head assessment, hosted checks, human approvals, #1238. No tick, closure or publication.
