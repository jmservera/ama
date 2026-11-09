---
title: Backlog sync demotes confirmed active delivery
description: Generic issue fields and reproduction record for #1207
ms.date: 2026-11-05
ms.topic: reference
---

## Created Issue

* Issue: #1207, https://github.com/jmservera/ama/issues/1207
* Template: generic; .github/ISSUE_TEMPLATE absent.
* Labels/assignees/type: none specified. Severity: Medium. Target: main; independent tooling repair, not a case-feature child.
* Title: Preserve confirmed active RPI delivery state during backlog reconciliation
* Scope: tools/backlog-sync.py and focused regressions; no acceptance fabrication.

## Reproduction and Evidence

* 2026-11-05, main 50c5a0902666524b556bbda05bd673fc8ed758f7, origin/main ead177ef90d24666557708ea344848a1be43bdf8: `--apply` moved #79/#80/#82 from In Progress to Todo while `rpi-79`, `rpi-80`, `rpi-82` were running. The coordinator restored and read back each status.
* Cause: only an open PR or a worktree directory named exactly `issue-<N>` counted as activity; real worktrees (`issue-79-publisher`, `rpi-80`) never matched.

## Acceptance Criteria

* [ ] Regression reproduces demotion with a confirmed live session or frozen candidate.
* [ ] Verified active delivery preserved or proposed In Progress despite merged PRs and no open PR.
* [ ] Missing or invalid activity evidence reported explicitly.
* [ ] Closed issues and open PRs keep their lifecycle mapping; criteria stay evidence-led.
* [ ] Coordinator command and recurring prompt use the supported mechanism, with focused tests and independent exact-head review (prompt wording owned by #1204).
