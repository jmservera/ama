---
title: Issue 1373 independent Functional assessment record
ms.date: 2026-11-10
task_id: 1373-independent-record-1110
---

<!-- markdownlint-disable-file -->
## Provenance

* Reviewer: independent Functional agent 494b8c89-2ed3-4ae5-97f5-826c648ba69d, assessed 2026-11-10 (about 09:43Z) for the Root. Source artifacts: Root session files `independent-1373-session-opacity-1110/functional-findings.json` and `readledger.json`, transcribed here, not raw logs.
* Exact head assessed: `3d89f63fcf5b7147d17ebd21bb119d00457ebe2a`, tree `26fcbc0362d3e516049eea7d0242d4f6169faa97`, against the CSV parent `9e71736bc09984b07d77c122747483548b580c7d`, not main.
* Depth: standard. Coverage: the full nine-file, 423-line supplied diff read once, plus the changed test, `SessionCodec` lines 405 to 475, and existing author-run logs and the seven original witness records.
* Limits stated by the reviewer: it executed no tests and no Git commands and recomputed no hash or exit status. Clean tree, diff check and original witness `verify` exit 0 with `events.jsonl` sha256 `b32bafed1b01b945e7313ac9800a5be56efc826ff41123002ede4fe444e6d8d2` are Root-reported, and the inspected witness output agreed. The raw CI token was not read.

## Verdict and findings

* Verdict: approve. Severity counts: critical 0, high 0, medium 0, low 0. Findings: none (zero new).
* Observations in the reviewer's words, summarized: production authentication, codec and RNG are unchanged; the fixture is issued and verified by real production methods with only the sid source stubbed; the independent HMAC formula matches `purpose|nonce|body`; handle binding, different-case and different-key separation, round trip and expiry checks are meaningful; the new regression guarantees a different MAC character. The author's first MAC-formula error remains in history and is not an outstanding defect.
* Acceptance coverage: the oracle replacement and the genuinely signed counterexample are Implemented; hosted checks, integration to main and full issue acceptance are Partial (not established).

## Read ledger

| Item read | Extent |
| --- | --- |
| Diff state, full diff, handoff, brief | Full |
| Test file | Lines 210 to 340 |
| `resident_showcase.py` | Lines 405 to 475 |
| Author logs `val2`, `core-discovery`, redacted red-before, `verify.out` | Full |
| Original witness `events.jsonl` | All seven records |

## Carried author evidence (by source identity, not re-run here)

Red before on the real fixed fixture; SessionTests 10; module 41; Core discovery 2,865 with 347 expected skips; Ruff check and format (235 files); configured mypy (288 files). The reviewer inspected these logs but did not execute them. The 200 repeat runs are not proof of absence of flakiness and not a required gate. No raw token-bearing log or raw gate archive is copied.

## Out-of-scope observation (UNCONFIRMED)

The reviewer noted that `token[:-2] + "xx"` in `test_tamper_expiry_and_garbage_denied` leaves a token already ending in `xx` unchanged, in which case `assertIsNone` would reject a valid token (a possible false failure). The original author Review described the same line as possibly vacuous. These wordings differ, neither was reproduced, and the Root is separately checking canonical base64 last-character constraints. It is not a new finding and not an established defect. No source repair, issue or allowance extension is made here, and any later work needs separate owner authorization.

## Not established

No GitHub approval, hosted CI, publication, main delivery or issue closure. This is not production authentication or security acceptance. Issue 1373 closure awaits reviewed work on main and all literal acceptance criteria; this child uses `Refs` for 1373, 80, 189 and 462 only.
