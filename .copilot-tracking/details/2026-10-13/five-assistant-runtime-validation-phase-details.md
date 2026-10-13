---
title: Five Assistant Runtime Validation Details
ms.date: 2026-10-13
---

## P01

Assistants.execute and stop share a short dispatch-admission lock. Do not hold
it while acquiring SQL, completing proposals or running provider work.
Requests already admitted remain subject to existing timeout/fencing rules.
Tests stop a delayed claim before it resumes; no subsequent dispatch occurs.

Case assistant panel returns its DOM immediately. Auxiliary GETs receive an
AbortSignal and finite deadline; failure is visible and independent of manual
case rendering. Completion must check the panel is current/connected. Extend
the existing isolated Chromium exercise, not a second browser test file.

## P02

Adapt existing fixtures through an overridable store factory, preserving
SQLite tests. Conditional SQL classes use only localhost/SQL-service targets
and a dedicated disposable test database. Never wipe pilot data. Keep the
existing 26 general SQL tests and add real assistant suites to that same job.
Provider remains a declared test double; SQL success is not real model proof.

## P03

Use existing unittest, Node, Chromium and Docker patterns. Publish source
before stamping an image with its exact commit. Current-date evidence must
distinguish corrected-source tests, local image and unchanged serving Azure.
No second parent Review or fabricated source-verification/human approval.
