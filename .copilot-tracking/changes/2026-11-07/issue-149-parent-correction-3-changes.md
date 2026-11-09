---
title: Issue 149 parent correction 3 changes
ms.date: 2026-11-07
---

## Changes

Start 0d8c39f1; three source commits touch `src/api` (checker, helper, test). origin/main bcd86707 was fetched, not merged. Source frozen at 0ee1c2be before the browser evidence. No product, Core, SQL or assertion change.

## Diagnosis and red/green

* Red (actual helper on the real render, no browser): `/tmp/zf149-correction3-1107/red.log`: 2 failed rows, cell 0 = EX-001/EX-002, cell 6 = SYN IDs, current assertion False.
* Green: 22 unit tests OK (AI state plus exception-register screen); ruff check and mypy strict (193 files) clean; 119 files formatted (checker files are configured exclusions, not claimed formatted). Installed production 211 files equal the archive. Test-helper PYTHONPATH only.

## Browser (flock -n, archive /tmp/zf149-correction3-1107, Chromium 1248 cache, axe 4.10.3 SHA 880970c0...8a68bb)

* Atlas: exit 0, 194 PASS, no axe step, screenshots unset.
* Data operator: exit 0, 100 PASS; required axe ran at 1280px on the queue page and the per-home view, no violations, incomplete []. This is not complete coverage, WCAG or assistive-technology acceptance. The harness supplies archive source paths to its child server, so this is not exclusively installed-runtime proof.
* Raw hashes: data-operator out 042fb269..., atlas out 08093407.... The earlier 48 PASS then exit 1 run stays in /tmp/zf149-b0d8-1107/ as adverse history.

## Pending

Independent review of the combined e270-to-correction-3 increment, hosted checks, human, AT and whole-issue acceptance. Refs #149 and #229 only.
