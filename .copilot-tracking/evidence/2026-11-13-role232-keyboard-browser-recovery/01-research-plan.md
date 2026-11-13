---
title: "#232 axe recovery: prospective research and plan (2026-11-13)"
ms.date: 2026-11-13
---

Authored before any recovery execution. The first attempt (fbd12ac94) ran no axe and had no prospective critique; those facts stand.

## Research (08:42 UTC)

* Axe file `/home/azureuser/.local/share/ama/gates/g79-p-dd92-r1-1108/axe-4.10.3.min.js` re-hashed read-only: 880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb, the expected value.
* Lock `/tmp/ama-rpi-heavy.lock`: `fuser` reports no holder (exit 1).
* Resource control: a probe `systemd-run --user --scope -p MemoryMax=2G -p MemorySwapMax=0` showed its cgroup `memory.max`=2147483648 and `memory.swap.max`=0. Headroom 4519 MiB available, no swap.
* Check script reads `ZF_AXE_JS`, compares the SHA256 and runs axe on `main` (role_screens_browser_check.py lines 341-354); it prints INFO for incompletes.

## Plan

1. Record the source tree hash, HEAD and venv (`~/.cache/ama-venv-133-hooks-1110`, read-only, source paths first in PYTHONPATH).
2. Take `flock -n` on the heavy lock (non-queued) and start the owned scope; inside it, before the browser command, print the cgroup `memory.max` and `memory.swap.max`; stop if not 2147483648 and 0.
3. Run `python -m checks.role_screens_browser_check 232` then `232s` once each with ZF_AXE_JS set, `timeout 150`, direct exits.
4. Diagnostic import-origin probe (a separate process, not the server) for api, core and agents modules; the foreign editable fallback remains disclosed.
5. Independent critique of this plan before step 2; independent Review of actual outputs after; fresh guideline fetch before Review.
6. No retry, no source change; FAIL or axe violations are kept verbatim.
