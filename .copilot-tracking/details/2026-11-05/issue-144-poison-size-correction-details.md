# Details: issue 144 poison-copy size correction

* Constant `POISON_TEXT_BYTES = 45000` raw bytes (base64 60,000 bytes, under 65,536 with wrapper margin).
* `poison_text(text)`: UTF-8 encode; if within budget, keep as is; else `[truncated original_bytes=N]\n` marker plus the longest valid-UTF-8 prefix that fits the budget.
* `_poison` base64-encodes that and posts; delete only after 201.
* Tests: large ASCII, multibyte, oversized-valid repeated-delivery task, small message unchanged, failed write keeps message. Each large case asserts the posted XML body is under 65,536 bytes.
