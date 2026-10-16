---
title: Resident decisions PR evidence mapping
description: Verified PR assembly from the completed RPI evidence and structured branch diff
ms.date: 2026-10-15
---

## Evidence

The pr-reference skill generated `.venv/resident-pr-reference.xml` from
`origin/main` with `--merge-base`: 3,492 lines for commit ee649f0.
The XML is temporary; no private data or environment files were included.
The single canonical RPI Review owns assessment findings; PR assembly did not
launch a second Review or duplicate that source comparison.

## Description Mapping

* Core decision/authority and dependency changes map to P01 and bounded A1-A3.
* Existing API/UI, two regression modules and fixture changes map to P02.
* Five suites and quality checks, loopback/browser evidence, component guides,
  reference index/log and RPI artifacts map to P03 and A5.
* The fourth issue criterion and operational/live gaps stay unchecked, grounded
  in RV-001 through RV-003; the PR uses Refs #86.
* The public PR body expands pr.md with the complete changes command/result
  record, excluding YAML frontmatter. No new discovery or acceptance claims.
* No repository PR template was found in `.github`, `docs` or repository root.
  Applied the fallback summary/changes/evidence/related-issue structure.
* Base advanced by two commits (#315/#316); no automatic lineage change.
  PR #319 reports CONFLICTING/DIRTY and no checks. The read-only merge-tree
  diagnostic identified four conflicting files, now listed in pr.md and changes.
  Owner-authorized integration is required; no source correction or repeated
  Review was performed. CI and mergeability are not local pass claims.
