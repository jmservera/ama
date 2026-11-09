---
title: Issue 530 focused-gate refresh r3 details
ms.date: 2026-11-08
---

## Integration

`git merge --no-ff -m "<Conventional message>" 2e0c676ada9264b4322224a24bc98aa3367d4f4a` after confirming `git fetch origin main` still yields that SHA and the worktree is ignored-clean.

## Proofs after merge (before records are committed, and again at freeze)

* `git merge-base --is-ancestor 2e0c676a HEAD`.
* `git rev-parse HEAD:src HEAD:tools HEAD:infra HEAD:.github` equal the same paths at `2e0c676a`.
* `git diff --name-only --no-renames 2e0c676a...HEAD` lists only `.copilot-tracking/` paths.
* Selected chat test blobs and `src/core`, `src/agents` trees and `src/api/src/zava_forward/api/web/chat-widget.js` and `chat.js` (consumed by the widget test) compared with `ed19cb94`; differences recorded as attribution loss.

## Gate (admitted only at freeze)

```text
python3 tools/rpi-checks.py --changed --jobs 1 --lock-timeout 0 \
  --base 2e0c676ada9264b4322224a24bc98aa3367d4f4a \
  --out /home/azureuser/.local/share/ama/gates/g530-refresh-r3 < /dev/null
```

One attached invocation with console and exit code written outside the output directory; fresh path (refuse existing); no queue, poll, sleep, setsid or resume. Then `--verify-receipt <out>/receipt.json --base <freshly fetched Main> --required-scope partial --exact-base`; stop if the freshly fetched Main differs from `2e0c676a` (no relaxation).

## Critique

[.copilot-tracking/challenges/2026-11-08-issue-530-refresh-r3-critique.md](../challenges/2026-11-08-issue-530-refresh-r3-critique.md)
