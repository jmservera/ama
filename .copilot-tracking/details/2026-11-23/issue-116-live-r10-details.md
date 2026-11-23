# Details 2026-11-23, issue 116 live r10

Phase 1: `src/core/src/zava_forward/core/ai.py`, `approved_payload`, decode `data` with `validate=True`; on `binascii.Error` raise `InputRefused("input-type-not-approved")`.
Phase 2: `test_shared_boundary_refuses_non_base64_image_data` (free text, whitespace, bad padding) via `refused`; zero meter reservations and no urlopen.
Phase 3: validation and docs.
