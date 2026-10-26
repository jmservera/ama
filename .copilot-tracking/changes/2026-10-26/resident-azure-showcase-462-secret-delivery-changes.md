# Changes: owner-local resident demo secret delivery helper (issue 462)

Date: 2026-10-26. Base HEAD `2af9a186` (fast-forwarded from `11808a01` with the rubric bot commit only). Tool authoring only. No Azure action, no real password, verifier or session key, no push, no gate.

## Files

* `infra/scripts/credential_arm.py`: fixed constants for the vault and two secret names; private `_deploy`; new `store_resident_demo`; stricter what-if gate (exactly N expected secret IDs, all `Create`, inside the ama group, no duplicates). `store` keeps its Entra-only regex.
* `infra/scripts/resident_demo_secrets.py` (new): dry run by default; `--apply` needs a terminal and a typed phrase; expiry capped at 2026-10-26T12:00Z and rechecked; hidden prompt or 0600 `--verifier-file` opened once with `O_NOFOLLOW`; verifier validated by the shared `PasswordVerifier`; session key generated at apply time only.
* `infra/tests/test_resident_demo_secrets.py` (new): 14 offline tests, fake CLI and fixtures only.
* `infra/README.md`: paragraph documenting the helper.
* Plan: `.copilot-tracking/plans/2026-10-26/resident-azure-showcase-462-secret-delivery-plan.md` (critique dispositions PC-001 to PC-004 applied).
* Review: `.copilot-tracking/reviews/2026-10-26/resident-azure-showcase-462-secret-delivery-review.md` (Conformant, four Low items routed later).

## Validation (local, existing ama462 venv, external pycache)

* `python -m unittest discover -s infra/tests -p test_resident_demo_secrets.py`: 14 tests OK.
* `python -m unittest discover -s infra/tests -p test_staff_azure.py`: 43 tests OK (employee credential path unchanged).
* Runner-style `ruff check --isolated --select E,F,I,B,UP --line-length 100` and `ruff format --check` on the three source files: pass.
* Mutation sanity: disabling expiry parsing or the private-file read made the matching tests fail.
* Not run: full infra suite (needs az bicep), mypy for the new script (not in the runner groups), full gate, browser, Docker, SQL.

## Hashes (sha256)

* credential_arm.py `22805379511bf93e23a9ae3e506491ada07f4cd71879c4aa1c75845d335bf6ac`
* resident_demo_secrets.py `4d5aac6a67df2c3314944f5284a4d167eaf82b5671a49ab6ae9563584bdc3d78`
* test_resident_demo_secrets.py `e5b8bb5d58f9af87486596ab2d61007f43d5c7919aea5dd1ead403e4e6ab8d2e`
* infra/README.md `787a20ecb0263bf6f6ba81f52350ab9af70cce55be5d634b0ac6023868458146`
* `git diff -- infra` (with intent-to-add) `768a4c9de5e690d9c9e3eef9b6043722c54f50f2fd088db5ecc320a856b50dda`

## Residuals

* Plaintext briefly exists in the owner process and in 0600 temp body files in a 0700 profile directory; this is not a no-disk guarantee.
* Whether ARM deployment history retains secureString values is not proven here.
* No proof that an ARM secret write works through the private-only vault (G4 open).
* No automatic cleanup after a part-failed write; a retry is refused fail-closed.
* `--apply` is not an authority. It needs separate exact write approval, cleared budget (G1), and RBAC.
* Source changed, so the gate 4 receipt `2fa8494b...` is stale for the new head. A fresh full gate and coordinator capacity admission are needed later. The runner does not cover these checks beyond infra discovery and ruff groups.
* G1 budget, G2 live provenance and G3 SQL view/principal remain open.
