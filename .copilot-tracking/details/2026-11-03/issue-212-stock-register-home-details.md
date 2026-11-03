---
title: Issue 212 register-linked home grouping details
description: Phase details for the stock register grouping slice
ms.date: 2026-11-03
---

## Phase 1: key derivation

* Accept `facts["stock_link"]` only when it is a dict with `status == "linked"` and
  `stock_home_id` a nonblank string without outer whitespace (same rule as `stock_fabric._valid_id`).
* Return `("stock-" + id, "stock_register")`. A recorded `home_id` still wins.
* Anything else falls through to the address key, then `case_only`.

## Phase 2: tests

* Two cases with different address text and a shared anchor group into one home.
* Unlinked, null, padded, non-string and non-dict links are ignored.
* Recorded `home_id` outranks the stock link.

## Phase 3: documentation

* README criterion 7 row and grouping paragraph name the order and the remaining unmet items.
