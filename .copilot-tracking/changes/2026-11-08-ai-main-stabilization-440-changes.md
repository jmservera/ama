---
title: AI and employee chat main stabilization 440 changes
ms.date: 2026-11-08
---

## Changes

* `docs/architecture/cutover-evidence-pack.md`: one dated section appended (93 lines) for main `608c98e6`.
* `docs/reference/README.md`: one index paragraph linking the new section.
* `docs/reference/log.md`: one append-only entry.
* No code, tools, workflows, agents, BRD, PRD, ADR or tests changed. No push, PR, issue edits or cleanup.

## Actual local results (2026-11-08, scratch venv in /tmp, SQLite or fixtures, all exit 0)

* Core: chat_panel 43, chat_privacy 29, chatthreads 27, chat_memory 21, chat_case_answers 4.
* Agents: chat_model 7, chat_eval 39.
* API: chat_panel 53 (1 skip, opt-in Chromium), chat_isolation 32, ai_boundary 6, ai_call_site_inventory 6, assistants 120 (58 skips, needs ZF_TEST_MSSQL=1).
* Not run: SQL Server, browser, real provider, Azure, full gate.

## Divergences and amendments

* Critique PC-001 to PC-006 were applied before implementation; requirement mappings were corrected after a BRD re-read (FR-049, NFR-011, RULE-025, RULE-026).
* Plan files were not rewritten; checkboxes ticked on completion.
