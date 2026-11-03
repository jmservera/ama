---
title: Research for issue 470 coordinator policy slice
---

* Disposition: executed. Planning Readiness: Ready.
* Evidence: `git show 5092cb10a` (#792) and `src/README.md` "Gate speed controls". #792 delivered changed-path tier, `--jobs`, API shards (`test_shards`, `shard_helpers`), scoped skips, layer cache, base relaxation, `--stack`, `--resume`, stdin=DEVNULL.
* Gap: the coordinator agent already covers changed tier, relaxation, stack and resume; it lacks shards, receipt shard fields, stdin handling and the stack-member limits.
* Issue criteria: all met except "Measured full-run time before and after is recorded in the PR" (unmet; this slice does not measure).
* Tier: focused (documentation only; no security, infrastructure, SQL or deployment change).
