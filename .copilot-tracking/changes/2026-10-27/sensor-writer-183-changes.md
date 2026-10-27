---
title: Historical writer blocked at shared consumer contract
ms.date: 2026-10-27
---

Refs #183. Refs #177. Branch docs/backfill-consumer-183-stack.
Common base e7d531c789dbaafafc05fb4cacf7d851e188cd58.

## Research and Exact Compatibility Evidence

The existing writer already supports stable seeds/as-of windows, declared
stock subsets, allowlisted fabric, synthetic labels, manifests, estimates,
hashes and evaluator-separated fault packets. Do not create another stock
or call its legacy SQL loader the #110 consumer.

`src/core/src/zava_forward/core/sensor_consumer.py` imports the exact fault
schema and requires uppercase sensor/reading/home IDs of at most 20/40/12
characters respectively. Stock sensor IDs are `SENS-SYN-` plus 64 lowercase
hex characters (73). Their reading IDs append epoch seconds (84 in the
public synthetic example); supplied opaque home IDs may also exceed 12.

On 2026-10-27 a focused installed-package verification used only the public
consumer fixture and one newly constructed synthetic home ID, not private
stock data. The normal consumer fixture passed `_shape` (`None`).
The fault-schema stock observation returned exactly `IDENTITY`, with lengths
sensor=73, reading=84, home=23. This is executable contract evidence, not an
assumption about SQL column width. No database or Azure was contacted.

## Plan and Implementation Disposition

Stop the writer child rather than silently remap stock IDs, widen admission,
install invented controls, bypass validation or import unmerged components.
One issue comment requests an owner-selected identity compatibility path.
Any future change needs mapping/schema/control/replay tests, stable lineage
and independent review. Climate reuse remains blocked separately at #178;
new #179/#180/#181 components are unmerged, not an integrated generator.

## Pre-Generation Volume Evidence

Using current installed `sensor_backfill.estimate(homes=60000, days=730,
cadence=480)`, no output generated and no private register read:
nominal paired observations/home=2,190; nominal total=131,400,000.
A measured 20-home legacy scale-fixture sample estimated 131,025,000 rows
after legacy dropout, 121.0 bytes/CSV row, 14.77 GiB.
This is a fictional capacity scenario, not measured existing-stock coverage,
a full-generation approval, a bound, SQL size, transmission/billing estimate
or evidence that legacy CSV is admissible through #110. Actual stock IDs,
modern fields, source history, faults and selected cadence change size.

## Original Acceptance Audit

| Criterion | Status |
| --- | --- |
| Same seed and inputs yield identical output | Existing bounded stock tests supply prior synthetic evidence, not integrated new-model proof. |
| All stock home/sensor IDs resolve | Existing adapter preserves declared selection; no private full-stock reconciliation performed. |
| Estimate volume/storage before generation | Conditional scenario above measured before any generation; no whole-stock coverage claim. |
| Reuse #110 validation | Actual stock observation refused by authoritative consumer; UNMET. |

No original checkbox ticked, no issue deferred/closed, no merge.
Validation: focused compatibility/estimate script, source-pointer review and
git diff check. Parent's one independent Review will include this evidence.
