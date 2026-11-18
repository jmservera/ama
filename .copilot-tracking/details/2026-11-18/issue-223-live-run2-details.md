# Details: issue 223 live evidence

* Harness: PYTHONPATH=src:../core/src python3 -m zava_forward.agents.review_effectiveness --json (in src/agents; installed site-packages copy lacks the golden file).
* Probe posts in-page with X-ZF-CSRF: 1; creates one rejected review record on case ZF-2025-0331.
* No Azure resources created.
