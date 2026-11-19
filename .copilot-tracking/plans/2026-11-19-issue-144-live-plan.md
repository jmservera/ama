# Plan: issue 144 deployed image audit (2026-11-19)

* [ ] Add `infra/scripts/deployed_images.py`: parse `az containerapp list` and `az containerapp job list` JSON, classify each container image, exit 1 on placeholder, `:latest`, tag-only, or foreign registry; always label provenance as unproven.
* [ ] Add `infra/tests/test_deployed_images.py` with focused cases.
* [ ] Document in infra/README.md hosting table row and add the research note under docs/reference/research/ plus log and index.
* [ ] Validate: unittest, ruff check and format, run the tool on live JSON.
