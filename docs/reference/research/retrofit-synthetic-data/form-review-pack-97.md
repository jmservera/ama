---
title: Fictional Form Template Review Pack (#97)
description: Reviewer guide for a fictional versioned funding form template and unresolved Finance authority and binding decisions, mapped to the existing form schema contract
ms.date: 2026-10-20
ms.topic: reference
---

> [!WARNING]
> FICTIONAL SYNTHETIC REVIEW PACK. It is not an approved template, not a real
> funder, scheme or round, and not evidence of Finance authority. No submission,
> no payment, no grant value and no signature exists. Issue #97 criterion 1
> (actual approved-template authority and binding) remains unmet.

## Purpose

Owner direction on #126 (2026-10-20) permits a fictional versioned form and
Finance authority/binding pack so people can review a concrete object. The pack
is [`src/core/evals/fictional_form_review_pack.json`](../../../../src/core/evals/fictional_form_review_pack.json),
registered as `DS-FICT-FORM-REVIEW-PACK` in the
[provenance register](./provenance-register.json). It reuses the delivered form
schema contract in the [core guide](../../../../src/core/README.md#form-schema-registry-and-candidate-staging-97)
and adds no runtime, API, loader or schema engine.

## What the pack contains

* Template `FICT-FUND-FORM` version 1, `effective_from` null and
  unresolved, with a fictional re-review date.
* A schema block that registers unchanged through the existing path (funding
  `Unknown`, always stamped `Unapproved`), with sixteen fields covering every
  allowed type, units (GBP, m2, kWh/m2/year), required and conditional fields,
  ranked source authority, required evidence and three human-only fields
  (declaration, signature, approval).
* Two data-only calculation references, per-field freshness with proposed
  maximum source ages, and parser/OCR lineage expectations that restate the
  existing staging contract.
* Preparer, reviewer and approver roles with `may_not` limits. Separation is a
  proposed control and is not enforced by the delivered registry.
* A stale-propagation map of nine triggers (template version, rule version,
  survey, EPC, design, cost document, funding evidence, consent, source age)
  that lists affected and unaffected fields and calculations. It is a proposal
  for the later #98 runtime.
* Fourteen Finance decision fields, `FD-01` to `FD-14`, each with a null value
  and the status `Unresolved - Finance to supply`.

## Review questions for Finance and Grants

* Which named role-holder and recorded delegation can approve a template
  version (`FD-01`, `FD-02`)?
* Which real scheme, route, template source, version and effective dates apply
  (`FD-03` to `FD-05`) and which terms source and approver (`FD-06`)?
* Are the ranked source kinds, calculation rules and attachment authorities
  approved, replaced or removed (`FD-07` to `FD-09`)?
* Who reviews preparation, and what is the approver decision, date, signature
  and binding statement (`FD-10` to `FD-14`)?

Answers must come from a named human authority with version-specific evidence.
Replace the fictional values; do not edit them into apparent approval.

## What the pack does not prove

* It does not approve a template, route, rule, field authority or role.
* It does not show a current scheme term, eligibility, value or deadline.
* Source ranks, evidence references, maximum source ages and stale triggers are
  fictional proposals pending `FD-07` and `FD-09`.
* The public file holds only a placeholder reviewer because public payloads may
  not hold email addresses; the focused test registers a copy with a registered
  reviewer substituted and proves the placeholder is refused.

## Evidence

* Focused test: `src/core/tests/test_form_review_pack.py`.
* PRD requirements and open question: FR-038, FR-039, AC-046, AC-047, OQ-015 in
  the [programme PRD](../../../prds/zava-forward-retrofit-programme-demonstrator.md).
