---
title: Issue 121 s3 details
date: 2026-11-04
---

* `dispatch_hold(class_id, env, derivative)`: None when `ZF_DATA_PROCESSING` is unset or `constructed`; otherwise reuses `model_dispatch` and returns reason plus manual path. Typos fail closed.
* `Ai.run` uses class `prompt_output`; `Ai.look_at` uses `raw_document` with no derivative, so intact bytes are never sent in actual mode; `_request` raises `DispatchDenied` as a backstop.
* Users see the template or "file is stored" text and the manual path (AI-unavailable behaviour preserved). No web UI change.
* Out of scope: derivative production, agents chat model, rights log persistence, any approval or retention value.
