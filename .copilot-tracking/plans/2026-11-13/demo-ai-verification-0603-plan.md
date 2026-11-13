---
title: Demo AI verification 0603 plan
description: Increment A from readiness, execute four existing modules in a source-pinned offline venv
ms.date: 2026-11-13
---

* Increment A only (not a source correction). Fresh venv, non-editable offline install of `src/core` then `src/agents` from `git archive HEAD`, `env -i` with owned HOME and ZF_DATA, run `unittest -v` for `test_ai_consumption`, `test_chat_panel` (core) and `test_candidate_comparison`, `test_chat_model` (agents), expose only test dirs for fixtures, record per-module counts, skips, import origins, true exit codes.
* Stop rules: zero tests, any skip or wrong import is not Pass; missing offline build prerequisite is BLOCKED, with no network or `PYTHONPATH` source fallback. No model, SQL, Docker, browser or private data. #891 attribution stays an owner hold; #531 live acceptance is not established.
