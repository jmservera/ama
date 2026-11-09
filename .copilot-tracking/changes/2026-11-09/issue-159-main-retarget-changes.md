<!-- markdownlint-disable-file -->
---
title: Issue 159 main retarget changes, review and target disposition
description: Dated append for the ordinary main merge and fresh composed-source checks
ms.date: 2026-11-09
---

## Changes

* Committed the prospective amendment, then ordinary `--no-ff` merge of `origin/main` `0dc4dd35ce9ea6bddd1d4ca34d5f8ec6e234adfe` (parent #189 squash). No conflicts, no rebase, amend or force.
* Proof: `git diff --stat de79f4b8b HEAD -- src` is empty, so source equals the independently reviewed head. Non-record paths that arrived: `.github/rubric/scores/latest.json`, `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md`. Main is an ancestor of the merged head.
* No source, fixture, config or ignore edit.

## Fresh raw evidence (external `159-main-retarget-logs/`, per-command .out/.err/.exit, SHA256SUMS.txt; earlier logs untouched)

* Ruff 0.17.1 `check .` and `format --check .`: Core and API exit 0 (223 and 127 files formatted).
* mypy 2.4.0 CI profile: Core 276 files, API 202 files, no issues.
* Core `test_chat*.py` 134 OK; `test_regulatory_chat.py` 25 OK. API `test_chat*.py` 100 OK with 1 skip (opt-in local Chromium, intentionally not run), regulatory_chat_api 9, role_endpoint_inventory 22, resident_chat_api 51, all OK.
* Not run: browser, SQL Server, full gate, hosted CI.

## Review and target disposition (authored, not independent)

* This closes the Core Ruff evidence gap with successful raw output on the composed source. Original critique, Review and independent Functional approve are retained unchanged; no new finding, no corrective cycle (history 1 confirmed, 1 possible, total unknown).
* Target: main, Refs #159 and Refs #189, no closing keyword. Independent reviewer qualification of this record/base delta and hosted CI remain required before publication.
