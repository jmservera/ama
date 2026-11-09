---
title: Lifecycle and simulator controls current-main checkpoint 440 details
ms.date: 2026-11-09
---

## Phase details

* P1 `git status --short` shows only the five new tracking files plus the critique; commit with the privacy email and Copilot trailer.
* P2 Append-only edit at the end of `docs/architecture/cutover-evidence-pack.md`. Table rows with exact identities; commands listed with results: `git diff e192bc747 48350983b -- src tools infra`, `git diff e192bc747 0dc4dd35c -- src tools infra`, `git rev-parse <954 merge tree>:src` versus `48350983b:src`, `sha256sum -c MANIFEST-projection-src.sha256` over `git archive` of main `src` (642 OK), capture manifests (78 OK, 16 OK).
* P3 Index: one paragraph after the SQL-wave entry in `docs/reference/README.md`; log: one entry at the end of `docs/reference/log.md` with the existing format.
* P4 Links: Python script over added lines resolving relative paths. Preservation: `git diff --numstat origin/main HEAD -- <pack> <index> <log>` deletions column 0.
* P5 Record changes and one Review; update state to Follow-up; commit.

## Wording constraints

ASCII only, no em dashes, no bolded-prefix list items, dated identities, coordinator-held and coordinator-reported labels, no approval, closure, live, AT or hosted-for-this-branch claim.
