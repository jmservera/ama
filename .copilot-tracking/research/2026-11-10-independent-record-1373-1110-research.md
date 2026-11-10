---
title: Issue 1373 independent-record metadata continuation research
ms.date: 2026-11-10
task_id: 1373-independent-record-1110
---

<!-- markdownlint-disable-file -->
## Disposition and scope

Research executed 2026-11-10 from 09:50Z. Disposition: `executed`. Planning Readiness: Ready.

This is a metadata-only continuation authorized once by the Root. It persists the independent Functional assessment of head `3d89f63fcf5b7147d17ebd21bb119d00457ebe2a` as new tracking records. No source, docs, earlier tracking or earlier witness bytes change. It grants no source correction, allowance, automatic follow-up, publication, GitHub approval, hosted CI or main delivery, and establishes no authentication or security acceptance.

## Evidence read

* Reviewer artifacts `independent-1373-session-opacity-1110/functional-findings.json` and `readledger.json` (Root session files). Reviewer agent 494b8c89-2ed3-4ae5-97f5-826c648ba69d, verdict approve, severity counts all 0, zero new findings, nine files and 423 diff lines read, depth standard.
* Provenance limits stated by the reviewer: no tests or Git executed; Root reported clean tree, diff check and original witness `verify` exit 0 with log sha256 `b32bafed1b01b945e7313ac9800a5be56efc826ff41123002ede4fe444e6d8d2`; the reviewer read existing author-run logs and witness records but did not recompute them.
* Actual worktree now: HEAD `3d89f63fcf5b7147d17ebd21bb119d00457ebe2a`, tree `26fcbc0362d3e516049eea7d0242d4f6169faa97`, zero status lines.

## Preserved original facts (not rewritten)

* Original same-agent Review stays valid as an author review, not independent.
* Real fixed fixture: sid `0000000000000024` through unchanged `issue`/`verify`; old assertion red on it.
* Intermediate author fault: the first independent-MAC formula omitted the `|` separator; production was correct.
* Author-run results: SessionTests 10, module 41, Core discovery 2,865 with 347 expected skips, ruff, format and configured mypy (288 files) clean. These are carried by source identity, not re-run here.
* 200 repeat runs are not proof of absence of flakiness and are not a required gate.

## Neighbouring tamper-test residual (UNCONFIRMED)

The original Review suspected `token[:-2] + "xx"` in `test_tamper_expiry_and_garbage_denied` is vacuous. The reviewer instead observed that a token already ending in `xx` would be unchanged and then `assertIsNone` would reject a valid token (a false failure, not vacuity). The two descriptions differ, neither was reproduced, and the Root is separately checking canonical base64 last-character constraints. The residual is therefore unconfirmed, is not a new finding and not an established defect. No repair, issue or allowance extension is made here.

## Method

Add new records only: this research, plan, details, critique, changes, a new independent-review record and state, a new witness chain. Verify source equality with `3d89f63` by empty `git diff 3d89f63 HEAD -- src docs` and a path allowlist.
