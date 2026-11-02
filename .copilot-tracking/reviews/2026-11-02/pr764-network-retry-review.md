---
title: PR 764 third CI failure review
date: 2026-11-02
---

Execution: executed once. Outcome: conformant for scope.

* Real cold-start behaviour preserved: GET reads, non-JSON 500/502/503/504, bounded, status restored.
* Trade-off: a connection reset during cold start is no longer retried; the Container Apps gateway answers with an HTTP response, and this is what the owner direction specifies.
* Open: hosted CI, independent exact-head review and human approval remain required. Container steps unverified locally.
