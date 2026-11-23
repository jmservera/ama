# Details 2026-11-23, issue 116 live r12

Phase 1: test with three images of `MAX_IMAGE_BYTES // 2` decoded bytes; expect `input-image-too-large`, no meter reservation, no `urlopen`. Phase 2: running total in the image branch of `approved_payload`.
