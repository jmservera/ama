---
title: Gate Chromium integration and native Runner evidence changes (#1208)
description: Changes made in the integration continuation; native results are recorded externally after the final commit
ms.date: 2026-11-05
ms.topic: reference
---

## Changes

* Merge commit 20dded33a: normal local merge of freshly fetched origin/main 3d7ad2feaa9c4cba5fe917edd2fbc40e40a5c246 (#1209) into 57da478bee37140034959f472f84a7f8becb75a7. No conflicts; the only tools/rpi-checks.py difference from the first parent is the WORKFLOW_HASHES src-ci.yml line. Original #1208 commits, records and both import-error logs are untouched.
* New records in this task: research, plan, details, changes, review and state JSON (slug gate-chromium-integration-1208).
* External, uncommitted: /tmp/ama-1208-runner-harness.py drives the real Runner (install, install_chromium, command, check_skips). No source change was needed beyond the merge.

## Divergences and disclosures

* The previous native run (/tmp/ama-1208-native-20261105T0910, standalone script) remains supplementary evidence and not a Runner-path proof; its import-error logs (SHA-256 ab6516fe...) are preserved.
* Native outcome, commands, identities and skip counts are not in this commit by design (the final head must not change after execution). They are written to /tmp/ama-1208-final-evidence-*/ after the final commit; nothing here claims a result.
* Not performed and not claimed: full gate, receipt, SQL, images, scanners, physical or live Azure acceptance.
