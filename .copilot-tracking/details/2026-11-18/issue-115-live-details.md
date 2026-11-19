---
title: Issue 115 live plan details
date: 2026-11-18
---

* Phase 1: Container Apps start API with command override and the job's own env; `python -m zava_forward.orchestrator.digest_blob` without `--publish`.
* Phase 2: throwaway job `job-cutover-test-ledger-verify-9` (name must start with the alert query prefix and fit 32 characters); inline script copies anchors to `ledger-digests-copy115`, alters one head hash in the copy, verifies, deletes copy.
* Phase 3: poll Alerts Management for the fired alert.
* Phase 4: documents only.
