<!-- markdownlint-disable-file -->
---
title: Issue 164 held-out freeze gate details
description: Phase details
ms.date: 2026-11-04
---

## Details

* The gate returns `insufficient` with named problems when the digest differs, the labeller is missing or is the implementer, the freeze date or critical errors are missing, a binding changed since freeze, or six consecutive words are shared with the development set or system prompt.
* Otherwise the set is scored with `chat_eval.run_scenario` and the result is `pass` or `fail`, with a claim that no actual-model or human effectiveness is shown.
* No model call, no memory capture, no live use, no approval or consent authority.
