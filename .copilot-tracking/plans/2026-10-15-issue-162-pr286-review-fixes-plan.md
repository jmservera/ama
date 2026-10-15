---
title: PR 286 review fixes plan
description: Plan for five review fixes on chat isolation
ms.date: 2026-10-15
---

## Phases

* [x] 1. memory_for delegates to privacy.prompt_memory with the thread task; prompt block is labelled JSON.
* [x] 2. Memory endpoints: opt-in, opt-out, edit, delete, global and task switches, status; add requires task.
* [x] 3. Mask question first and prompt the masked text; redact stored replies.
* [x] 4. Case out of scope raises ChatNotFound; 404 for not found.
* [x] 5. Tests (lifecycle, masking, 404) and README; run the full suite.

## Critique

Executed once inline. Verdict: compatible. Keeping 403 for role denial is consistent with the existing role-matrix tests and leaks no case existence.
