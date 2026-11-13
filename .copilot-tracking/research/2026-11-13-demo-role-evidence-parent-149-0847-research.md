---
title: Role-screen evidence parent integration research (Refs 149, 231, 232)
description: Research for integrating two frozen local children into one main-based docs parent
ms.date: 2026-11-13
---

## Scope and disposition

Research disposition: executed (read-only inspection). Planning Readiness: Ready.
Base: origin/main 347962dace94171724cc8db4044c8d783335fecf, fetched and reconfirmed equal to the worktree HEAD at start (no move, no overlap question).
This parent's RPI is a genuine integration RPI. It does not claim the first #232 attempt fulfilled the required phase order.

## Inputs (immutable local commits)

* #231 review child `32fd2163547589b50f1e4e4bea4407321b82ab71`: six original RPI files under `.copilot-tracking/` (research, plan, critique, changes, review, state). Static guideline Technical/Quality review. Critique ProceedWithAmendments, Review ConformantWithFindings, addendum corrects CSS and citation lines, no repeat Review. Reported Low: "1 days old" plural. The `p.ok` glyph/style mismatch is grep-qualified, noncolour text exists, and is not a proved colour-only WCAG failure. No runtime, keyboard or AT observation.
* #232 validation child `eeb8ec157905265355f94177f9280863ba92486e`, containing original `fbd12ac941473bc468d2518a154673fd3003c66f` (16 files under `.copilot-tracking/evidence/2026-11-13-role232-keyboard-browser/`) and recovery (19 files under `.../2026-11-13-role232-keyboard-browser-recovery/`).
  * Original: both selectors `232` and `232s` exit 0, no FAIL, axe SKIP twice, critique NOTRUN, independent Review Partial.
  * Recovery: prospective plan and critique before execution, independent Review Partial. Pinned axe 4.10.3 sha256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`, both selectors exit 0, no axe violations or incompletes, Tab reach at 1280 px only, page-only CSV, no POST, reflow markers 320/390/1280. Own cgroup memory.max 2147483648 and swap.max 0 captured before the browser; ancestors not captured. Import-origin probe separate from the server; foreign editable namespace fallback remains. Source is the configured current tree, not fully attested server-process origins. The 232s text check asserts heading and panel only.

## Verified by the root and re-checked here

* Both children descend directly from the base; each adds only `.copilot-tracking/` files. `src`, `infra`, `tools` and `.github` are byte-equal to the base in both children.
* Original-to-recovery commits `fbd12ac9` to `eeb8ec15` leave original 232 files unchanged.
* The recovery log birth 08:41:52.547 and exit file 08:44:42.440 imply under 2m50s wall as an upper bound; no independent timing proof is claimed.

## Targets

`docs/architecture/cutover-evidence-pack.md` (append-only section), `docs/reference/README.md` (link), `docs/reference/log.md` (append-only). No new canonical page.

## Constraints

No source, helper, test, policy, fixture or workflow edits; no runtime rerun, SQL, browser, provider, cloud, deployment, private data, default `ZF_DATA`, `.env`, install or cleanup. Docs-only tier. No push, PR, issue, board or acceptance-criteria writes.
