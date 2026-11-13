---
title: Issue 133 evaluator outcomes and neutral text details
ms.date: 2026-11-13
---

## Outcomes cell

* Count `row.concerns[].outcome` values; a missing or null value counts as `no_outcome_yet`; a value with no label counts as `Unknown`.
* Render `"No concerns raised"` when empty, else `"Label: n"` entries joined by `; ` using `acLabel`, in order of first appearance.
* Caption stays free of banned jargon (gate, hold, provenance, trace, snapshot, envelope).

## neutral_text

* Normalise curly apostrophes to `'` and lower-case.
* Regex list: `you'?ll save`, `you will (?:save|pay less)`, `cut your (?:energy )?bills?`, `bills? will (?:fall|drop|go down|reduce)`, `savings? of`, `(?:tenant|resident|household|occupant) (?:caused|misunderstood)`, `(?:tenant|resident|household) is at fault`, `occupant'?s? behaviou?r`, `resident misunderstood`.
* Clauses introduced by `cannot determine`, `unknown`, `not known` or `no evidence` are not scanned by the paraphrase patterns.
* Neutral text (`higher bills reported`, `resident reported cold room`, `cannot determine`) must still pass.

## Static scan

Extract double-quoted and template string literals from `aftercare.js` with a regex in the test, scan every string literal (single, double, template) of any length, self-test the scanner on prohibited examples, and assert each passes `neutral_text` and contains no banned jargon word.
