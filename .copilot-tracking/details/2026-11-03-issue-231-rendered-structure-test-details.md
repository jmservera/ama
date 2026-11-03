# Details: issue #231 rendered structure test

* Render technical-queue (complete, missing reference, empty) and quality-queue (accepted, no records) through the node harness already in the test module.
* Assert rendered class names are a subset of `inventory_classes()` (non-vacuous), no simulator or impersonation text, `h2` and `section` present, and `caption` and `th` present when a table renders.
