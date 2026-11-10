<!-- markdownlint-disable-file -->
# Preserved original independent assessment: issue 129 constructed learning CLI

Durable copy of the independent assessment of the original candidate. It is preserved as received and is not an assessment of the D1 correction.

* Reviewer: `dabfdd4e-e835-499f-b8e6-bb1d170f3f90`. Depth: standard functional review. Verdict: `approve_with_comments`. Severity counts: 0 critical, 0 high, 0 medium, 1 low.
* Supplied pin: head `5cec9663559bebfae3b3a2a7d38fd179b8c84b10`, tree `840083bcb731da15cab0797721b79428fb607e87`, base main `d52f20a5198de7269f39daf794911545aee01ced`. The reviewer read the complete supplied 10-file, 697-line packet and the original dated RPI records.
* Source of record: external `independent-129-learning-cli-1110/functional-findings.json` and `read-ledger.json` in the Root session files (not copied here).

## Finding 1 (Low, Error Handling)

`learning_test_bundles.py` lines 317-319. With stdin closed (`<&-`) Python sets `sys.stdin` to `None`; `isatty` raises `AttributeError`, which the `ValueError`/`RecursionError` handler does not catch, so the operator sees a traceback instead of the promised single-line refusal. It confirms original self-review R1. Nonblocking: exit stays nonzero, stdout empty, no report or stored data. Suggested fix: explicit `sys.stdin is None` check raising a fixed `ValueError`; real subprocess regression with descriptor 0 closed; do not broaden the handler.

## Positives recorded

* Delegates to the unchanged scorer and renderer; STOP precedes effort and comparator-lower outcomes stay visible.
* Validation rejects boolean numbers, nonfinite effort, duplicate keys, unknown fields, invalid counts and oversized input before scoring.
* False retention and O16 accounting checks remain delegated to `run_report`.
* Constructed/unverified, unconfirmed mapping, unsatisfied retention and capacity-only qualifications are kept.
* No persistence, discovery, network, model or default `ZF_DATA` access in the added path.

## Limitations

* The reviewer executed no tests and no Git commands; head provenance relies on the supplied packet.
* Raw gate logs were not independently read. Test-file versus patch fixture literal differences for participant and text-case fixtures were noted as a provenance caveat.
* Root, not the reviewer, verified the clean exact head, diffcheck and original seven-event witness (exit 0, sha256 `2e1a73fa71f78f3c4f7732e556051fedf482431b80609a43ff6554af2a776874`).
* Original R2 (knowledge-base serialization) is not a functional blocker and remains routed.

## Status of the D1 correction

The D1 source is not independently assessed by this record. A follow-up independent review of the exact delta and regression evidence is still required.
