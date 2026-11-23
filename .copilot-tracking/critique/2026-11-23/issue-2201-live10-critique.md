---
title: Issue 2201 live10 critique
ms.date: 2026-11-23
---

Executed once on the final candidate. Verdict: approve with direct dispositions.

* Risk: the class name could leak detail. Disposition: a class name carries none; message and traceback stay excluded and the test asserts it.
* Risk: log parsers match `Cannot run: RECEIVER_FAILED` exactly. Disposition: the prefix is unchanged and the suffix is appended after a space.
* Tier: src change, so FULL tier applies; the coordinator runs the gate, `--all` is not run here.
