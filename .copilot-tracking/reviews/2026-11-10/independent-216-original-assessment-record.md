---
title: Record - original independent assessment of the constructed paired report (Refs #216, #208)
description: Durable record of the original independent static assessment of ab365e53
ms.date: 2026-11-10
---

## Source of the record

Session files under `independent-216-paired-report-1110/`: `functional-findings.json` (sha256 `20cc5257ea2f29fbb335d97ccf607c2cbde7947cdf8f4e758d016593c798f7cb`) and `read-ledger.json` (sha256 `4be9a340390a63255250bec1b145e78f307674dbd69a519f643224bc6984fc97`). Reviewer id `6339ad63-3729-49ea-924b-b9293482c70d`. No raw archive is copied and no old file is rewritten.

## Original assessment (preserved as issued)

* Exact head assessed: `ab365e53d024e269c9ad4f0b0e33a8361a43e30b` against `d52f20a5198de7269f39daf794911545aee01ced`.
* Verdict `approve_with_comments`; 0 Critical, 0 High, 2 Medium, 0 Low. Not erased or reclassified.
* Medium 1: the one-year seconds cap does not keep a derived elapsed ratio finite (subnormal cards with maximum chat gives `Infinity`).
* Medium 2: a minus sign with a 401-digit integer bypasses the positive-only cap and raises `OverflowError`.
* The review was static. The reviewer did not execute tests and did not reproduce the producer's reported test counts.
* Out of scope observation: explicit `--record` can overwrite an operator-selected canonical path. The reviewer classed this as an operational risk and not a new contract defect.

## Status now

The numeric D1 commit `4e61626b` was written to address the two Medium findings. That is the producer's claim. It has NOT been independently resolved; the same reviewer is to inspect the actual numeric source delta and evidence after this frozen process candidate. Publication, hosted CI and whole-issue closure remain unobserved.
