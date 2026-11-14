<!-- markdownlint-disable-file -->
# Plan: C1 mypy typing correction (Refs #104)

* Research: [research](../../research/2026-11-14/104-controlled-nomutate-c1-mypy-0247-research.md)
* Details: [details](../../details/2026-11-14/104-controlled-nomutate-c1-mypy-0247-details.md)
* [x] Annotate all methods, fixtures and locals in the test module.
* [x] Use narrow ignores only for calls into untyped sibling helpers.
* [x] Validate: `mypy`, ruff check and format, unittest module.
* Critique: not separately executed; focused tier, test-only change with no behaviour edit.
