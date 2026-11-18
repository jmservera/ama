---
title: Changes for #159
ms.date: 2026-11-14
---

## Changed files

* `src/core/src/zava_forward/core/synthetic/privacy.py`: stricter `source_issues`, new `dataset_source_issues`, wired into the source audit.
* `docs/reference/research/retrofit-synthetic-data/provenance-register.json`: v1.3.0, new fields, ERA5 weather source, rule and open item.
* `src/core/tests/test_synthetic_provenance.py`: new and updated tests.
* `docs/reference/log.md`: appended entry.

## Validation

* `python3 -m ruff check` and `ruff format --line-length 100 --check` in `src/core`: pass.
* `PYTHONPATH=src:tests python3 -m unittest tests.test_synthetic_provenance tests.test_needs_inventory tests.test_form_review_pack tests.test_climate_history`: 45 tests OK.
* `python3 -m zava_forward.core.synthetic.privacy --public-root . --sources`: no issues.
* Not run: complete local gate (focused tier; not pushed, so no hosted CI).

## Divergences

None. Not pushed per instruction.
