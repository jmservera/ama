# Research: issue 144 poison-copy size correction (2026-11-05)

Prospective correction loop in session 0bd489d3-4546-4229-94f9-d1812eadef27. Preserved unchanged: the 2026-11-04 original artifacts, the 2026-11-05 preparation artifacts and review, and the passed full receipt `/tmp/g144-r5-1105/receipt.json` (SHA256 5b83913995bd4b225bf8667d65b29305dcbd5c6fbe44cbef31561e999b2afc4a), now historical for head `9f14e6cb9`.

Disposition: executed. Planning Readiness: Ready.

## Finding F1 (independent functional review, REQUEST_CHANGES, P2)

Report: `/home/azureuser/.copilot/session-state/77149bdf-2f9a-4b04-b1dc-af3109946991/files/144-independent-9f14-assessment.txt`. `_poison` truncates to 128,000 characters before UTF-8 and base64, so the stored message can exceed the Azure Queue 64 KiB encoded limit (reproduced offline: 80,000 and 80,004 bytes, size-enforcing transport returns 400, no delete, redelivery continues). Source: Microsoft Learn Put Message, retrieved 2026-11-05. The reproduction is a model of the documented limit, not a live Azure observation.

## Own reading

Confirmed in code: the cap counts characters, not encoded bytes. Receive also poisons any message over 128,000 characters, which is the case that cannot be stored whole. Not changed: the bearer header (terminal masking only) and no Date header, as directed.

## Constraints

Stdlib only; keep poison-write-before-delete; failed write retains the original; no MI, post-back, serve or Azure work; light checks only (heavy admission is held by 233).
