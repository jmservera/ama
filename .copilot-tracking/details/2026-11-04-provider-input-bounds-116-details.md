# Details: provider input bounds for issue 116

## Phase 1

* MAX_TEXT_BYTES 128 KiB checked on the encoded body for string prompts in Ai._request, before the financial meter and any network call.
* run() already falls back to the template and reports error=InputRefused; evidence() reports outcome input-refused.
* look_at: images limited to image/png and image/jpeg and 4 MiB (below the 5 MiB upload cap), returning the stored/manual-route template before base64 encoding.

## Phase 2

Six tests with a spy meter and patched urlopen; assert zero reservations and zero provider calls on refusal, and that bounded inputs still reach the meter.

## Phase 3

Focused unittest set (ai input bounds, rai_release, ai_consumption, safety, statement sources), ruff, mypy in src/core with --cache-dir=/tmp/mypy-116.
