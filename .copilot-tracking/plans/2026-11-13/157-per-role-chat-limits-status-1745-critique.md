---
title: Issue 157 per-role chat limits plan critique
ms.date: 2026-11-13
---

Independent critique by rubber-duck, executed once. Verdict: Revise.

* PC-001 blocking: concurrent turns could exceed the thread cap. Applied: count inside the lock that persists the question.
* PC-002: usage off by one. Applied: usage includes the current question.
* PC-003: usage not displayed. Applied: chat.js shows turns used.
