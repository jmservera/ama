---
title: Issue 440 ranking main currency plan
description: Plan for merging current main and refreshing checkpoint provenance, focused tier
ms.date: 2026-11-08
---

## Objective

Make the ranking checkpoint current with origin/main 77fa5d35e915e524af9a5d536e3ae093b69c5807 by a normal merge, update provenance without rewriting old observations, freeze a clean final head, then run the native focused gate once. Refs #440 #79 #1231; no closing keyword.

## Tier and critique

Focused: documentation and bookkeeping only. Critique disposition: the original independent critique (Revise, PC-001 to PC-007) stays untouched and its dispositions apply. This currency plan is a small operation inside that scope and gets no second critique; this is recorded here, not claimed as a new independent critique.

## Phases

* [x] 1.1 Commit these currency Research, Plan and details records first, with a fresh gh api user identity.
* [x] 2.1 Normal merge of origin/main (git merge --no-ff, no rebase or reset). Preserve .github/rubric/scores/latest.json blob 6741ddd61aba2ff80cd8b7cb2f59e63cb1af7db3, mode 100644, and validate JSON.
* [x] 2.2 Append one short dated currency note to the pack section (new lines only, 0 removed) and a log entry; leave the README paragraph. Old observations are untouched.
* [x] 3.1 Refresh selectors in the new scratch directory /mnt/ama-gates/c440-currency-r2-1108-checks: fresh venv from git archive of the merged tree, non-editable install, import identity, core, API and cohort selectors, retention pytest. Synthetic ZF_DATA, PYTHONDONTWRITEBYTECODE=1.
* [x] 3.2 diff --check, ASCII, closing-keyword and anchor scans.
* [x] 4.1 Changes record and one author Review for the currency step, then state JSON, one final commit. The final head is frozen before the gate; the gate result lives only in external files and the response.
* [ ] 5.1 Gate: python3 tools/rpi-checks.py --changed --jobs 1 --lock-timeout 0 --base <fresh origin/main> --out /mnt/ama-gates/c440-currency-r2-1108 with stdin /dev/null, foreground. Refused or blocked is reported as such.
* [ ] 5.2 If a receipt exists: --verify-receipt <receipt> --required-scope partial --base <fresh origin/main>, then compare recorded groups with preflight, namespace and static.

## Stop conditions

Main changes production inputs, conflict not reconcilable, main moves again before the gate (report; no BASE RELAX), disk below 2 GB, lock held.
