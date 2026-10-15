# Changes: #176

* generator/zf_stock_fabric.py, zf_stock_epc.py: summary records `generator_revision`.
* mvp/tests/test_generated_dataset.py: new byte-determinism test for both.
* docs/reference/research/retrofit-synthetic-data/README.md and log.md updated.
* Validation: `cd mvp && PYTHONPATH=. python3 -m unittest tests.test_generated_dataset` OK (12 tests); full suite run started, no failures seen in tail output.
