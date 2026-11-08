---
title: Ranking archive ancestor durability 1258 correction 2 critique
description: One independent critique of the correction 2 plan, run before any code or test was drafted, with dispositions
ms.date: 2026-11-08
---

Independent critique (rubber-duck agent, read-only), one execution, verdict Revise. Sequencing: unlike correction 1, no code or test had been drafted when this critique ran; it reviewed research and plan only. Correction 1's late critique remains disclosed history. The critique is not repeated.

| ID | Severity given | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | Blocking | Treating every mountinfo path as active lets an overmounted (hidden) mount entry act as a boundary and omit an unsynced parent. | Applied. A listed mount counts only when no later line has the same or an ancestor mount point (later mountinfo lines are newer and hide earlier ones below or at their path). A hidden entry is ignored, so the walk continues upward, which can only add syncs, never omit one. Stacked-mount fixtures added, including a same-path overmount. Reliance on mountinfo order is stated as an assumption. |
| PC-002 | Blocking | Mount topology can change between link, resolve and sync. | Accepted as an operational precondition, not fixed: descriptor-based detection is not available through the supported mechanism, and a mount change during the few-millisecond confirmation is outside the demonstrator's contract. Stated in the plan, Changes and Review as an unproved residual for deployment assurance; no test claims otherwise. Reported for the human ledger. |
| PC-003 | Non-blocking | Parsing grammar and exception normalization underspecified; bytes safety. | Applied. Read bytes, decode with `os.fsdecode`, split on the first ` - ` separator, require at least five fields before it, octal-unescape, and convert any parse or decode error to `OSError` so `_confirmed` records the audited unconfirmed outcome. Fixtures: spaces, escapes, optional fields, truncated line, undecodable bytes. |
| PC-004 | Non-blocking | Planned tests did not exercise parsing, visibility, bind subdirectory chain or the API failure; unavailable-data tests may pass before the helper exists. | Applied. Added: parser fixtures, stacked/overmount visibility, bind-mounted subdirectory chain (archive inside a mount, not at its root: sync through the mount root), API wiring test with the reader failing (record kept, 409, unconfirmed audit, retry sound). Red-on-e40 expectations are stated per test: bind-at-archive, subvolume continue-past, overmount and parser tests fail (helper absent or wrong boundary); the unavailable-data core test and API failure test may already pass or be inapplicable pre-fix and are labelled coverage, not red. |

Also noted by the critique and carried as limits: chroot or container-relative mountinfo and overlayfs durability need deployment validation; non-Linux fail-closed is a platform trade-off, not support evidence.
