---
title: Phase details for issue 691 API error diagnosis
ms.date: 2026-11-02
---

* Critique (single pass, self-run): connection-dropping behavior replaced by a 500 JSON body only when no response has started; client disconnects are logged at warning and never answered; logged fields exclude message, query and headers. Verdict proceed; no conflicting advice.
* The guard sits in `handle_one_request`, so GET, HEAD and POST are covered once.
