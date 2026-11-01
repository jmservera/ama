---
title: Issue 608 Chromium socket path research
ms.date: 2026-11-01
---

## Disposition

Research executed. Planning Readiness: Ready.

## Findings

* `tools/rpi-checks.py` `admit_browser_output` (merged in #610, commit 84035ae9) rejects a `--out` whose `<out>/tmp` plus `/org.chromium.Chromium.XXXXXX/SingletonSocket` exceeds 107 bytes, before any expensive check, with an actionable bound and example short path.
* `tools/test_rpi_checks.py` `test_chromium_output_byte_boundary_matches_linux_socket` binds a real AF_UNIX socket at exactly 107 bytes and proves 108 fails; further tests cover alias/symlink paths and the CLI error message.
* Local run on origin/main cb57c1b7: `python3 -m unittest test_rpi_checks` in `tools/`: 55 tests OK.
* Issue comments record that a short-output full gate ran every group but sealed FAILED because HEAD/origin-main moved; no accepted exact-head zero-skip receipt exists.

## Acceptance criteria mapping

| Criterion | Status | Evidence |
| --- | --- | --- |
| Long paths fail clearly before expensive checks | Proven | #610, boundary and CLI tests |
| Boundary/cleanup/receipt contracts with regression test | Proven | `tools/test_rpi_checks.py` |
| Full browser and SQL groups execute without skips | Unmet | Needs an isolated, stable-head full gate; out of scope for the focused tier |

## Decision

No source change. Deliver evidence only, referencing the issue without closing it.
