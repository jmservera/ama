---
title: Issue 951 phase details
ms.date: 2026-11-04
---

* `max_days` has no default; the docstring says no limit is owner-approved.
* A referral with age below zero is returned with `data_quality` = "received_on is in the future" and its negative `referral_age_days`.
* New test covers the missing argument (TypeError) and the future flag, and checks the register is unchanged. Existing test passes `max_days=1` explicitly.
* README paragraph updated.
