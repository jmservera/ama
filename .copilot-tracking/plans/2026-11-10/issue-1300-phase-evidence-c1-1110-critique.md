---
title: Issue 1300 C1 plan critique
description: Single critique of the C1 plan, original verdict and direct dispositions
ms.date: 2026-11-10
---

Executed once (rubber-duck, read-only) on the final-candidate plan. Original verdict: Revise, 4 findings, all compatible with confirmed decisions and applied directly. Not repeated.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | Log and lock targets can themselves be symlinks outside their directory | Applied: check `events.jsonl` and `events.lock` as well as the directory before any open; test both substitutions |
| 2 | Blocking | Dirty-artifact hashing in `dirty_identities` runs before artifact loading | Applied: containment before hashing tracking paths, in record and verify; test no external open |
| 3 | Non-blocking | `git diff` succeeds for a non-ancestor HEAD, so divergence is not "unable to compare" | Applied: explicit `merge-base --is-ancestor`; non-ancestor is qualified as unable to compare |
| 4 | Non-blocking | Quoted non-ASCII names can falsely qualify tracking-only changes | Applied: `git diff --name-only -z` and NUL parsing |
